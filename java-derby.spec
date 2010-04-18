#
# Conditional build:
%bcond_without	tests	# do not perform tests
#
Summary:	Derby DB (ex Cloudscape)
Summary(pl.UTF-8):	Derby DB (dawniej Cloudscape)
Name:		java-derby
Version:	10.1.1.0
Release:	0.1
License:	Apache v2.0
Group:		Applications/Databases
Source0:	http://www.apache.org/dist/db/derby/db-derby-%{version}/db-derby-%{version}-src.tar.gz
# Source0-md5:	122cbf34bf8e637802255baed5cc10ed
Source1:	%{name}-test.script
Patch0:		%{name}-compilepath_properties.patch
Patch1:		%{name}-extrapath_properties.patch
Patch2:		%{name}-JDBC30only-BrokeredConnection.patch
Patch3:		%{name}-JDBC30only-BrokeredCallableStatement.patch
Patch4:		%{name}-JDBC30only-BrokeredPreparedStatement.patch
Patch5:		%{name}-JDBC30only-BrokeredCallableStatement30.patch
Patch6:		%{name}-JDBC30only-BrokeredConnection30.patch
Patch7:		%{name}-JDBC30only-EmbedConnection.patch
Patch8:		%{name}-JDBC30only-EmbedCallableStatement20.patch
Patch9:		%{name}-JDBC30only-EmbedPreparedStatement20.patch
URL:		http://db.apache.org/derby/
BuildRequires:	ant >= 1.6
BuildRequires:	java(jta)
BuildRequires:	java-oro
BuildRequires:	java-servletapi5
BuildRequires:	java-xalan
BuildRequires:	java-xerces
BuildRequires:	java-xml-commons-apis
BuildRequires:	javacc
BuildRequires:	jdk >= 0:1.4.2
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java >= 1.4.2
Requires:	java(jta)
Requires:	java-oro
Requires:	java-servletapi5
Requires:	java-xalan
Requires:	java-xerces
Requires:	java-xml-commons-apis
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
- ij - a tool that allows SQL scripts to be executed against any JDBC
  database.
- dblook - Schema extraction tool for a Derby database.
- sysinfo - Utility to display version numbers and class path.

%description -l pl.UTF-8
Projekt Derby rozwija technologię bazodanową o otwartych źródłach
będącą: w czystej Javie, łatwą w użyciu, o niewielkich rozmiarach,
opartą na standardach, bezpieczną. Podstawa tej technologii, silnik
bazodanowy Derby.s, jest w pełni funkcjonalnym osadzalnym silnikiem
relacyjnych baz danych. API programistyczne to JDBC i SQL. Serwer
sieciowy Derby zwiększa zasięg silnika bazodanowego Derby
udostępniając tradycyjną funkcjonalność klient-serwer. Serwer sieciowy
pozwala klientom na łączenie się po TCP/IP przy użyciu standardowego
protokołu DRDA.

Serwer sieciowy pozwala silnikowi Derby obsługiwać sieciowe JDBC,
ODBC/CLI, Perla i PHP.

Narzędzia bazodanowe:
- ij - narzędzie pozwalające na wykonywanie skryptów SQL na dowolnej
  bazie JDBC
- dblook - narzędzie do wyciągania schematów dla bazy danych Derby
- sysinfo - narzędzie do wyświetlania numerów wersji i ścieżek klas


%package javadoc
Summary:	Javadoc for Derby DB
Summary(pl.UTF-8):	Dokumentacja javadoc do Derby DB
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for Derby DB.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc do Derby DB.

%package manual
Summary:	Documents for Derby DB
Summary(pl.UTF-8):	Dokumenty do Derby DB
Group:		Documentation

%description manual
Documents for Derby DB.

%description manual -l pl.UTF-8
Dokumenty do Derby DB.

%package demo
Summary:	Examples for Derby DB
Summary(pl.UTF-8):	Przykłady do Derby DB
Group:		Documentation

%description demo
Examples for Derby DB.

%description demo -l pl.UTF-8
Przykłady do Derby DB.

%prep
%setup -q -n db-derby-%{version}-src
for j in $(find -name '*.jar'); do
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
required_jars="javacc jta jce servletapi5 oro xalan xerces-j2 xml-commons-apis"

CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

export OPT_JAR_LIST="ant/ant-nodeps"

%ant \
	-Dj13lib=$JAVA_HOME/jre/lib \
	-Dj14lib=$JAVA_HOME/jre/lib \
	buildsource testing buildjarsclean javadoc

%if %{with tests}
mkdir testdir
install %{SOURCE1} testdir/testderby.sh
cd testdir
./testderby.sh
for f in $(find -name '*.fail'); do
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
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%{_javadir}/%{name}
%{_datadir}/%{name}

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

%files manual
%defattr(644,root,root,755)
%{_docdir}/%{name}
