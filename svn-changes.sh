#!/bin/bash
svn st $1 | cut -d ' ' -f 8 > .changelist
python daemon.py --src $1 --host $2 --dst $3 --sync .changelist
