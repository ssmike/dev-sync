#!/bin/bash
cd $1
git status --porcelain | sed -e 's/.*\s//g'
