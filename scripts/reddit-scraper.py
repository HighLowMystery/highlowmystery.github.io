#!/usr/bin/env python3
"""
Reddit Insight Scraper — Work From Home Pro Affiliate Pipeline
Scrapes r/WorkFromHome, r/HomeOffice, r/Ergonomics for:
- Pain points (content ideas)
- Product mentions (affiliate targets)
- Questions (FAQ / article ideas)

Uses Reddit's free JSON API — no auth required for public posts.
Rate limit: 1 request per 2 seconds (respectful)
"""

import json
import time
import urllib.request
import urllib.parse
import re
import os
from datetime import datetime

SUBREDDITS = [
    "WorkFromHome",
    "HomeOffice", 
    "Ergonomics",
    "DeskSetup",
    "battlestations",
]

# Keywords that signal buying intent / product research
BUYING_SIGNALS = [
    "recommend", "suggestion", "best", "worth it", "review",
    "bought", "purchased", "tried", "compared", "vs",
    "under $", "budget", "cheap", "affordable", "expensive",
    "chair", "desk", "monitor", "keyboard", "mouse", "stand",
    "back pain", "neck pain", "wrist pain", "posture"
]

OUTPUT_DIR = f"/home/Apollo/sites/affiliate-hub/scraped-data/{datetime.now().strftime('%Y-%m-%d')}"

def fetch_reddit_json(subreddit, sort="hot", limit=50):
    """Fetch posts from a subreddit using Reddit's public JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; affiliate-research-bot/1.0; personal use)"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  [WARN] Failed to fetch r/{subreddit}: {e}")
        return None

def score_relevance(text):
    """Score how relevant a post is to our affiliate niche."""
    text_lower = text.lower()
    score = sum(1 for signal in BUYING_SIGNALS if signal in text_lower)
    return score

def extract_insights(data, subreddit):
    """Extract valuable insights from Reddit JSON response."""
    insights = []
    if not data or "data" not in data:
        return insights
    
    posts = data["data"].get("children", [])
    for post in posts:
        d = post.get("data", {})
        title = d.get("title", "")
        selftext = d.get("selftext", "")
        score = d.get("score", 0)
        num_comments = d.get("num_comments", 0)
        permalink = d.get("permalink", "")
        
        full_text = f"{title} {selftext}"
        relevance = score_relevance(full_text)
        
        if relevance >= 2 or num_comments >= 20:
            insights.append({
                "subreddit": subreddit,
                "title": title,
                "excerpt": selftext[:300] if selftext else "",
                "upvotes": score,
                "comments": num_comments,
                "relevance_score": relevance,
                "url": f"https://reddit.com{permalink}",
                "content_idea": derive_content_idea(title)
            })
    
    # Sort by engagement
    insights.sort(key=lambda x: (x["relevance_score"] * 10 + x["comments"]), reverse=True)
    return insights[:20]  # Top 20 per subreddit

def derive_content_idea(title):
    """Derive a content article idea from a Reddit post title."""
    title_lower = title.lower()
    
    if any(w in title_lower for w in ["best chair", "chair recommendation", "chair help"]):
        return "Best Ergonomic Chairs article opportunity"
    elif any(w in title_lower for w in ["standing desk", "sit stand"]):
        return "Standing Desk guide opportunity"
    elif any(w in title_lower for w in ["monitor", "screen", "display"]):
        return "Monitor setup guide opportunity"
    elif any(w in title_lower for w in ["back pain", "neck pain", "wrist"]):
        return "Pain relief / ergonomics guide opportunity"
    elif any(w in title_lower for w in ["setup", "battlestation", "desk setup"]):
        return "Home office setup guide opportunity"
    elif "vs" in title_lower or "or" in title_lower:
        return "Comparison article opportunity"
    else:
        return "General content opportunity"

def extract_keywords(insights):
    """Extract keyword opportunities from insights."""
    keywords = {}
    
    common_queries = [
        r"best (\w+ ?\w*) (chair|desk|monitor|keyboard|mouse|stand|hub|pad)",
        r"(\w+ ?\w*) vs (\w+ ?\w*)",
        r"(ergonomic|standing|gaming|office) (\w+) under \$?(\d+)",
        r"how to (fix|reduce|stop|improve) (\w+ ?\w*)",
    ]
    
    for insight in insights:
        text = insight["title"].lower()
        for pattern in common_queries:
            matches = re.findall(pattern, text)
            for match in matches:
                keyword = " ".join(m for m in match if m).strip()
                if len(keyword) > 5:
                    keywords[keyword] = keywords.get(keyword, 0) + 1
    
    return sorted([{"keyword": k, "frequency": v} for k, v in keywords.items()], 
                  key=lambda x: x["frequency"], reverse=True)

def main():
    print(f"🔍 Reddit Scraper starting — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_insights = []
    all_keywords = []
    
    for subreddit in SUBREDDITS:
        print(f"  Scraping r/{subreddit}...")
        
        # Fetch hot posts
        data_hot = fetch_reddit_json(subreddit, "hot", 50)
        insights = extract_insights(data_hot, subreddit)
        all_insights.extend(insights)
        
        time.sleep(2)  # Respectful rate limiting
        
        # Fetch top posts from past week
        data_top = fetch_reddit_json(subreddit + "?t=week", "top", 25)
        insights_top = extract_insights(data_top, subreddit)
        all_insights.extend(insights_top)
        
        print(f"    → Found {len(insights)} relevant posts")
        time.sleep(2)
    
    # Deduplicate by URL
    seen_urls = set()
    unique_insights = []
    for insight in all_insights:
        if insight["url"] not in seen_urls:
            seen_urls.add(insight["url"])
            unique_insights.append(insight)
    
    # Sort by relevance
    unique_insights.sort(key=lambda x: x["relevance_score"] * 10 + x["comments"], reverse=True)
    
    # Extract keywords
    all_keywords = extract_keywords(unique_insights)
    
    # Write outputs
    insights_file = f"{OUTPUT_DIR}/reddit-insights.json"
    keywords_file = f"{OUTPUT_DIR}/keywords-from-reddit.json"
    summary_file = f"{OUTPUT_DIR}/content-ideas.md"
    
    with open(insights_file, "w") as f:
        json.dump(unique_insights[:50], f, indent=2)
    
    with open(keywords_file, "w") as f:
        json.dump(all_keywords[:50], f, indent=2)
    
    # Write human-readable summary
    with open(summary_file, "w") as f:
        f.write(f"# Content Ideas from Reddit — {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"Total relevant posts found: {len(unique_insights)}\n\n")
        f.write("## Top Content Opportunities\n\n")
        
        for i, insight in enumerate(unique_insights[:15], 1):
            f.write(f"### {i}. {insight['title']}\n")
            f.write(f"- **Source:** r/{insight['subreddit']} | {insight['upvotes']} upvotes | {insight['comments']} comments\n")
            f.write(f"- **Content idea:** {insight['content_idea']}\n")
            f.write(f"- **URL:** {insight['url']}\n\n")
        
        f.write("## Keyword Opportunities\n\n")
        for kw in all_keywords[:20]:
            f.write(f"- `{kw['keyword']}` (mentioned {kw['frequency']}x)\n")
    
    print(f"\n✅ Scrape complete!")
    print(f"   Insights: {insights_file}")
    print(f"   Keywords: {keywords_file}")
    print(f"   Summary:  {summary_file}")
    print(f"   Total posts: {len(unique_insights)}")
    
    # Print top 5 for quick review
    print("\n🔥 Top 5 content opportunities:")
    for insight in unique_insights[:5]:
        print(f"  - {insight['title'][:80]} [{insight['relevance_score']} relevance]")
    
    return {
        "insights_count": len(unique_insights),
        "keywords_count": len(all_keywords),
        "output_dir": OUTPUT_DIR
    }

if __name__ == "__main__":
    result = main()
    print(f"\nResult: {json.dumps(result)}")
