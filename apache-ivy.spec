%{?scl:%scl_package apache-ivy}
%{!?scl:%global pkg_name %{name}}

%global upstream_version %(echo %{version} | tr '~' '-')

Name:           %{?scl_prefix}apache-ivy
Version:        2.5.0~rc1
Release:        1.1%{?dist}
Summary:        Java-based dependency manager
# One .js in asciidoc directory is MIT but we do not include it
License:        ASL 2.0
URL:            http://ant.apache.org/ivy
Source0:        http://www.apache.org/dist/ant/ivy/%{upstream_version}/%{pkg_name}-%{upstream_version}-src.tar.gz
BuildArch:      noarch

# Non-upstreamable.  Add /etc/ivy/ivysettings.xml at the end list of
# settings files Ivy tries to load.  This file will be used only as
# last resort, when no other setting files exist.
Patch0:         %{pkg_name}-global-settings.patch

Provides:       %{?scl_prefix}ivy = %{version}-%{release}

BuildRequires:  %{?scl_prefix}ivy-local >= 4
BuildRequires:  %{?scl_prefix}ant
BuildRequires:  %{?scl_prefix}mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  %{?scl_prefix}mvn(oro:oro)

%description
Apache Ivy is a tool for managing (recording, tracking, resolving and
reporting) project dependencies.  It is designed as process agnostic and is
not tied to any methodology or structure. while available as a standalone
tool, Apache Ivy works particularly well with Apache Ant providing a number
of powerful Ant tasks ranging from dependency resolution to dependency
reporting and publication.

%package javadoc
Summary:        API Documentation for ivy

%description javadoc
JavaDoc documentation for %{pkg_name}

%prep
%setup -q -n %{pkg_name}-%{upstream_version}
%patch0

find -name '*.jar' -delete

# Don't hardcode sysconfdir path
sed -i 's:/etc/ivy/:%{_sysconfdir}/ivy/:' src/java/org/apache/ivy/ant/IvyAntSettings.java

%pom_remove_dep :jsch
%pom_remove_dep :jsch.agentproxy
%pom_remove_dep :jsch.agentproxy.connector-factory
%pom_remove_dep :jsch.agentproxy.jsch
rm -r src/java/org/apache/ivy/plugins/repository/{ssh,sftp}
rm src/java/org/apache/ivy/plugins/resolver/*{Ssh,SFTP}*.java

%pom_remove_dep org.bouncycastle
rm src/java/org/apache/ivy/plugins/signer/bouncycastle/OpenPGPSignatureGenerator.java

# Remove test dependencies
%pom_remove_dep :junit
%pom_remove_dep :hamcrest-core
%pom_remove_dep :hamcrest-library
%pom_remove_dep :ant-testutil
%pom_remove_dep :ant-launcher
%pom_remove_dep :ant-junit
%pom_remove_dep :ant-junit4
%pom_remove_dep :ant-contrib
%pom_remove_dep :xmlunit

%mvn_alias : jayasoft:ivy
%mvn_file : %{pkg_name}/ivy ivy

# Remove dependency on commons-vfs
sed -i /commons-vfs/d ivy.xml
rm -rf src/java/org/apache/ivy/plugins/repository/vfs
rm -rf src/java/org/apache/ivy/plugins/resolver/VfsResolver.java

# Remove prebuilt documentation
rm -rf asciidoc

# Publish artifacts through XMvn
sed -i /ivy:publish/s/local/xmvn/ build.xml

%build
%ant -Divy.mode=local -Dtarget.ivy.bundle.version=%{version} -Dtarget.ivy.bundle.version.qualifier= -Dtarget.ivy.version=%{version} jar javadoc publish-local

%install
%mvn_install -J build/reports/api

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "apache-ivy/ivy" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/%{pkg_name}

%files -f .mfiles
%{_sysconfdir}/ant.d/%{pkg_name}
%doc README.adoc
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Tue Sep  3 2019 Java Maintainers <java-maint@redhat.com> - 2.5.0~rc1-1.1
- Automated package import and SCL-ization

* Tue Aug 20 2019 Marian Koncek <mkoncek@redhat.com> - 2.5.0~rc1-1
- Update to upstream version 2.5.0~rc1

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-15
- Mass rebuild for javapackages-tools 201901

* Tue Jul 17 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-14
- Allow building without vfs support

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 28 2018 Michael Simacek <msimacek@redhat.com> - 2.4.0-12
- Remove now unneeded patch

* Fri Mar 16 2018 Michael Simacek <msimacek@redhat.com> - 2.4.0-11
- Fix build against ant 1.10.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar  1 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-8
- Don't hardcode sysconfdir path

* Tue Feb 14 2017 Michael Simacek <msimacek@redhat.com> - 2.4.0-7
- Add conditional for bouncycastle

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.4.0-6
- Add conditional for ssh

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Michal Srb <msrb@redhat.com> - 2.4.0-3
- Update comment

* Mon May 04 2015 Michal Srb <msrb@redhat.com> - 2.4.0-2
- Port to bouncycastle 1.52

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.4.0-1
- Update to upstream version 2.4.0

* Fri Sep 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-17
- Add compat symlink for ivy.jar

* Mon Aug 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-16
- Add alias for jayasoft:ivy

* Thu Jun 26 2014 Michal Srb <msrb@redhat.com> - 2.3.0-15
- Drop workaround for broken apache-ivy

* Thu Jun 26 2014 Michal Srb <msrb@redhat.com> - 2.3.0-14
- Fix /etc/ant.d/apache-ivy (Resolves: rhbz#1113275)

* Mon Jun 23 2014 Michal Srb <msrb@redhat.com> - 2.3.0-13
- Add BR on missing parent POMs

* Mon Jun 09 2014 Michal Srb <msrb@redhat.com> - 2.3.0-12
- Add missing BR: apache-commons-lang

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-10
- Use features of XMvn 2.0.0

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-9
- BuildRequire ivy-local >= 3.5.0-2

* Thu Jan 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-8
- Build with ivy-local
- Add patch for global settings

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.3.0-7
- Remove prebuilt documentation in %%prep
- Install NOTICE file with javadoc subpackage

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.3.0-6
- Restore PGP signing ability
- Remove unneeded R

* Thu Dec 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-5
- Enable VFS resolver

* Wed Dec  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4
- Install POM files, resolves: rhbz#1032258
- Remove explicit requires; auto-requires are in effect now

* Fri Nov  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-3
- Add Maven depmap

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 1 2013 Alexander Kurtakov <akurtako@redhat.com> 2.3.0-1
- Update to latest upstream.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 31 2012 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-5
- Fix osgi metadata.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 6 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-2
- Fix ant integration.

* Fri Feb 25 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-1
- Update to 2.2.0.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 09 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.1.0-1
- Initial Fedora packaging
