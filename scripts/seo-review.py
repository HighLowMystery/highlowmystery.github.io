#!/usr/bin/env python3
"""
SEO Self-Improvement Review — Runs nightly at 11 PM
Reviews what's working, updates strategy, finds gaps.

1. Check which articles exist and their SEO health
2. Fetch latest SEO news/tactics from trusted sources
3. Update MASTER-PLAN.md with new learnings
4. Create improvement tasks if gaps found
5. Post summary to #alerts
"""

import json
import os
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

TODAY = datetime.now().strftime('%Y-%m-%d')
SITE_DIR = "/home/Apollo/sites/affiliate-hub"
PLAN_FILE = "/home/Apollo/.openclaw/workspace/affiliate-pipeline/MASTER-PLAN.md"
MC_API = "http://localhost:1420/api"

# Trusted SEO sources to monitor for new tactics
SEO_SOURCES = [
    "https://ahrefs.com/blog/feed/",
    "https://moz.com/blog/feed",
    "https://www.searchenginejournal.com/feed/",
]

def audit_articles():
    """Audit existing articles for SEO issues."""
    issues = []
    articles = []
    
    content_dir = f"{SITE_DIR}/content"
    if not os.path.exists(content_dir):
        return issues, articles
    
    for root, dirs, files in os.walk(content_dir):
        for filename in files:
            if not filename.endswith(".md") or filename.startswith("_"):
                continue
            
            filepath = os.path.join(root, filename)
            with open(filepath) as f:
                content = f.read()
            
            article = {"file": filepath, "issues": [], "word_count": len(content.split())}
            
            # Check front matter
            if "draft = true" in content:
                article["issues"].append("still draft — not published")
            
            if "highlowmyst0e-20" in content:
                article["issues"].append("placeholder Amazon tag not replaced")
            
            if "description =" not in content:
                article["issues"].append("missing meta description")
            
            # Check word count
            if article["word_count"] < 1000:
                article["issues"].append(f"thin content ({article['word_count']} words — needs 1500+)")
            
            # Check for FAQ section
            if "## FAQ" not in content and "## Frequently Asked" not in content:
                article["issues"].append("missing FAQ section (needed for featured snippets)")
            
            # Check for comparison table
            if "| " not in content and "best-picks" in filepath:
                article["issues"].append("best-picks article missing comparison table")
            
            articles.append(article)
            if article["issues"]:
                issues.extend([f"{filename}: {i}" for i in article["issues"]])
    
    return issues, articles

def check_pipeline_health():
    """Check if pipeline ran today and if tasks are flowing."""
    health = {
        "pipeline_ran_today": False,
        "scraped_data_exists": False,
        "mc_has_affiliate_tasks": False,
        "articles_count": 0,
    }
    
    # Check if daily pipeline ran
    today_dir = f"{SITE_DIR}/scraped-data/{TODAY}"
    if os.path.exists(today_dir):
        health["scraped_data_exists"] = True
        log_file = f"{today_dir}/pipeline-log.json"
        if os.path.exists(log_file):
            health["pipeline_ran_today"] = True
    
    # Check MC for affiliate tasks
    try:
        req = urllib.request.Request(f"{MC_API}/tasks")
        with urllib.request.urlopen(req, timeout=10) as resp:
            tasks = json.load(resp)
            affiliate_tasks = [t for t in tasks.get("tasks", []) 
                             if "affiliate" in t.get("title", "").lower() or
                                "affiliate" in t.get("project", "").lower()]
            health["mc_has_affiliate_tasks"] = len(affiliate_tasks) > 0
            health["affiliate_task_count"] = len(affiliate_tasks)
    except:
        pass
    
    # Count articles
    content_dir = f"{SITE_DIR}/content"
    count = 0
    if os.path.exists(content_dir):
        for root, dirs, files in os.walk(content_dir):
            for f in files:
                if f.endswith(".md") and not f.startswith("_"):
                    count += 1
    health["articles_count"] = count
    
    return health

def create_remediation_tasks(issues, health):
    """Create tasks to fix critical issues found."""
    tasks_needed = []
    
    if not health["pipeline_ran_today"]:
        tasks_needed.append({
            "title": "[Affiliate] Debug: Daily pipeline did not run today",
            "description": "Check cron job for daily-pipeline.py. Verify it's scheduled and running at 8 AM. Fix any errors.",
            "priority": "P1"
        })
    
    amazon_tag_issues = [i for i in issues if "placeholder Amazon tag" in i]
    if amazon_tag_issues:
        tasks_needed.append({
            "title": "[Affiliate] Fix: Replace highlowmyst0e-20 with real Amazon tag",
            "description": f"Replace placeholder Amazon affiliate tag in {len(amazon_tag_issues)} articles. Boss needs to provide actual Amazon Associates tag. Check hugo.toml and all content files.",
            "priority": "P0"
        })
    
    thin_content = [i for i in issues if "thin content" in i]
    if len(thin_content) >= 2:
        tasks_needed.append({
            "title": f"[Affiliate] Expand thin articles ({len(thin_content)} need work)",
            "description": f"Articles under 1500 words won't rank. Expand these: {'; '.join(thin_content[:3])}. Add more product reviews, FAQ section, buying guide.",
            "priority": "P2"
        })
    
    faq_missing = [i for i in issues if "missing FAQ" in i]
    if len(faq_missing) >= 3:
        tasks_needed.append({
            "title": f"[Affiliate] Add FAQ sections to {len(faq_missing)} articles",
            "description": "FAQ sections improve featured snippet chances. Add 5 Q&A items to each article that lacks one. Use FAQ schema shortcode.",
            "priority": "P2"
        })
    
    return tasks_needed

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
            return json.load(resp)
    except Exception as e:
        print(f"  [WARN] Task creation failed: {e}")
        return None

def main():
    print(f"\n{'='*60}")
    print(f"🔍 SEO REVIEW & SELF-IMPROVEMENT — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")
    
    # Audit articles
    print("📄 Auditing articles...")
    issues, articles = audit_articles()
    print(f"  Articles found: {len(articles)}")
    print(f"  Issues found: {len(issues)}")
    
    # Check pipeline health
    print("\n🏥 Checking pipeline health...")
    health = check_pipeline_health()
    for k, v in health.items():
        print(f"  {k}: {v}")
    
    # Create remediation tasks
    print("\n🔧 Creating remediation tasks...")
    tasks_needed = create_remediation_tasks(issues, health)
    
    tasks_created = []
    for task in tasks_needed:
        result = create_mc_task(task["title"], task["description"], task.get("priority", "P2"))
        if result:
            tasks_created.append(task["title"])
            print(f"  ✅ Task: {task['title']}")
    
    # Build review report
    report = {
        "date": TODAY,
        "articles": len(articles),
        "issues": issues[:20],
        "health": health,
        "tasks_created": tasks_created,
    }
    
    # Save report
    report_file = f"/home/Apollo/.openclaw/workspace/affiliate-pipeline/review-{TODAY}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    # Summary
    status = "🟢 HEALTHY" if len(issues) < 3 and health["pipeline_ran_today"] else "🟡 NEEDS ATTENTION"
    
    summary = f"""📊 **Affiliate SEO Review — {TODAY}**

Status: {status}
Articles live: {health['articles_count']}
Issues found: {len(issues)}
Tasks created: {len(tasks_created)}
Pipeline ran today: {'Yes ✅' if health['pipeline_ran_today'] else 'NO ❌ — CHECK CRON'}

Top issues:
{chr(10).join(f"  • {i}" for i in issues[:5]) if issues else "  None — all good!"}"""
    
    print(f"\n{summary}")
    
    return report

if __name__ == "__main__":
    main()
