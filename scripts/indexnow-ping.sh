#!/usr/bin/env bash
# indexnow-ping.sh — Submit all URLs from sitemap.xml to IndexNow
# Covers: Bing, DuckDuckGo (via Bing), ChatGPT (via Bing Search API), Yandex, Seznam
#
# Usage:
#   ./scripts/indexnow-ping.sh                # submits all URLs in public/sitemap.xml
#   ./scripts/indexnow-ping.sh --dry-run      # print URLs only, no POST
#
# Requirements: curl, python3 (or xmllint)
# Run after every `hugo build` that adds/changes content.

set -euo pipefail

SITE_URL="https://ergoremote.com"
API_KEY="a880730626f47ec8820cffe35d510f7d"
KEY_LOCATION="${SITE_URL}/${API_KEY}.txt"
SITEMAP="${BASH_SOURCE%/*}/../public/sitemap.xml"
INDEXNOW_ENDPOINT="https://api.indexnow.org/indexnow"
DRY_RUN=false

for arg in "$@"; do
  [[ "$arg" == "--dry-run" ]] && DRY_RUN=true
done

if [[ ! -f "$SITEMAP" ]]; then
  echo "ERROR: sitemap not found at $SITEMAP — run hugo build first"
  exit 1
fi

# Extract all <loc> URLs from sitemap
URLS=$(python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('$SITEMAP')
root = tree.getroot()
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs = [loc.text.strip() for loc in root.findall('.//sm:loc', ns) if loc.text]
print('\n'.join(locs))
")

URL_COUNT=$(echo "$URLS" | wc -l)
echo "Found $URL_COUNT URLs in sitemap"

if $DRY_RUN; then
  echo "[DRY RUN] Would submit:"
  echo "$URLS"
  exit 0
fi

# IndexNow accepts bulk submission — max 10,000 URLs per POST
# Build JSON array
URL_JSON=$(python3 -c "
import json, sys
urls = [u for u in '''$URLS'''.split('\n') if u.strip()]
print(json.dumps(urls))
")

PAYLOAD=$(python3 -c "
import json
data = {
  'host': 'ergoremote.com',
  'key': '$API_KEY',
  'keyLocation': '$KEY_LOCATION',
  'urlList': json.loads('''$URL_JSON''')
}
print(json.dumps(data, indent=2))
")

echo "Submitting $URL_COUNT URLs to IndexNow..."

HTTP_CODE=$(curl -s -o /tmp/indexnow-response.json -w "%{http_code}" \
  -X POST "$INDEXNOW_ENDPOINT" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$PAYLOAD")

RESPONSE=$(cat /tmp/indexnow-response.json 2>/dev/null || echo "(empty)")

if [[ "$HTTP_CODE" == "200" || "$HTTP_CODE" == "202" ]]; then
  echo "✅ IndexNow submission accepted (HTTP $HTTP_CODE)"
  echo "   Coverage: Bing, DuckDuckGo, ChatGPT (via Bing), Yandex, Seznam, Naver"
elif [[ "$HTTP_CODE" == "422" ]]; then
  echo "⚠️  HTTP 422 — one or more URLs invalid or not under host. Check sitemap."
  echo "Response: $RESPONSE"
  exit 1
else
  echo "❌ IndexNow error: HTTP $HTTP_CODE"
  echo "Response: $RESPONSE"
  exit 1
fi
