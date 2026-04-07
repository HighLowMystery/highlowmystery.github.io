#!/usr/bin/env python3
"""
Daily Pipeline Orchestrator — Affiliate Autonomous Loop
Runs every day at 8 AM via cron.

Steps:
1. Run Reddit scraper
2. Run keyword scraper  
3. Read scraped data
4. Post top opportunities to #research-grunt Discord channel
5. Create MC tasks for highest-priority content
6. Post status to #alerts

This is the "brain" that keeps the pipeline always moving.
"""

import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime

# Config
TODAY = datetime.now().strftime('%Y-%m-%d')
SCRAPED_DIR = f"/home/Apollo/sites/affiliate-hub/scraped-data/{TODAY}"
SITE_DIR = "/home/Apollo/sites/affiliate-hub"
MC_API = "http://localhost:1420/api"

# Discord webhook/bot IDs (using openclaw message tool via CLI)
ALERTS_CHANNEL = "1490282406349897748"
RESEARCH_GRUNT_CHANNEL = "1490262512741122109"
MASTER_CODER_CHANNEL = "1490232347751092244"

def run_scraper(script_name):
    """Run a scraper script and return results."""
    script_path = f"{SITE_DIR}/scripts/{script_name}"
    print(f"  Running {script_name}...")
    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print(f"  ✅ {script_name} completed")
            return True, result.stdout
        else:
            print(f"  ❌ {script_name} failed: {result.stderr[:200]}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"  ⏱ {script_name} timed out (2 min limit)")
        return False, "timeout"
    except Exception as e:
        print(f"  ❌ {script_name} exception: {e}")
        return False, str(e)

def load_scraped_data():
    """Load today's scraped data."""
    data = {}
    
    reddit_file = f"{SCRAPED_DIR}/reddit-insights.json"
    keywords_file = f"{SCRAPED_DIR}/keyword-opportunities.json"
    ideas_file = f"{SCRAPED_DIR}/content-ideas.md"
    
    if os.path.exists(reddit_file):
        with open(reddit_file) as f:
            data["reddit"] = json.load(f)
    
    if os.path.exists(keywords_file):
        with open(keywords_file) as f:
            data["keywords"] = json.load(f)
    
    if os.path.exists(ideas_file):
        with open(ideas_file) as f:
            data["ideas_md"] = f.read()
    
    return data

def get_existing_tasks():
    """Get existing MC tasks to avoid duplicates."""
    try:
        req = urllib.request.Request(f"{MC_API}/tasks")
        with urllib.request.urlopen(req, timeout=10) as resp:
            tasks = json.load(resp)
            return [t.get("title", "").lower() for t in tasks.get("tasks", [])]
    except:
        return []

def create_mc_task(title, description, priority="P2"):
    """Create a task in Mission Control."""
    payload = {
        "action": "add",
        "task": {
            "title": title,
            "description": description,
            "status": "BACKLOG",
            "priority": priority,
            "agentId": "master-coder",
            "project": "Affiliate"
        }
    }
    
    try:
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{MC_API}/tasks",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.load(resp)
            return result.get("id") or result.get("task", {}).get("id")
    except Exception as e:
        print(f"  [WARN] Task creation failed: {e}")
        return None

def select_best_keyword_for_article(keywords, existing_tasks):
    """Pick the best keyword to write about that isn't already in progress."""
    if not keywords:
        return None
    
    for kw in keywords:
        keyword = kw.get("keyword", "")
        # Check not already in existing tasks
        if not any(keyword.lower() in task for task in existing_tasks):
            return kw
    return keywords[0]  # Fallback to first if all exist

def generate_article_brief(keyword_data):
    """Generate a brief for Master Coder to write an article."""
    keyword = keyword_data.get("keyword", "")
    article_type = keyword_data.get("article_type", "best-picks")
    
    type_instructions = {
        "best-picks": f"""
Write a "Best X" affiliate article for: **{keyword}**

Structure:
1. Open with 1-2 paragraph personal story (remote work pain point)
2. Quick answer box (40-60 words, answer the query directly)  
3. Comparison table (5-7 products, with Amazon affiliate links, placeholder tag highlowmyst0e-20)
4. Individual product reviews (200-300 words each, pros/cons, who it's for)
5. Buying guide section (what to look for)
6. FAQ section (5 questions with schema markup)

Word count: 3,000-4,000 words
Humanization: 9th grade reading, personal voice, varied sentences, no AI tells
File: content/best-picks/{keyword_data.get('slug_idea', 'article')}.md
Hugo front matter required (title, date, draft=false, description, categories, tags)
""",
        "comparison": f"""
Write a comparison article for: **{keyword}**

Structure:
1. Quick verdict at top (who should buy which)
2. Side-by-side spec comparison table
3. Detailed comparison sections (3-4 key criteria)
4. Real-world usage differences
5. Price/value analysis
6. Final recommendation

Word count: 2,000-2,500 words
File: content/comparisons/{keyword_data.get('slug_idea', 'article')}.md
""",
        "how-to": f"""
Write a how-to guide for: **{keyword}**

Structure:
1. Open with the problem/pain point
2. Overview of what we'll cover
3. Step-by-step guide (numbered, clear)
4. Product recommendations woven in naturally (soft affiliate links)
5. Troubleshooting section
6. FAQ

Word count: 1,500-2,500 words
File: content/how-to/{keyword_data.get('slug_idea', 'article')}.md
"""
    }
    
    return type_instructions.get(article_type, type_instructions["best-picks"])

def get_articles_published_count():
    """Count articles in content directory."""
    count = 0
    content_dir = f"{SITE_DIR}/content"
    if os.path.exists(content_dir):
        for root, dirs, files in os.walk(content_dir):
            for f in files:
                if f.endswith(".md") and not f.startswith("_"):
                    count += 1
    return count

def main():
    print(f"\n{'='*60}")
    print(f"🚀 AFFILIATE PIPELINE DAILY RUN — {datetime.now().strftime('%Y-%m-%d %H:%M CDT')}")
    print(f"{'='*60}\n")
    
    articles_before = get_articles_published_count()
    
    # Step 1: Run scrapers
    print("📡 STEP 1: Running scrapers...")
    os.makedirs(SCRAPED_DIR, exist_ok=True)
    
    reddit_ok, reddit_out = run_scraper("reddit-scraper.py")
    time.sleep(3)
    keyword_ok, keyword_out = run_scraper("keyword-scraper.py")
    
    # Step 2: Load data
    print("\n📊 STEP 2: Loading scraped data...")
    data = load_scraped_data()
    
    keywords = data.get("keywords", [])
    reddit_insights = data.get("reddit", [])
    
    print(f"  Keywords found: {len(keywords)}")
    print(f"  Reddit insights: {len(reddit_insights)}")
    
    # Step 3: Pick best article opportunities
    print("\n📝 STEP 3: Selecting content opportunities...")
    existing_tasks = get_existing_tasks()
    
    tasks_created = []
    for i in range(2):  # Create max 2 tasks per day (batch sizing)
        best_kw = select_best_keyword_for_article(keywords[i*10:], existing_tasks)
        if not best_kw:
            break
        
        title = f"[Affiliate] Write: {best_kw['keyword']}"
        brief = generate_article_brief(best_kw)
        
        task_id = create_mc_task(title, brief, "P1")
        if task_id:
            tasks_created.append({"id": task_id, "keyword": best_kw["keyword"]})
            existing_tasks.append(title.lower())
            print(f"  ✅ Task created: {title}")
        
        time.sleep(1)
    
    # Step 4: Write pipeline log
    log_file = f"{SCRAPED_DIR}/pipeline-log.json"
    log = {
        "date": TODAY,
        "run_time": datetime.now().isoformat(),
        "scrapers": {
            "reddit": reddit_ok,
            "keywords": keyword_ok
        },
        "data": {
            "keywords_found": len(keywords),
            "reddit_insights": len(reddit_insights)
        },
        "tasks_created": tasks_created,
        "articles_total": get_articles_published_count()
    }
    
    with open(log_file, "w") as f:
        json.dump(log, f, indent=2)
    
    # Step 5: Build status message
    top_keywords = [k["keyword"] for k in keywords[:5]]
    
    summary = f"""🏗️ **Affiliate Pipeline Daily Run — {TODAY}**

📡 Scrapers: Reddit {'✅' if reddit_ok else '❌'} | Keywords {'✅' if keyword_ok else '❌'}
📊 Data: {len(keywords)} keyword opps | {len(reddit_insights)} Reddit insights
📝 Tasks created: {len(tasks_created)} (dispatched to Master Coder)
📄 Articles live: {log['articles_total']}

🔥 Top opportunities today:
{chr(10).join(f"  • {k}" for k in top_keywords[:5])}

Tasks: {', '.join(t['id'] for t in tasks_created) if tasks_created else 'none'}"""
    
    print(f"\n{summary}")
    
    # Write summary for Jarvis to read
    summary_file = "/home/Apollo/.openclaw/workspace/affiliate-pipeline/daily-status.md"
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)
    with open(summary_file, "w") as f:
        f.write(f"# Affiliate Pipeline Status\n")
        f.write(f"Last run: {datetime.now().isoformat()}\n\n")
        f.write(summary.replace("**", "").replace("✅", "OK").replace("❌", "FAIL"))
        f.write(f"\n\n## Log\n```json\n{json.dumps(log, indent=2)}\n```")
    
    print(f"\n✅ Pipeline run complete. Log: {log_file}")
    return log

if __name__ == "__main__":
    main()
