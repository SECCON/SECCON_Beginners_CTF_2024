#!/bin/bash

rm -rf /var/www/htmls/ctf/*

base_path="/var/www/htmls/ctf/"

depth=$((RANDOM % 10 + 15))

current_path="$base_path"

for i in $(seq 1 $depth); do
  char=$(printf "%d" $((RANDOM % 36)))
  if [[ $char -lt 26 ]]; then
    char=$(printf "\\$(printf "%03o" $((char + 97)) )")
  else
    char=$(printf "%d" $((char - 26)))
  fi
  current_path+="${char}/"
  mkdir -p "$current_path"
done

echo 'ctf4b{*****REDACTED*****}' > "${current_path}flag.txt"