#!/bin/bash
svn st $1 | sed -e 's/.*\s//g'
