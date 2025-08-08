#!/bin/bash

BASE_URL="https://pioneers-swaps.com"
HTML_FILE="loading.html"
ASSETS_DIR="assets"

# Download the homepage HTML
curl -s "$BASE_URL" -o "$HTML_FILE"

# Extract asset URLs from href and src attributes
grep -oP '(?<=href=")[^"]+|(?<=src=")[^"]+' "$HTML_FILE" | \
grep -E '\.(css|js|png|jpg|jpeg|gif|svg)$' | \
sort -u > asset_urls.txt

mkdir -p "$ASSETS_DIR"

# Download each asset
while read -r url; do
  # If the URL is relative, prepend the base URL
  if [[ $url != http* ]]; then
    full_url="${BASE_URL}${url}"
  else
    full_url="$url"
  fi

  filename=$(basename "$url")

  echo "Downloading $full_url"
  curl -s "$full_url" -o "$ASSETS_DIR/$filename"
done < asset_urls.txt

# Replace redirect URL /pi/ with index.html in the downloaded HTML file
sed -i 's|/pi/|index.html|g' "$HTML_FILE"

echo "Done! Animation page is saved as $HTML_FILE with assets in $ASSETS_DIR/"
