#!/usr/bin/env bash
# PUSH SCRIPT — Run this after getting a new GitHub token
# ===========================================================
# Your token MUST have "Contents: Read and Write" scope
# 
# Step 1: Go to https://github.com/settings/tokens
# Step 2: "Generate new token (classic)" 
# Step 3: Give it a name like "deploy-blog"
# Step 4: Check the "repo" scope (full control of private repos)
# Step 5: Generate → copy the token (starts with ghp_)
# Step 6: Paste it below and run this script

set -e

# ── PASTE YOUR NEW TOKEN HERE ─────────────────────────────────
GITHUB_TOKEN="ghp_PASTE_YOUR_TOKEN_HERE"
# ─────────────────────────────────────────────────────────────

REPO="HighLowMystery/highlowmystery.github.io"
SITE_DIR="/home/Apollo/Documents/Projects/Revenue/affiliate-blog"

if [[ "$GITHUB_TOKEN" == "ghp_PASTE_YOUR_TOKEN_HERE" ]]; then
  echo "❌ You need to paste your GitHub token above first!"
  echo "   Get one at: https://github.com/settings/tokens"
  exit 1
fi

cd "$SITE_DIR"

# Set remote URL with token
git remote set-url origin "https://${GITHUB_TOKEN}@github.com/${REPO}.git"

echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Pushed! Now enable GitHub Pages:"
echo "   1. Go to: https://github.com/${REPO}/settings/pages"
echo "   2. Source: Deploy from a branch"
echo "   3. Branch: main / (root)"
echo "   4. Click Save"
echo "   5. Wait 2-5 min"
echo "   6. Site live at: https://highlowmystery.github.io"
echo ""
echo "🔗 Direct link: https://github.com/${REPO}/settings/pages"
