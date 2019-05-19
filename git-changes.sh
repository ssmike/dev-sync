#!/bin/bash
cd $1
git status --porcelain | cut -d' ' -f2
