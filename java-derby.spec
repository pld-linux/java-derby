#
# Conditional build:
%bcond_without	tests	# do not perform tests
#
Summary:	Derby DB (ex Cloudscape)
Name:		derby
Version:	10.1.1.0
Release:	0.1
License:	Apache License Version 2.0
Group:		Applications/Databases
URL:		http://db.apache.org/derby/
Source0:	http://www.apache.org/dist/db/derby/db-derby-10.1.1.0/db-%{name}-%{version}-src.tar.gz
# Source0-md5:	122cbf34bf8e637802255baed5cc10ed
Source1:	%{name}-%{version}-test.script
Patch0:		%{name}-10.1.1.0-compilepath_properties.patch
Patch1:		%{name}-10.1.1.0-extrapath_properties.patch
Patch2:		%{name}-10.1.1.0-JDBC30only-BrokeredConnection.patch
Patch3:		%{name}-10.1.1.0-JDBC30only-BrokeredCallableStatement.patch
Patch4:		%{name}-10.1.1.0-JDBC30only-BrokeredPreparedStatement.patch
Patch5:		%{name}-10.1.1.0-JDBC30only-BrokeredCallableStatement30.patch
Patch6:		%{name}-10.1.1.0-JDBC30only-BrokeredConnection30.patch
Patch7:		%{name}-10.1.1.0-JDBC30only-EmbedConnection.patch
Patch8:		%{name}-10.1.1.0-JDBC30only-EmbedCallableStatement20.patch
Patch9:		%{name}-10.1.1.0-JDBC30only-EmbedPreparedStatement20.patch
BuildRequires:	ant >= 0:1.6
BuildRequires:	jakarta-oro
BuildRequires:	javacc
BuildRequires:	jdk >= 0:1.4.2
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	jta
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	servletapi5
BuildRequires:	xalan-j
BuildRequires:	xerces-j
BuildRequires:	xml-commons-apis
Requires:	java >= 0:1.4.2
Requires:	jta
Requires:	oro
Requires:	servletapi5
Requires:	xalan-j2
Requires:	xerces-j2
Requires:	xml-commons-apis
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Derby project develops open source database technology that is:

Pure Java, Easy to use, Small footprint, Standards based, Secure. The
core of the technology, Derby.s database engine is a full functioned
relational embedded database engine. JDBC and SQL are the programming
APIs. The Derby network server increases the reach of the Derby
database engine by providing traditional client server functionality.
The network server allows clients to connect over TCP/IP using the
standard DRDA protocol.

The network server allows the Derby engine to support networked JDBC,
ODBC/CLI, Perl and PHP.

Database Utilities:
- ij - -- a tool that allows SQL scripts to be executed against any
  JDBC database.
- dblook -- Schema extraction tool for a Derby database.
- sysinfo -- Utility to display version numbers and class path.


%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation
Requires(post):	/bin/rm,/bin/ln
Requires(postun):	/bin/rm

%description javadoc
Javadoc for %{name}

%package manual
Summary:	Documents for %{name}
Group:		Documentation

%description manual
Documents for %{name}

%package demo
Summary:	Examples for %{name}
Group:		Documentation

%description demo
Examples for %{name}

%prep
%setup -q -n db-%{name}-%{version}-src

for j in $(find . -name "*.jar"); do
	mv $j $j.no
done

%patch0
%patch1
%patch2
%patch3
%patch4
%patch5
%patch6
%patch7
%patch8
%patch9

%build
cd tools/java
ln -sf $(build-classpath javacc) .
ln -sf $(build-classpath jta) .
ln -sf $(build-classpath jce) .
ln -sf $(build-classpath servletapi5) .
ln -sf $(build-classpath oro) .
ln -sf $(build-classpath xalan-j2) .
ln -sf $(build-classpath xerces-j2) .
ln -sf $(build-classpath xml-commons-apis) .
cd -

export OPT_JAR_LIST="ant/ant-nodeps"

# set both jres to 1.4.2 !!
%ant \
	-Dj13lib=/usr/lib/jvm/java-1.4.2/jre/lib \
	-Dj14lib=/usr/lib/jvm/java-1.4.2/jre/lib \
	buildsource testing buildjarsclean javadoc

%if %{with tests}
mkdir testdir
cp %{SOURCE1} testdir/testderby.sh
cd testdir
chmod +x testderby.sh
./testderby.sh
for f in $(find . -name "*.fail"); do
	echo FAILED $f
	cat $f
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}

install -pm 644 jars/sane/derbyclient.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyclient-%{version}.jar
install -pm 644 jars/sane/derby.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derby-%{version}.jar
install -pm 644 jars/sane/derbyLocale_de_DE.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyLocale_de_DE-%{version}.jar
install -pm 644 jars/sane/derbyLocale_es.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyLocale_es-%{version}.jar
install -pm 644 jars/sane/derbyLocale_fr.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyLocale_fr-%{version}.jar
install -pm 644 jars/sane/derbyLocale_it.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyLocale_it-%{version}.jar
install -pm 644 jars/sane/derbyLocale_ja_JP.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyLocale_ja_JP-%{version}.jar
install -pm 644 jars/sane/derbyLocale_ko_KR.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyLocale_ko_KR-%{version}.jar
install -pm 644 jars/sane/derbyLocale_pt_BR.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyLocale_pt_BR-%{version}.jar
install -pm 644 jars/sane/derbyLocale_zh_CN.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyLocale_zh_CN-%{version}.jar
install -pm 644 jars/sane/derbyLocale_zh_TW.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyLocale_zh_TW-%{version}.jar
install -pm 644 jars/sane/derbynet.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbynet-%{version}.jar
install -pm 644 jars/sane/derbyTesting.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbyTesting-%{version}.jar
install -pm 644 jars/sane/derbytools.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/derbytools-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
install -pm 644 jars/sane/derby.war \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/derby-%{version}.war
install -pm 644 CHANGES $RPM_BUILD_ROOT%{_datadir}/%{name}
install -pm 644 COPYRIGHT $RPM_BUILD_ROOT%{_datadir}/%{name}
install -pm 644 LICENSE $RPM_BUILD_ROOT%{_datadir}/%{name}
install -pm 644 NOTICE $RPM_BUILD_ROOT%{_datadir}/%{name}
install -pm 644 STATUS $RPM_BUILD_ROOT%{_datadir}/%{name}

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/publishedapi $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/engine $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# manual
install -dm 755 $RPM_BUILD_ROOT%{_docdir}/%{name}
cp -pr javadoc/language $RPM_BUILD_ROOT%{_docdir}/%{name}
cp -pr javadoc/tools $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%{_javadir}/%{name}
%{_datadir}/%{name}

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files manual
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}
