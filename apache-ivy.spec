%global pkg_name apache-ivy
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.3.0
Release:        4.16%{?dist}
Summary:        Java-based dependency manager

License:        ASL 2.0
URL:            http://ant.apache.org/ivy/
Source0:        http://www.apache.org/dist/ant/ivy/%{version}/%{pkg_name}-%{version}-src.tar.gz
BuildArch:      noarch


BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}jakarta-commons-httpclient
BuildRequires:  %{?scl_prefix_java_common}jsch
BuildRequires:  %{?scl_prefix_java_common}jakarta-oro
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
Requires:       %{?scl_prefix_java_common}jakarta-oro
Requires:       %{?scl_prefix_java_common}jsch
Requires:       %{?scl_prefix_java_common}ant
Requires:       %{?scl_prefix_java_common}jakarta-commons-httpclient

%description
Apache Ivy is a tool for managing (recording, tracking, resolving and
reporting) project dependencies.  It is designed as process agnostic and is
not tied to any methodology or structure. while available as a standalone
tool, Apache Ivy works particularly well with Apache Ant providing a number
of powerful Ant tasks ranging from dependency resolution to dependency
reporting and publication.

%package javadoc
Summary:        API Documentation for ivy
Requires:       %{name} = %{version}-%{release}

%description javadoc
JavaDoc documentation for %{pkg_name}

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

# Fix messed-up encodings
for F in RELEASE_NOTES README LICENSE NOTICE CHANGES.txt
do
        sed 's/\r//' $F |iconv -f iso8859-1 -t utf8 >$F.utf8
        touch -r $F $F.utf8
        mv $F.utf8 $F
done
rm -fr src/java/org/apache/ivy/plugins/signer/bouncycastle

# Remove prebuilt documentation
rm -rf doc build/doc

# How to properly disable a plugin?
# we disable vfs plugin since commons-vfs is not available
rm -rf src/java/org/apache/ivy/plugins/repository/vfs \
        src/java/org/apache/ivy/plugins/resolver/VfsResolver.java
sed '/vfs.*=.*org.apache.ivy.plugins.resolver.VfsResolver/d' -i \
        src/java/org/apache/ivy/core/settings/typedef.properties
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# Craft class path
mkdir -p lib
build-jar-repository lib ant/ant jakarta-commons-httpclient jakarta-oro jsch

# Build
ant /localivy /offline -Dtarget.ivy.bundle.version=%{version} -Dtarget.ivy.bundle.version.qualifier= -Dtarget.ivy.version=%{version} jar javadoc
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# Code
install -d $RPM_BUILD_ROOT%{_javadir}
install -p -m644 build/artifact/jars/ivy.jar $RPM_BUILD_ROOT%{_javadir}/ivy.jar

# API Documentation
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp build/doc/reports/api/. $RPM_BUILD_ROOT%{_javadocdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir_java_common}/ant.d
echo "ivy" > $RPM_BUILD_ROOT%{_sysconfdir_java_common}/ant.d/%{pkg_name}

# Maven POM and depmap
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -d -m 755 $RPM_BUILD_ROOT%{_mavendepmapfragdir}
echo "<project><modelVersion>4.0.0</modelVersion><groupId>org.apache.ivy</groupId><artifactId>ivy</artifactId><version>2.3.0</version></project>" >$RPM_BUILD_ROOT%{_mavenpomdir}/JPP-ivy.pom
%add_maven_depmap JPP-ivy.pom ivy.jar
%{?scl:EOF}

%files -f .mfiles
%{_sysconfdir_java_common}/ant.d/%{pkg_name}
%doc RELEASE_NOTES CHANGES.txt LICENSE NOTICE README

%files javadoc
%{_javadocdir}/*
%doc LICENSE NOTICE

%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 2.3.0-4.16
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 2.3.0-4.15
- maven33 rebuild

* Thu Jan 15 2015 Michael Simacek <msimacek@redhat.com> - 2.3.0-4.14
- Replace hardcoded path with macro

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.3.0-4.13
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 2.3.0-4.12
- BR/R on packages from rh-java-common

* Fri Jan 09 2015 Michael Simacek <msimacek@redhat.com> - 2.3.0-4.11
- Install ant.d file into rh-java-common's ant.d

* Wed Jan 07 2015 Michal Srb <msrb@redhat.com> - 2.3.0-4.10
- Migrate to .mfiles

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.3.0-4.9
- Mass rebuild 2015-01-06

* Tue Dec 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4.8
- Install Maven POM and depmap

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4.4
- Remove requires on java

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4.3
- SCL-ize requires and build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-4.1
- First maven30 software collection build

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 2.3.0-4
- Remove prebuilt documentation in %%prep
- Install NOTICE file with javadoc subpackage
- Resolves: rhbz#854311

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.3.0-3
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-2
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

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
