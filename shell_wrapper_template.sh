#!/bin/bash

#  *.sh: a script that 
#+ 
#+ i.e.,

DEFAULT_LOGFILE=logfile.txt

ARGS=1          # Script requires 1 arguments.
E_BADARGS= 85   # Wrong number of arguments passed to script.

if [ $# -ne "$ARGS" ]
then
  echo "Usage: `basename $0` "
  exit $E_BADARGS
fi

LOGFILE=
if [ -z "$LOGFILE" ]
then     # If not set, default to ...
  LOGFILE="$DEFAULT_LOGFILE"
fi

var1=$1         # Pass to more meaningful variable names
# ----------------
# Check input file
# ----------------
if [ -f "$3" ]
then
    file_name=$3
else
    echo "File \"$3\" does not exist."
    exit $E_BADARGS
fi

#         Command-line arguments, if any, for the operation.
OPTIONS="$@"


# Log it.
echo "`date` + `whoami` + $OPERATION "$@"" >> $LOGFILE
# Now, do it.
exec $OPERATION "$@"

exit $?  # Redirect the output of this script to write to a file.


