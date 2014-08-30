#
# Conditional build:
%bcond_without	tests	# do not perform tests
%bcond_without	javadoc		# don't build javadoc

%define		srcname	derby
%include	/usr/lib/rpm/macros.java
Summary:	Derby DB (ex Cloudscape)
Summary(pl.UTF-8):	Derby DB (dawniej Cloudscape)
Name:		java-%{srcname}
Version:	10.10.2.0
Release:	0.1
License:	Apache v2.0
Group:		Applications/Databases
Source0:	http://www.apache.org/dist/db/derby/db-derby-%{version}/db-derby-%{version}-src.tar.gz
# Source0-md5:	90227f670d05862a52d2729428786b63
Source1:	derby.sh
Patch1:		derby-javacc5.patch
Patch2:		derby-net.patch
URL:		http://db.apache.org/derby/
BuildRequires:	ant >= 1.6
#BuildRequires:	java-jta
BuildRequires:	java-oro
BuildRequires:	java-servletapi
BuildRequires:	java-xalan
#BuildRequires:	java-xerces
#BuildRequires:	java-xml-commons-apis
BuildRequires:	javacc
BuildRequires:	jdk >= 1.6
BuildRequires:	jpackage-utils >= 1.5
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.553
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
%setup -qc

mv db-derby-%{version}-doc-src doc-src
mv db-derby-%{version}-src/* .

for j in $(find -name '*.jar'); do
	mv $j $j.no
done

%undos -f jj,xml

rm java/engine/org/apache/derby/impl/sql/compile/Token.java
%patch1 -p0
%patch2 -p0

# Using generics
find -name build.xml | xargs sed -i -e '
        s/target="1.4"/target="1.6"/
        s/source="1.4"/source="1.6"/
        /Class-Path/d
'

%build
# tools/ant/properties/extrapath.properties
ln -sf $(build-classpath javacc) tools/java/javacc.jar
ln -sf $(build-classpath servlet-api) tools/java/geronimo-spec-servlet-2.4-rc4.jar
ln -sf $(build-classpath xalan-j2) tools/java/xalan.jar
ln -sf $(build-classpath xalan-j2-serializer) tools/java/serializer.jar
ln -sf $(build-classpath oro) tools/java/jakarta-oro-2.0.8.jar
ln -sf $(build-classpath junit) tools/java/junit.jar

# Fire
%ant buildsource buildjars %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_javadir}/%{srcname}}

cp -p jars/sane/*.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}

# Wrapper scripts
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{srcname}-ij
for P in sysinfo NetworkServerControl startNetworkServer stopNetworkServer; do
	ln -s %{srcname}-ij $RPM_BUILD_ROOT%{_bindir}/%{srcname}-$P
done

# Derby home dir
install -d $RPM_BUILD_ROOT/var/lib/derby

%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
%pre
%groupadd -r derby
%useradd -r -g derby -d /var/lib/derby -s /sbin/nologin -c "Apache Derby service account" derby
%endif

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc README NOTICE LICENSE RELEASE-NOTES.html published_api_overview.html
%attr(755,root,root) %{_bindir}/derby-ij
%attr(755,root,root) %{_bindir}/derby-sysinfo
%attr(755,root,root) %{_bindir}/derby-NetworkServerControl
%attr(755,root,root) %{_bindir}/derby-startNetworkServer
%attr(755,root,root) %{_bindir}/derby-stopNetworkServer
%dir %{_javadir}/%{srcname}
%{_javadir}/%{srcname}/derby.jar
%{_javadir}/%{srcname}/derbyclient.jar
%{_javadir}/%{srcname}/derbynet.jar
%{_javadir}/%{srcname}/derbyrun.jar
%{_javadir}/%{srcname}/derbytools.jar
%lang(cs) %{_javadir}/%{srcname}/derbyLocale_cs.jar
%lang(de_DE) %{_javadir}/%{srcname}/derbyLocale_de_DE.jar
%lang(es) %{_javadir}/%{srcname}/derbyLocale_es.jar
%lang(fr) %{_javadir}/%{srcname}/derbyLocale_fr.jar
%lang(hu) %{_javadir}/%{srcname}/derbyLocale_hu.jar
%lang(it) %{_javadir}/%{srcname}/derbyLocale_it.jar
%lang(ja_JP) %{_javadir}/%{srcname}/derbyLocale_ja_JP.jar
%lang(ko_KR) %{_javadir}/%{srcname}/derbyLocale_ko_KR.jar
%lang(pl) %{_javadir}/%{srcname}/derbyLocale_pl.jar
%lang(pt_BR) %{_javadir}/%{srcname}/derbyLocale_pt_BR.jar
%lang(ru) %{_javadir}/%{srcname}/derbyLocale_ru.jar
%lang(zh_CN) %{_javadir}/%{srcname}/derbyLocale_zh_CN.jar
%lang(zh_TW) %{_javadir}/%{srcname}/derbyLocale_zh_TW.jar

%attr(755,derby,derby) /var/lib/derby

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

%if 0
%files manual
%defattr(644,root,root,755)
%{_docdir}/%{name}
%endif
