#! /bin/bash

cat source.txt | tr [A-Z] [a-z] | sed 's/\.$//' | rev | awk -F/ '{print $1}' | awk -F. '{printf "%s.%s\n", $1, $2}' | rev | sort | uniq
