#!/bin/bash
svn st $1 | sed -e 's/.*\s//g' > .changelist
DIR=`dirname $0`
python $DIR/daemon.py --src $1 --host $2 --dst $3 --sync .changelist
