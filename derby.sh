#!/bin/sh
# 
# Derby script
# Lubomir Rintel <lkundrak@v3.sk>

# Source functions library
if [ -f /usr/share/java-utils/java-functions ] ; then 
	. /usr/share/java-utils/java-functions
else
	echo >&2 "Can't find functions library, aborting"
	exit 1
fi

# Configuration
SCRIPT_PATH=$0
PROGNAME=$(basename $SCRIPT_PATH |sed 's/^derby-//')

# Wrappers
[ $PROGNAME = ij ]		&& MAIN_CLASS=org.apache.derby.tools.ij
[ $PROGNAME = sysinfo ]		&& MAIN_CLASS=org.apache.derby.tools.sysinfo
[ $PROGNAME = NetworkServerControl ] && MAIN_CLASS=org.apache.derby.drda.NetworkServerControl
[ $PROGNAME = startNetworkServer ] && MAIN_CLASS=org.apache.derby.drda.NetworkServerControl
[ $PROGNAME = stopNetworkServer ] && MAIN_CLASS=org.apache.derby.drda.NetworkServerControl

# Default parameters
[ $PROGNAME = startNetworkServer ] && set -- start "$@"
[ $PROGNAME = stopNetworkServer ] && set -- shutdown "$@"

# Load system-wide configuration
if [ -f /etc/derby.conf ]; then
  . /etc/derby.conf
fi

# Load user configuration
[ -f "$HOME/.derbyrc" ] && . "$HOME/.derbyrc"
[ -f "$HOME/.derby/startup" ] && . "$HOME/.derby/startup"

# Bail out if there's nothing to run
if [ -z "$MAIN_CLASS" ]; then
	echo >&2 "Can not determine main class for '$PROGNAME'"
	exit 1
fi

# Not loading all of derby, so that secure class loader can kick in
BASE_JARS="$BASE_JARS derby/derby"
BASE_JARS="$BASE_JARS derby/derbynet"
BASE_JARS="$BASE_JARS derby/derbytools"
BASE_JARS="$BASE_JARS derby/derbyclient"

# Set parameters
set_jvm
set_classpath $BASE_JARS
set_flags $BASE_FLAGS
set_options $BASE_OPTIONS $DERBY_OPTS

# Add locales in a rather dirty way
CLASSPATH=$CLASSPATH:$(build-classpath derby |sed 's/:/\n/g' |
	grep derbyLocale |xargs echo |sed 's/ /:/g')

# Let's start
run "$@"
