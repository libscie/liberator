#!/bin/bash

# Return error if arg is missing
if [ ! "$1" ]; then
  echo "Please point towards cmine project directory"
  exit 1
fi

for path in $(ls $1/*/ -d)
do
  if [ -f "$path/fulltext.pdf" ]; then
    # Include country
    PUB=$(jq '.["publisher"]' "$path"crossref_result.json)
    # Include year
    YEAR=$(jq '.["published-print"]' "$path"crossref_result.json | jq '.["date-parts"][][]' | grep -P "\d{4}")

    if [ $YEAR -gt 1886 ]; then
      echo "This seems to published after 1886, so skipping this for now."
    else
      # Creator
      NAME=$(jq '.["author"][] | .family + ", " + .given' "$path"crossref_result.json || echo NA)
      AFFILIATION=$(jq '.["author"][]["affiliation"]' "$path"crossref_result.json || echo null)
      NAMES=$(echo "$NAME" | tr '\n' ' ' | sed 's/"//g')

      PUBLICATIONDATE=$(echo $(jq '.["published-print"]' "$path"crossref_result.json | jq '.["date-parts"][][]') | cut -d" " -f1)
      TITLE=$(jq .title[] "$path"crossref_result.json)
      CREATOR=$()
#      DESCRIPTION=$(scripts/description.sh $PUB $YEAR)
      DESCRIPTION="Any copyright on this work is most likely expired, given life expectancy and copyright duration at the time of publication, or when rolling copyright occurred (i.e., changes to the legislation extending the copyright term). In case of a takedown request, the depositor requests to be provided with legal documentation from the person/organization instigating the takedown request and to be heard by Zenodo before making a decision about the takedown."
      LICENSE="other-pd"
      DOI=$(jq .DOI "$path"crossref_result.json)
      NOTES="This file was uploaded by Chris Hartgerink (chris@libscie.org), 
      not the original authors or the publisher. This upload is part of 
      ensuring public access to the public domain.
      Please see description for legal justification of why this work is (likely to be) 
      in the public domain and it is considered reasonable to be uploaded to Zenodo."
      JOURNAL=$(jq '.["container-title"][]' "$path"crossref_result.json | tail -n 1)
      VOLUME=$(jq .volume "$path"crossref_result.json)
      ISSUE=$(jq .issue "$path"crossref_result.json)
      PAGES=$(jq .page "$path"crossref_result.json)

      DATA=$(cat <<EOF
{"metadata":{
      "upload_type": "publication",
      "publication_type": "article",
      "publication_date": "1823-01-01",
      "title": $TITLE,
      "creators": [{"name":"$NAMES"}],
      "description": "$DESCRIPTION",
      "access_right": "open",
      "license": "$LICENSE",
      "doi": $DOI,
      "keywords": ["public-domain"],
      "notes": "$NOTES",
      "journal_title": $JOURNAL,
      "journal_volume": $VOLUME,
      "journal_issue": $ISSUE,
      "journal_pages": $PAGES,
      "communities": [{"identifier":"libscie"}]}}
EOF
)
echo $DATA > "$path"zenodo-deposit.json

cat "$path"zenodo-deposit.json
      # Create deposit
      curl -iv -H "Content-Type: application/json" -X POST https://zenodo.org/api/deposit/depositions/?access_token=$TOKEN \
      --data @"$path"zenodo-deposit.json | tee "$path"zenodo.json

      # Get zenodo id
      zid=$(cat "$path"zenodo.json|tr , '\n'|awk '/"id"/{printf"%i",$2}')
      echo $zid
    
      # Add file to deposit
      curl -i -F name=fulltext.pdf -F file=@"$path"fulltext.pdf https://zenodo.org/api/deposit/depositions/$zid/files?access_token=$TOKEN
        
      # Publish deposit
      curl -i -X POST "https://zenodo.org/api/deposit/depositions/$zid/actions/publish?access_token=$TOKEN"
    fi
  fi
done
