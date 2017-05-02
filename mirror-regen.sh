#!/bin/bash

# Initializing/Clearing Variables
ORG="TheMuppets"
OUTPUT="default.xml"
NUM_REPOS=0
NUM_PAGES=0
TMP=""
AUTH=""
if [ -n "$1" ]; then
  AUTH="-u $1"
fi
echo -n "" > $OUTPUT

function filter_json()
{
  # Define filter function to extract data from the JSON returned by the GitHub API
  cat - | grep "\"$1\"" | sed -e "s/ *\"$1\": \"//g" | sed -e "s/ *\"$1\": //g" | sed -e "s/\",$//g" | sed -e "s/,$//g"
}

# Fetching Organization Information (Number of Repos, etc.)
echo "---- Fetching organization information ----"
NUM_REPOS=$(curl -i -# $AUTH "https://api.github.com/orgs/$ORG" | filter_json "public_repos")
NUM_PAGES=$(( NUM_REPOS / 100 ))
if [ $((NUM_PAGES * 100)) -lt $NUM_REPOS ]; then
  NUM_PAGES=$((NUM_PAGES+1))
fi
echo ""
echo "Number of Repos: $NUM_REPOS"
echo "Number of Pages: $NUM_PAGES"
echo ""

# Fetch the repo names
COUNTER=1
while [ ! $COUNTER -gt $NUM_PAGES ]; do
  echo "---- Fetching page $COUNTER of $NUM_PAGES ----"
  if [ "$TMP" != "" ]; then
    TMP="$TMP
"
  fi
  TMP="$TMP$(curl -# $AUTH "https://api.github.com/orgs/$ORG/repos?per_page=100&type=public&page=$COUNTER" | filter_json "full_name")"
  let COUNTER=COUNTER+1
  echo ""
done

# Write to the output file
cat >> $OUTPUT << "EOF"
<?xml version="1.0" encoding="UTF-8"?>
<manifest>

  <remote  name="github"
           fetch=".." />

  <default revision="master"
           remote="github"
           sync-j="4" />

EOF
while read repo; do
  echo "  <project name=\"$repo\" />" >> $OUTPUT
done <<< "$(echo "$TMP" | sort - | uniq )"
echo "</manifest>" >> $OUTPUT

echo "Done generating manifest at $OUTPUT"
