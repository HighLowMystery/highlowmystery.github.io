# MASTER-PLAN.md — ErgoRemote Affiliate Strategy
# Last updated: 2026-04-09 | v2 (Corrected with verified Amazon policy)

## What We're Building
- Site: ErgoRemote (ergoremote.com)
- Niche: Home office ergonomics
- Monetization: Amazon Associates (tag: highlowmyst0e-20)
- Stack: Hugo static site on Cloudflare Pages
- Current state: 21 articles live, 0 GSC impressions (not indexed yet)

---

## 🚨 URGENT: Amazon April 14, 2026 Policy Update
Source: affiliate-program.amazon.com/help/operating/compare
- "Original Content" now REQUIRES commentary, analysis, or transformation
- Onsite commission now only for Direct Qualifying Purchases of same ASIN variant
- 180-day shipping/payment time limit
- Purchases from paid/boosted ads linking to Amazon = DISQUALIFIED from commission
- Action: Audit all 21 articles for compliance BEFORE Monday April 14

---

## Phase 1: COMPLIANCE & FOUNDATIONS (This Week — HARD DEADLINE Monday April 14)

### P0: Editorial Opinion Audit (BEFORE MONDAY)
- [ ] Audit all 21 articles: each must have commentary, analysis, or transformation
- [ ] Any article that's pure product listing without opinion → add "Our Verdict" / "Bottom Line" section
- [ ] Our articles already have first-person voice — verify none slipped through as generic
- [ ] Ensure Amazon affiliate disclosure is on every page

### P1: Author Identity Fix
- [ ] Replace "Work From Home Pro" with real pen name + credentials
- [ ] Create detailed author bio on every article page
- [ ] Update About page with verifiable experience claims
- [ ] Add Author schema linked to about page
- [ ] This satisfies both Google EEAT and Amazon "real person" signals

### P2: Schema Upgrades
- [ ] Add FAQ schema to all 21 articles (questions as H2/H3)
- [ ] Add Product/Review schema per product recommendation
- [ ] Add ProductCollection schema to all listicles (enables price comparison rich results)
- [ ] Validate all schema with Google Rich Results Test

### P3: "Answer-First" Verdict Boxes
- [ ] Each product section (H2) needs a 2-sentence verdict at the top
- [ ] Our `{{< quick-answer >}}` at page top is good — extend to per-section
- [ ] This increases per-section AI citation probability

---

## Phase 2: INDEXING & VISIBILITY (Weeks 2-4)

### Google
- [ ] Submit sitemap to Google Search Console
- [ ] Manual URL submission of all 21 articles via GSC URL Inspection
- [ ] Monitor for first impressions (currently 0 rows)

### Bing (Priority — less competition, feeds ChatGPT)
- [ ] Register at bing.com/webmasters
- [ ] Submit sitemap to Bing Webmaster Tools
- [ ] Implement IndexNow protocol in Hugo build pipeline
  - IndexNow pings Bing + Yandex + Naver + Seznam on every publish
  - 22% of clicked Bing URLs come from IndexNow
  - DuckDuckGo uses Bing's index → covered automatically
  - ChatGPT uses Bing Search API → IndexNow feeds ChatGPT citations
- [ ] Monitor Bing indexing (typically faster than Google for new sites)

---

## Phase 3: CONTENT SCALING (Month 2, after indexing confirmed)
- Cadence: 2-3 articles/week (quality over volume, move slowly)
- Scale ONLY after GSC/Bing shows consistent indexing within 24-48 hours
- Never exceed 1 article/day in first 6 months (avoid content farm signals)

### Topic Clusters (build depth, not breadth)
- Cluster 1: "Work From Home [Country]" (India, Philippines, Malaysia) — low competition
- Cluster 2: "Best [Product] for Tall People" (chairs, desks, monitors) — semantic depth
- Cluster 3: "Home Office Under $[Budget]" ($500, $1000, $2000) — buyer intent

### Content Freshness
- Quarterly refresh cycle on all published articles
- Visible "Last Updated" date on every article
- Pages not updated in 12 months lose 70%+ of AI citations
- Research Grunt cron: quarterly audit for stale content

---

## Phase 4: AUTHORITY BUILDING (Month 2-3)

### Backlinks (Quality > Quantity)
- Research Grunt: Find 10 relevant podcasts/newsletters in remote work niche
- Strategy: "Review Exchange" — review their content on ErgoRemote, they mention us in show notes
- Brand mentions (even without links) count as ranking signals in 2026
- Research Winnipeg tech/remote-work communities for .ca mentions
- Goal: 5-10 quality backlinks in first 3 months

### Local Authority Play
- Winnipeg-based .ca mentions from local institutions = high trust signals
- Target: RRC Polytech blogs, local coworking spaces, Manitoba tech meetups
- Proves to Google: real person, not faceless bot farm

---

## Phase 5: GEO OPTIMIZATION (Month 3+)

### Structure for AI Citation
- Direct answer in first 50 words → "Why it matters" (100-150 words) → Deep analysis (1000+ words)
- FAQ schema on every article
- "Answer-First" verdict boxes per H2 section
- 32.5% of all LLM citations come from comparative listicles (our exact format)

### Interactive Tools (Month 4+)
- "Find Your Ideal Desk Height" calculator
- "Ergonomic Chair Fit Finder" quiz
- These keep users on-site (zero-click shield)

### Monitor AI Citation Share
- Spot-check Perplexity and Google AI Overview for our target keywords
- Track which articles get cited and which don't
- Double down on formats that earn citations

---

## Search Engine Strategy
| Engine | Share | Priority | Strategy |
|---|---|---|---|
| Google | 84% US | Primary | EEAT, quality content, schema, sitemap |
| Bing | 10-17% US desktop | Secondary (high ROI) | IndexNow, clean meta, JSON-LD, Webmaster Tools |
| DuckDuckGo | ~2% | Covered by Bing | Uses Bing's index |
| ChatGPT/Perplexity | Growing | Covered by Bing + GEO | Uses Bing API + favors citation-ready content |

---

## Key 2026 SEO Facts (Verified)
- Google March 2026 Core Update: "Experience" in EEAT is now primary differentiator
- AI content fine IF anchored to real experience. AI-only generalities penalized.
- Author bios with verifiable credentials directly influence page authority
- GEO is real: 32.5% of LLM citations come from comparative listicles
- Backlinks still valid: quality > quantity, brand mentions count without links
- New site sandbox: Google suppresses new domains until trust established
- Content freshness: pages not updated in 12 months lose 70%+ AI citations
- IndexNow: 5B+ daily URLs, 22% of Bing clicks, feeds ChatGPT
- Amazon April 14 policy: original content must have commentary/analysis/transformation

## ASIN Variant Risk (New April 14 Rule)
- New rule: commission only applies to "Direct Qualifying Purchases of the same ASIN variant"
- Old way: user clicks your link, buys a different color/size, you still get commission on entire cart
- New way: if your link is for Blue variant and they buy Red, it may be disqualified
- Our status: 65 direct /dp/ links (specific ASIN) + 24 search /s?k= links (safer)
- Fix: where possible, link to parent ASIN or use search links. Add "Prices vary by color/size" disclaimer
- MC task: audit product links for variant-specific ASINs and convert to parent where possible

## What NOT To Do
- 10+ articles/day = content farm → penalized
- AI-generated fake "testing lab" photos → violates EEAT
- Buying backlinks → Google's 2026 detection catches this
- Keyword stuffing → dead strategy
- Running paid ads through affiliate links → Amazon now disqualifies these purchases
- Panic scaling before indexing is confirmed

## Research Team Upgrade
Research Grunt focus: "friction points" not "keyword volumes"
- Reddit: what people hate about top products (r/homeoffice, r/ergonomics, r/standingdesk)
- Unanswered questions in niche subreddits
- Competitor content gaps
- User intent: "why does my back hurt" > "best ergonomic chair"
- Quarterly: check all published articles for staleness
