#!/usr/bin/env python3
"""
Google People Also Ask (PAA) Scraper — Affiliate Pipeline
Scrapes "People Also Ask" sections for long-tail keyword discovery.
Uses Playwright (headless browser) for JavaScript-rendered content.

Also fetches Google Autocomplete suggestions (free, no API key needed).
"""

import json
import time
import urllib.request
import urllib.parse
import os
import subprocess
from datetime import datetime

OUTPUT_DIR = f"/home/Apollo/sites/affiliate-hub/scraped-data/{datetime.now().strftime('%Y-%m-%d')}"

# Seed queries for our niche
SEED_QUERIES = [
    "best ergonomic chair",
    "best home office chair",
    "standing desk review",
    "best monitor for work from home",
    "ergonomic desk setup",
    "home office setup guide",
    "best laptop stand",
    "ergonomic keyboard and mouse",
    "how to reduce back pain working from home",
    "best USB hub for home office",
    "herman miller vs steelcase",
    "best budget ergonomic chair",
    "standing desk mat review",
    "best webcam for home office",
    "home office lighting setup",
]

def get_autocomplete_suggestions(query):
    """Get Google Autocomplete suggestions using the free suggestion API."""
    encoded = urllib.parse.quote(query)
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={encoded}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            suggestions = data[1] if len(data) > 1 else []
            return suggestions
    except Exception as e:
        print(f"  [WARN] Autocomplete failed for '{query}': {e}")
        return []

def get_paa_via_playwright(query):
    """Get People Also Ask results using Playwright (requires playwright installed)."""
    script = f"""
import asyncio
from playwright.async_api import async_playwright

async def get_paa(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Set realistic headers
        await page.set_extra_http_headers({{
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }})
        
        encoded = query.replace(' ', '+')
        await page.goto(f"https://www.google.com/search?q={{encoded}}&hl=en")
        await page.wait_for_timeout(2000)
        
        # Try to get PAA questions
        paa_questions = []
        try:
            questions = await page.query_selector_all('[data-q]')
            for q in questions:
                text = await q.inner_text()
                if text and len(text) > 10:
                    paa_questions.append(text.strip())
        except:
            pass
        
        # Also try alternative selectors
        try:
            elements = await page.query_selector_all('.related-question-pair span')
            for el in elements:
                text = await el.inner_text()
                if text and len(text) > 10 and '?' in text:
                    paa_questions.append(text.strip())
        except:
            pass
        
        await browser.close()
        return list(set(paa_questions))

result = asyncio.run(get_paa("{query.replace('"', '')}"))
import json
print(json.dumps(result))
"""
    
    try:
        result = subprocess.run(
            ["python3", "-c", script],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout.strip())
        return []
    except Exception as e:
        print(f"  [WARN] PAA playwright failed for '{query}': {e}")
        return []

def analyze_keyword_opportunity(query, suggestions, paa_questions):
    """Score and categorize keyword opportunities."""
    opportunities = []
    
    all_keywords = [query] + suggestions + paa_questions
    
    for kw in all_keywords:
        kw = kw.strip()
        if len(kw) < 10:
            continue
        
        # Score signals
        score = 0
        article_type = "general"
        
        kw_lower = kw.lower()
        
        # Buying intent signals (high value)
        if any(w in kw_lower for w in ["best", "top", "review", "buy", "worth"]):
            score += 3
            article_type = "best-picks"
        
        if any(w in kw_lower for w in ["vs", "versus", "compared", "difference"]):
            score += 3
            article_type = "comparison"
        
        if any(w in kw_lower for w in ["how to", "how do", "guide", "tips"]):
            score += 2
            article_type = "how-to"
        
        # Price modifiers (conversion gold)
        if any(w in kw_lower for w in ["under $", "cheap", "budget", "affordable", "under 100", "under 200", "under 300", "under 500"]):
            score += 2
        
        # Pain point modifiers
        if any(w in kw_lower for w in ["back pain", "neck pain", "wrist", "posture", "comfortable"]):
            score += 2
        
        # Specific product categories we cover
        if any(w in kw_lower for w in ["chair", "desk", "monitor", "keyboard", "mouse", "stand", "hub", "webcam", "lighting", "mat"]):
            score += 1
        
        if score >= 2:
            opportunities.append({
                "keyword": kw,
                "score": score,
                "article_type": article_type,
                "source": "paa" if kw in paa_questions else ("suggestion" if kw in suggestions else "seed"),
                "slug_idea": kw_lower.replace(" ", "-").replace("?", "").replace("$", "").replace("/", "-")[:60]
            })
    
    return sorted(opportunities, key=lambda x: x["score"], reverse=True)

def main():
    print(f"🔍 PAA/Autocomplete Scraper starting — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_opportunities = []
    
    # Check if playwright is available
    playwright_available = False
    try:
        result = subprocess.run(["python3", "-c", "from playwright.async_api import async_playwright"], 
                               capture_output=True, timeout=5)
        playwright_available = result.returncode == 0
    except:
        pass
    
    if not playwright_available:
        print("  [INFO] Playwright not available — using autocomplete only (good enough for now)")
    
    for i, query in enumerate(SEED_QUERIES):
        print(f"  [{i+1}/{len(SEED_QUERIES)}] Processing: '{query}'")
        
        # Always get autocomplete (free, fast, reliable)
        suggestions = get_autocomplete_suggestions(query)
        print(f"    → {len(suggestions)} autocomplete suggestions")
        
        # Get PAA if playwright available
        paa = []
        if playwright_available:
            paa = get_paa_via_playwright(query)
            print(f"    → {len(paa)} PAA questions")
            time.sleep(3)  # Be respectful
        
        opportunities = analyze_keyword_opportunity(query, suggestions, paa)
        all_opportunities.extend(opportunities)
        
        time.sleep(2)  # Rate limiting
    
    # Deduplicate
    seen = set()
    unique_opps = []
    for opp in all_opportunities:
        if opp["keyword"] not in seen:
            seen.add(opp["keyword"])
            unique_opps.append(opp)
    
    # Sort by score
    unique_opps.sort(key=lambda x: x["score"], reverse=True)
    
    # Save outputs
    keywords_file = f"{OUTPUT_DIR}/keyword-opportunities.json"
    
    with open(keywords_file, "w") as f:
        json.dump(unique_opps[:100], f, indent=2)
    
    # Append to master keyword list
    master_keywords_file = "/home/Apollo/sites/affiliate-hub/data/master-keywords.json"
    os.makedirs(os.path.dirname(master_keywords_file), exist_ok=True)
    
    existing = []
    if os.path.exists(master_keywords_file):
        with open(master_keywords_file) as f:
            try:
                existing = json.load(f)
            except:
                existing = []
    
    existing_kws = {k["keyword"] for k in existing}
    new_keywords = [k for k in unique_opps if k["keyword"] not in existing_kws]
    
    with open(master_keywords_file, "w") as f:
        json.dump(existing + new_keywords, f, indent=2)
    
    print(f"\n✅ Keyword scrape complete!")
    print(f"   Total opportunities: {len(unique_opps)}")
    print(f"   New to master list: {len(new_keywords)}")
    print(f"   Output: {keywords_file}")
    
    print("\n🔥 Top 10 keyword opportunities:")
    for opp in unique_opps[:10]:
        print(f"  [{opp['score']}★] ({opp['article_type']}) {opp['keyword']}")
    
    return {
        "total_opportunities": len(unique_opps),
        "new_keywords": len(new_keywords),
        "top_5": [o["keyword"] for o in unique_opps[:5]]
    }

if __name__ == "__main__":
    result = main()
    print(f"\nResult: {json.dumps(result)}")
