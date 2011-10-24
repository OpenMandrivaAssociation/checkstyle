# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           checkstyle
Version:        5.3
Release:        1
Summary:        Java source code checker
URL:            http://checkstyle.sourceforge.net/
# src/checkstyle/com/puppycrawl/tools/checkstyle/grammars/java.g is GPLv2+
# Most of the files in contrib/usage/src/checkstyle/com/puppycrawl/tools/checkstyle/checks/usage/transmogrify/ are BSD
License:        LGPLv2+ and GPLv2+ and BSD
Group:          Development/Java
Source0:        http://download.sf.net/checkstyle/checkstyle-%{version}-src.tar.gz
Source1:        %{name}-script
Source2:        %{name}.catalog

# Used for releases only, no use for us
Patch0:         0001-Remove-sonatype-parent.patch

# not available in Fedora yet
Patch1:         0002-Remove-linkcheck-plugin.patch

BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  maven2
BuildRequires:  antlr-maven-plugin
BuildRequires:  maven-antrun-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-eclipse-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-plugin-cobertura
BuildRequires:  maven-plugin-exec
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4
BuildRequires:  apache-commons-beanutils
BuildRequires:  apache-commons-cli
BuildRequires:  apache-commons-logging
BuildRequires:  apache-commons-collections
BuildRequires:  xerces-j2
BuildRequires:  jdom
BuildRequires:  velocity
BuildRequires:  emma
BuildRequires:  junit4
BuildRequires:  guava

Requires:       java
Requires:       apache-commons-cli
Requires:       apache-commons-beanutils
Requires:       apache-commons-collections
Requires:       apache-commons-logging
Requires:       jaxp_parser_impl
Requires:       antlr >= 0:2.7.1
Requires:       xalan-j2
Requires:       xerces-j2
Requires:       jdom
Requires:       velocity
Requires:       jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes:      %{name}-optional < %{version}-%{release}
# revisit later, maybe manual will come back when change from ant to
# maven build system will settle down
Obsoletes:      %{name}-manual < %{version}-%{release}

%description
A tool for checking Java source code for adherence to a set of rules.

%package        demo
Group:          Development/Java
Summary:        Demos for %{name}
Requires:       %{name} = %{version}

%description    demo
Demonstrations and samples for %{name}.

%package        javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description    javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

# fix encoding issues in docs
sed -i 's/\r//' LICENSE LICENSE.apache20 README RIGHTS.antlr \
         checkstyle_checks.xml sun_checks.xml suppressions.xml \
         contrib/hooks/*.pl src/site/resources/css/*css \
         java.header

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:aggregate


%install
rm -rf %{buildroot}

# jar
install -dm 755 %{buildroot}%{_javadir}
cp -pa target/%{name}-%{version}.jar %{buildroot}%{_javadir}
(cd %{buildroot}%{_javadir} &&
    for jar in *-%{version}.jar;
        do %__ln_s ${jar} `echo $jar| %__sed "s|-%{version}||g"`;
    done
)

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-checkstyle.pom
%add_to_maven_depmap com.puppycrawl.tools checkstyle %{version} JPP checkstyle


# script
install -Dm 755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# dtds
install -Dm 644 %{SOURCE2} %{buildroot}%{_datadir}/xml/%{name}/catalog
cp -pa src/checkstyle/com/puppycrawl/tools/checkstyle/*.dtd \
  %{buildroot}%{_datadir}/xml/%{name}

# javadoc
install -dm 755  %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -par target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# demo
install -dm 755 %{buildroot}%{_datadir}/%{name}
cp -par contrib/* %{buildroot}%{_datadir}/%{name}

# ant.d
install -dm 755  %{buildroot}%{_sysconfdir}/ant.d
cat > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
checkstyle antlr regexp jakarta-commons-beanutils jakarta-commons-cli jakarta-commons-logging jakarta-commons-collections jaxp_parser_impl
EOF

%clean
rm -rf %{buildroot}

%post
%update_maven_depmap
# Note that we're using a fully versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --add \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/xml/%{name}/catalog > /dev/null || :
fi

%postun
%update_maven_depmap
# Note that we're using a fully versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --remove \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/xml/%{name}/catalog > /dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc LICENSE LICENSE.apache20 README RIGHTS.antlr
%doc checkstyle_checks.xml java.header sun_checks.xml suppressions.xml

%{_mavenpomdir}/*pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_datadir}/xml/%{name}
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/ant.d/%{name}

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{name}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*


