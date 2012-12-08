%define gcj_support 1
%define section free
%define build_free 1
%define build_tests 0

Name:           checkstyle
Version:        4.4
Release:        0.0.6
Epoch:          0
Summary:        Helps programmers write Java code that adheres to a coding standard
License:        LGPL
Group:          Development/Java
URL:            http://checkstyle.sourceforge.net/
Source0:        http://downloads.sourceforge.net/checkstyle/checkstyle-src-%{version}.tar.gz
Source1:        %{name}-script
Source2:        %{name}.catalog
Patch0:         %{name}-build.patch
Patch1:         %{name}-javadoc-crosslink.patch
Patch2:         %{name}-build-free.patch
Patch3:         %{name}-exclude-smap.patch
Requires:       ant >= 0:1.6
Requires:       antlr >= 0:2.7.1, jakarta-commons-logging
Requires:       jakarta-commons-cli, jakarta-commons-beanutils
Requires:       jakarta-commons-collections, jpackage-utils >= 0:1.5
Requires:       jaxp_parser_impl
BuildRequires:  ant >= 0:1.6, ant-nodeps >= 0:1.6
%if %{build_tests}
BuildRequires:  ant-junit >= 0:1.6
# FIXME: Need to package emma <http://emma.sf.net/>
BuildRequires:  emma
%endif
BuildRequires:  junit, antlr >= 0:2.7.1
BuildRequires:  jakarta-commons-beanutils, jakarta-commons-lang
BuildRequires:  jakarta-commons-cli, xalan-j2, java-rpmbuild >= 0:1.5
# xerces-j2 because tests fail with gnujaxp...
BuildRequires:  jakarta-commons-logging, jakarta-commons-collections, xerces-j2
BuildRequires:  antlr-javadoc
#BuildRequires:  xml-commons-jaxp-1.3-apis-javadoc
BuildRequires:  xml-commons-apis-javadoc
BuildRequires:  jakarta-commons-beanutils-javadoc, ant-javadoc, perl-base
BuildRequires:  java-devel
BuildRequires:  java-javadoc
BuildRequires:  avalon-logkit 
BuildRequires:  jdom
BuildRequires:  velocity
BuildRequires:  werken.xpath
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
Checkstyle is a development tool to help programmers write Java code 
that adheres to a coding standard. It automates the process of checking 
Java code to spare humans of this boring (but important) task. This 
makes it ideal for projects that want to enforce a coding standard.

Checkstyle is highly configurable and can be made to support almost any 
coding standard. An example configuration file is supplied supporting 
the Sun Code Conventions. As well, other sample configuration files are 
supplied for other well known conventions.

Checkstyle can check many aspects of your source code. Historically 
it's main functionality has been to check code layout issues, but since 
the internal architecture was changed in version 3, more and more checks 
for other purposes have been added. Now Checkstyle provides checks that 
find class design problems, duplicate code, or bug patterns like double 
checked locking.

Checkstyle is most useful if you integrate it in your build process or 
your development environment. The distribution includes:

    * An Ant task.
    * A command line tool.

%package        demo
Group:          Development/Java
Summary:        Demos for %{name}
Requires:       %{name} = %{epoch}:%{version}

%description    demo
Demonstrations and samples for %{name}.

%package        javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}.

%package        manual
Group:          Development/Java
Summary:        Manual for %{name}

%description    manual
Manual for %{name}.

%package        optional
Group:          Development/Java
Summary:        Optional functionality for %{name}
Requires:       %{name} = %{epoch}:%{version}

%description    optional
Optional functionality for %{name}.

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1 -b .build
%patch1 -p1 -b .javadoc
%if %{build_free}
%patch2 -p1 -b .free
%endif
%patch3 -p1 -b .smap

%{__perl} -pi -e 's|\./{\@docRoot}/\.\./index\.html|file://%{_docdir}/%{name}-manual-%{version}/index.html|' build.xml
%{__perl} -pi -e 's|.*classpathref="javadoc\.classpath".*\n||g;' build.xml

# remove all binary libs
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}

# fix end-of-line
%{__perl} -pi -e 's/\r$//g' LICENSE LICENSE.apache LICENSE.apache20 \
README RIGHTS.antlr *.header *.xml

%if %{build_free}
%{__rm} -rf src/checkstyle/com/puppycrawl/tools/checkstyle/doclets
%endif

%build
OPT_JAR_LIST="ant/ant-nodeps"
%if %{build_tests}
OPT_JAR_LIST="$OPT_JAR_LIST ant/ant-junit"
%endif
export OPT_JAR_LIST
export CLASSPATH=$(build-classpath antlr commons-beanutils \
commons-collections commons-cli commons-logging jdom junit velocity \
werken.xpath xalan-j2 xerces-j2 avalon-logkit commons-lang)

%{ant} \
  -Dbuild.sysclasspath=first \
  -Dant.javadoc=%{_javadocdir}/ant \
  -Dantlr.javadoc=%{_javadocdir}/antlr \
  -Djaxp.javadoc=%{_javadocdir}/xml-commons-apis \
  -Dbeanutils.javadoc=%{_javadocdir}/jakarta-commons-beanutils \
  -Djava.javadoc=%{_javadocdir}/java \
  compile.checkstyle
%{ant} \
  -Dant.javadoc=%{_javadocdir}/ant \
  -Dantlr.javadoc=%{_javadocdir}/antlr \
  -Djaxp.javadoc=%{_javadocdir}/xml-commons-apis \
  -Dbeanutils.javadoc=%{_javadocdir}/jakarta-commons-beanutils \
  -Djava.javadoc=%{_javadocdir}/java \
  javadoc
%{ant} \
  -Dbuild.sysclasspath=first \
  -Dant.javadoc=%{_javadocdir}/ant \
  -Dantlr.javadoc=%{_javadocdir}/antlr \
  -Djaxp.javadoc=%{_javadocdir}/xml-commons-apis \
  -Dbeanutils.javadoc=%{_javadocdir}/jakarta-commons-beanutils \
  -Djava.javadoc=%{_javadocdir}/java \
  xdocs
%{ant} \
  -Dbuild.sysclasspath=first \
  -Dant.javadoc=%{_javadocdir}/ant \
  -Dantlr.javadoc=%{_javadocdir}/antlr \
  -Djaxp.javadoc=%{_javadocdir}/xml-commons-apis \
  -Dbeanutils.javadoc=%{_javadocdir}/jakarta-commons-beanutils \
  -Djava.javadoc=%{_javadocdir}/java \
  build.bindist
%if %{build_tests}
%{ant} \
  -Dbuild.sysclasspath=first \
  -Dant.javadoc=%{_javadocdir}/ant \
  -Dantlr.javadoc=%{_javadocdir}/antlr \
  -Djaxp.javadoc=%{_javadocdir}/xml-commons-apis \
  -Dbeanutils.javadoc=%{_javadocdir}/jakarta-commons-beanutils \
  -Djava.javadoc=%{_javadocdir}/java \
  run.tests
%endif

%install
%{__rm} -rf %{buildroot}

# jar
%{__mkdir_p} %{buildroot}%{_javadir}
cp -a target/dist/%{name}-%{version}/%{name}-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
cp -a target/dist/%{name}-%{version}/%{name}-optional-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-optional-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do %{__ln_s} ${jar} `echo $jar| %__sed "s|-%{version}||g"`; done)

# script
%{__mkdir_p} %{buildroot}%{_bindir}
cp -a %{SOURCE1} %{buildroot}%{_bindir}/%{name}

# dtds
%{__mkdir_p} %{buildroot}%{_datadir}/xml/%{name}
cp -a %{SOURCE2} %{buildroot}%{_datadir}/xml/%{name}/catalog
cp -a src/checkstyle/com/puppycrawl/tools/checkstyle/*.dtd \
  %{buildroot}%{_datadir}/xml/%{name}

# demo
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
cp -a target/dist/%{name}-%{version}/contrib/* \
  %{buildroot}%{_datadir}/%{name}

# ant.d
%{__mkdir_p}  %{buildroot}%{_sysconfdir}/ant.d
%{__cat} > %{buildroot}%{_sysconfdir}/ant.d/%{name} << EOF
checkstyle antlr jakarta-commons-beanutils jakarta-commons-cli jakarta-commons-logging jakarta-commons-collections jaxp_parser_impl
EOF

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
# FIXME: This allows --short-circuit (%%exclude should be used instead).
if [ -d target/dist/%{name}-%{version}/docs/api ]; then
  cp -a target/dist/%{name}-%{version}/docs/api/* \
    %{buildroot}%{_javadocdir}/%{name}-%{version}
fi
%{__rm} -rf target/dist/%{name}-%{version}/docs/api
%{__ln_s} %{_javadocdir}/%{name} target/dist/%{name}-%{version}/docs/api
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

for i in `find %{buildroot}%{_datadir}/%{name} -type f`; do
  %{__perl} -pi -e 's/\r$//g' $i
done

for i in `find target/dist/%{name}-%{version}/docs -type f`; do
  %{__perl} -pi -e 's/\r$//g' $i
done

for i in `find %{buildroot}%{_datadir}/xml/%{name} -type f -name "*.dtd"`; do
  %{__perl} -pi -e 's/\r$//g' $i
done

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%post
%if %{gcj_support}
%{update_gcjdb}
%endif
# Note that we're using a fully versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --add \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/xml/%{name}/catalog > /dev/null 2>&1 || :
fi

%postun
# Note that we're using a fully versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --remove \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/xml/%{name}/catalog > /dev/null 2>&1 || :
fi
%if %{gcj_support}
%{clean_gcjdb}
%endif

%post optional
%if %{gcj_support}
%{update_gcjdb}
%endif
%{__grep} -q checkstyle-optional %{_sysconfdir}/ant.d/%{name} || \
%{__perl} -pi -e 's|checkstyle|checkstyle checkstyle-optional|' %{_sysconfdir}/ant.d/%{name}

%postun optional
%{__grep} -q checkstyle-optional %{_sysconfdir}/ant.d/%{name} && \
%{__perl} -pi -e 's|checkstyle-optional ||' %{_sysconfdir}/ant.d/%{name} || :
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE LICENSE.apache LICENSE.apache20 README RIGHTS.antlr
%doc build.xml checkstyle_checks.xml import-control.xml java.header
%doc sun_checks.xml suppressions.xml
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif
%{_datadir}/xml/%{name}
%attr(0755,root,root) %{_bindir}/*
%config(noreplace) %{_sysconfdir}/ant.d/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.xsl

%files demo
%defattr(0644,root,root,0755)
%exclude %{_datadir}/%{name}/*.xsl
%{_datadir}/%{name}/*

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc target/dist/%{name}-%{version}/docs/*

%files optional
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-optional.jar
%{_javadir}/%{name}-optional-%{version}.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-optional-%{version}.jar.*
%endif


%changelog
* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0:4.4-0.0.4mdv2011.0
+ Revision: 603826
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0:4.4-0.0.3mdv2010.1
+ Revision: 522358
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0:4.4-0.0.2mdv2010.0
+ Revision: 413232
- rebuild

* Tue Apr 07 2009 Funda Wang <fwang@mandriva.org> 0:4.4-0.0.1mdv2009.1
+ Revision: 364751
- rediff javadoc patch

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0:4.4-0.0.1mdv2009.0
+ Revision: 140692
- restore BuildRoot

* Thu Dec 20 2007 David Walluck <walluck@mandriva.org> 0:4.4-0.0.1mdv2008.1
+ Revision: 135942
- 4.4

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:4.3-5mdv2008.1
+ Revision: 120849
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Mon Nov 26 2007 David Walluck <walluck@mandriva.org> 0:4.3-4mdv2008.1
+ Revision: 112037
- fix build by requiring commons-lang (thanks akurtakov)

  + Anssi Hannula <anssi@mandriva.org>
    - remove unnecessary Requires(post) on java-gcj-compat

  + Thierry Vignaud <tv@mandriva.org>
    - kill file require on perl-base


* Sun Mar 04 2007 David Walluck <walluck@mandriva.org> 4.3-1mdv2007.0
+ Revision: 132014
- 4.3
- Import checkstyle

* Tue Jul 11 2006 David Walluck <walluck@mandriva.org> 0:4.2-1mdv2007.0
- 4.2
- add supressions 1.2 dtd to catalog

* Tue Jun 06 2006 David Walluck <walluck@mandriva.org> 0:4.1-4mdv2007.0
- fix macro in %%post

* Mon Jun 05 2006 David Walluck <walluck@mandriva.org> 0:4.1-3
- rebuild for libgcj.so.7
- own %%{_libdir}/gcj/%%{name}

* Wed Jan 18 2006 David Walluck <walluck@mandriva.org> 0:4.1-2mdk
- BuildRequires
- fix javadoc build
- fix file permissions

* Fri Dec 16 2005 David Walluck <walluck@mandriva.org> 0:4.1-1mdk
- 4.1

* Tue Nov 29 2005 David Walluck <walluck@mandriva.org> 0:4.0-1mdk
* Tue Nov 08 2005 David Walluck <walluck@mandriva.org> 0:4.0-0.beta6.2mdk
- don't require ant-junit unconditionally
- include xsl files in main package instead of demo package

* Wed Nov 02 2005 David Walluck <walluck@mandriva.org> 0:4.0-0.beta6.1mdk
- 4.0-beta6
- natively compile

* Sun May 29 2005 David Walluck <walluck@mandriva.org> 0:3.5-1.1mdk
- release

* Mon Feb 21 2005 David Walluck <david@jpackage.org> 0:3.5-1jpp
- 0.3.5
- fix ant task with new ant
- add more files to %%doc

* Sat Aug 21 2004 Ralph Apel <r.apel at r-apel.de> - 0:3.4-4jpp
- Build with ant-1.6.2
- Runtime Req ant >= 0:1.6.2

* Sat Aug 07 2004 Ralph Apel <r.apel at r-apel.de> - 0:3.4-3jpp
- Void change

* Wed Jun 02 2004 Randy Watler <rwatler at finali.com> - 0:3.4-2jpp
- Upgrade to Ant 1.6.X

* Tue Apr 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.4-1jpp
- Update to 3.4.
- Make -optional depend on the main package.
- Update DTD catalog, move DTDs to %%{_datadir}/xml/%%{name}.
- New style versionless javadoc dir symlinking.
- Add -optional jar to classpath in startup script if available.

