#! /bin/bash

# cast letter to lower case
# remove http[s]:// from the beginning of the strings
# remove trailing point
# keep the last two part splitted by points
# sort keeping the unque entries

cat source.txt | \
  tr '[:upper:]' '[:lower:]' | \
  sed 's/^https\?:\/\///' | \
  sed 's/[.]*$//'
  awk -F. '{ n = NF ; print $(n-1) "." $n }' | \
  sort -u
