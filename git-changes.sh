#!/bin/bash
p=$PWD
cd $1
git status --porcelain | sed -e 's/.*\s//g' > $p/.changelist
cd $p
python daemon.py --src $1 --host $2 --dst $3 --sync .changelist
