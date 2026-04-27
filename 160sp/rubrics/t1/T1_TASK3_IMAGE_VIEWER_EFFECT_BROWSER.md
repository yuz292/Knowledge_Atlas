# Track 1 · Task 3: Annotate the Collection & Build the Image Viewer

**Track:** Image Tagger  
**Prerequisite:** Task 1 (your 500 images with provenance) + Task 2 (your 6 latent tag detectors)  
**Points:** 75  
**What you'll have when you're done:** Every image in your 500-image collection annotated with latent tag scores, plus an interactive web page where anyone can search and browse images by tag category OR by human effect.

---

## Why we need this

Your team built 6 latent tag detectors in Task 2. But you only tested them on a small gold-set. Now it's time to run them on the **entire 500-image collection** and then build a viewer so humans can actually browse, search, and verify the results.

Right now, the image-tagger repo has an Explorer app (v3.4.74), but it's a full React/Vite application that requires a running backend, database, and authentication. It's developer infrastructure, not something students and researchers can open in a browser and start using.

Here's the gap:

| What exists | What's missing |
|---|---|
| 424 tags in the `Tagging_Contractor` registry, organized by 44 domains | No way to browse images *by tag* without running the full tagger backend |
| 839 outcome terms in the `Outcome_Contractor`, across 7 domains (Cognitive, Affective, Behavioral, Social, Physiological, Neural, Health) | No way to ask "show me spaces that promote creativity" and see matching images |
| 832 constitutive bridges linking effects into a hierarchy | No UI that uses this hierarchy for filtering |
| Your 500 images with provenance (Task 1) | No searchable viewer for your collection |
| Your 6 latent tag detectors (Task 2) | **They've only run on a small gold-set — not the full collection** |

You're going to close both gaps: first annotate everything, then build the viewer.

---

## Phase 1: Run your detectors on the full image collection

Before you can browse annotations, you need to produce them. This is the moment of truth for your Task 2 detectors: do they actually work at scale?

### 1A. Write the batch runner contract

> **Contract objective:** "I want a script that runs all 6 of my latent tag detectors on every image in `collection.json` and produces a single `annotations.json` file with scores per image."
> **Contract is with:** Your 6 detector functions (from Task 2) and your `collection.json` (from Task 1).
> **Prompt hint:** *"I have 6 detector functions and 500 images. Write a batch runner that loads each image, computes the intermediate representations (segmentation mask, depth map, skeleton) if not already cached, runs all 6 detectors, and writes the results to annotations.json. It must handle failures gracefully — if one detector crashes on one image, log the error and continue."*

**Your contract must cover:**
- Reads image paths from `collection.json`
- For each image, loads or computes intermediate representations (seg mask, depth map, skeleton)
- Runs all 6 detectors, collecting `TagResult` per detector per image
- Writes a single `annotations.json` with this structure:

```json
{
  "version": "1.0",
  "generated_at": "2026-04-27T...",
  "detectors": ["L44", "L42", "L48", "L49", "L53", "L54"],
  "images": {
    "img_001.jpg": {
      "room_type": "living_room",
      "tags": {
        "L44_sociopetal_seating": {"score": 0.72, "confidence": 0.65},
        "L42_interactional_visibility": {"score": 0.85, "confidence": 0.71},
        "L48_dyadic_intimacy": {"score": 0.31, "confidence": 0.55}
      }
    },
    "img_002.jpg": { ... }
  },
  "errors": {
    "img_099.jpg": {"detector": "L53", "error": "segmentation mask not found"}
  },
  "stats": {
    "total_images": 500,
    "images_annotated": 497,
    "images_with_errors": 3,
    "mean_scores": {"L44": 0.38, "L42": 0.52, ...}
  }
}
```

### 1B. Write your tests BEFORE running

- [ ] Script runs on 10 images without crashing
- [ ] Each image gets scores for all 6 detectors (or a logged error)
- [ ] `annotations.json` is valid JSON and matches the schema above
- [ ] Failed images appear in the `errors` section (not silently dropped)
- [ ] Stats section has correct counts
- [ ] Score distributions are plausible (not all 0.0 or all 1.0)

### 1C. Run the batch and verify

```bash
python3 batch_annotate.py --collection collection.json --output annotations.json
```

After it finishes, check:

> *"How many images were annotated? How many had errors? Show me the score distribution for each detector — are they plausible?"*

**Reality check:** If a detector scores > 0.5 on more than 80% of images, something is wrong — not every space has sociopetal seating. If a detector scores < 0.1 on everything, it might not be working. Plot histograms of scores per detector and sanity-check them.

```python
# Quick sanity check
import json
ann = json.load(open("annotations.json"))
for det in ann["detectors"]:
    scores = [img["tags"].get(det, {}).get("score", 0) 
              for img in ann["images"].values() if det in img.get("tags", {})]
    print(f"{det}: mean={sum(scores)/len(scores):.2f}, "
          f">0.5: {sum(1 for s in scores if s > 0.5)}/{len(scores)}")
```

### 1D. Fix detector issues discovered at scale

Running on 500 images will surface problems that 10 gold-set images didn't catch:
- Depth maps missing for certain room types
- Segmentation failing on unusual furniture
- Edge cases in your geometric predicates

Document what broke, fix it, re-run. This is the most valuable engineering learning in the task.

**Your deliverable:** `annotations.json` with scores for 500 images, plus a "batch run report" documenting errors found and fixes applied.

---

## Phase 2: Build the tag browser

Now that you have annotations, build a viewer.

> **Contract objective:** "I want a standalone HTML page where I can browse images by selecting tag categories from the Tagging_Contractor registry."
> **Contract is with:** The registry (`registry_v0.2.8.json`), your `collection.json`, and your `annotations.json`.
> **Prompt hint:** *"Build an HTML page that reads the tag registry JSON and shows the high-level tag domains as checkboxes. When I check a domain, show all images from annotations.json that have tags in that domain with score above a threshold. Show thumbnails in a grid with room type and key tags."*

Write YOUR OWN contract. Include inputs, processing, outputs, success conditions.

### Two search modes

**Mode 1: Search by Tag (from Tagging_Contractor)**

The user picks environmental features they want to see. The tag categories come from the registry's domain hierarchy:

| Domain | Example tags | What a user might search for |
|---|---|---|
| Lighting | daylight ratio, glare, light warmth | "Show me spaces with strong daylighting" |
| Spatial | ceiling height, openness, enclosure | "Show me high-ceiling spaces" |
| Biophilia | plant count, water view, natural materials | "Show me biophilic interiors" |
| Social-Spatial | sociopetal seating, prospect, privacy | "Show me conversation-friendly layouts" |
| Materials | wood, concrete, glass | "Show me warm material palettes" |
| Color | warmth, saturation, contrast | "Show me cool-toned interiors" |
| Visual Complexity | clutter, symmetry, entropy | "Show me visually calm spaces" |

Use the registry's 44 domains as high-level categories. Dropdowns or checkboxes. When a user selects a domain, show all images tagged with any tag in that domain.

**Mode 2: Search by Effect (from Outcome_Contractor)**

Instead of asking "what does this space *look like*?", the user asks "what does this space *do to people*?"

The Outcome_Contractor has 839 effect terms organized into 7 domains:

| Domain | # Terms | Example effects |
|---|---|---|
| Cognitive | 100 | Attention, Concentration, Creativity, Memory, Wayfinding |
| Affective | 94 | Stress, Restoration, Mood, Comfort, Awe |
| Behavioral | 147 | Collaboration, Productivity, Creative Output, Exploration |
| Social | 128 | Collaboration, Trust, Communication, Privacy |
| Physiological | 131 | Alertness, Fatigue, Sleep Quality, Cortisol |
| Neural | 107 | Amygdala, Prefrontal, Default Mode Network |
| Health | 132 | Flourishing, Well-being, Recovery |

Present the 7 domains as top-level checkboxes. Let users drill into sub-effects. Use the constitutive bridges (`constitutive_bridges.json`) to resolve which effects roll up into which — so selecting "Restoration" also pulls in "Stress Recovery" and "Attention Restoration."

**How effects connect to images:** The PNU templates link environmental features to outcomes. If a PNU says "daylight → circadian entrainment → alertness," then images tagged with high daylight scores should appear when the user searches for "alertness." Build a `effect_tag_mapping.json` that maps effects to tags. You can generate it by asking your AI to read the PNU templates:

```json
{
  "effect_to_tags": {
    "cog.attention": ["lighting.daylight_ratio", "complexity.edge_density", "spatial.openness"],
    "affect.restoration": ["biophilia.plant_count", "biophilia.water_view", "lighting.daylight_ratio"],
    "behav.creativity": ["spatial.ceiling_height", "color.warmth", "complexity.visual_complexity"],
    "social.collaboration": ["social.sociopetal_seating", "social.interactional_visibility"]
  }
}
```

**Success conditions:**
- [ ] All 44 tag domains appear as filterable categories
- [ ] All 7 Outcome_Contractor domains appear as filterable categories with drill-down
- [ ] Free text search works across tag names, room types, and effect names
- [ ] Grid handles 500 images without freezing (lazy loading or pagination)
- [ ] Clicking an image shows detail view with all tags, confidence scores, linked effects, and provenance
- [ ] Effect filtering shows the chain: tag → mechanism → effect

---

## Phase 3: Polish and integrate

- [ ] Both search modes (tag and effect) can be combined
- [ ] Image detail view shows BOTH tags and linked effects
- [ ] Provenance is visible (source URL, photographer, license) on every image
- [ ] Annotation scores are shown as visual bars or badges
- [ ] Data persists — reads from JSON files, no backend required
- [ ] Works as a standalone HTML file that can be opened in any browser

Write YOUR OWN contract and tests for this phase.

---

## What you submit

| Item | What it is |
|---|---|
| **`annotations.json`** (Phase 1) | All 500 images annotated with all 6 detector scores |
| **Batch run report** (Phase 1) | Errors found at scale, fixes applied, score distributions |
| **`ka_image_viewer.html`** (Phase 2) | Standalone viewer with tag + effect search |
| **`effect_tag_mapping.json`** (Phase 2) | Mapping from effects to tags |
| **Contracts + tests** | Your written contracts and test checklists for each phase |
| **Viewer walkthrough** | Screenshots or recording showing both search modes |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 10 | Written BEFORE building. Specific. **(CONTRACT GATE)** |
| **Batch annotation** | 15 | 500 images annotated, errors logged, score distributions plausible |
| **Scale fixes** | 10 | Documented what broke at scale and how you fixed it |
| **Tag browser** | 15 | Checkboxes for domains, filtering works, grid handles 500 images |
| **Effect browser** | 15 | 7 Outcome domains, drill-down, tag→effect chain shown |
| **Image detail + polish** | 10 | Tags, effects, provenance, confidence all visible, standalone HTML |

> ⛔ **Contract gate**: If your contracts and tests are missing or vague, your work will be flagged as not ready for integration.

---

## Data sources you should know about

### Tag and annotation data

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | 424 tags across 44 domains — your tag filter categories |
| `Tagging_Contractor/.../observations/image_tagger_observation.schema.json` | **Official annotation schema** — your `annotations.json` should conform to this. Each tag entry has `tag_id`, `value_type` (binary/ordinal/continuous), `value`, `confidence`, and `evidence` |
| `Tagging_Contractor/contracts/localized_image_tags.schema.json` | Spatial annotation schema with `semantic_regions`, `dense_maps`, and `pipeline_provenance` — use this if your detectors produce region-level output |
| Your `collection.json` from Task 1 | 500 images with room types and provenance |
| Your 6 detector functions from Task 2 | Detectors that produce `TagResult` per image |

### Effect and outcome data

| Repo / File | What it gives you |
|---|---|
| `Outcome_Contractor/contracts/oc_export/outcome_vocab.json` | 839 effect terms across 7 domains — your effect filter categories |
| `Outcome_Contractor/contracts/oc_export/constitutive_bridges.json` | 832 parent→child bridges — the effect hierarchy for drill-down |
| `Outcome_Contractor/contracts/oc_export/ae_outcome_lookup.json` | **Pre-built tag→outcome lookup** — 2,114 entries mapping text terms to outcome IDs. This is your shortcut for the effect browser. Instead of building `effect_tag_mapping.json` from scratch, start here |
| `Outcome_Contractor/contracts/oc_export/bn_outcome_nodes.json` | Bayesian network node definitions — shows causal structure between outcomes |
| `Outcome_Contractor/contracts/oc_export/VERSION_MANIFEST.json` | Tells you the schema versions and file checksums for all OC exports |

### Existing viewer code (reference, not required)

| Repo / File | What it gives you |
|---|---|
| `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/frontend/apps/explorer/` | Existing React explorer — study `ImageDetailModal.jsx` to see what APIs it calls (depth, segmentation, materials, affordance). You don't need to use this code, but it shows the data model |
| `image-tagger/docs/CONTRACT.md` | Image Tagger API contract — `ExplorerSearchResponse` shows the response shape |
| `image-tagger/docs/ENGINEERING_BRIEF.md` | Architecture overview — four user journeys: Explorer, Workbench, Monitor, Admin |
| `Article_Eater/data/templates/` | 166 PNU templates linking tags to effects — use these to enrich your `effect_tag_mapping.json` beyond what `ae_outcome_lookup.json` provides |

---

## Reuse

Your `annotations.json` becomes the canonical annotation layer for the image collection. Your viewer becomes the public-facing tool for the Image Tagger track. Both will be reused by future cohorts — build them as infrastructure, not throwaway assignments.
