#! /bin/bash

# cast letters to lower case
# remove trailing dots
# reverse the strings
# split by / and keep only the first part
# split by point and keep the two first parts
# reverse back
# sort
# and keep only the unique entries

cat source.txt | tr [A-Z] [a-z] | sed 's/\.$//' | rev | awk -F/ '{print $1}' | awk -F. '{printf "%s.%s\n", $1, $2}' | rev | sort | uniq
