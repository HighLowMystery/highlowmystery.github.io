## GitHub Setup (One-Time — Boss Must Do)

```bash
# 1. Create repo on GitHub: github.com/new
#    Name: highlowmystery.github.io  (for root user page)
#    OR: affiliate-hub  (for project page at highlowmystery.github.io/affiliate-hub)
#    Visibility: Public
#    Do NOT initialize with README

# 2. Add remote and push from this machine:
cd /home/Apollo/sites/affiliate-hub
git remote add origin git@github.com:highlowmystery/highlowmystery.github.io.git
git push -u origin main

# 3. Enable GitHub Pages in repo settings:
#    Settings → Pages → Build and deployment
#    Source: GitHub Actions
#    (The workflow at .github/workflows/deploy.yml handles everything)

# 4. Your site will be live at: https://highlowmystery.github.io
#    First deploy takes 2-3 minutes after the push.

# 5. Replace Amazon tag in hugo.toml:
#    Find: amazonTag = "YOURTAG-20"
#    Replace with your actual tag from: https://affiliate-program.amazon.com
#    Then: git add hugo.toml && git commit -m "config: add Amazon tag" && git push
```

## Amazon Associates Signup

1. Go to: https://affiliate-program.amazon.com
2. Sign in with your Amazon account
3. Enter your website URL: https://highlowmystery.github.io
4. Choose your tag (usually firstname-20 or sitename-20)
5. Copy the tag and replace YOURTAG-20 in hugo.toml

## What's Live Right Now (After Push)

Posts:
- best-ergonomic-chairs-under-500
- best-standing-desks-under-500
- best-monitors-under-300
- flexispot-e7-vs-uplift-v2 (comparison)
- home-office-setup-under-1000 (how-to)

Pages:
- About
- Disclaimer

## Git Commit History
All code is committed locally. Run `git log --oneline` to see state.
Waiting on remote push by Boss.
