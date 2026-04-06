#!/usr/bin/env bash
# DEPLOY GUIDE — Push AI Income Lab to GitHub Pages + Cloudflare Pages
# =====================================================================
# GitHub Account: https://github.com/HighLowMystery
# Site URL: https://highlowmystery.github.io

# ─── STEP 1: Push to GitHub ───────────────────────────────────────────────────
# Create the repo first at: https://github.com/new
# Name: highlowmystery.github.io
# ⚠️  Must be EXACTLY this name (your username + .github.io)
# Set to PUBLIC, do NOT initialize with README

cd /home/Apollo/Documents/Projects/Revenue/affiliate-blog

git remote add origin https://github.com/HighLowMystery/highlowmystery.github.io.git
git push -u origin main

# After push:
# 1. Go to: https://github.com/HighLowMystery/highlowmystery.github.io/settings/pages
# 2. Source: "Deploy from a branch"
# 3. Branch: main / (root)
# 4. Save
# 5. Wait 2-5 min → site live at https://highlowmystery.github.io

# ─── STEP 2: Verify live ──────────────────────────────────────────────────────
# Open: https://highlowmystery.github.io
# Should show premium dark homepage

# ─── NOTE: GitHub Pages ToS ───────────────────────────────────────────────────
# ⚠️  GitHub Pages prohibits "running your online business" or affiliate monetization
# However: Personal/portfolio sites with affiliate links in content ARE common
# and GitHub rarely enforces this for small content sites.
#
# SAFER option if you want zero ToS risk: Cloudflare Pages (see below)
# For a personal blog with affiliate links, GitHub Pages is used by millions of sites.

# ─── OPTION B: Cloudflare Pages (SAFEST, recommended) ────────────────────────
# 1. Go to: https://pages.cloudflare.com
# 2. Sign up free (Cloudflare account)
# 3. "Connect to Git" → authorize GitHub → select highlowmystery.github.io repo
# 4. Build settings: Framework preset = "None", build command = (blank), output dir = "/"
# 5. Deploy!
# Site live at: https://highlowmystery.pages.dev (or custom domain)
# Cloudflare Pages = unlimited bandwidth, no commercial restrictions, global CDN

# ─── STEP 3: Publish first articles ──────────────────────────────────────────
# Use the pipeline from seo-blog/:
# cd /home/Apollo/Documents/Projects/Revenue/seo-blog
# bash scripts/pipeline.sh
# Then copy generated post HTML to affiliate-blog/posts/
# Update sitemap.xml with new URLs

# ─── STEP 4: Affiliate signups ────────────────────────────────────────────────
# After site is live with 3+ real articles:
# Amazon Associates: https://affiliate-program.amazon.com/
# Jasper AI (30% recurring): https://www.jasper.ai/affiliate
# Hostinger (60%): https://www.hostinger.com/affiliates

echo "✅ Ready to deploy — run git push"
