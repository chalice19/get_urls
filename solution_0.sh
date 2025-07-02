#! /bin/bash


cat source.txt | \
  tr '[:upper:]' '[:lower:]' | \
  sed 's~^[a-zA-Z]*://~~' | \
  sed 's/[[:space:].]$//' | \
  awk -F. '{ n = NF if (n >= 2) print $(n-1) "." $n }' | \
  sort -u
