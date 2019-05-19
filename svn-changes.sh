#!/bin/bash
svn st $1 | sed -e 's/.*\s//g' > .changelist
python daemon.py --src $1 --host $2 --dst $3 --sync .changelist
