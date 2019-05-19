#!/bin/bash
svn st -q $1 | cut -d ' ' -f 8
