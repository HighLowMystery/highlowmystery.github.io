# AFFILIATE-PLAYBOOK.md — Reusable Niche Site Blueprint
# Version: 1.0 | Created: 2026-04-09
# Purpose: Template for launching any new affiliate site. Proven strategies only.
# Based on: ErgoRemote learnings + verified 2026 SEO/affiliate research

---

## 🏗️ PHASE 0: FOUNDATION (Before any content)

### Site Setup
- [ ] Choose niche with: buyer intent, $100-$500 product range, passionate community
- [ ] Register domain (prefer .com, or country TLD if targeting specific country)
- [ ] Static site generator (Hugo recommended — fast, cheap hosting)
- [ ] Cloudflare Pages for hosting (free, fast CDN)
- [ ] Set up Google Search Console + Bing Webmaster Tools from day 1
- [ ] Submit sitemap to both immediately

### Amazon Associates
- [ ] Apply with 5-10 original articles already live
- [ ] Must generate 3 qualified sales within first 180 days
- [ ] Affiliate disclosure on every page: "As an Amazon Associate, I earn from qualifying purchases."
- [ ] Track your tag (format: yourname-20)

### Compliance (as of April 2026)
- [ ] Every article must contain "commentary, analysis, or transformation for additional value"
- [ ] No copied Amazon product descriptions
- [ ] No paid/boosted ads linking through affiliate URLs (purchases get disqualified)
- [ ] Link to parent ASIN when possible (not specific color/size variants)
- [ ] Commission only counts for "Direct Qualifying Purchases of same ASIN variant"

### Schema Markup (build into theme from day 1)
- [ ] Article schema on every page
- [ ] Person schema (author identity)
- [ ] Organization schema
- [ ] FAQ schema on articles with FAQ sections
- [ ] Product/Review schema on product recommendations
- [ ] ProductCollection schema on listicle/roundup pages

---

## 📝 PHASE 1: CONTENT (Weeks 1-8)

### Author Identity (EEAT requirement — do this FIRST)
- [ ] Real pen name or identity (not "Staff Writer" or "Admin")
- [ ] Author bio with verifiable credentials on every article
- [ ] Detailed About page with experience claims
- [ ] Link author bio to educational/professional background where possible
- [ ] Location-specific experience signals (climate testing, local context = unfakeable)

### Article Formula (proven format)
```
Structure for every article:
1. Quick Answer box (50 words — direct recommendation, AI-friendly)
2. Personal story intro (first-person, real experience)
3. Quick Picks table (product names + prices + one-line verdict)
4. Individual product reviews (each H2 starts with 2-sentence "Verdict")
   - Pros/Cons from actual use
   - Who it's for / who should skip it
   - Editorial opinion (not just specs)
5. Buying Guide (what to look for, common mistakes)
6. FAQ section (with FAQ schema)
7. Amazon affiliate disclosure
```

### Content Standards
- First-person voice throughout (real experiences, not generic)
- 9th grade reading level (Hemingway app)
- 2,000-4,000 words depending on topic depth
- Editorial commentary in every section (Amazon requires "commentary, analysis, or transformation")
- Never copy product descriptions from Amazon
- "Verdict" box at start of every product H2 (GEO snippet bait)

### Publishing Cadence
- Weeks 1-4: 2-3 articles/week (build foundation)
- Month 2-3: 3-4 articles/week (only after indexing confirmed in GSC)
- Month 4-6: maintain 3-4/week, focus on topic clusters
- NEVER: 10+ articles/day (content farm signal → penalized)
- Quality > quantity at every stage

### Topic Clusters (build depth, not scattered keywords)
```
Example cluster for "ergonomic chairs":
- Hub: "Complete Guide to Ergonomic Chairs"
- Spoke: "Best Ergonomic Chair for Back Pain"
- Spoke: "Best Budget Ergonomic Chair Under $300"
- Spoke: "Best Ergonomic Chair for Tall People"
- Spoke: "Ergonomic Chair vs Standing Desk: Which Is Better?"
- Spoke: "How to Adjust Your Ergonomic Chair Properly"
Each spoke links to hub. Hub links to all spokes.
```

---

## 🔍 PHASE 2: INDEXING (Weeks 2-6)

### Google
- [ ] Submit sitemap to Google Search Console
- [ ] Manually submit each article via GSC URL Inspection tool
- [ ] Monitor for first impressions (new sites take 2-8 weeks)
- [ ] Google does NOT support IndexNow — uses its own crawling

### Bing (High ROI, less competition)
- [ ] Register at bing.com/webmasters
- [ ] Submit sitemap
- [ ] Implement IndexNow protocol:
  - Generate API key at bing.com/indexnow
  - Add key file to static/ folder
  - Script: ping IndexNow API on every publish
  - One ping covers: Bing + Yandex + Naver + Seznam + DuckDuckGo (uses Bing index)
  - ChatGPT uses Bing Search API → IndexNow feeds ChatGPT too
- [ ] Bing desktop market share: 10-17% US — real traffic
- [ ] Bing SEO is simpler: rewards exact keyword matching, clean meta descriptions

### Indexing Facts
- New sites face Google "sandbox" — reduced visibility until trust established
- Bing is often faster to index new sites
- Don't panic if GSC shows 0 data for weeks — this is normal
- Scale content ONLY after you see consistent 24-48 hour indexing

---

## 🔗 PHASE 3: AUTHORITY (Month 2-6)

### Backlinks Strategy (quality > quantity)
- Brand mentions (even without links) now count as ranking signals
- Target: 5-10 quality backlinks in first 3 months
- Methods:
  - [ ] Find 10 niche podcasts/newsletters → "Review Exchange" (you review them, they mention you)
  - [ ] Guest post on related blogs
  - [ ] Local authority play: .ca / .edu / local institution mentions
  - [ ] HARO (Help a Reporter Out) — respond to journalist queries in your niche
- Do NOT: buy backlinks, link exchange schemes, PBNs, comment spam

### Local Authority (if applicable)
- Mention your city/region in content (weather testing, local context)
- Get mentioned on local institution sites (universities, meetup groups, coworking spaces)
- This signals "real person" to Google — impossible for bot farms to fake

---

## 🤖 PHASE 4: GEO & AI OPTIMIZATION (Month 3+)

### Generative Engine Optimization (GEO)
- AI engines (Google AI Overview, Perplexity, ChatGPT) now cite sources directly
- 32.5% of all LLM citations come from comparative listicles
- Best structure: Direct answer (50 words) → Why it matters (150 words) → Deep analysis (1000+ words)
- FAQ schema increases AI citation probability
- Per-section "Verdict" boxes = per-section snippet bait for AI engines

### Content Freshness
- Pages not updated in 12 months lose 70%+ of AI citations
- Quarterly refresh cycle on all published articles
- Visible "Last Updated" date on every article
- Update prices, product availability, add new competitors

### Interactive Tools (Month 4+)
- Calculators, quizzes, finders (e.g., "Find Your Ideal Desk Height")
- These keep users on-site (zero-click shield)
- Build once, drives traffic and engagement permanently

---

## 📊 KEY METRICS TO TRACK

| Metric | Tool | Target |
|---|---|---|
| Indexed pages | GSC + Bing Webmaster | All pages indexed within 48 hours |
| Organic impressions | GSC | Growing week over week |
| Click-through rate | GSC | >3% average |
| Amazon conversion rate | Amazon Associates dashboard | >5% for "best X" articles |
| AI citations | Manual spot-check Perplexity/Google AI | Appearing for target keywords |
| Backlinks | Bing Webmaster backlink report | 5-10 quality in 3 months |
| Content freshness | Manual audit | No article >6 months without update |

---

## 🚫 WHAT NEVER TO DO (learned the hard way)

1. **Never** publish 10+ articles/day — content farm signals
2. **Never** use AI-generated fake product photos — violates EEAT
3. **Never** buy backlinks — Google's 2026 detection is sophisticated
4. **Never** run paid ads through affiliate links — Amazon disqualifies purchases
5. **Never** copy Amazon product descriptions — instant rejection risk
6. **Never** publish without editorial opinion — Amazon requires commentary/analysis
7. **Never** use a generic author name — EEAT requires verifiable identity
8. **Never** keyword stuff — dead since 2022
9. **Never** ignore Bing — 10-17% desktop share, feeds ChatGPT, less competition
10. **Never** scale before indexing is confirmed — build foundation first

---

## 🔄 REPEATING FOR A NEW SITE

To launch a new niche site using this playbook:
1. Copy this file to the new project
2. Replace niche-specific details (products, keywords, clusters)
3. Follow phases in order — don't skip ahead
4. Use same Hugo theme + schema setup (saves weeks)
5. Same Amazon tag works across multiple sites
6. Each site needs its own GSC + Bing Webmaster Tools property
7. Each site needs its own unique author identity
8. Share backlink-building effort across sites where relevant

---

*Last verified: April 2026 | Sources: Amazon Associates Operating Agreement, Google March 2026 Core Update, Bing SEO documentation, GEO research papers*
