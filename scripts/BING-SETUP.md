# Bing Webmaster Tools Setup

One-time manual steps. Takes ~10 minutes. Required for IndexNow dashboard + Bing sitemap monitoring.

---

## Step 1: Register at Bing Webmaster Tools

1. Go to: https://www.bing.com/webmasters
2. Sign in with a Microsoft account (create one free if needed)
3. Click **Add a Site** → enter `https://ergoremote.com`

## Step 2: Verify Site Ownership

Choose one method (XML file is easiest for Hugo):

**Option A — XML file (recommended):**
1. Bing gives you a file like `BingSiteAuth.xml`
2. Save it to `/home/Apollo/sites/affiliate-hub/static/BingSiteAuth.xml`
3. Run `hugo build` — file will appear at `public/BingSiteAuth.xml`
4. Click **Verify** in Bing Webmaster Tools

**Option B — Meta tag:**
1. Bing gives you a `<meta>` tag like `<meta name="msvalidate.01" content="XXXX" />`
2. Add it to `themes/affiliate-base/layouts/partials/head.html` after the IndexNow meta tag
3. Run `hugo build` then click **Verify**

## Step 3: Submit Sitemap

1. In Bing Webmaster Tools → **Sitemaps** → **Submit a Sitemap**
2. Enter: `https://ergoremote.com/sitemap.xml`
3. Click Submit — Bing will crawl within 24–48 hours

## Step 4: Add IndexNow API Key in Dashboard

1. Go to **IndexNow** tab in Bing Webmaster Tools
2. Enter API key: `a880730626f47ec8820cffe35d510f7d`
3. This links your manual script submissions to the verified property

---

## Running IndexNow After Each Publish

After every `hugo build` (or Cloudflare Pages deploy):

```bash
cd /home/Apollo/sites/affiliate-hub
./scripts/indexnow-ping.sh
```

This submits all 108 URLs to IndexNow in one bulk POST.
Coverage: **Bing, DuckDuckGo, ChatGPT (via Bing Search API), Yandex, Seznam, Naver**

Dry-run (no actual POST):
```bash
./scripts/indexnow-ping.sh --dry-run
```

---

## IndexNow Key Details

| Item | Value |
|---|---|
| API Key | `a880730626f47ec8820cffe35d510f7d` |
| Key file URL | `https://ergoremote.com/a880730626f47ec8820cffe35d510f7d.txt` |
| Key file path | `static/a880730626f47ec8820cffe35d510f7d.txt` |
| Meta tag | `<meta name="indexnow" content="a880730626f47ec8820cffe35d510f7d">` in head.html |

---

## Expected Results

- Bing indexes new/updated pages within **hours** (vs weeks for Google)
- DuckDuckGo picks up changes within 24–48 hours (uses Bing index)
- ChatGPT citations sourced via Bing Search API — IndexNow accelerates inclusion
- Yandex / Seznam / Naver also receive pings from the same POST
