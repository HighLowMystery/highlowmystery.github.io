# Google Search Console Setup — ErgoRemote

Manual one-time setup for Boss.

## 1) Open Search Console
- Go to: https://search.google.com/search-console
- Sign in with the Google account you want tied to ErgoRemote

## 2) Add the property
- Click **Add property**
- Choose **Domain**
- Enter: `ergoremote.com`
- Continue

## 3) Verify via DNS (CNAME/TXT method shown by Google)
Google will give you a DNS verification record for the domain.

Typical flow:
- Copy the DNS record Google provides
- Open your DNS provider for `ergoremote.com`
- Add the verification record exactly as shown
- Save DNS changes
- Return to Search Console and click **Verify**

Notes:
- DNS propagation can take a few minutes to a few hours
- If verification fails immediately, wait 10–15 minutes and try again

## 4) Submit the sitemap
After verification:
- In Search Console, open **Sitemaps**
- Submit this sitemap URL:
  - `https://ergoremote.com/sitemap.xml`

## 5) What to expect
- Initial discovery can take a few days
- Indexing is not instant even after sitemap submission
- Re-check **Pages** and **Sitemaps** reports over the next 1–2 weeks

## Current local verification
- Local sitemap path: `/home/Apollo/sites/affiliate-hub/public/sitemap.xml`
- Current URL count: 64
- Base URL: `https://ergoremote.com/`
