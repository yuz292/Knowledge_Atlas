# Remote Provisioning Commands

Date: 2026-03-24

Use this after creating the empty GitHub repos in the browser. Do not initialize those GitHub repos with a README, license, or .gitignore.

## 1. Designing_Experiments

Recommended GitHub repo name:
- `Designing_Experiments`

Local repo state:
- path: `/Users/davidusa/REPOS/Designing_Experiments`
- branch: `master`
- latest local snapshot commit: `8f29cb2`

Commands:

```bash
cd /Users/davidusa/REPOS/Designing_Experiments
git remote add origin https://github.com/dkirsh/Designing_Experiments.git
git push -u origin master
```

## 2. Article_Finder_v3_2_3

Recommended GitHub repo name:
- `Article_Finder_v3_2_3`

Local repo state:
- path: `/Users/davidusa/REPOS/Article_Finder_v3_2_3`
- branch: `main`
- latest local source snapshot commit: `f57d2b6`

Commands:

```bash
cd /Users/davidusa/REPOS/Article_Finder_v3_2_3
git remote add origin https://github.com/dkirsh/Article_Finder_v3_2_3.git
git push -u origin main
```

Notes:
- the first snapshot intentionally excludes:
  - `data/`
  - `venv/`
  - zip bundles
  - local secrets
- if later you want data mirrored, do that via a separate storage/backup plan, not normal git

## 3. theory_guides

Recommended GitHub repo name:
- `theory_guides`

Current state:
- path: `/Users/davidusa/REPOS/theory_guides`
- not currently a git repo

If you want to preserve it as its own repo:

```bash
cd /Users/davidusa/REPOS/theory_guides
git init -b main
git add .
git commit -m "repo: initialize theory guides corpus"
git remote add origin https://github.com/dkirsh/theory_guides.git
git push -u origin main
```

If you do not want a separate repo:
- keep it local for now and treat it as an auxiliary content corpus pending integration

## 4. Authentication

If `git push` prompts for auth, either authenticate through the prompt flow or run:

```bash
gh auth login -h github.com
```

Then re-run the `git push` command.

## 5. Verification

After each push:

```bash
git remote -v
git branch -vv
```

And verify the repo exists in the browser under:
- `https://github.com/dkirsh/`
