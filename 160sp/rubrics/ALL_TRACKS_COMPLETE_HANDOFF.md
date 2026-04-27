# 160sp Complete Assignment Set — All Three Tracks

> **Purpose:** This document contains the complete, finalized assignment specifications for all three tracks of the 160sp Knowledge Atlas course. Each track has three tasks (225 points total per track). Hand this entire document to Claude or another AI for HTML conversion, dashboard generation, or student-facing deployment.

> **Generated:** 2026-04-27  
> **Source files:**  
> - Track 1: `t1/T1_ALL_TASKS_HTML_CONVERSION_REVISED.md` (1,025 lines)  
> - Track 2: `t2/T2_ALL_TASKS_HTML_CONVERSION_REVISED.md` (1,021 lines)  
> - Track 3: `t3_new/T3_ALL_TASKS_FOR_HTML_CONVERSION.md` (1,095 lines)

---
---

=== TRACK 1 ===
# Track 1: Image Tagger — All Tasks

**Track overview:** Build and operate a complete image annotation and browsing pipeline for the Knowledge Atlas. You start with openly-licensed photographs of building interiors, gather 500 of them with full provenance, write detectors for *latent tags* (computational measures of how a space affects the people in it), annotate the whole collection, and ship an interactive viewer that lets anyone browse the images by environmental feature or by human effect.

**Three tasks, one pipeline:**

| Task | What you build | Points |
|---|---|---|
| Task 1 | A 500-image collection of openly-licensed interior photos with full provenance | 75 points |
| Task 2 | Six latent-tag detectors for social-spatial features | 75 points |
| Task 3 | The annotated collection plus an image viewer | 75 points |

**Contract gate (all tasks):** Every task requires a written contract: inputs, processing, outputs, success conditions, and a test checklist. Vague or missing contracts will flag your work as not ready for integration.

---

# Track 1 · Task 1: Build an Image Collection

**Track:** Image Tagger  
**Points:** 75  
**What you'll have when you're done:** 500 openly-licensed photographs of architectural interiors, organised by room type, with every image traceable back to the web page you found it on.

---

## The big picture

The Knowledge Atlas studies how buildings shape people — how ceiling height changes thinking, how daylight shifts mood, how clutter raises stress. Studying these effects computationally takes thousands of photographs of real interior spaces. Your job is to gather 500 of them.

But "gather" does not mean "drag images off Google." Every image must:

1. **Carry an open licence** — Creative Commons, public domain, or equivalent. No copyright violations.
2. **Carry provenance** — for every image you know where you found it, who took it, and what licence it carries.
3. **Carry a category** — you know what kind of room it shows.

You will build the tools that make this efficient, then use those tools to gather your 500.

---

## The 15 room types

The collection must span a wide range of interior spaces. Use these 15 categories:

| # | Room type | What to search for | Why we need it |
|---|---|---|---|
| 1 | `living_room` | living room, lounge, sitting room | Furniture layout, daylight, biophilia, colour warmth |
| 2 | `bedroom` | bedroom, sleeping quarters | Lighting warmth, enclosure, materials, tranquillity |
| 3 | `kitchen` | kitchen, cooking area | Component detection (cabinets, counters), materials, layout |
| 4 | `bathroom` | bathroom, restroom, washroom | Materials (tile, glass), fixtures, spatial geometry |
| 5 | `office` | office interior, workspace, workstation | Task lighting, spatial openness, visual complexity |
| 6 | `classroom` | classroom, lecture hall, seminar room | Social-spatial layout, lighting, legibility |
| 7 | `hospital` | hospital room, clinic interior, patient room | Safety, materials, lighting, wayfinding |
| 8 | `restaurant` | restaurant interior, café, dining room | Social density, lighting ambience, material warmth |
| 9 | `lobby` | hotel lobby, building lobby, atrium | Spatial volume, ceiling height, prospect-refuge |
| 10 | `corridor` | hallway, corridor, passage | Spatial geometry, wayfinding, enclosure ratio |
| 11 | `library` | library interior, reading room | Cognitive restoration, natural light, visual order |
| 12 | `retail` | retail store, shop interior, showroom | Colour, lighting, visual complexity, layout |
| 13 | `museum` | museum gallery, exhibition space | Spatial volume, lighting, visual complexity |
| 14 | `worship` | church interior, temple, mosque | Ceiling height, geometry, fractal patterns, affect |
| 15 | `gym` | gym, fitness centre, sports hall | Spatial openness, materials, lighting intensity |

You may add up to 5 more categories if you discover important gaps. These 15 are the minimum.

Save this list as `space_types.json` in your repo. Use this format:

```json
{
  "living_room": {
    "search_terms": ["living room interior", "lounge interior", "sitting room"],
    "why": "Furniture layout, daylight, biophilia, color warmth"
  },
  "bedroom": {
    "search_terms": ["bedroom interior", "sleeping quarters"],
    "why": "Lighting warmth, enclosure, materials, tranquility"
  }
}
```

---

## Phase 1: Find your image sources

Find at least **5 websites or databases** that supply openly-licensed photographs of architectural interiors. Some offer free APIs; some you will browse by hand. All must publish a clear licence.

### What "openly licensed" means

| Licence | OK to use? | Attribution needed? |
|---|---|---|
| CC0 (Public Domain) | ✅ Yes | No |
| CC-BY | ✅ Yes | Yes — credit the photographer |
| CC-BY-SA | ✅ Yes | Yes — credit and share alike |
| Unsplash Licence | ✅ Yes | Attribution appreciated, not required |
| Pexels Licence | ✅ Yes | No attribution required |
| CC-NC (Non-Commercial) | ⚠️ Check | OK for academic research, not commercial |
| All Rights Reserved / © | ❌ No | Cannot use |

### Starting points (you must find more)

- **Unsplash** (unsplash.com) — high-quality, free API, strong architectural content
- **Pexels** (pexels.com) — free API, no attribution needed
- **Flickr** (flickr.com) — API with CC-licence filtering, large architecture groups
- **Wikimedia Commons** (commons.wikimedia.org) — CC and public-domain interiors
- **Pixabay** (pixabay.com) — free, CC0-equivalent licence

### Your deliverable: `image_sources.json`

> **Contract objective:** "I want a tested, documented list of image sources I can use to collect 500 interior photos."
> **Contract is with:** Public image APIs and websites.
> **Prompt hint:** *"I need to find 5+ sources of openly-licensed architectural interior photos. For each: does it have an API? What license? How do I search it? Test one query and tell me how many results."*

Write YOUR OWN contract for this phase. Cover Inputs, Processing, Outputs, and Success Conditions.

**Success conditions (minimum):**

- [ ] At least 5 sources documented
- [ ] Each source records: name, URL, licence type, API availability (yes/no)
- [ ] At least 3 sources tested with a sample query
- [ ] Each tested source records how many results the sample query returned

```json
{
  "sources": [
    {
      "name": "Unsplash",
      "url": "https://unsplash.com",
      "api_url": "https://api.unsplash.com/",
      "has_api": true,
      "license": "Unsplash License (free, attribution appreciated)",
      "rate_limit": "50 requests/hour (free tier)",
      "tested": true,
      "test_query": "modern living room interior",
      "test_results": 1247
    }
  ]
}
```

---

## Phase 2: Build the search pipeline

Now automate the gathering. Write a Python script that takes a room type and a source, runs the search, and saves the results. We call this the **search pipeline** — the script that drives queries against your image sources and returns structured records.

> **Contract objective:** "I want a script that searches my image sources for photos of each room type and saves the results as JSON."
> **Contract is with:** Your image source APIs and `space_types.json`.
> **Prompt hint:** *"Build a Python script that reads space_types.json, loops through each room type, queries the Unsplash/Pexels/Flickr API for that room type's search terms, and saves results as JSON. Each result must include: image URL, thumbnail URL, photographer name, source name, source page URL, and license."*

Write YOUR OWN contract. Then write your tests BEFORE building:

- [ ] API keys live in environment variables, not in source code
- [ ] The script respects rate limits (look for `time.sleep`)
- [ ] Every image record carries `url`, `source_name`, `source_page_url`, and `license`
- [ ] Output JSON validates
- [ ] Zero-result searches are logged, not silently skipped

### What each image record must look like

```json
{
  "url": "https://images.unsplash.com/photo-abc123",
  "thumbnail_url": "https://images.unsplash.com/photo-abc123?w=400",
  "title": "Modern minimalist living room",
  "photographer": "Jane Doe",
  "source_name": "Unsplash",
  "source_page_url": "https://unsplash.com/photos/abc123",
  "license": "Unsplash License",
  "space_type": "living_room",
  "search_query": "modern living room interior",
  "collected_at": "2026-05-01T12:00:00Z"
}
```

**Deliverable:** `search_pipeline.py` + `search_results.json`

---

## Phase 3: Build the collection page

Build a web page that lets you browse search results, accept or reject images, upload local files, and watch your progress toward 500.

> **Contract objective:** "I want an interactive page where I can manage my image collection — search, browse, accept/reject, upload, and export."
> **Contract is with:** Your search results and the Image Tagger upload API.
> **Prompt hint:** *"Build an HTML page with these features: (1) a search bar that loads results from search_results.json, (2) a thumbnail grid with accept/reject buttons, (3) a file upload zone for drag-and-drop, (4) provenance fields that are required before accepting, (5) a progress counter showing N/500, (6) an export button that downloads the collection as JSON."*

### Required features

| Feature | What it does |
|---|---|
| **Search / filter** | Filters images by room type or keyword |
| **Thumbnail grid** | Shows images with title, source, licence |
| **Accept / Reject** | Accepts an image into the collection or rejects it |
| **Upload** | Drag-and-drop for local files or folders |
| **Provenance fields** | Source URL and source name — required before accepting |
| **Progress counter** | Shows how many images you have collected out of 500 |
| **Export** | Downloads `collection.json` with full provenance |

### Provenance is non-negotiable

Every image in your collection must carry these fields:

| Field | Required? | Auto-filled from search? |
|---|---|---|
| `source_page_url` | ✅ Yes | Yes (from API) |
| `source_name` | ✅ Yes | Yes (from API) |
| `photographer` | Best effort | Usually (from API) |
| `license` | ✅ Yes | Yes (from API) |
| `space_type` | ✅ Yes | Yes (from search) |

For images you upload **manually** (not from a search), type in the source URL and source name yourself. If you cannot tell where an image came from, **leave it out**.

Write YOUR OWN contract and tests for this phase.

**Deliverable:** `ka_image_collection.html`

---

## Phase 4: Collect 500 images

Use your pipeline and your collection page to gather the 500.

### Distribution targets

| Requirement | Target |
|---|---|
| Total images | 500 |
| Room types covered | ≥ 12 of the 15 |
| Images per top-10 room type | ≥ 15 each |
| Sources used | ≥ 3 different databases |
| Images with full provenance | 500 / 500 |

### Spot-check your provenance

Pick **10 random images** from your collection. For each one:

1. Open the `source_page_url` in a browser. Does the page exist?
2. Does the licence on the page match what you recorded?
3. Is the photographer credit correct?

Record what you find. Discrepancies happen — what counts is that you checked.

### Collection report

Fill in this table:

| Metric | Your count |
|---|---|
| Total images | /500 |
| Room types represented | /15 |
| Images from search pipeline | |
| Images from manual upload | |
| Sources used | |
| Provenance spot-check: pages exist | /10 |
| Provenance spot-check: licence matches | /10 |

**Deliverables:** `collection.json` + the collection report (in your submission)

---

## What you submit

| Item | Filename |
|---|---|
| Space types | `space_types.json` |
| Image sources | `image_sources.json` |
| Search pipeline | `search_pipeline.py` |
| Search results | `search_results.json` |
| Collection page | `ka_image_collection.html` |
| Image collection | `collection.json` (500 images with provenance) |
| Collection report | The table above, filled in |
| Contracts + tests | Your written contracts and test checklists |
| File manifest | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 20 | Written BEFORE building. Specific, not vague. **(CONTRACT GATE)** |
| **Image sources** | 10 | ≥ 5 sources, ≥ 3 tested, licences documented |
| **Search pipeline** | 10 | Automated, respects rate limits, tracks provenance |
| **Collection page** | 15 | Search + browse + upload + provenance + export |
| **500 images** | 15 | Full provenance, ≥ 12 room types, ≥ 3 sources |
| **Verification** | 5 | Spot-checked provenance, caught issues in the AI's implementation |

> ⛔ **Contract gate**: Missing or vague contracts ("it works") flag your submission and keep your images out of the Atlas. Write real contracts with real success conditions.

---

## Reuse

The work you ship in Task 1 is infrastructure for the rest of the track. Your image sources, your search pipeline, and your collection page feed Task 2 (where you tag these images), Task 3 (where you run inter-rater agreement on them), and Task 4 (where you train a classifier on them). Build them right the first time.

---

## Existing code you should know about

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | The tag registry — 424 tags grouped by domain. Tells you which features matter in each room type. |
| `Tagging_Contractor/Tagging_Contractor_What_it_is_and_How_to_use_it.md` | How the tagging system works |
| `image-tagger/docs/CONTRACT.md` | Image Tagger API — the upload endpoint your images will eventually pass through |
| `Outcome_Contractor/README.md` | The human-side vocabulary (cognitive and affective effects) — the reason we need these images |

---

# Track 1 · Task 2: Build Latent Tag Detectors

**Track:** Image Tagger  
**Prerequisite:** Task 1 (you need your 500 images with provenance)  
**Points:** 75  
**What you'll have when you're done:** Working Python detectors for 6 latent environmental tags. Each detector ships with a design note, a typed contract, and a test suite that runs against a gold-set of labelled images.

---

## The big picture

In Task 1 you gathered 500 architectural interior photographs with provenance. In Task 2 you tag them — not with simple labels like "living room" or "bedroom," but with **latent tags**: numerical measures of environmental features that affect human cognition and behaviour. (Latent because the feature is not directly visible as a noun in the image; you compute it from geometric relationships among visible objects.)

### What the instructor already did (Sprint 1)

Before this course began, the instructor finished Sprint 1: the 18 social-interaction latent variables (L41–L58) from the Environment-Cognition Taxonomy V2.6 (the project's master vocabulary of environmental tags) are already integrated into the Tagging Contractor registry. That means:

- Every latent tag (L44 Sociopetal Seating, L17 Prospect, L42 Interactional Visibility, and the rest) **already exists in the registry**, with a full semantic contract.
- Each entry has a `definition_long` field that explains what the tag means in human terms.
- Each entry has a `method_family` field that specifies *how* to detect the tag from an image.
- Each entry has `extractability` flags that tell you whether the tag can be detected from a 2D photo.

You can read these entries directly:
```bash
python3 -c "
import json
r = json.load(open('Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json'))
tags = r['tags']
# Look at one latent tag
for tid, t in tags.items():
    if 'sociopetal' in t.get('canonical_name','').lower() or 'L44' in tid:
        print(json.dumps(t, indent=2))
        break
"
```

**The registry is your source of truth.** Your detectors must match the registry's vocabulary. If your detector drifts from the `definition_long`, the semantic audit gate will catch it.

### What you bring from Task 1

- Your **500 images**, organised by room type, with provenance
- Your **`space_types.json`** taxonomy
- Your **collection page** for browsing and managing images

### What the tagger provides (intermediate representations)

For a gold-set of images, the tagger has already computed the heavy machine-vision outputs you would otherwise have to produce yourself:
- **COCO-133 segmentation masks** — pixel-level labels for 133 object classes (people, furniture, objects)
- **Monocular depth maps** — estimated distance per pixel
- **Skeletonised floor masks** — circulation paths extracted from the floor regions
- **Basic VLM/CLIP tag predictions** — simple visual features predicted by a Vision-Language Model (a neural net that maps images to text labels)

Your detectors compute *on top of* these intermediate representations. You are not training neural networks. You are writing geometric and logical predicates — computational geometry, not deep learning.

---

## The 18 latent tags, grouped by detection method

Each tag belongs to one of three families, set by the kind of geometric computation it requires:

### Family A: Furniture geometry (object detection + spatial arrangement)

These tags fall out of pairwise angles, distances, and cluster counts over the COCO-133 segmentation masks the tagger has already produced. Classical F-formation geometry (Kendon, 1990; Marquardt et al., 2012) supplies the predicates.

| Tag ID | Tag name | What it measures |
|---|---|---|
| L44 | Sociopetal Seating | Are seats arranged facing each other (conversation-promoting)? |
| L48 | Dyadic Intimacy | Is there a pair of seats at intimate distance (< 1.2 m)? |
| L49 | Small-Group Support | Does the seating arrangement support 3–5 person groups? |
| L53 | Shared Attention Anchor | Is there a focal point (screen, fireplace, window) that the seating faces? |

### Family B: Sightlines and isovists (depth map + spatial analysis)

These tags fall out of *isovist* analysis: the polygon visible from a vantage point, with metrics like isovist area, maximum viewshed depth, and partition-height ratios computed over the monocular depth map (Benedikt, 1979; Wiener et al., 2007).

| Tag ID | Tag name | What it measures |
|---|---|---|
| L42 | Interactional Visibility | Can occupants see each other across the space? |
| L54 | Boundary Permeability | How open versus enclosed are the spatial boundaries? |
| L17 | Prospect | Does the space offer long views (high prospect)? |

### Family C: Circulation and apertures (floor plan skeleton + graph analysis)

These tags reduce to path counts, aperture widths, and dead-end detection over the skeletonised floor mask (Hillier & Hanson, 1984).

| Tag ID | Tag name | What it measures |
|---|---|---|
| L41 | Chance-Encounter Potential | Does the layout create intersections where people meet by accident? |
| L47 | Turn-Taking Support | Do circulation paths support natural conversational turn-taking? |
| L57 | Disengagement Ease | Can a person leave a social situation without disrupting it? |

---

## Your assignment: implement 6 detectors

Each student team picks **6 tags**, with at least 2 from each family. For each tag, follow the 7-step scaffold below.

---

## The 7-Step Scaffold

The scaffold runs Panel → Spec → Tests → Build → Verify → Diagnose → Iterate. Each step locks down a commitment before the next step extends it.

### Step 1: Panel — write a detector design note

For each of your 6 tags, write a one-page **detector design note** that nails down:

**(a)** The upstream tags the detector consumes — which intermediate representations does it need (depth map, segmentation mask, skeleton)?

**(b)** The geometric or logical predicate that encodes the latent tag. Example: "Sociopetal Seating = TRUE if ≥ 3 detected seating objects have pairwise facing angles < 45° and centroid distances < 2.5 m in the depth-projected coordinate frame."

**(c)** The failure modes you expect. Example: "Monocular depth is unreliable beyond 5 m, so L17 Prospect may underestimate viewshed depth in large atriums."

> **Contract objective:** "I want a one-page design note for detector L__ that states what inputs it consumes, what geometric predicate it computes, and where it will fail."
> **Contract is with:** The Tagging Contractor registry (for the tag's `definition_long` and `method_family`) and the tagger's existing intermediate representations.
> **Prompt hint:** *"Read the registry entry for tag L__ in `registry_v0.2.8.json`. What does `definition_long` say? What does `method_family` say? Now design a detector: what intermediate data do I need, what geometric computation do I run, and what score do I output?"*

**Panel review:** Before moving on to Step 2, critique your teammates' design notes. Does the predicate actually encode what the tag means? Are the failure modes realistic?

### Step 2: Spec — convert the note to a typed function signature

Convert the design note into a **typed function signature with a docstring**, written in the same vocabulary the registry uses in `definition_long`. The docstring is the contract: if it drifts from the registry, the semantic gate will catch it.

```python
def detect_sociopetal_seating(
    segmentation_mask: np.ndarray,
    depth_map: np.ndarray,
    detected_objects: list[DetectedObject],
) -> TagResult:
    """Detect sociopetal seating arrangement (L44).
    
    Computes pairwise facing angles between detected seating objects
    using F-formation geometry (Kendon, 1990). Returns score > 0.5
    when >= 3 seating objects have pairwise facing angles < 45 degrees
    and centroid distances < 2.5m in the depth-projected coordinate frame.
    
    Inputs:
        segmentation_mask: COCO-133 segmentation output (H x W int array)
        depth_map: Monocular depth estimate (H x W float array, meters)
        detected_objects: List of detected objects with class, bbox, confidence
    
    Returns:
        TagResult with score (0-1), confidence, and evidence dict
    
    Failure modes:
        - Depth unreliable > 5m: facing angle estimation degrades
        - Occluded furniture: segmentation misses partially visible seats
    """
```

> **Contract objective:** "I want a typed function signature for detector L__ that matches the registry vocabulary."
> **Contract is with:** The registry's `definition_long` field.

### Step 3: Tests — write pytest cases BEFORE you implement

Write your test cases against the Sprint 1 gold-set images. **Minimum:**
- 6 passing positives (images where the tag IS present, confirmed by human labelling)
- 4 passing negatives (images where the tag is NOT present)
- A regression fixture for every edge case the panel surfaced in Step 1

```python
def test_sociopetal_seating_positive_living_room():
    """Living room with U-shaped sofa arrangement should score > 0.5."""
    result = detect_sociopetal_seating(
        segmentation_mask=load_gold("img_042_seg.npy"),
        depth_map=load_gold("img_042_depth.npy"),
        detected_objects=load_gold("img_042_objects.json"),
    )
    assert result.score > 0.5
    assert result.confidence > 0.3

def test_sociopetal_seating_negative_corridor():
    """Empty corridor with no seating should score < 0.2."""
    result = detect_sociopetal_seating(...)
    assert result.score < 0.2
```

> **Write the tests BEFORE you write the detector.** That is test-driven development. The tests are what defines "correct."

### Step 4: Build — implement the detector

Now write the detector function. Rules:

- **Keep each detector under 150 lines.** If it grows past that, the predicate is probably wrong.
- **Reuse the existing intermediate representations.** Don't recompute segmentation or depth — consume what the tagger already produces.
- **Keep the computation transparent.** A reader should be able to diagnose the detector by reading the code, not by probing a neural network.
- **Commit to `track1/extractors/L__-your-team/`.**

Most detectors in Families A–C reduce to one of three computations over the tagger's intermediate representations:
- **Family A (Furniture geometry):** pairwise operations over COCO-133 bounding boxes plus depth-projected coordinates
- **Family B (Sightlines):** isovist computation over the monocular depth map
- **Family C (Circulation):** graph analysis (path counting, dead-end detection) over the skeletonised floor mask

### Step 5: Verify — run your tests

```bash
pytest track1/extractors/L44-your-team/test_L44.py -v
```

All 10 tests (6 positive + 4 negative) must pass. If they fail, one of three things is wrong:
- Your detector has a bug (fix the code)
- A test has a bad gold label (verify the image manually)
- The intermediate representation is poor quality (document it as a known limitation)

### Step 6: Diagnose — run the semantic gate

The Tagging Contractor ships an audit tool that checks your detector's output vocabulary against the registry:

```bash
./bin/tc audit-semantics --extractor track1/extractors/L44-your-team/
```

If the audit fails, your docstring or output format has drifted from the registry. Fix it.

### Step 7: Iterate — write the detector card

For each detector, write a short card:

| Field | Content |
|---|---|
| **Tag ID** | L44 |
| **Tag name** | Sociopetal Seating |
| **Family** | A (Furniture geometry) |
| **Inputs consumed** | COCO-133 segmentation, monocular depth |
| **Predicate** | ≥ 3 seating objects with pairwise facing angles < 45° and centroids < 2.5 m |
| **Score range** | 0.0 – 1.0 |
| **Known failure modes** | Depth unreliable > 5 m; occluded furniture |
| **Test results** | 6/6 positive, 4/4 negative |
| **Audit status** | PASS |

---

## What you submit

| Item | What it is |
|---|---|
| **6 design notes** (Step 1) | One page each, with inputs, predicate, failure modes |
| **6 typed function signatures** (Step 2) | Docstrings match registry vocabulary |
| **6 test suites** (Step 3) | ≥ 10 tests each (6 positive + 4 negative) |
| **6 detector implementations** (Step 4) | Under 150 lines each |
| **Test results** (Step 5) | pytest output showing all tests pass |
| **Audit results** (Step 6) | `tc audit-semantics` output for each detector |
| **6 detector cards** (Step 7) | One summary table per detector |
| **Contracts** | Your written contracts for each phase |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + design notes** | 15 | Written BEFORE building. Predicates are specific. **(CONTRACT GATE)** |
| **Test suites** | 15 | Written BEFORE detectors. ≥ 10 tests per detector. |
| **Detector implementations** | 20 | Correct, under 150 lines, reuses existing intermediates |
| **Audit pass** | 10 | `tc audit-semantics` passes for all 6 detectors |
| **Detector cards** | 5 | Complete, accurate, failure modes documented |
| **Verification** | 10 | Caught problems in the AI's implementation, documented the fixes |

> ⛔ **Contract gate**: Missing or vague design notes and contracts flag your detectors and keep them out of the tagger. Write real predicates with real failure modes.

---

## Key references

| Reference | What it provides |
|---|---|
| Kendon, A. (1990). *Conducting Interaction.* | F-formation geometry for seating arrangement analysis |
| Marquardt, N. et al. (2012). | Computational F-formation detection from spatial data |
| Benedikt, M.L. (1979). "To Take Hold of Space: Isovists and Isovist Fields." | Isovist theory for visibility analysis |
| Wiener, J.M. et al. (2007). | Isovist-based spatial cognition metrics |
| Hillier, B. & Hanson, J. (1984). *The Social Logic of Space.* | Space syntax for circulation and encounter analysis |

---

## Existing code you should know about

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | 424 tags with `definition_long`, `method_family`, and `extractability` |
| `Tagging_Contractor/contracts/localized_image_tags.schema.json` | JSON schema for tagged image output |
| `./bin/tc audit-semantics` | Checks detector output vocabulary against the registry |
| `./bin/tc audit-tags` | Checks tag completeness |
| `image-tagger/docs/CONTRACT.md` | Image Tagger API contract (upload, explore, workbench) |
| Sprint 1 gold-set | Pre-computed segmentation masks, depth maps, skeletons for labelled images |

---

## Reuse

The detectors you ship here become science-pipeline infrastructure. Task 3 runs your detectors on the full 500-image collection and surfaces them in a public viewer; later cohorts will run inter-rater agreement on your output and evaluate detector accuracy against human judgement. Build them as long-lived components, not throwaway code.

---

# Track 1 · Task 3: Annotate the Collection and Build the Image Viewer

**Track:** Image Tagger  
**Prerequisite:** Task 1 (your 500 images with provenance) + Task 2 (your 6 latent-tag detectors)  
**Points:** 75  
**What you'll have when you're done:** Every image in your 500-image collection annotated with latent-tag scores, plus an interactive web page where anyone can search and browse the images by tag category OR by human effect.

---

## Why we need this

In Task 2 you built 6 latent-tag detectors. But you only tested them on a small gold-set. Task 3 runs them on the **entire 500-image collection** and then ships a viewer so humans can browse, search, and verify the results.

The image-tagger repo already has an Explorer app (v3.4.74), but it is a full React/Vite application that needs a running backend, a database, and authentication. It is developer infrastructure — not something a student or researcher can open in a browser and use.

The gap looks like this:

| What exists | What's missing |
|---|---|
| 424 tags in the `Tagging_Contractor` registry, organised across 44 domains | No way to browse images *by tag* without running the full tagger backend |
| 839 outcome terms in the `Outcome_Contractor`, across 7 domains (Cognitive, Affective, Behavioural, Social, Physiological, Neural, Health) | No way to ask "show me spaces that promote creativity" and see matching images |
| 832 constitutive bridges that link effects into a hierarchy | No UI that uses this hierarchy for filtering |
| Your 500 images with provenance (Task 1) | No searchable viewer for your collection |
| Your 6 latent-tag detectors (Task 2) | **They have only run on a small gold-set — not on the full collection** |

You are going to close both gaps: first annotate everything, then build the viewer.

---

## Phase 1: Run your detectors on the full image collection

Annotations come before the browser. This is the moment of truth for your Task 2 detectors: do they actually work at scale?

### What we learned from prototyping this task

We prototyped the full pipeline for one latent tag (L42 Interactional Visibility) to confirm everything works end-to-end. Here is what the prototype taught us:

**Dependencies are minimal.** You only need `Pillow` (PIL) and `numpy`. No deep-learning frameworks are required — your detectors compute geometric predicates over image statistics, not neural-network features.

**Proxy features work.** The registry says L42 wants "floor-plan-augmented isovist computation." You don't have floor plans. That's fine. The registry acknowledges this: the 2D-proxy approach uses edge density, brightness variance, and partition coverage as stand-ins for the full isovist. Document what your detectors are proxying and why.

**Directional accuracy is what matters.** Our prototype scored an open office at 2.4/4.0 and a cubicle farm at 1.9/4.0 — the right direction, modest separation. That is what to expect from a proxy approach without real depth maps. If your detector separates high-visibility from low-visibility spaces in the right direction, it is working.

**Use the registry's output format.** Each tag in the registry carries a `value_type` (binary, ordinal, continuous) and a `value_range`. The social-interaction tags use `ordinal` over `[0, 4]` (a Likert scale). Your annotations must use the registry's `tag_id` as the key, not a name you invent.

**Set confidence honestly.** Without real depth maps or segmentation, your confidence should be low (0.2–0.4). If you add a real depth model like MiDaS, confidence rises. Document what confidence means in your detector's docstring.

### 1A. Write the batch-runner contract

> **Contract objective:** "I want a script that runs all 6 of my latent tag detectors on every image in `collection.json` and produces a single `annotations.json` file with scores per image."
> **Contract is with:** Your 6 detector functions (from Task 2) and your `collection.json` (from Task 1).
> **Prompt hint:** *"I have 6 detector functions and 500 images. Write a batch runner that loads each image, runs all 6 detectors using PIL and numpy, and writes the results to annotations.json. It must handle failures gracefully — if one detector crashes on one image, log the error and continue. I only need Pillow and numpy, no ML frameworks."*

**Your contract must cover:**
- Reads image paths from `collection.json`
- For each image, loads the image with PIL and computes proxy features (edge density, brightness statistics, colour statistics)
- Runs all 6 detectors and collects the results per detector per image
- Writes a single `annotations.json` that follows the `image_tagger_observation` schema:

```json
{
  "version": "1.0",
  "generated_at": "2026-04-27T...",
  "detectors": ["social.interactional_visibility", "social.sociopetal_seating",
                "social.dyadic_intimacy", "social.small_group_conversation",
                "social.shared_attention_anchor", "social.boundary_permeability"],
  "images": {
    "img_001.jpg": {
      "room_type": "living_room",
      "tags": {
        "social.sociopetal_seating": {
          "value": 2.8,
          "value_type": "ordinal",
          "confidence": 0.35,
          "evidence": {
            "facing_pairs": 3,
            "cluster_size": 4,
            "depth_source": "proxy"
          }
        },
        "social.interactional_visibility": {
          "value": 3.2,
          "value_type": "ordinal",
          "confidence": 0.30,
          "evidence": {
            "partition_score": 0.15,
            "openness_score": 0.82,
            "partition_coverage": 0.08
          }
        }
      }
    }
  },
  "errors": {
    "img_099.jpg": {"detector": "social.shared_attention_anchor", "error": "image too dark for edge detection"}
  },
  "stats": {
    "total_images": 500,
    "images_annotated": 497,
    "images_with_errors": 3,
    "mean_scores": {"social.sociopetal_seating": 1.85, "social.interactional_visibility": 2.10}
  }
}
```

**Key:** Use the registry's `tag_id` (e.g. `social.interactional_visibility`), NOT a name you invent. Use `value` (not `score`) with the tag's `value_type` and `value_range` from the registry.

### 1B. Write your tests BEFORE running

- [ ] The script runs on 10 images without crashing
- [ ] Each image gets scores for all 6 detectors (or a logged error)
- [ ] `annotations.json` is valid JSON and matches the schema above
- [ ] Failed images appear in the `errors` section (not silently dropped)
- [ ] The `stats` section has correct counts
- [ ] Score distributions are plausible (not all 0.0, not all 1.0)

### 1C. Run the batch and verify

```bash
python3 batch_annotate.py --collection collection.json --output annotations.json
```

When it finishes, check:

> *"How many images were annotated? How many had errors? Show me the score distribution for each detector — are they plausible?"*

**Reality check:** these are 0–4 Likert scores. If a detector scores > 2.5 on more than 80% of images, something is wrong — not every space has sociopetal seating. If a detector scores < 0.5 on everything, it is probably broken. Our prototype found means around 1.9–2.4 across room types, which is plausible.

```python
# Quick sanity check
import json
ann = json.load(open("annotations.json"))
for det in ann["detectors"]:
    scores = [img["tags"][det]["value"]
              for img in ann["images"].values() if det in img.get("tags", {})]
    print(f"{det}: mean={sum(scores)/len(scores):.2f}, "
          f">2.5: {sum(1 for s in scores if s > 2.5)}/{len(scores)}")
```

### 1D. Fix the detector issues that scale surfaces

Running on 500 images surfaces problems that 10 gold-set images never reveal:
- Missing depth maps for certain room types
- Segmentation that fails on unusual furniture
- Edge cases in your geometric predicates

Document what broke, fix it, re-run. This is the most valuable engineering lesson in the task.

**Your deliverable:** `annotations.json` with scores for 500 images, plus a "batch run report" that documents the errors found and the fixes applied.

---

## Phase 2: Build the image viewer

With `annotations.json` in hand, build a standalone HTML viewer. We have prototyped this and confirmed it ships as a single HTML file with inline CSS and JavaScript — no framework, no backend, no build step.

> **Contract objective:** "I want a standalone HTML page that loads `annotations.json` and the tag registry, and lets users browse images by tag domain or by human effect."

### Architecture: one HTML file, three data files

```
ka_image_viewer.html      ← your viewer (HTML + CSS + JS, all inline)
annotations.json          ← your Phase 1 output (500 images × 6 tag scores)
effect_tag_mapping.json   ← maps Outcome_Contractor effects to tag IDs
collection.json           ← your Task 1 image manifest (paths + provenance)
```

The viewer loads these JSON files at startup with `fetch()`. Everything runs client-side.

### Component 1: Mode selector (tag mode vs. effect mode)

Two tab buttons sit at the top. Clicking a tab switches the filter bar.

```
┌─────────────────────────────────────────────────────┐
│  🏷️ [Search by Tag]   🧠 [Search by Effect]        │
└─────────────────────────────────────────────────────┘
```

- **Tag mode** shows domain checkboxes from the Tagging_Contractor registry.
- **Effect mode** shows domain checkboxes from the Outcome_Contractor vocabulary.

### Component 2: Filter bar

**In tag mode**, generate one checkbox per tag domain dynamically from the registry. Group the 44 domains into manageable categories:

```
┌─────────────────────────────────────────────────────┐
│ 🔍 [Search images, tags, effects...              ]  │
│                                                     │
│ ☐ Social-Spatial (18)  ☐ Lighting (41)             │
│ ☐ Spatial Config (39)  ☐ Biophilia (20)            │
│ ☐ Materials (14)       ☐ Complexity (22)           │
│ ☐ Color (14)           ☐ ...more                   │
└─────────────────────────────────────────────────────┘
```

**In effect mode**, show one checkbox per Outcome_Contractor domain:

```
┌─────────────────────────────────────────────────────┐
│ ☐ Cognitive (100)    ☐ Affective (94)              │
│ ☐ Behavioral (147)  ☐ Social (128)                 │
│ ☐ Physiological (131)  ☐ Neural (107)              │
│ ☐ Health (132)                                      │
└─────────────────────────────────────────────────────┘
```

**How to build the domain checkboxes:**

```javascript
// Load registry, extract unique domains, count tags per domain
const registry = await fetch('registry_v0.2.8.json').then(r => r.json());
const domains = {};
for (const [tid, tag] of Object.entries(registry.tags)) {
  const d = tag.domain || 'unknown';
  domains[d] = (domains[d] || 0) + 1;
}
// Render as checkbox inputs
filterBar.innerHTML = Object.entries(domains)
  .sort((a,b) => b[1] - a[1])
  .map(([name, count]) => 
    `<input type="checkbox" id="d-${name}" onchange="render()">` +
    `<label for="d-${name}">${name} (${count})</label>`
  ).join('');
```

### Component 3: Image grid

A CSS Grid of image cards. Each card shows:
- **Thumbnail** (the actual image, served from a `collection.json` path)
- **Image name** (from the filename)
- **Room type** (from collection metadata)
- **Tag count** ("6 tags")
- **Top tag score** as a coloured bar (green > 0.6, yellow 0.3–0.6, red < 0.3)
- **Score label** ("interactional visibility: 3.2/4.0")

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}
```

**Filtering logic:** when checkboxes are selected, filter `annotations.json` to show only images that carry tags in the selected domains with scores above a threshold (for example, > 0.5).

**Pagination:** 500 images is too many for one DOM render. Use lazy loading or "Load more" — 50 images per page.

### Component 4: Image detail modal

When the user clicks a card, open a modal:

```
┌─────────────────────────────────────────────────────┐
│                                              [×]    │
│  test open office                                   │
│  Room: office · Source: Unsplash · License: CC0     │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │                                             │    │
│  │          [Full-size image]                   │    │
│  │                                             │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  Tags & Scores                                      │
│  ┌─────────────────────────────────────────────┐    │
│  │ interactional visibility    3.2/4.0  ████░  │    │
│  │   partition_score: 0.150                    │    │
│  │   openness: 0.820                           │    │
│  │   partition_coverage: 0.080                 │    │
│  ├─────────────────────────────────────────────┤    │
│  │ sociopetal seating          1.8/4.0  ██░░░  │    │
│  │   facing_pairs: 2                           │    │
│  │   cluster_size: 3                           │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  Linked Effects                                     │
│  [Social] ← interactional visibility, sociopetal    │
│  [Cognitive] ← interactional visibility             │
└─────────────────────────────────────────────────────┘
```

The modal must show:
- **Score bars:** coloured bars proportional to the 0–4 Likert value
- **Evidence table:** every key/value pair from the `evidence` dict in the annotation
- **Linked effects:** for each Outcome_Contractor domain that maps to tags present on this image, show the domain name and which tags triggered it. Drive this from `effect_tag_mapping.json`.
- **Provenance:** source URL, photographer, licence — pulled from `collection.json`

### Component 5: Effect explanations (effect mode only)

When browsing by effect, each card must show WHY it matched:

```
tag → mechanism → effect

Example: "interactional visibility (3.2/4.0) → mutual awareness → Social outcomes"
```

Build the chain from `ae_outcome_lookup.json` (a pre-built mapping between text terms and outcome IDs in the Knowledge Atlas pipeline) and the PNU templates.

### How to build `effect_tag_mapping.json`

This file is the bridge between the Outcome_Contractor's 7 effect domains and the Tagging_Contractor's tag IDs. The effect-mode filter cannot work without it.

**Option A (recommended — reuse existing data):**

```python
# Start from ae_outcome_lookup.json (2,114 pre-built term→outcome mappings)
import json
lookup = json.load(open('Outcome_Contractor/contracts/oc_export/ae_outcome_lookup.json'))
# This maps text terms → outcome IDs
# Cross-reference with your tag IDs to build domain-level mapping
```

**Option B (manual, for your 6 tags):**

You only have 6 detectors, so you can map them to effects by hand:

```json
{
  "effect_to_tags": {
    "social": ["social.interactional_visibility", "social.sociopetal_seating",
               "social.dyadic_intimacy", "social.shared_attention_anchor"],
    "cog": ["social.interactional_visibility"],
    "affect": ["social.sociopetal_seating", "social.dyadic_intimacy"],
    "behav": ["social.sociopetal_seating", "social.interactional_visibility"]
  }
}
```

Ask your AI: *"Given these 6 latent tags and their registry definitions, which Outcome_Contractor domains (Cognitive, Affective, Behavioral, Social, Physiological, Neural, Health) does each tag relate to? Use the PNU templates in Article_Eater/data/templates/ for evidence."*

### Success conditions

- [ ] The viewer loads `annotations.json`, `collection.json`, and `effect_tag_mapping.json` at startup
- [ ] Tag mode: domain checkboxes are generated from the registry; filtering shows only matching images
- [ ] Effect mode: 7 domain checkboxes from the Outcome_Contractor; filtering uses the effect→tag mapping
- [ ] Free-text search works across image names, room types, tag names, and effect names
- [ ] The image grid handles 500 images via lazy loading or pagination (50 per page)
- [ ] Clicking a card opens a detail modal with all tags, scores, evidence, effects, and provenance
- [ ] Score bars are colour-coded (green/yellow/red) and proportional to the value
- [ ] The viewer needs no backend — it works as a standalone HTML file opened directly in a browser
- [ ] The two modes can be combined (e.g. "Social-Spatial" tag domain + "Cognitive" effect domain)

---

## Phase 3: Polish and integrate

- [ ] Score distributions look correct (not all 0.0, not all 4.0)
- [ ] Provenance is visible on every image (source URL, photographer, licence)
- [ ] Annotation scores show as visual bars with value labels
- [ ] The modal closes on Escape and on overlay click
- [ ] The layout is responsive (works on mobile and desktop)
- [ ] The page title and subtitle describe what the tool does
- [ ] An empty state ("No images match your filters") shows when nothing matches

Write YOUR OWN contract and tests for this phase.

---

## What you submit

| Item | What it is |
|---|---|
| **`annotations.json`** (Phase 1) | All 500 images annotated with all 6 detector scores |
| **Batch run report** (Phase 1) | Errors found at scale, fixes applied, score distributions |
| **`ka_image_viewer.html`** (Phase 2) | Standalone viewer with tag and effect search |
| **`effect_tag_mapping.json`** (Phase 2) | Mapping from effects to tags |
| **Contracts + tests** | Your written contracts and test checklists for each phase |
| **Viewer walkthrough** | Screenshots or a recording showing both search modes |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 10 | Written BEFORE building. Specific. **(CONTRACT GATE)** |
| **Batch annotation** | 15 | 500 images annotated, errors logged, score distributions plausible |
| **Scale fixes** | 10 | Documents what broke at scale and how you fixed it |
| **Tag browser** | 15 | Domain checkboxes work, filtering works, grid handles 500 images |
| **Effect browser** | 15 | 7 Outcome domains, drill-down, tag→effect chain shown |
| **Image detail + polish** | 10 | Tags, effects, provenance, confidence all visible; standalone HTML |

> ⛔ **Contract gate**: Missing or vague contracts and tests flag your work as not ready for integration.

---

## Data sources you should know about

### Tag and annotation data

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | 424 tags across 44 domains — your tag-filter categories |
| `Tagging_Contractor/.../observations/image_tagger_observation.schema.json` | **Official annotation schema** — your `annotations.json` must conform to this. Each tag entry carries `tag_id`, `value_type` (binary/ordinal/continuous), `value`, `confidence`, and `evidence`. |
| `Tagging_Contractor/contracts/localized_image_tags.schema.json` | Spatial annotation schema with `semantic_regions`, `dense_maps`, and `pipeline_provenance` — use this if your detectors emit region-level output |
| Your `collection.json` from Task 1 | 500 images with room types and provenance |
| Your 6 detector functions from Task 2 | Detectors that produce a `TagResult` per image |

### Effect and outcome data

| Repo / File | What it gives you |
|---|---|
| `Outcome_Contractor/contracts/oc_export/outcome_vocab.json` | 839 effect terms across 7 domains — your effect-filter categories |
| `Outcome_Contractor/contracts/oc_export/constitutive_bridges.json` | 832 parent→child bridges — the effect hierarchy for drill-down |
| `Outcome_Contractor/contracts/oc_export/ae_outcome_lookup.json` | **Pre-built tag→outcome lookup** — 2,114 entries that map text terms to outcome IDs. This is the shortcut for the effect browser; start here instead of building `effect_tag_mapping.json` from scratch. |
| `Outcome_Contractor/contracts/oc_export/bn_outcome_nodes.json` | Bayesian-network node definitions — shows the causal structure between outcomes |
| `Outcome_Contractor/contracts/oc_export/VERSION_MANIFEST.json` | Schema versions and file checksums for every OC export |

### Existing viewer code (reference, not required)

| Repo / File | What it gives you |
|---|---|
| `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/frontend/apps/explorer/` | Existing React explorer — read `ImageDetailModal.jsx` to see which APIs it calls (depth, segmentation, materials, affordance). You don't need to use this code, but it lays out the data model. |
| `image-tagger/docs/CONTRACT.md` | Image Tagger API contract — `ExplorerSearchResponse` shows the response shape |
| `image-tagger/docs/ENGINEERING_BRIEF.md` | Architecture overview — four user journeys: Explorer, Workbench, Monitor, Admin |
| `Article_Eater/data/templates/` | 166 PNU templates that link tags to effects — use these to enrich `effect_tag_mapping.json` beyond what `ae_outcome_lookup.json` provides |

---

## Reuse

What you ship here outlives the assignment. Your `annotations.json` becomes the canonical annotation layer for the image collection, and your viewer becomes the public-facing tool for the Image Tagger track. Future cohorts will inherit both — build them as long-lived infrastructure, not as throwaway code.


---
---
---


=== TRACK 2 ===
# Track 2: Article Finder — All Tasks

**Track overview:** You will build and run a literature-discovery pipeline for the Knowledge Atlas that follows the PRISMA reporting standard (Preferred Reporting Items for Systematic Reviews and Meta-Analyses — the gold-standard checklist for documenting how you found, screened, and selected papers). You start with a broken contribute page. You wire in a working classifier, pull knowledge gaps from the Article Eater's PNU mechanism templates, turn those gaps into targeted search queries, run the queries through SerpAPI, triage the returned papers at the abstract level, and report every step of the funnel on a dashboard.

**Three tasks, one pipeline:**

| Task | What you build | Points |
|---|---|---|
| Task 1 | Fix the contribute page — wire in the classifier | Graded on diagnosis, spec, fix, and validation |
| Task 2 | Gap targeting — extract gaps, score them by VOI, generate queries | 60 points |
| Task 3 | Search execution — SerpAPI, abstract collection, triage, PRISMA | 75 points |

**Contract gate (all tasks):** Every task requires a written contract that specifies inputs, processing, outputs, success conditions, and a test checklist. A weak contract means weak work; we will flag it as not ready for integration. Tasks 2 and 3 each award 20 bonus points for contract quality.

---

# Task 1: Fix the Contribute Page

**Track:** Article Finder
**What's wrong:** The contribute page accepts PDFs but does nothing with them — no classification, no storage, no feedback to the user.
**Your job:** Repair it so submitted papers get classified, stored in the right place, and reported back to the user.

---

## What This Assignment Teaches

You will use AI to fix a broken page. The point, though, is not the fix — the AI will write the code. The point is the three skills around the AI:

- Can you **diagnose** what is broken by asking your AI the right questions?
- Can you **specify** the fix precisely enough that the AI builds the right thing?
- Can you **verify** that the fix actually works — and catch the silent failures the AI hides from you?

---

## Setup: Clone the Repositories

You need four repositories. All live at [github.com/dkirsh](https://github.com/dkirsh):

```bash
# 1. The Knowledge Atlas site (contains the contribute page you'll fix)
git clone https://github.com/dkirsh/Knowledge_Atlas.git

# 2. The Article Finder pipeline (the discovery half of the system)
git clone https://github.com/dkirsh/Article_Finder.git

# 3. The Article Eater extraction engine (the processing half)
git clone https://github.com/dkirsh/Article_Eater.git

# 4. The shared classifier module (the ID function you'll wire in)
git clone https://github.com/dkirsh/atlas_shared.git
cd atlas_shared && pip install -e . && cd ..
```

Confirm `atlas_shared` installed cleanly:
```bash
python3 -c "from atlas_shared.classifier_system import AdaptiveClassifierSubsystem; print('OK')"
```

---

## Phase 1: Diagnose — What's Broken?

Before you can connect two programs, you have to understand both. This phase walks you through each one separately, then asks you to name the gap between them.

### 1A. Ask your AI to explain the contribute page

Open `Knowledge_Atlas/ka_contribute_public.html`. Hand the full source to your AI and ask:

> *"Walk me through exactly what happens when a user drops a PDF and clicks 'Send suggestion.' For each step, tell me: what function runs, what data is created, and where it goes. Then tell me everything that is MISSING that a working version would need."*

Then ask:

> *"Draw a box-and-arrow diagram showing the data flow. Label every missing component."*

**Your deliverable:** A boxology diagram and a short "Current State" paragraph describing what the page does and does not do.

### 1B. Ask your AI to explain the classifier

Now do the same for the classifier. Open `atlas_shared/src/atlas_shared/classifier_system.py`, give it to your AI, and ask:

> *"This is the classifier for the Knowledge Atlas. Explain two things:*
> 1. *How does it decide what TYPE of article a PDF is? (empirical, review, theoretical, etc.)*
> 2. *How does it decide what TOPIC a paper belongs to? (daylight + cognition, ceiling height + creativity, etc.)*
>
> *For each, tell me the class name, the method, and what data it looks at. Then draw a box-and-arrow diagram showing what happens inside `classify()`."*

**Your deliverable:** A boxology diagram of the classifier's internal steps.

### 1C. Name the gap between them

You now have two diagrams: one of what the contribute page does, one of what the classifier does. The gap between them is your assignment.

> *Ask your AI: "Given these two programs, what would I need to build to connect them? Be specific — what endpoint, what data transformations, what storage?"*

> *Also ask: "Are there any existing files in the Knowledge Atlas repo that already handle article submission? Search for files with 'article' or 'submit' in their names."*

This second question is critical. The repo already contains partial infrastructure, and your AI should find it. Make the AI tell you what is already built so you do not redo it.

**Your deliverable:** A one-paragraph gap statement of the form: "The contribute page currently does X. The classifier can do Y. The existing backend already does Z. To finish the integration, we need W."

---

## Phase 2: Spec — Write the Contract

A contract is the spec you write before any code is written. It tells the AI — and the grader — what "done" means. Write a contract called the **Classifier Integration Contract** that nails down:

- **Inputs:** What the user provides (PDF, citation, or both)
- **Processing:** What the backend does with it (build the evidence object, call the classifier)
- **Outputs on the page:** For each submitted paper, the user sees in a results section:
  - The verdict — **accepted**, **edge case**, or **rejected**
  - The article type
  - The topic(s) it matches
  - The classifier's confidence score
- **Storage rules:**
  - Accepted papers — store both the PDF and a database entry
  - Edge-case papers — store, but flag as edge cases
  - Rejected papers — show in the results panel but do NOT store
- **Success conditions:** At least three specific test cases with expected outcomes

### Check for duplicates before you store

Do not let the page store a paper that is already in the corpus. We give you a foolproof probe that works even on hard-to-read PDFs:

```bash
python3 /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/scripts/course_scaffolding.py \
  probe-collection-pdf --pdf-path /absolute/path/to/file.pdf
```

**How to read the result:**
- `sha256_exact` or `doi_exact` → **The file is already in the corpus. Do not re-ingest it.**
- `title_fuzzy` or `page_text_match` → Possible duplicate. Inspect by hand before deciding.
- No match → Safe to store as a new paper.

If you are calling this from inside Article Finder code rather than from the shell, use the function `probe_pdf_against_article_eater(...)` in `ae_waiting_room_probe.py`.

Your contract's storage rules must include this check. A submission flow that stores duplicates is a bug.

### Ask your AI about storage layout

You also need to know where the PDFs live and where the database entries live. Ask:

> *"In the Knowledge Atlas project, where are article PDFs stored? There is a lifecycle database (a SQLite database that tracks every paper's stage in the pipeline) — what tables does it have, and what should a new paper's entry look like when it first arrives? Show me the schema."*

> *"The pipeline has defined stages. What is the first stage a newly contributed paper should be at? What status should it have?"*

Do not take the AI's answer on faith. Open the database yourself and verify:

```bash
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db ".schema papers"
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db ".schema lifecycle_events"
sqlite3 Knowledge_Atlas/160sp/pipeline_lifecycle_full.db "SELECT stage_name, stage_order FROM stage_definitions ORDER BY stage_order;"
```

**Your deliverable:** The completed contract with concrete storage paths, database column values, and duplicate-check logic filled in.

---

## Phase 3: Fix — Delegate to Your AI

Now hand the work to the AI. Give it:
1. Your contract
2. The source of `ka_contribute_public.html`
3. The source of `classifier_system.py`
4. Any existing backend files your AI surfaced in Phase 1C

Ask it to build:
1. A backend endpoint that receives the form submission and runs the classifier
2. A results section on the contribute page that displays the classifier's verdict
3. Storage logic for accepted and edge-case papers

### Verification questions you must ask before you trust the code

When the AI hands you code, do not just run it. Interrogate it first. These questions catch the failures the AI will not volunteer:

> *"Show me exactly where in your code the PDF file gets saved to disk. What path does it use? What happens if that directory does not exist?"*

> *"Show me the line where you call `AdaptiveClassifierSubsystem.classify()`. What are you passing in as the `evidence_like` argument? Walk me through which fields of ClassificationEvidence get populated from the user's submission."*

> *"Show me where you write to the database. Which table? What values go in each column? What happens if the paper_id already exists?"*

> *"What happens when the classifier returns `next_action = 'need_abstract_or_keywords'`? Does your code handle that case, or does it silently ignore it?"*

> *"How do you distinguish an accepted paper from an edge case in storage? Show me the exact field or flag."*

> *"If I submit five PDFs in one session, does the results section show all five? Or does each new submission overwrite the previous one?"*

If the AI cannot answer any of these clearly, the fix is incomplete. Push back.

**Your deliverable:** The working code, plus a log of which verification questions surfaced problems and how you fixed each one.

---

## Phase 4: Prove — Run the Tests

A spec is worthless without execution proof. This phase produces the evidence that the system actually works.

### Prepare test papers

Get at least four PDFs:
1. A known on-topic empirical paper (one already in the Atlas works well)
2. A clearly off-topic paper (a machine-learning paper, for example)
3. An edge case (an architectural-theory paper with no empirical data)
4. A citation-only submission (no PDF attached)

### Run each test and record the result

| Test | Input | Expected verdict | Actual verdict | Expected type | Actual type | Stored? | DB entry? | PASS? |
|------|-------|-----------------|----------------|---------------|-------------|---------|-----------|-------|
| 1 | On-topic PDF | accept | | empirical | | yes | yes | |
| 2 | Off-topic PDF | reject | | — | | no | no | |
| 3 | Edge-case PDF | edge_case | | theoretical | | yes (flagged) | yes | |
| 4 | Citation only | varies | | varies | | — | — | |

### Verify storage

For every paper that should be stored, check both the file system and the database:

```bash
# Does the PDF file exist?
ls -la <expected_path>

# Does the database entry exist?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT paper_id, article_type, current_stage, current_status FROM papers WHERE paper_id='<id>';"

# Is there a lifecycle event?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT stage_name, status, agent FROM lifecycle_events WHERE paper_id='<id>';"

# Is the edge case distinguishable from the accepted paper?
sqlite3 pipeline_lifecycle_full.db \
  "SELECT paper_id, current_status FROM papers ORDER BY created_at DESC LIMIT 5;"
```

### When a test fails — diagnose where the bug lives

For each failure, decide: **is the spec wrong, or is the AI's implementation wrong?**

- If the classifier returns the wrong verdict, the spec may be right but the constitution data may not yet cover the topic. That is a classifier issue, not your bug.
- If the classifier returns the right verdict but the page does not show it, the AI's code has a rendering bug. That IS your bug.
- If the PDF lands on disk but the database entry never appears, the AI's code has a storage bug. That IS your bug.

**Your deliverable:** The completed validation matrix, plus a diagnosis note for any failure that explains whether it was a spec bug or an implementation bug.

---

## What You Submit

| Item | Description and Format |
|------|-----------|
| **Boxology diagrams** (Phase 1) | Two diagrams: the contribute page data flow, and the classifier's internal steps |
| **Gap statement** (Phase 1) | One paragraph: what exists, what the classifier does, what is missing |
| **Classifier Integration Contract** (Phase 2) | Your spec with inputs, outputs, storage, and success conditions |
| **Working code** (Phase 3) | The fixed contribute page, endpoint, and storage logic |
| **Verification log** (Phase 3) | The questions you asked your AI, which ones surfaced problems, how you fixed them |
| **Validation matrix** (Phase 4) | Test results for all four (or more) test cases |
| **Storage proof** (Phase 4) | Terminal output showing the PDF exists and the DB entries are correct |
| **Diagnosis notes** (Phase 4) | For any failure: spec bug or implementation bug? |

---

## Files You Must Submit

Your submission must include a **file manifest** that lists every file you changed or created with a one-line description. The instructor will diff your repo against the upstream to verify.

These are the minimum expected files; your list may include more:

| File | Change Type | What It Does |
|------|------------|-------------|
| `ka_contribute_public.html` | Modified | Form now posts to a real endpoint; results section sits below the form |
| Backend endpoint file (e.g., added to `ka_article_endpoints.py` or a new file) | Modified or New | Receives the form submission, runs the `atlas_shared` classifier, returns a JSON result |
| `data/storage/` or `data/pnu_articles/` | New files | Stored PDFs for accepted and edge-case papers |
| Database (e.g., `data/ka_auth.db` or `pipeline_lifecycle_full.db`) | Modified | New rows for submitted papers |

**How to generate your manifest:**
```bash
cd Knowledge_Atlas
git diff --name-only HEAD    # files you changed
git status --short           # new files
```

Include the output of both commands in your submission.

---

## Grading

| Criterion | What we check |
|-----------|--------------|
| **Diagnosis** | Your boxology diagrams are accurate; your gap statement is correct |
| **Spec quality** | Your contract is complete, specific, and testable |
| **Verification questions** | You asked probing questions that caught real problems in the AI's code |
| **Validation** | At least three of four test papers produce correct results and storage |
| **Diagnosis of failures** | You correctly identified whether each failure was a spec bug or an implementation bug |
| **File manifest** | Your manifest is complete and matches your actual changes |
---

# Task 2: Gap Targeting & Query Generation

**Track:** Article Finder
**What you build:** A gap extractor that reads the Article Eater's 166 PNU templates, finds the knowledge gaps inside them, scores those gaps by Value of Information (VOI — a measure of how much filling the gap would change the system's beliefs), and writes targeted search queries in two formats: Google AI Citation (natural language) and Google Scholar Boolean.
**Core lesson:** Before you search for anything, you have to know *what* you are looking for and *why*. VOI scoring tells you which gaps matter most. Query design decides whether you find relevant papers or noise.

---

## Setup

You should already have the four repositories from Task 1:
- `Knowledge_Atlas` — the site (with your fixed contribute page)
- `Article_Finder` — the discovery pipeline
- `Article_Eater` — the extraction engine (it holds both the gap data and the VOI functions)
- `atlas_shared` — the shared classifier (installed via `pip install -e .`)

---

## Phase 1: Understand the Gap Data and the VOI System

Before you build anything, you need to understand the raw material — what a PNU template looks like, what VOI measures, and what the corpus already contains. Skip this phase and your queries will hunt for papers we already have.

### 1A. Understand the PNU templates

The Article Eater holds 166 PNU (Plausible Neural Underpinning) templates. Each template describes a mechanism chain — how an environmental feature (say, ceiling height) produces a psychological outcome (say, creativity) through a series of neural processes. Every step in that chain has a **confidence score**. A low-confidence step is a **knowledge gap**: a place in the chain where the literature has not yet pinned down the mechanism.

Pick three templates from `Article_Eater/data/templates/` and ask your AI:

> *"These are PNU templates from the Knowledge Atlas. Walk me through one template completely: what does each step in the `mechanism_chain` represent, what does `confidence` mean for each step, and what does a low-confidence step (< 0.6) tell us about what is missing from the research corpus?"*

> *"Now look at all three templates and identify: which steps have confidence below 0.6? For each gap, tell me what specific study would fill it."*

### 1B. Understand the VOI scoring system

Value of Information is the lever you use to rank gaps. The Article Eater already supplies a `VOICalculator` for this; you will call it. Ask your AI:

> *"Read `Article_Eater/src/services/voi_search.py`. Find `VOICalculator` and its `calculate_voi()` method. What inputs does it take? What does the combined VOI score mean? When would a gap get a HIGH score vs. a LOW score?"*

**What you should learn:** A gap that sits at a hub in the belief network — high centrality, many downstream beliefs that depend on it — with confidence near 0.4 scores far higher in VOI than an isolated gap with confidence 0.45. VOI answers the question: "how much would knowing this change our predictions?"

### 1C. Know what is already in the corpus

Before you generate a single search query, find out what we already have. Searching for papers we already own wastes API credits and pollutes the funnel.

The lifecycle database tracks every PDF in the system.

**Primary source:** `pipeline_lifecycle_full.db`, table `pdf_corpus_inventory`

This table lists every known PDF and its state:
- Whether it is in `CURRENT_GOLD` (fully processed and validated)
- Whether it is admitted but not yet gold
- Whether it is staged only
- Whether it is registry-backed

**Easiest readable version:** `pdf_corpus_inventory/latest.csv`

The summary report is at `pdf_corpus_inventory/latest.md`.

Ask your AI:

> *"Read `pdf_corpus_inventory/latest.csv`. How many papers are in CURRENT_GOLD? What topics do they cover? This tells me what we already have — I should NOT generate search queries for papers that are already in the corpus."*

If you also need to catch the same paper appearing under different filenames or DOIs, use the companion table:

**Dedupe source:** `pipeline_lifecycle_full.db`, table `pdf_identity_inventory`
**CSV:** `pdf_identity_inventory/latest.csv`

### 1D. Understand the two query types

You will write queries in two formats, and they answer different questions. Read `160sp/ka_google_search_guide.html` for the full tutorial, then ask your AI:

> *"Explain the difference between a Google AI Citation query and a Google Scholar Boolean query. When would I use each? What makes one better than the other for finding specific mechanism-level evidence?"*

**Google AI Citation** (natural language — what you type into Google):
```
What neuroimaging evidence shows that exposure to natural versus urban
environments reduces amygdala reactivity, and does this explain the
stress-buffering effect attributed to Stress Recovery Theory?
```

**Google Scholar Boolean** (structured — what SerpAPI sends to Google Scholar):
```
("amygdala" OR "amygdala reactivity") AND ("natural environment" OR
"nature exposure") AND ("stress" OR "cortisol") AND ("fMRI" OR
"neuroimaging") -review
```

The differences in plain terms:
- **AI Citation** uses full sentences with theory names and mechanism descriptions. Google's AI handles synonyms and intent for you.
- **Boolean** uses exact keywords joined by AND/OR with quotes around phrases. Add `-review` to exclude review articles when you want primary research. Use `intitle:` to require that a term appear in the title.

### 1E. Get a boxology diagram of the full pipeline

> *"Draw a box-and-arrow diagram of this complete pipeline (Tasks 2 and 3 combined):*
> 1. *Read PNU templates → extract gaps with confidence < 0.5*
> 2. *Score gaps using VOICalculator → sort by priority*
> 3. *Generate search queries (AI Citation + Boolean)*
> 4. *Execute searches via SerpAPI → get titles, snippets, DOIs*
> 5. *Collect full abstracts via Semantic Scholar / CrossRef / PubMed / OpenAlex*
> 6. *Triage abstracts through classifier + VOI scoring*
> 7. *Classify papers: ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT*
> 8. *Display PRISMA funnel on dashboard"*

**Your deliverable:** The boxology diagram, plus a list of five specific gaps with their confidence scores.

---

## Phase 2: Build the Gap Extractor

The gap extractor turns 166 templates into a ranked, machine-readable list of knowledge gaps. It is the input to everything downstream.

### 2A. Write YOUR OWN contract

> **Contract objective:** "I want a program that reads PNU template JSON files and tells me which knowledge gaps are most worth searching for."
> **Contract is with:** The `VOICalculator` in `Article_Eater/src/services/voi_search.py` and the PNU templates in `Article_Eater/data/templates/`.
> **Prompt hint:** *"I need to write a contract for a gap extraction program. The program reads PNU template JSON files, walks their mechanism_chain, and uses VOICalculator.calculate_voi() to score each gap. Help me write the Inputs, Processing, Outputs, and Success Conditions sections."*

Write the contract yourself before you ask any AI to build anything. This is the most important habit in the course: **if you cannot specify what you want, you cannot verify what you got.**

Your contract must have these four sections:

1. **Inputs** — Which files does the program read? In what format?
2. **Processing** — What does the program do, step by step?
3. **Outputs** — What does the program produce? Which fields, in what format?
4. **Success conditions** — How will you know it worked? Be specific. "It works" is not a success condition. "Extracts at least 10 gaps across 166 templates, each with template_id, step_number, confidence < 0.6, and gap_type" IS a success condition.

**Minimum bar** — your contract must cover at least these:
- Reads PNU template JSON files and walks `mechanism_chain`
- Extracts steps whose confidence falls below a threshold you set
- Scores each gap with `VOICalculator.calculate_voi()`
- Writes structured JSON with gap_type, voi_score, and what is missing

### 2B. Write your tests BEFORE you build

A test is a sentence about what the program must do, written before the program exists. Ask your AI:

> *"Given my contract, what are 5 things that could go wrong? For each, write a test I can run to check. For example: 'What if a template has no mechanism_chain field?'"*

Write your tests as a checklist:
- [ ] Handles templates with no low-confidence steps (skips them, does not crash)
- [ ] VOI scores fall between 0 and 1
- [ ] Output JSON is valid and parseable
- [ ] At least 10 gaps found (if fewer, is the threshold wrong?)
- [ ] Gaps sorted by VOI, highest first

### 2C. Delegate to your AI, then validate

Hand the AI your contract and ask it to build a Python script. Then run your tests and interrogate the result:

> *"Show me how you read the mechanism_chain from a template. Which field has the confidence? What threshold do you use?"*

> *"Show me the VOI scores for 3 gaps. Why does one score higher than another?"*

> *"Run the script on 3 templates. Does the output match my contract's output spec? Show me the JSON."*

---

## Phase 3: Generate Search Queries

A ranked gap list is useless without queries to chase the gaps. This phase turns each gap into a matched pair of search queries — one natural-language and one Boolean — ready for Task 3 to execute.

### 3A. Write YOUR OWN query-generator contract

> **Contract objective:** "I want a program that takes my ranked gap list and generates search queries I can use to find papers that fill those gaps."
> **Contract is with:** The `QueryGenerator` in `Article_Eater/src/services/voi_search.py` and the patterns in `ka_google_search_guide.html`.
> **Prompt hint:** *"I need to write a contract for a query generator. It takes a JSON list of knowledge gaps (with VOI scores) and produces two search queries per gap: a Google AI Citation natural-language query and a Google Scholar Boolean query. Help me write the contract."*

Same discipline as Phase 2: **you** write the contract. Cover:
1. **Inputs** — the gap list from Phase 2
2. **Processing** — how queries are generated (refer to `ka_google_search_guide.html`)
3. **Outputs** — what fields each gap carries (both query types plus a gap summary)
4. **Success conditions** — at minimum:
   - At least 10 gaps carry both an AI Citation and a Boolean query
   - AI Citation queries are full sentences that follow the 5-component pattern
   - Boolean queries use `"exact phrases"`, `AND`, `OR`, and `-review`
   - At least three queries have been tested manually in Google and produce relevant first-page results

### 3B. Write your validation tests

> *"What makes a bad Boolean query? Give me 3 examples of common mistakes and how to detect them automatically."*

Your validation checklist:
- [ ] No Boolean query is a bare comma-separated word list (it must contain AND/OR)
- [ ] Every AI Citation query ends with `?` and runs longer than 50 characters
- [ ] Every Boolean query contains at least one `"exact phrase"`
- [ ] At least three queries return relevant results when tested in Google

### 3C. Use the query-generation prompt template

We supply a prompt template designed to produce high-quality queries. See `query_generator_skill.md` in this rubrics folder.

> *Give your AI the prompt template along with three gaps from your extractor. Ask it to generate queries. Then test one AI Citation query in Google by hand — does the first page of results contain relevant papers?*

### 3D. Verification questions

> *"Show me the Boolean query for one gap. Does it use exact-phrase quotes? Does it have OR groups for synonyms? Would Google Scholar parse it correctly?"*

> *"Show me the AI Citation query for the same gap. Does it follow the 5-component pattern? Could a researcher read it as a real research question?"*

> *"Take a gap about [specific mechanism]. Generate both query types. Now explain: which query would find a broader set of papers, and which would find more precisely targeted papers?"*

---

## Phase 4: Prove It Works

### Step 1: Run the gap extractor

```bash
python3 gap_extractor.py --templates Article_Eater/data/templates/
```

Verify:
- [ ] At least 10 gaps identified
- [ ] Gaps sorted by VOI score
- [ ] Each gap carries template_id, step number, confidence, gap_type, voi_score

### Step 2: Generate queries for the top 10 gaps

```bash
python3 query_generator.py --gaps gap_results.json
```

Verify:
- [ ] Each gap carries both an AI Citation and a Boolean query
- [ ] AI Citation queries are full sentences, not keyword lists
- [ ] Boolean queries use AND/OR/quotes properly

### Step 3: Manual spot-check

Pick three queries and paste the AI Citation version into Google. For each:

| Gap | Query (first 50 chars) | First-page relevant? | Top result title |
|-----|----------------------|---------------------|-----------------|
| 1 | | Yes / No / Partial | |
| 2 | | | |
| 3 | | | |

### Step 4: Review your query quality

> *Ask your AI: "Review these 10 queries against the patterns in ka_google_search_guide.html. Which queries are strong? Which are weak? How would you improve the weak ones?"*

**Your deliverable:** Gap list, query pairs, the spot-check table, and the AI's review of query quality.

---

## What You Submit

| Item | Description and Format |
|---|---|
| **Gap analysis** (Phase 1) | Boxology diagram plus five gaps with VOI scores |
| **Gap extractor** (Phase 2) | Working script plus contract |
| **Query pairs** (Phase 3) | Ten or more gaps with AI Citation + Boolean queries |
| **Spot-check** (Phase 4) | Manual test of three queries in Google |
| **Query review** (Phase 4) | AI review of query quality |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Files You Must Change or Create

| File | Type | What It Does |
|---|---|---|
| `gap_extractor.py` | New | Reads templates, extracts gaps, scores them by VOI |
| `query_generator.py` | New | Generates AI Citation + Boolean queries per gap |
| `gap_results.json` | New | Ranked gap list with VOI scores |
| `query_results.json` | New | Query pairs for each gap |

---

## Grading (60 points)

| Criterion | Points | What we check |
|---|---|---|
| **Gap extraction** | 15 | Correctly identifies low-confidence steps from templates |
| **VOI scoring** | 10 | Gaps ranked by VOI; you can explain why one scores higher |
| **AI Citation queries** | 10 | Follow the 5-component pattern, specific enough for retrieval |
| **Boolean queries** | 10 | Proper AND/OR/quotes, not just comma-separated words |
| **Spot-check** | 5 | Three queries tested manually in Google, results reported |
| **Verification questions** | 10 | Caught real problems in the AI's implementation |

---

## A Note About Reuse

The contract → success conditions → test → validate workflow you are practicing here is not a one-off exercise. **You will reuse it directly in Task 3,** where you execute searches and triage results through a PRISMA funnel, and in every later task that touches the corpus. In particular, the PRISMA funnel becomes a recurring deliverable: any time you add papers to the corpus, you must show the funnel as proof that you did so rigorously. Treat this Task 2 contract as a template you will refine, not a throwaway.

---

## Existing Code You Should Know About

| File | What it provides |
|---|---|
| `src/services/voi_search.py` | `VOICalculator.calculate_voi()` — scores gaps |
| `src/services/voi_search.py` | `QueryGenerator.generate_queries()` — baseline query generation |
| `src/services/voi_search.py` | `CrossFieldVocabulary.expand_query()` — cross-discipline synonyms |
| `pipeline_lifecycle_full.db` | Table `pdf_corpus_inventory` — every PDF and its state (CURRENT_GOLD, staged, etc.) |
| `pdf_corpus_inventory/latest.csv` | Readable export of the corpus inventory — check what you already have |
| `pdf_identity_inventory/latest.csv` | Dedupe info — catches the same paper under different filenames |
| `course_scaffolding.py probe-collection-pdf` | Foolproof duplicate check — run on any PDF to see if it is already in the corpus |
| `ae_waiting_room_probe.py` | `probe_pdf_against_article_eater()` — the same check, callable from Python |
| `build_pdf_corpus_inventory_surface.py` | Builds the inventory surface from the lifecycle DB |
| `refresh_v7_state_surfaces.py` | Regenerates all state surfaces (run this to get fresh data) |
| `160sp/ka_google_search_guide.html` | Full tutorial on writing AI Citation queries |
| `query_generator_skill.md` | Prompt template for generating queries from gaps |
---

# Task 3: Search Execution & Abstract-First Triage

**Track:** Article Finder
**Prerequisite:** Task 2 (you need your ranked gap list and query pairs)
**What you build:** Run your search queries through SerpAPI (which scrapes Google Scholar), collect each paper's abstract through a fallback chain of free academic APIs, decide at the abstract level whether each paper is worth keeping, and report the whole funnel on a PRISMA-style dashboard.
**Core lesson:** Never download a PDF to decide whether it is relevant. Triage at the cheapest level — abstracts — using free APIs. Then prove the pipeline works with real PRISMA funnel numbers.

---

## What PRISMA Is and Why You Are Building One

PRISMA (**Preferred Reporting Items for Systematic Reviews and Meta-Analyses**) is the gold-standard reporting checklist for systematic literature searches. It forces you to document your funnel transparently — every paper that came in, every paper that fell out, and the reason for each removal:

```
Records identified through database searching        (n = ?)
    ↓
Duplicates removed                                    (n = ?)
    ↓
Records screened by title + abstract                  (n = ?)  →  Excluded (n = ?)
    ↓
Full-text articles assessed for eligibility           (n = ?)  →  Excluded with reasons (n = ?)
    ↓
Studies included in final synthesis                   (n = ?)
```

Your dashboard must show these numbers. They are the proof that your pipeline works.

---

## Setup

### Get your SerpAPI key

1. Go to [serpapi.com](https://serpapi.com) and sign up (free plan).
2. The free plan gives you **250 searches per month** for non-commercial use.
3. After email and phone verification, copy your API key from the dashboard.
4. Store it as an environment variable: `export SERPAPI_KEY=your_key_here`

> **Budget your searches.** At 250 per month, you have enough for roughly 10–15 gaps × 2 queries each, plus retries. Do not waste credits on test queries — debug your Boolean syntax in Google Scholar manually first.

### Verify your Task 2 outputs

You need these files from Task 2:
- `gap_results.json` — ranked gaps with VOI scores
- `query_results.json` — AI Citation + Boolean query pairs per gap

---

## Phase 1: Understand the Search & Triage Architecture

Four pieces have to fit together: SerpAPI to find papers, an abstract fallback chain to enrich them, the triage logic to classify them, and a deduplication check to skip what we already have. This phase walks you through each piece before you start building.

### 1A. Understand SerpAPI

SerpAPI scrapes Google Scholar and returns the results as structured JSON. Ask your AI:

> *"Read the SerpAPI Google Scholar documentation. What fields does it return per result? Does it return full abstracts? What about DOIs?"*

**What you should learn:** Each SerpAPI result gives you:
- `title`, `link`, `snippet` (a 2–3-sentence fragment, NOT the full abstract)
- `publication_info` (authors, venue, year)
- `inline_links.cited_by.total` (citation count)
- Sometimes a `resource.link` (a direct PDF link)
- **It does NOT reliably return DOIs or full abstracts**

So SerpAPI gets you only halfway. You then need a second step that looks each paper up by title or DOI to fetch the full abstract.

### 1B. Understand the abstract fallback chain

The Article Eater ships with working API clients for the major free abstract sources. When SerpAPI hands you a title but no abstract, you try each source in order:

```
SerpAPI result (title + snippet + maybe DOI)
  ↓ extract DOI from link if possible
  1. Semantic Scholar (fetch_by_doi or search by title) → abstract?
  2. CrossRef (fetch by DOI) → abstract?
  3. PubMed (search by title) → abstract?
  4. OpenAlex (api.openalex.org/works/doi:XXX) → abstract?
  5. If ALL fail → tag: MISSING_ABSTRACT
```

Ask your AI:

> *"Read `Article_Eater/src/services/paper_fetcher.py`. Find `SemanticScholarClient`, `CrossRefClient`, and `PubMedClient`. Each has a `search()` method and a `fetch()` or `fetch_by_doi()` method. Show me how I would: (1) take a title from SerpAPI, (2) search Semantic Scholar for it, (3) get the abstract from the result."*

### 1C. Understand the triage logic

Once you have abstracts, you classify each paper into one of five buckets:

| Decision | Criteria | What happens |
|---|---|---|
| **ACCEPT** | On-topic (per the classifier) AND voi_score ≥ 0.5 | Stored in lifecycle DB |
| **EDGE_CASE** | On-topic but voi_score < 0.5, OR a borderline topic match | Stored separately and flagged |
| **REJECT** | Off-topic per the classifier | Logged but not stored |
| **MISSING_ABSTRACT** | No abstract found from any source | Stored with a flag, not triaged |
| **DUPLICATE** | Already in `pdf_corpus_inventory` | Counted in the PRISMA funnel, not re-triaged |

Ask your AI:

> *"Read `Article_Eater/src/cmr/voi_scoring.py`. Find `score_voi()`. What does it score — the abstract text? The finding type? How does it decide between high (0.8+), medium (0.5–0.8), and low (< 0.5)?"*

### 1D. Know what is already in the corpus (deduplication)

Before you triage a paper, check whether it is already in the corpus. You met this probe in Task 1; here it does the same job for a different reason. In Task 1 you used it to stop the contribute page from re-storing a duplicate. In Task 3 you use it to mark search hits as `DUPLICATE` so they show up in the right slot of the PRISMA funnel rather than getting re-processed.

The lifecycle database tracks every PDF in the system.

**Primary source:** `pipeline_lifecycle_full.db`, table `pdf_corpus_inventory`
**Easiest readable version:** `pdf_corpus_inventory/latest.csv`

This table tells you whether a paper sits in `CURRENT_GOLD` (already processed), is admitted, or is staged. If a search result matches a paper already in the inventory, mark it `DUPLICATE` in your PRISMA funnel — it counts as "identified" but is removed at the deduplication stage.

For matching by DOI or title, use the companion table:

**Dedupe source:** `pipeline_lifecycle_full.db`, table `pdf_identity_inventory`
**CSV:** `pdf_identity_inventory/latest.csv`

### Foolproof duplicate check (use this)

If you have a PDF in hand and want to know whether it is already anywhere in the pipeline or corpus, run the probe tool — the same one you used in Task 1:

```bash
python3 /Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/scripts/course_scaffolding.py \
  probe-collection-pdf --pdf-path /absolute/path/to/file.pdf
```

**How to read the result:**
- `sha256_exact` or `doi_exact` → **Existing duplicate. Do not re-ingest.**
- `title_fuzzy` or `page_text_match` → Possible duplicate. Inspect by hand before deciding.
- No match → New paper, safe to triage and store.

If you are calling this from inside Article Finder code rather than from the shell, use `probe_pdf_against_article_eater(...)` in `ae_waiting_room_probe.py`. The test that proves this works is `test_cataloger_skips_article_eater_duplicate_before_db_insert` in `test_import.py`.

To refresh the inventory tables before you start:
```bash
python refresh_v7_state_surfaces.py
```

---

## Phase 2: Build the Search Runner

The search runner is the first executable stage of the Task 3 pipeline. It takes the query pairs from Task 2 and turns them into raw SerpAPI results.

### 2A. Write YOUR OWN search-runner contract

> **Contract objective:** "I want a program that takes my search queries and runs them against Google Scholar via SerpAPI, collecting structured results."
> **Contract is with:** The SerpAPI `google_scholar` engine and your query pairs from Task 2.
> **Prompt hint:** *"I need a contract for a search runner that sends Boolean queries to SerpAPI's Google Scholar endpoint, extracts DOIs from result URLs, de-duplicates by title, and records null results. Help me write Inputs, Processing, Outputs, and Success Conditions."*

Same discipline as Task 2: **you** write the contract, with Inputs, Processing, Outputs, and Success Conditions.

**Minimum bar** your contract must cover:
- Takes the query pairs from Task 2 as input
- Sends Boolean queries to SerpAPI's `google_scholar` engine
- Extracts a DOI from each result URL where possible
- De-duplicates by title
- Records null results (gap searched, zero papers found)
- Tracks API credit usage

### 2B. Write your tests BEFORE you build

Your test checklist:
- [ ] SerpAPI call uses `engine: google_scholar` (not regular Google)
- [ ] Each search costs exactly one credit (verify in the SerpAPI dashboard)
- [ ] Total searches stay under 250
- [ ] Zero-result searches are recorded, not skipped
- [ ] Output JSON is valid and parseable
- [ ] DOI extraction regex works on three sample URLs

### 2C. Build and validate

Ask your AI to build it. The SerpAPI call should look like this:
```python
import serpapi
params = {
    "engine": "google_scholar",
    "q": your_boolean_query,
    "api_key": os.environ["SERPAPI_KEY"],
    "num": 10
}
results = serpapi.search(params)
```

Then run your tests and interrogate the result:

> *"Show me the exact SerpAPI call. What engine are you using? What parameters?"*

> *"How many API credits does each search cost? How many searches will my pipeline run total? Will I stay under 250?"*

---

## Phase 3: Collect Abstracts

SerpAPI hands you titles and snippets. To triage, you need full abstracts. This phase walks each result through the fallback chain until a real abstract appears — or until every source comes up empty and you tag the paper MISSING_ABSTRACT.

### 3A. Write YOUR OWN abstract-collector contract

> **Contract objective:** "I want a program that takes SerpAPI results (which have snippets, not abstracts) and finds the full abstract for each paper from free academic APIs."
> **Contract is with:** The `SemanticScholarClient`, `CrossRefClient`, `PubMedClient` in `Article_Eater/src/services/paper_fetcher.py`, and the OpenAlex API.
> **Prompt hint:** *"I need a contract for an abstract collector. It takes search results with DOIs and tries to find full abstracts from Semantic Scholar, CrossRef, PubMed, and OpenAlex in fallback order. Papers with no abstract from any source get tagged MISSING_ABSTRACT. Help me write the contract."*

**Minimum bar** your contract must cover:
- Takes SerpAPI results as input (with DOIs where available)
- Tries multiple abstract sources in fallback order (S2 → CrossRef → PubMed → OpenAlex)
- For papers without DOIs, falls back to title-based search
- Tags papers with no abstract as `MISSING_ABSTRACT` (does not silently drop them)
- Records which source supplied the abstract
- Respects rate limits (Semantic Scholar: ≤ 20 req/min without an API key)

**Success conditions you must define:**
- What abstract hit rate is acceptable? (Aim for ≥ 70 percent on papers with DOIs.)
- What counts as a "found" abstract versus a snippet?
- How do you handle ambiguous title matches?

### 3B. Write your tests BEFORE you build

- [ ] Fallback chain actually tries multiple sources, not just Semantic Scholar
- [ ] Rate-limiting delays are present (look for `time.sleep` or `_RateLimiter`)
- [ ] MISSING_ABSTRACT count is tracked and reported
- [ ] Each paper's `abstract_source` field is set correctly
- [ ] Output includes `study_type` from `estimate_study_type()`

### 3C. Build and validate

> *"Show me the fallback chain. If Semantic Scholar has no abstract for a DOI, what is the next source you try?"*

> *"How do you handle rate limits? Do you add delays between API calls?"*

> *"For papers without DOIs, how do you search by title? What happens if the title match is ambiguous?"*

---

## Phase 4: Triage Abstracts

With abstracts in hand, the pipeline can finally make decisions. Triage is the choke point: it converts a long list of candidate papers into a short list of papers worth downloading.

### 4A. Write YOUR OWN triage contract

> **Contract objective:** "I want a program that reads each paper's abstract and decides: is this paper worth downloading?"
> **Contract is with:** The `atlas_shared` classifier (from Task 1) and `score_voi()` from `Article_Eater/src/cmr/voi_scoring.py`.
> **Prompt hint:** *"I need a contract for an abstract triage module. It runs each abstract through the atlas_shared topic classifier, then scores it with score_voi(). Output is a 4-way classification: ACCEPT, EDGE_CASE, REJECT, or MISSING_ABSTRACT, each with a human-readable reason. Help me write the contract."*

**Minimum bar** your contract must cover:
- Runs each abstract through the `atlas_shared` classifier (topic matching)
- Scores each abstract with `score_voi()` from `cmr/voi_scoring.py`
- Produces a four-way classification: ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT
- Attaches a human-readable `triage_reason` to every decision
- Stores ACCEPT papers in the lifecycle DB; stores EDGE_CASE separately

**Success conditions you must define:**
- What is the minimum number of papers triaged?
- What classifier confidence threshold separates on-topic from off-topic?
- What VOI threshold separates ACCEPT from EDGE_CASE?

### 4B. Write your tests BEFORE you build

- [ ] Every triaged paper carries a `triage_decision` field
- [ ] Every triaged paper carries a `triage_reason` (never empty)
- [ ] ACCEPT papers appear in the database
- [ ] EDGE_CASE papers are stored but flagged
- [ ] REJECT papers are logged, not silently dropped
- [ ] MISSING_ABSTRACT papers skip triage rather than getting scored as REJECT

---

## Phase 5: Build the PRISMA Dashboard

The dashboard is the public face of your pipeline. It collects every count along the funnel and shows them in one place, so a reader can see — at a glance — how many papers entered, how many fell out at each stage, and why.

### 5A. Dashboard requirements

Build a web page (`ka_topic_proposer.html` or similar) that shows:

1. **Gap Summary** — how many gaps were identified, top five by VOI
2. **Search Summary** — how many queries ran, how many results came back
3. **Abstract Collection** — how many abstracts were found vs. tagged MISSING_ABSTRACT
4. **Triage Results** — ACCEPT / EDGE_CASE / REJECT counts
5. **PRISMA Funnel** — the complete funnel with real numbers
6. **Null Results** — gaps for which no papers were found

Data must persist after a page refresh (use a JSON file, localStorage, or an API endpoint).

### 5B. The PRISMA funnel table (required deliverable)

| Funnel Stage | Count |
|---|---|
| Gaps targeted (from Task 2) | |
| Queries executed (SerpAPI) | |
| Records returned | |
| Duplicates removed | |
| Abstracts collected | |
| MISSING_ABSTRACT (no abstract found) | |
| Screened by classifier | |
| → ACCEPT (on-topic, high VOI) | |
| → EDGE_CASE (borderline) | |
| → REJECT (off-topic) | |

---

## Phase 6: Prove It Works

### Step 1: Run the full pipeline

```bash
python3 search_runner.py --queries query_results.json
python3 abstract_collector.py --results search_results.json
python3 abstract_triage.py --papers papers_with_abstracts.json
```

### Step 2: Trace one paper end-to-end

Pick ONE paper that made it through the entire pipeline and trace its journey:

```
Gap source: Template T__ step __ (confidence: 0.__, VOI: 0.__)
  → Boolean query: "_______________"
  → SerpAPI result #__ of __
  → Title: [paper title]
  → DOI: [if found]
  → Abstract source: Semantic Scholar / CrossRef / PubMed / OpenAlex
  → Abstract: [first 100 chars...]
  → Classifier: topic=Q__, confidence=0.__
  → VOI score: 0.__, bucket=high/medium/low
  → Triage: ACCEPT / EDGE_CASE
  → Stored at: [DB entry or file path]
```

### Step 3: Report null results

For high-VOI gaps that returned zero search results, write up each one:

```
Gap: Template T__ step __ (VOI: 0.__)
  Description: _______________
  Queries tried: [list]
  Result: NO PAPERS FOUND
  Implication: This gap may be genuinely unfilled in the literature.
```

### Step 4: Report MISSING_ABSTRACT papers

```
Papers with MISSING_ABSTRACT: N out of M total
  Example: [title] — no abstract from any source
  These papers cannot be triaged but are stored for future manual review.
```

---

## What You Submit

| Item | Description and Format |
|---|---|
| **Search results** | Raw SerpAPI results as JSON |
| **Abstract collection** | Papers with abstracts plus source attribution |
| **Triage results** | ACCEPT / EDGE_CASE / REJECT / MISSING_ABSTRACT decisions |
| **PRISMA funnel** | Completed funnel table with real numbers |
| **Dashboard** | Working web page showing pipeline results |
| **End-to-end trace** | One paper traced from gap → SerpAPI → abstract → triage → store |
| **Null result report** | Gaps for which no papers were found |
| **File manifest** | `git diff --name-only HEAD` and `git status --short` |

---

## Files You Must Change or Create

| File | Type | What It Does |
|---|---|---|
| `search_runner.py` | New | Calls SerpAPI with Boolean queries |
| `abstract_collector.py` | New | Collects abstracts via the fallback chain |
| `abstract_triage.py` | New | Runs the classifier + VOI on abstracts |
| `search_results.json` | New | Raw SerpAPI results |
| `triage_results.json` | New | Triage decisions with reasons |
| `ka_topic_proposer.html` | New | PRISMA dashboard |
| Database | Modified | New entries for ACCEPT papers |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **SerpAPI integration** | 10 | Successfully queried Google Scholar, got results back |
| **Abstract collection** | 15 | Fallback chain works; ≥ 70 percent abstract hit rate on DOI papers |
| **Abstract triage** | 15 | Classifier + VOI yield defensible ACCEPT/EDGE_CASE/REJECT decisions |
| **PRISMA funnel** | 10 | Dashboard shows real numbers at every stage |
| **End-to-end trace** | 10 | One paper fully traced through the pipeline |
| **Null results + MISSING_ABSTRACT** | 5 | Documented, not treated as failures |
| **Verification questions** | 10 | Caught real problems in the AI's implementation |

---

## A Note About Reuse

The PRISMA funnel you just built is not a one-off deliverable. **Every future task that adds papers to the corpus will require the same funnel,** updated with new numbers. Design your dashboard with that in mind — when the next task runs new searches, the same page should refresh with new counts rather than be rebuilt from scratch. Treat the PRISMA dashboard as durable infrastructure for the rest of the course, not a deliverable you ship and forget.

---

## Existing Code You Should Know About

| File | What it provides |
|---|---|
| `src/services/paper_fetcher.py` | `SemanticScholarClient.search()` + `fetch_by_doi()` |
| `src/services/paper_fetcher.py` | `CrossRefClient.search()` + `fetch()` |
| `src/services/paper_fetcher.py` | `PubMedClient.search()` + `fetch()` |
| `src/services/paper_fetcher.py` | `PaperFetcher.search()` — unified multi-source search |
| `src/services/paper_fetcher.py` | `estimate_study_type()` — auto-derives study type from abstract |
| `src/services/paper_fetcher.py` | `UnpaywallClient` — checks open-access availability |
| `src/cmr/voi_scoring.py` | `score_voi()` — scores findings by information value |
| `src/services/discovery_funnel.py` | `classify_closure()` — FULL/PARTIAL/NONE/NEGATIVE |
| `pipeline_lifecycle_full.db` | Table `pdf_corpus_inventory` — every PDF and its state |
| `pdf_corpus_inventory/latest.csv` | Readable export — check what is already in the corpus |
| `pdf_identity_inventory/latest.csv` | Dedupe info — catches the same paper under different filenames |
| `course_scaffolding.py probe-collection-pdf` | Foolproof duplicate check — run on any PDF to see if it is already in the corpus |
| `ae_waiting_room_probe.py` | `probe_pdf_against_article_eater()` — the same check, callable from Python |
| `refresh_v7_state_surfaces.py` | Regenerates all state surfaces (run before starting) |
| `atlas_shared` | Topic classifier (from Task 1) |


---
---
---


=== TRACK 3 ===
# Track 3: VR Studio — All Tasks

**Track overview:** You will build a pipeline that lets neuroarchitecture researchers modify 3D interior environments via natural language. Starting from openly-licensed 3D models (or generating them from photographs via World Labs Marble), you'll curate a library of VR-ready rooms, build a real-time viewer with slider controls for 8 environmental manipulation classes, and wire up an AI front-end that converts instructions like "make this a cozy library with 4m ceilings and wood on the north wall" into instant 3D scene modifications.

**Three tasks, one pipeline:**

| Task | What you build | Points |
|---|---|---|
| Task 1 | Collect & catalog ≥ 20 VR-ready 3D models with per-wall mesh annotations | 75 points |
| Task 2 | VR conversion & manual factor testing — real-time sliders, 10 models × 8 factors, path-traced lighting | 75 points |
| Task 3 | AI front-end — natural language → validated parametric scene modification | 75 points |

**Contract gate (all tasks):** Every task requires written contracts with inputs, processing, outputs, success conditions, and test checklists.

**Speed:** Three.js scene modifications execute at **120+ fps**. Path-traced lighting converges in ~2 seconds on any modern laptop.

---

# Track 3 · Task 1: Collect & Catalog VR-Ready 3D Interior Models

**Track:** VR Studio  
**Points:** 75  
**What you'll have when you're done:** A curated library of ≥ 20 VR-ready 3D interior models in glTF/GLB format, each evaluated against 8 manipulation classes, cataloged in a Google Sheet with viability scores, and accompanied by a mesh annotation file that maps every mesh to its semantic role (ceiling, wall_north, floor, window, etc.).

---

## The big picture

The Knowledge Atlas stores evidence that specific environmental features alter human cognition and affect. Researchers have manipulated these features experimentally:

| Manipulation Class | Registry tags | What researchers change |
|---|---|---|
| **Geometry** (ceiling height, volume, enclosure) | 46 tags | Ceiling height ≥ 3.0m vs ≤ 2.4m; room proportions; isovist area |
| **Lighting** (intensity, spectrum, direction) | 33 tags | Illuminance (lux); color temperature (2700K–6500K); daylight vs artificial |
| **Materials** (surface texture, roughness) | 13 tags | Wood vs concrete vs glass; natural material ratio; texture density |
| **Color** (hue, warmth, saturation) | 5 tags | Warm vs cool palettes; color diversity; chroma levels |
| **Biophilic elements** (plants, water, nature views) | 6 tags | Plant count; window view content (greenery vs built-up) |
| **Furniture layout** (density, arrangement) | 17 tags | Seating count; sociopetal vs sociofugal arrangement; clutter density |
| **Acoustic properties** | 5 tags | Acoustic privacy; natural sound sources |
| **Visual complexity** (detail, order, fractals) | 22 tags | Fractal dimension; symmetry; ornament density |

To test these relationships in VR, researchers need 3D room models where each factor can be **varied independently while holding others constant**. Your job is to collect models that make this possible.

---

## What makes a model "VR-ready"

Not every 3D model can be parametrically modified. These are hard constraints:

### Constraint 1: Separable Named Meshes

The ceiling must be a **separate mesh** from the walls. Each wall must be individually identifiable. This rules out:
- ❌ Photogrammetry scans (single fused mesh)
- ❌ "Baked" models (one mesh with texture atlas)
- ✅ Architectural models with separate named objects

**Test:** Open in Blender → check the Outliner. Named objects like "Ceiling", "Wall_North", "Floor" = viable. One object called "mesh_001" = not viable.

### Constraint 2: PBR Materials (not baked textures)

Models must use **PBR material slots** (base color, roughness, metalness), not a single pre-baked lightmap. This enables material swapping.

### Constraint 3: Architectural Scale

Models must be at **real-world scale** (meters). Ceiling height manipulation requires knowing the actual height. VR immersion breaks if scale is wrong.

### Constraint 4: VR-Compatible Polygon Count

For WebXR at ≥ 72 fps: < 500K polygons per scene, < 20 unique materials, textures ≤ 4096×4096.

### Constraint 5: Open License

CC0, CC-BY, CC-BY-SA. No "editorial use only" or "All Rights Reserved."

---

## Phase 1: Find model sources

> **Contract objective:** "I want a tested, documented list of 3D model sources I can use to collect VR-ready interior models."
> **Contract is with:** 3D model repositories and their APIs.
> **Prompt hint:** *"I need 5+ sources of openly-licensed architectural interior 3D models in glTF/GLB/FBX/OBJ format. For each: license, API availability, format, and whether models have separable meshes. Test one search per source."*

Write YOUR OWN contract. Include Inputs, Processing, Outputs, Success Conditions.

### Starting points

- **Sketchfab** — CC-licensed, API available, downloadable glTF, many architectural interiors
- **3D Warehouse** — SketchUp models with groups/components, export via Blender
- **BlenderKit** — Free tier, natively separable meshes
- **TurboSquid** (free section) — Check license per model
- **Poly Haven** — CC0, excellent HDRIs and some room models
- **CGTrader** (free section) — Mixed quality, check license

### Advanced source: World Labs Marble (image → 3D world)

[World Labs Marble](https://marble.worldlabs.ai/) uses spatial AI to generate explorable 3D worlds from a single photograph, text prompt, or video. Instead of downloading someone else's model, you photograph a real space and generate a 3D version. This is directly relevant to neuroarchitecture research — [Champalimaud Foundation and King's College London already use Marble to generate patient-specific VR environments for OCD exposure therapy](https://www.worldlabs.ai/case-studies/3-health-systems).

#### Step 1: Generate a world

**Option A — Web UI (easiest to start):**
Go to [marble.worldlabs.ai](https://marble.worldlabs.ai/) → click Create → upload a photo of an interior or type a text prompt → wait ~5 minutes.

**Option B — API (automatable, required for batch processing):**

```bash
# Generate a world from a text prompt
curl -X POST 'https://api.worldlabs.ai/marble/v1/worlds:generate' \
  -H 'Content-Type: application/json' \
  -H 'WLT-Api-Key: YOUR_API_KEY' \
  -d '{
    "display_name": "Clinical Office Baseline",
    "model": "marble-1.1",
    "world_prompt": {
      "type": "text",
      "text_prompt": "A clinical white office with 3m ceilings, fluorescent lighting, one window on the south wall, a desk and two chairs"
    }
  }'

# Generate a world from a photograph
curl -X POST 'https://api.worldlabs.ai/marble/v1/worlds:generate' \
  -H 'Content-Type: application/json' \
  -H 'WLT-Api-Key: YOUR_API_KEY' \
  -d '{
    "display_name": "Psychology Lab Room 204",
    "model": "marble-1.1",
    "world_prompt": {
      "type": "image",
      "image_prompt": {
        "source": "uri",
        "uri": "https://your-host.com/photo_of_room_204.jpg"
      },
      "text_prompt": "Interior of a university research lab"
    }
  }'

# Poll for completion (~5 min)
curl -X GET 'https://api.worldlabs.ai/marble/v1/operations/OPERATION_ID' \
  -H 'WLT-Api-Key: YOUR_API_KEY'
```

**Generation times:** Text/image → pano: ~30 sec. Pano → full world: ~5 min. High-quality mesh export: ~1 hour.

#### Step 2: Export the mesh

In the Marble web viewer, click Export → **High-quality mesh (GLB)**. This runs server-side for ~1 hour and produces:
- A **600K triangle mesh** with texture maps
- A **1M triangle mesh** with vertex colors
- Both in GLB format (loadable in Blender and Three.js)

> **Important:** The exported mesh is a **single fused object** — all walls, ceiling, floor are one continuous surface. You cannot select individual walls yet. That's what Step 3 fixes.

#### Step 3: Segment the fused mesh into separate architectural elements

The Marble export is a single continuous surface. To make it parametrically modifiable, you must separate it into individual objects (ceiling, walls, floor, furniture) and assign PBR materials to each. This is a core part of the assignment — **you are expected to use at least one of the AI-assisted approaches below**, not do everything by hand.

---

### Controlling Blender: Manual, AI-Assisted, and Fully Automated

There are four approaches to Blender mesh segmentation, ranging from fully manual to fully automated. The choice is yours, but you must **document which approach you used and evaluate its accuracy.**

#### Approach A — Manual segmentation in Blender (~30-45 min per model)

This is the baseline — every student should know how to do this even if they automate it later.

1. Import GLB: `File → Import → glTF 2.0`
2. Enter Edit Mode (`Tab`)
3. Select ceiling faces: `Select → Select All by Trait → Normal` (faces pointing downward)
4. Separate: `Mesh → Separate → Selection` (`P`)
5. Name the new object "Ceiling" in the Outliner
6. Repeat for floor (upward normals), each wall (by face orientation), furniture
7. Assign PBR materials to each separated object
8. Export: `File → Export → glTF 2.0`

**Effectiveness:** 100% accurate but slow. Use for your first 1-2 models to understand the geometry, then automate.

---

#### Approach B — BlenderMCP: Claude/Cursor controls Blender via MCP (recommended)

[**BlenderMCP**](https://github.com/ahujasid/blender-mcp) (20.7k ★, MIT license) connects Blender to Claude AI through the [Model Context Protocol](https://modelcontextprotocol.io/). Claude can see your Blender viewport, execute Python code, create/modify/delete objects, apply materials, and download Poly Haven assets — all through natural language conversation.

**Why this is the most powerful option:** Unlike BlenderGPT, BlenderMCP gives the LLM **viewport screenshots** so it can see what it's doing and correct errors. It also integrates with Poly Haven for HDRIs and materials, which is directly useful for our VR pipeline.

**Setup:**
1. Install `uv`: `brew install uv` (Mac) or `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows)
2. Download `addon.py` from the [repo](https://github.com/ahujasid/blender-mcp), install it in Blender: `Edit → Preferences → Add-ons → Install`
3. In Blender sidebar (`N`), find the "BlenderMCP" tab → click "Connect to Claude"
4. Configure your AI client:

**For Claude Desktop** (add to `claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    }
  }
}
```

**For Cursor** (add to `.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    }
  }
}
```

**Then tell Claude/Cursor:**
```
"I've imported a Marble-exported GLB of a room interior. It's a single 
fused mesh. I need you to:
1. Take a screenshot to see the current scene
2. Select all downward-facing faces (normal Z < -0.8) and separate them 
   as a new object called 'Ceiling'
3. Select all upward-facing faces (normal Z > 0.8) and separate them 
   as 'Floor'
4. Use face normal direction to separate remaining faces into 
   'Wall_North', 'Wall_South', 'Wall_East', 'Wall_West'
5. Assign Principled BSDF materials to each object
6. Take a final screenshot to verify"
```

**Effectiveness:** ~85-90% accurate for rectangular rooms. The LLM can see the viewport and self-correct. Irregular room shapes may need manual cleanup. Expect to iterate 2-3 prompts per model. Total time: ~10-15 min per model including verification.

**Additional capabilities relevant to T3:**
- Download Poly Haven HDRIs and materials directly (useful for Task 2 lighting)
- Generate 3D models via Hyper3D Rodin integration
- Export scene information as JSON for the AI front-end

---

#### Approach C — BlenderGPT: Natural language inside Blender (~10 min per model)

[**BlenderGPT**](https://github.com/gd3kr/BlenderGPT) (4.9k ★, MIT license) is a Blender addon that takes natural language → GPT-4 generates Blender Python (`bpy`) code → executes it directly inside Blender.

**Setup:** Download the ZIP from GitHub → `Edit → Preferences → Add-ons → Install` → paste your OpenAI API key in addon preferences. Open the sidebar (`N`) → find "GPT-4 Assistant" tab.

**Key difference from BlenderMCP:** BlenderGPT runs entirely inside Blender (no external MCP server) but has **no viewport awareness** — it can't see what it did. It writes code blindly based on your description. This means it works well when you describe geometry precisely (face normals, coordinates) but can't self-correct visual errors.

**Segmentation prompts:**
```
"Select all faces on the active mesh object whose normal Z component is 
less than -0.8. Separate the selected faces into a new object. Rename 
that new object to 'Ceiling'."
```

```
"Select all faces whose normal Z component is greater than 0.8. 
Separate into a new object called 'Floor'."
```

```
"For the remaining mesh, select faces where the absolute Y component 
of the normal exceeds 0.7 and the Y component is negative. Separate 
into 'Wall_North'. Then select faces where Y normal > 0.7 and 
separate into 'Wall_South'. Repeat for X axis: negative X normal 
→ 'Wall_West', positive X normal → 'Wall_East'."
```

```
"Assign a new Principled BSDF material to each separated object. 
Set Ceiling base color to (0.9, 0.9, 0.9), Floor to (0.4, 0.4, 0.4), 
all walls to (0.85, 0.82, 0.75). Set roughness 0.7 for all."
```

**Effectiveness:** ~80% for rectangular rooms. Without viewport feedback, errors accumulate — you'll need to visually inspect in Blender and fix manually. Total time: ~10-15 min per model.

---

#### Approach D — Headless Blender Python script (fully automated, no AI needed)

This is the fastest option for batch processing. You write the segmentation logic once as a Python script, then run it headlessly (no GUI) on every model:

```python
# segment_marble_export.py
# Run: blender --background --python segment_marble_export.py -- input.glb output.glb
import bpy, bmesh, sys, math

argv = sys.argv[sys.argv.index("--") + 1:]
input_path, output_path = argv[0], argv[1]

# Clear scene, import
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=input_path)
obj = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
bpy.context.view_layer.objects.active = obj

# Enter edit mode
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(obj.data)

# Classify faces by normal direction
def classify_face(face):
    n = face.normal
    if n.z > 0.7: return 'Floor'      # Facing up
    if n.z < -0.7: return 'Ceiling'    # Facing down
    angle = math.atan2(n.y, n.x)       # Horizontal direction
    if -0.785 < angle <= 0.785: return 'Wall_East'
    if 0.785 < angle <= 2.356: return 'Wall_North'
    if angle > 2.356 or angle <= -2.356: return 'Wall_West'
    return 'Wall_South'

# Select and separate each category
for role in ['Ceiling', 'Floor', 'Wall_North', 'Wall_South', 'Wall_East', 'Wall_West']:
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(obj.data)
    for face in bm.faces:
        if classify_face(face) == role:
            face.select = True
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.mesh.separate(type='SELECTED')
    # Rename the newly created object
    new_obj = [o for o in bpy.context.scene.objects if o.name.startswith(obj.name) and o != obj][-1]
    new_obj.name = role

bpy.ops.object.mode_set(mode='OBJECT')

# Assign PBR materials
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH': continue
    mat = bpy.data.materials.new(name=f"PBR_{obj.name}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Roughness'].default_value = 0.7
    obj.data.materials.clear()
    obj.data.materials.append(mat)

# Export
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
```

Run: `blender --background --python segment_marble_export.py -- marble_room.glb room_segmented.glb`

Batch all models: `for f in marble_exports/*.glb; do blender --background --python segment_marble_export.py -- "$f" "segmented/$(basename $f)"; done`

**Effectiveness:** ~75-80% for simple rectangular rooms. Fails on L-shaped rooms, angled walls, curved surfaces, or rooms where furniture faces look similar to wall faces. The script has no visual judgment — it's purely geometric. **You must visually inspect every output in Blender and fix misclassified faces manually.** This is the ruthless validation step.

**Advantage:** Zero cost, zero API keys, processes 20 models in under 5 minutes. The human review step is where you earn the grade.

---

### Which approach should you use?

| Approach | Stars | API cost | Viewport aware | Batch mode | Accuracy | Best for |
|---|---|---|---|---|---|---|
| **A: Manual** | — | $0 | N/A (you are the eyes) | ❌ | 100% | Learning; fixing AI errors |
| **B: BlenderMCP** | 20.7k | Claude API | ✅ Yes (screenshots) | ❌ | ~85-90% | Best single-model workflow |
| **C: BlenderGPT** | 4.9k | OpenAI API | ❌ No | ❌ | ~80% | Quick iteration in Blender |
| **D: Headless script** | — | $0 | ❌ No | ✅ Yes | ~75-80% | Batch processing 20 models |

**Recommended workflow:** Use **Approach D** (headless script) to batch-process all models, then **visually inspect each one in Blender** and use **Approach A or B** to fix errors. Document every correction — this is your ruthless validation data.

#### Marble pricing

| Plan | Worlds/month | Mesh export | Cost |
|---|---|---|---|
| **Free** | 4 | ❌ No export | $0 |
| **Standard** | 12 | ✅ Collider mesh | Check [pricing page](https://marble.worldlabs.ai/pricing) |
| **Pro** | 25 | ✅ High-quality mesh + commercial rights | Check [pricing page](https://marble.worldlabs.ai/pricing) |
| **Max** | 75 | ✅ Everything | Check [pricing page](https://marble.worldlabs.ai/pricing) |
| **API** | Pay-per-use (credits) | ✅ Via API | [API pricing](https://docs.worldlabs.ai/api/pricing) |

For this assignment, the **Free plan** (4 worlds) is enough to try the workflow. The **Standard plan** is enough for 12 Marble-generated rooms. Use Sketchfab for the remaining models.

Use Marble for at least 3 of your 20 models to demonstrate the photo → 3D → parametric pipeline.

**Deliverable:** `model_sources.json`

---

## Phase 2: Collect and evaluate ≥ 20 models

For each model, evaluate it against all 8 manipulation classes. Can you actually change the ceiling? Can you swap the wall material? Can you modify individual walls independently?

### Google Sheet columns (minimum)

| Column | What it records |
|---|---|
| `model_id` | Unique ID (e.g., `SKF_office_001`) |
| `source` / `source_url` | Where you got it |
| `license` | CC0 / CC-BY / CC-BY-SA |
| `room_type` | office / classroom / living_room / etc. |
| `format` | glTF / GLB / FBX (must convert to glTF) |
| `poly_count` | Total polygons |
| `named_meshes` | Yes/No — are architectural elements separate? |
| `pbr_materials` | Yes/No — PBR workflow? |
| `realistic_scale` | Yes/No — meters, not arbitrary? |
| `individual_walls` | Yes/No — can you select and modify each wall independently? |
| `ceiling_modifiable` | Yes/No |
| `lighting_modifiable` | Yes/No — are lights separate objects? |
| `materials_modifiable` | Yes/No |
| `windows_identifiable` | Yes/No — can you find and resize window meshes? |
| `furniture_separable` | Yes/No — is furniture separate from architecture? |
| `viability_score` | 0–8 (count of modifiable classes) |
| `resolution` | Low / Medium / High |
| `naturalness` | 1–5 (visual realism) |
| `notes` | Issues, conversion needed, what's missing |

### Minimum bar

- ≥ 20 models total
- ≥ 10 with viability score ≥ 4
- ≥ 5 different room types
- ≥ 3 different sources

---

## Phase 3: Create mesh annotation files

For each model, create a `mesh_roles.json` that maps every mesh name to its semantic role. This is what the AI front-end (Task 3) will use to know which mesh to modify.

```json
{
  "model_id": "SKF_office_001",
  "meshes": {
    "Cube.003": { "role": "ceiling", "notes": "single plane, height=3.0m" },
    "Cube.004": { "role": "wall", "wall_id": "north", "notes": "back wall" },
    "Cube.005": { "role": "wall", "wall_id": "south", "notes": "front wall with window cutout" },
    "Cube.006": { "role": "wall", "wall_id": "east" },
    "Cube.007": { "role": "wall", "wall_id": "west" },
    "Plane.001": { "role": "floor" },
    "Cube.010": { "role": "window", "parent_wall": "south", "position": "center" },
    "Cube.011": { "role": "furniture", "subtype": "desk" },
    "Cube.012": { "role": "furniture", "subtype": "chair" },
    "Lamp": { "role": "light", "light_type": "point" }
  },
  "room_dimensions": { "width_m": 6.0, "depth_m": 5.0, "height_m": 3.0 }
}
```

> **Each wall must have a `wall_id`** (north/south/east/west or left/right/back/front). This enables per-wall material and geometry changes.

---

## Phase 4: Write a ruthless validation prompt

Before declaring a model "ready," you must test it with a **ruthless prompt** — an adversarial instruction designed to break things.

### What a ruthless prompt is

A ruthless prompt is an AI instruction that systematically probes every failure mode. Instead of "does it work?", you ask "in exactly which ways does it fail?" The structure:

> *"You are a hostile QA engineer. Your job is to find every way this 3D model catalog entry could be wrong, misleading, or unusable. For model {model_id}:*
> 1. *Open the model in Blender. Count the actual meshes and compare to the mesh_roles.json. Are any missing or mislabeled?*
> 2. *Try to move the ceiling mesh up by 1 meter. Does the room still look correct? Do walls gap?*
> 3. *Try to change the north wall material to a different color. Does only that wall change, or do others change too (shared material)?*
> 4. *Check every material — is it PBR or is it a baked texture that can't be swapped?*
> 5. *Measure the room in Blender. Does it match room_dimensions in the JSON?*
> 6. *Is the model oriented correctly (Y-up or Z-up)? Does the 'north' wall actually face north?*
> *Report every discrepancy found."*

Write a ruthless validation prompt for your catalog. Run it on at least 5 models. Document what broke.

---

## What you submit

| Item | What it is |
|---|---|
| `model_sources.json` | ≥ 5 sources, ≥ 3 tested |
| Google Sheet catalog | ≥ 20 models with all columns filled |
| `models/` directory | All glTF/GLB files |
| `mesh_roles/` directory | One `mesh_roles.json` per model |
| Conversion scripts | Any Blender scripts used for format conversion |
| Ruthless validation report | Results of running adversarial prompt on ≥ 5 models |
| Contracts + tests | Written BEFORE building |
| File manifest | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 15 | Written BEFORE collecting. Specific success conditions. **(CONTRACT GATE)** |
| **Model sources** | 10 | ≥ 5 sources, ≥ 3 tested, licenses documented |
| **Model catalog** | 15 | ≥ 20 models, ≥ 10 viable, ≥ 5 room types, viability scores accurate |
| **Mesh annotations** | 15 | Per-wall IDs, roles correct, dimensions measured |
| **Ruthless validation** | 10 | Run on ≥ 5 models, failures documented, fixes applied |
| **Verification** | 10 | Spot-checked claims, caught discrepancies |

> ⛔ **Contract gate**: If your contracts and tests are missing or vague, your models will not be usable by the VR pipeline. Write real contracts with real success conditions.

---

## Existing code you should know about

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | 424 tags — 330 are continuous/ordinal and represent manipulable environmental features |
| `Article_Eater/data/templates/` | 166 PNU templates showing what IVs researchers actually manipulate (ceiling height, lighting, materials, etc.) |
| `Outcome_Contractor/contracts/oc_export/outcome_vocab.json` | 839 effect terms — the dependent variables these manipulations affect |
| `160sp/context/context_vr_production.md` | VR production context including K-ATLAS evidence model and scene specification format |
| [World Labs Marble](https://marble.worldlabs.ai/) | Photo/text → 3D world generation; [API docs](https://docs.worldlabs.ai/api); [SparkJS](https://sparkjs.dev/) for Gaussian Splat rendering |
| [BlenderMCP](https://github.com/ahujasid/blender-mcp) (20.7k ★) | Claude/Cursor → Blender via MCP; viewport-aware AI control with Poly Haven integration |
| [BlenderGPT](https://github.com/gd3kr/BlenderGPT) (4.9k ★) | Natural language → Blender Python code execution inside Blender; no viewport awareness |
| Blender CLI: `blender --background --python script.py` | Run segmentation/conversion scripts headlessly (no GUI); batch-process all models |

---

## Reuse

Your model library and mesh annotations are infrastructure. In Task 2, you'll manually test modifications in A-Frame. In Task 3, you'll build the AI front-end that uses your `mesh_roles.json` files to know which mesh to modify. Accurate annotations now save hours of debugging later.

---

# Track 3 · Task 2: VR Conversion & Manual Factor Testing

**Track:** VR Studio  
**Prerequisite:** Task 1 (your 20+ models with mesh annotations)  
**Points:** 75  
**What you'll have when you're done:** ≥ 10 models loaded in A-Frame with verified, real-time slider controls for all 8 manipulation classes, plus a factor viability matrix proving which modifications work on which models.

---

## The big picture

You cataloged 20+ 3D models and annotated their meshes. Now you need to **prove** those annotations are correct by actually loading the models into a VR-capable viewer and manually testing every modification class. This is not a demo — it's validation engineering.

### Why A-Frame (not Unity or Unreal)

| Platform | Learning curve | Verdict |
|---|---|---|
| **A-Frame** (WebXR) | HTML+JS; loads glTF natively; runs in browser; zero install | ✅ Use this |
| **Unity** | C#; 2+ week onboarding; heavy project files | ❌ Too slow for 6 weeks |
| **Unreal** | C++/Blueprint; steepest curve; massive files | ❌ Not feasible |

You already know HTML and JavaScript from Tracks 1 and 2. A-Frame wraps Three.js — a glTF loads with one HTML tag. Modifications are JavaScript property changes and execute at **120+ fps** (verified by prototype).

---

## Phase 1: Build the interactive viewer

> **Contract objective:** "I want an HTML page that loads any of my glTF models and provides real-time slider controls for each manipulation class."
> **Contract is with:** Your glTF models, your `mesh_roles.json` annotations, and the Three.js/A-Frame API.

Write YOUR OWN contract. Include Inputs, Processing, Outputs, Success Conditions.

### The viewer must support

**Real-time sliders (continuous, instant feedback):**

| Slider | What it controls | Range |
|---|---|---|
| Ceiling height | `ceiling` mesh position.y + wall scale | 2.0m – 6.0m |
| Wall roughness | Material roughness on selected wall(s) | 0.0 – 1.0 |
| Light intensity | Main light + ambient intensity | 0.1 – 3.0 |
| Color temperature | Light color mapped from Kelvin | 2700K – 6500K |
| Window scale | Window mesh scale | 0.2x – 3.0x |
| Partition depth | Refuge partition visibility + depth | 0.0 – 2.5m |

**Discrete selectors (click to apply):**

| Selector | What it controls | Options |
|---|---|---|
| Wall material swatches | Wall color + roughness | Plaster, Brick, Concrete, Wood, White, Glass, Slate |
| Floor material swatches | Floor color + roughness | Hardwood, Carpet, Tile, Polished |
| Wall selector | Which wall(s) are affected | All, North, South, East, West, Individual |

**Per-wall selection is critical.** The user must be able to click "North Wall" and change only that wall's material. This requires your `mesh_roles.json` wall_id mapping from Task 1.

### How wall selection works

```javascript
// mesh_roles.json tells us which mesh is which wall
const roles = await fetch('mesh_roles/SKF_office_001.json').then(r => r.json());

// Build a wall selector dropdown from the annotations
const walls = Object.entries(roles.meshes)
  .filter(([name, info]) => info.role === 'wall')
  .map(([name, info]) => ({ meshName: name, wallId: info.wall_id }));

// When user selects "north" and clicks a material swatch:
function setWallMaterial(wallId, color, roughness) {
  const target = wallId === 'all' ? walls : walls.filter(w => w.wallId === wallId);
  target.forEach(w => {
    const mesh = scene.getObjectByName(w.meshName);
    mesh.material.color.set(color);
    mesh.material.roughness = roughness;
  });
}
```

### How ceiling height works (the geometry challenge)

```javascript
function setCeilingHeight(newHeight) {
  const ceiling = scene.getObjectByName(ceilingMeshName);
  const originalHeight = roles.room_dimensions.height_m;
  ceiling.position.y = newHeight;

  // Scale walls proportionally
  walls.forEach(w => {
    const mesh = scene.getObjectByName(w.meshName);
    mesh.scale.y = newHeight / originalHeight;
    mesh.position.y = newHeight / 2;
  });

  // Move lights to stay near ceiling
  lights.forEach(l => { l.position.y = newHeight - 0.3; });
}
```

**Speed:** These are JavaScript property changes. No re-rendering, no re-compilation. Measured at **120 fps** in our prototype. Slider dragging is perceptually instant.

### Lighting quality requirement

Basic Three.js lights (DirectionalLight + AmbientLight) produce flat, unrealistic scenes with no light bounce, no color bleeding, and no ambient occlusion. For research stimuli, this is unacceptable — 33 of the registry's lighting tags describe properties of **indirect** light.

Your viewer must implement **at least one** of these lighting upgrades:

| Level | Technique | What it adds | Implementation | Laptop requirement |
|---|---|---|---|---|
| **Level 2 (minimum)** | HDRI environment map + tone mapping | Realistic ambient from all directions; reflections on glossy surfaces | Load a `.hdr` file from Poly Haven; set `scene.environment`; use `ACESFilmicToneMapping`. ~20 lines. | Any laptop, 120 fps |
| **Level 3 (expected)** | + Screen-space ambient occlusion (SSAO) | Corners and crevices naturally darken; huge realism boost | Add `SSAOPass` from Three.js post-processing. ~40 lines. | Any laptop, 60-90 fps |
| **Level 5 (stretch)** | Path tracing via `three-gpu-pathtracer` | Full global illumination: light bounces between surfaces, color bleeds from colored walls to ceiling, soft shadows, caustics | Replace `renderer.render()` with `pathTracer.renderSample()`. ~20 lines. See [Interior Scene demo](https://gkjohnson.github.io/three-gpu-pathtracer/example/bundle/interior.html). | Any laptop with WebGL 2 (all modern laptops). Renders progressively: noisy during interaction, converges to clean in ~2 seconds when you stop. **Not harder to implement than Level 2 — the library does the work.** |

**Verified empirically:** The `three-gpu-pathtracer` [Interior Scene demo](https://gkjohnson.github.io/three-gpu-pathtracer/example/bundle/interior.html) runs on standard laptop GPUs (MacBook Air M1 and up). It uses WebGL 2 (not WebGPU), renders at half resolution during interaction (`renderScale: 0.5`), and reaches 38 samples (visually clean) within ~30 seconds at rest. At 370+ samples, the result is publication-quality. The library has 1.7k GitHub stars, 2,332 commits, MIT license, and is actively maintained.

**The interactive UX for path tracing:**

```
SLIDER DRAG:     Scene goes noisy (like Blender viewport) — still responsive
SLIDER RELEASE:  pathTracer.updateMaterials() + pathTracer.reset()
                 Image converges to clean GI in ~2 seconds
EXPORT:          Capture converged frame as the research stimulus
```

**HDRI sources (all CC0, free):**

| Source | What you need |
|---|---|
| [Poly Haven](https://polyhaven.com/hdris) | Filter "indoor" category. Download ≥ 3 HDRIs at different color temps (warm interior, neutral studio, cool overcast) |
| [Ambient CG](https://ambientcg.com) | CC0 HDRIs + matching PBR material textures |

---

## Phase 2: Test each model × each factor

Load each of your top 10 models (viability score ≥ 4) and systematically test all 8 manipulation classes.

### The factor viability matrix

For each model × factor combination, record:

| | Geometry | Lighting | Materials | Color | Biophilic | Furniture | Acoustic | Complexity |
|---|---|---|---|---|---|---|---|---|
| Model 1 | ✅ | ✅ | ⚠️ | ✅ | ❌ | ✅ | n/a | ⚠️ |
| Model 2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | n/a | ✅ |
| ... | | | | | | | | |

Legend:
- ✅ Works correctly (visual change is clearly visible)
- ⚠️ Partially works (e.g., shared material affects multiple walls)
- ❌ Doesn't work (e.g., no separate ceiling mesh)
- n/a Not applicable (no acoustic meshes to modify)

### Testing protocol for each factor

**For each modification on each model:**
1. Set to the **lowest** value (e.g., ceiling = 2.0m)
2. Take a screenshot
3. Set to the **highest** value (e.g., ceiling = 6.0m)
4. Take a screenshot
5. Record: did it work? What broke? How long did the modification take?

### The extended manipulation class (beyond the 5 original factors)

Your viewer should also support these where the model allows:

| Class | What to test | How to implement |
|---|---|---|
| **Window placement** | Move window mesh from one wall to another | Re-parent window to different wall mesh; update position |
| **Furniture density** | Show/hide furniture meshes | Toggle `mesh.visible` for furniture-role meshes |
| **View content** | Change what's visible through the window | Swap the window mesh's emissive texture or backdrop |
| **Partition walls** | Add/remove internal dividers | Toggle visibility of partition-role meshes |
| **Floor plan proportions** | Make room wider/narrower | Scale floor + walls + ceiling on X or Z axis |

---

## Phase 3: Write ruthless validation tests

For each model you tested, write a **ruthless prompt** that an AI cannot pass unless the viewer actually works:

> *"Load model SKF_office_001 in the viewer. Execute these 12 tests in sequence:*
> 1. *Set ceiling to 2.0m. Is the ceiling visually at desk height? If not, the scale is wrong.*
> 2. *Set ceiling to 5.0m. Do the walls extend to meet it, or is there a gap?*
> 3. *Select ONLY the north wall. Change it to brick. Verify: south/east/west walls are unchanged.*
> 4. *Set color temperature to 2700K. Does the room look warm? Set to 6500K. Does it look clinical?*
> 5. *Set window scale to 3.0x. Does the window mesh overlap adjacent walls?*
> 6. *Set window scale to 0.2x. Is the window still visible or does it disappear?*
> 7. *Change floor to marble (roughness 0.15). Does it look reflective?*
> 8. *Hide all furniture meshes. Is only architecture remaining?*
> 9. *Check FPS counter during slider drag. Is it ≥ 60fps throughout?*
> 10. *Set all sliders to extreme values simultaneously. Does anything z-fight or overlap?*
> 11. *Reset to defaults. Does the model return to its original state exactly?*
> 12. *Open the browser console. Are there any JavaScript errors?*
> *Report pass/fail for each test."*

Run this on **every model** you test. The results go into the factor viability matrix.

---

## What you submit

| Item | What it is |
|---|---|
| `ka_vr_viewer.html` | Interactive viewer with sliders + material swatches + per-wall selection |
| Factor viability matrix | 10 models × 8 factors, each ✅/⚠️/❌ |
| Before/after screenshots | For every factor × every model (minimum 80 screenshots) |
| Ruthless validation results | Pass/fail for the 12-test protocol on each model |
| Modification log | What broke at scale and how you fixed it |
| Contracts + tests | Written BEFORE building |
| File manifest | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 10 | Written BEFORE building. Specific. **(CONTRACT GATE)** |
| **Viewer functionality** | 20 | All 8 factors controllable; per-wall selection; sliders real-time |
| **Model coverage** | 15 | ≥ 10 models tested, ≥ 5 room types |
| **Factor viability matrix** | 15 | Accurate, supported by screenshots, failures documented |
| **Ruthless validation** | 10 | 12-test protocol run on all models, results honest |
| **Verification** | 5 | Caught problems, documented fixes |

> ⛔ **Contract gate**: If your viewer doesn't include per-wall selection or your viability matrix is fabricated, your work will not be integrated.

---

## Existing code you should know about

| Resource | What it gives you |
|---|---|
| `scratch/t3_ai_frontend_v2.html` | Working prototype with sliders, material swatches, FPS counter, and NL parser — study this before building |
| A-Frame documentation (aframe.io) | Entity-component system, glTF loading, light components |
| Three.js GLTFLoader docs | How to traverse loaded glTF scene graphs |
| Your `mesh_roles/*.json` from Task 1 | The mesh-to-role mappings your viewer consumes |

---

## Reuse

Your viewer is the testing harness for Task 3's AI front-end. Every slider you build here becomes a parameter the LLM can control via natural language. Your factor viability matrix tells Task 3 exactly which modifications are safe to expose.

---

# Track 3 · Task 3: AI Front-End for Parametric Scene Modification

**Track:** VR Studio  
**Prerequisite:** Task 2 (working viewer with sliders + factor viability matrix)  
**Points:** 75  
**What you'll have when you're done:** A web-based tool where a researcher types natural language instructions like "make this a warm, cozy library with 4-meter ceilings and exposed brick on the north wall" and the system modifies the 3D scene in real time, with all changes validated against your factor viability matrix before being applied.

---

## The big picture

In Task 2, you built sliders and swatches that modify 3D scenes in real time. But sliders require the user to know *which* parameter to change and *what value* to set. A researcher who wants to study "cozy vs. clinical environments" shouldn't need to manually set ceiling=2.6m, CCT=2700K, walls=wood, roughness=0.6, lighting=0.8. They should just say it.

**No existing product does this.** Tools like Veras, DecorAI, and Decory produce 2D images, not modified 3D models. Meshy and Luma generate new models, not parametric modifications of existing ones. You are building something novel — but every component uses proven technology.

### The architecture

```
User types: "warm cozy library with 4m ceiling, wood on north wall,
             dim lighting, small windows, carpet floor"
                    │
                    ▼
    ┌──────────────────────────────────┐
    │  Scene Introspector              │
    │  Reads mesh_roles.json +         │
    │  current slider values →         │
    │  produces scene summary JSON     │
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │  LLM Parameter Extractor         │
    │  Input: user text + scene summary│
    │  Output: structured JSON spec    │
    │  {                               │
    │    ceiling_height: 4.0,          │
    │    wall_north_color: "#8B6914",  │
    │    wall_north_roughness: 0.6,    │
    │    light_intensity: 0.8,         │
    │    light_cct: 2700,              │
    │    window_scale: 0.5,            │
    │    floor_color: "#DEB887",       │
    │    floor_roughness: 0.9          │
    │  }                               │
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │  Validation Gate                 │
    │  Check each modification against │
    │  factor viability matrix:        │
    │  - Is ceiling modifiable? ✅     │
    │  - Is north wall selectable? ✅  │
    │  - Block unsupported mods ❌     │
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │  Scene Modifier                  │
    │  Applies validated JSON to       │
    │  Three.js scene via your         │
    │  Task 2 slider functions         │
    │  Updates slider positions to     │
    │  reflect new state               │
    └──────────────┬───────────────────┘
                   │
                   ▼
    ┌──────────────────────────────────┐
    │  Live 3D Preview                 │
    │  + before/after comparison       │
    │  + modification history          │
    │  + export modified glTF          │
    └──────────────────────────────────┘
```

**Key insight:** The LLM does NOT generate 3D geometry. It maps natural language to a small, constrained JSON schema. The actual 3D manipulation is your Task 2 code.

---

## Phase 1: Build the scene introspector

> **Contract objective:** "I want a function that reads a loaded glTF scene + mesh_roles.json and produces a structured summary the LLM can understand."

```javascript
function introspectScene(gltfScene, meshRoles) {
  const summary = {
    room: meshRoles.room_dimensions,
    current_state: {},
    modifiable: { walls: [], ceiling: false, floor: false, lights: [], windows: [] }
  };

  for (const [meshName, info] of Object.entries(meshRoles.meshes)) {
    const mesh = gltfScene.getObjectByName(meshName);
    if (!mesh) continue;
    if (info.role === 'ceiling') {
      summary.current_state.ceiling_height = mesh.position.y;
      summary.modifiable.ceiling = true;
    } else if (info.role === 'wall') {
      summary.modifiable.walls.push(info.wall_id);
      summary.current_state[`wall_${info.wall_id}_color`] = '#' + mesh.material.color.getHexString();
    } else if (info.role === 'window') {
      summary.modifiable.windows.push({ wall: info.parent_wall, position: info.position });
    }
    // ... floor, lights, furniture
  }
  return summary;
}
```

**Success conditions:**
- [ ] Produces valid JSON from any loaded model
- [ ] Correctly identifies which walls are individually selectable
- [ ] Reports current ceiling height, material colors, light settings
- [ ] Lists which modifications are supported for this model

---

## Phase 2: Wire up the LLM parameter extractor

### The system prompt (this IS the contract)

```
You are a 3D scene modification assistant for architectural research.

Given a scene description and a user instruction, output ONLY a JSON object 
with the modifications to apply. Available fields:

GEOMETRY:
- ceiling_height: number (meters, range 2.0-6.0)

WALLS (per-wall or all):
- wall_all_color: hex string       - wall_all_roughness: number 0-1
- wall_north_color: hex string     - wall_north_roughness: number 0-1
- wall_south_color / roughness     - wall_east_color / roughness
- wall_west_color / roughness

FLOOR:
- floor_color: hex string          - floor_roughness: number 0-1

LIGHTING:
- light_intensity: number 0.1-3.0
- light_cct: number 2700-6500 (Kelvin)

PROSPECT & REFUGE:
- window_scale: number 0.2-3.0 (1.0 = current)
- partition_depth: number 0-2.5 (0 = no partition)

FURNITURE:
- furniture_visible: boolean

Only include fields the user's instruction changes.
If the user says "north wall" or "back wall", use wall_north_* fields.
If the user says "walls" without specifying, use wall_all_* fields.
Output ONLY valid JSON, no explanation.
```

### API integration

```javascript
async function extractModifications(userText, sceneSummary, apiKey) {
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        systemInstruction: { parts: [{ text: SYSTEM_PROMPT }] },
        contents: [{ parts: [{ text:
          `Current scene: ${JSON.stringify(sceneSummary)}\n\nUser instruction: "${userText}"`
        }] }],
        generationConfig: { responseMimeType: 'application/json' }
      })
    }
  );
  const data = await response.json();
  return JSON.parse(data.candidates[0].content.parts[0].text);
}
```

**Why `responseMimeType: 'application/json'` matters:** This forces the LLM to output valid JSON — no markdown wrapping, no explanation text. If the JSON is invalid, it's a hard error you can catch.

### Multi-instruction parsing

A single user input can specify changes across all 8 factors simultaneously:

> "Make it a cathedral — soaring 5.5m ceiling, cool daylight at 6500K, white plaster walls except the north wall which should be exposed stone, marble floor, large panoramic windows, and remove all furniture"

The LLM should return:
```json
{
  "ceiling_height": 5.5,
  "light_intensity": 2.0,
  "light_cct": 6500,
  "wall_all_color": "#F5F5F5",
  "wall_all_roughness": 0.7,
  "wall_north_color": "#808080",
  "wall_north_roughness": 0.85,
  "floor_color": "#F5F5DC",
  "floor_roughness": 0.15,
  "window_scale": 2.5,
  "furniture_visible": false
}
```

All modifications are applied **atomically** — in a single render frame. The user sees one transition, not a sequence of individual changes.

---

## Phase 3: Build the validation gate

Before applying any LLM output, validate it against your Task 2 factor viability matrix.

```javascript
function validateModifications(mod, viabilityMatrix, modelId) {
  const model = viabilityMatrix[modelId];
  const errors = [];
  const validated = {};

  for (const [key, value] of Object.entries(mod)) {
    if (key === 'ceiling_height' && model.geometry !== '✅') {
      errors.push(`Ceiling modification not supported on ${modelId}`);
    } else if (key.startsWith('wall_') && key.includes('_color')) {
      const wallId = key.split('_')[1];
      if (wallId !== 'all' && !model.individual_walls) {
        errors.push(`Per-wall selection not supported; applying to all walls`);
        validated['wall_all_color'] = value; // fallback
      } else {
        validated[key] = value;
      }
    } else {
      validated[key] = value;
    }
  }

  return { validated, errors, blocked: errors.filter(e => e.includes('not supported')) };
}
```

The UI must show:
- ✅ Modifications that were applied
- ⚠️ Modifications that were degraded (e.g., per-wall → all-wall fallback)
- ❌ Modifications that were blocked (unsupported by this model)

---

## Phase 4: Build presets from the research literature

Create ≥ 5 presets derived from actual neuroarchitecture experimental conditions:

| Preset | Based on | Modifications |
|---|---|---|
| **Meyers-Levy High Ceiling** | Meyers-Levy & Zhu (2007) ceiling height × creativity | ceiling=3.5m, walls=white, light_cct=5000K |
| **Meyers-Levy Low Ceiling** | Same study, low condition | ceiling=2.4m, walls=white, light_cct=5000K |
| **Biophilic Restoration** | Browning et al. (2014) | wall_north_color=green tones, window_scale=2.5, floor=wood |
| **Prospect-Dominant** | Appleton (1975) prospect-refuge | window_scale=3.0, ceiling=4.0m, partition_depth=0 |
| **Refuge-Dominant** | Same theory, refuge condition | window_scale=0.4, ceiling=2.4m, partition_depth=2.0 |
| **Clinical Control** | Standard lab environment | ceiling=2.7m, walls=white, light_cct=6500K, floor=tile |

Each preset must cite the original paper and explain which IV is being manipulated.

---

## Phase 5: Test on 10+ diverse models

The AI front-end must be tested on **at least 10 different models** of varied style:
- ≥ 2 offices, ≥ 2 residential, ≥ 1 classroom, ≥ 1 healthcare, ≥ 1 retail/hospitality, ≥ 3 other
- Include at least 2 "difficult" models (low viability score) to test graceful degradation

### The 15-test ruthless protocol

For each model, run this validation suite:

1. Type "raise the ceiling to 5 meters" → ceiling moves, walls extend, no gaps
2. Type "change the north wall to brick" → only north wall changes
3. Type "make it warm and cozy" → ceiling lowers, CCT drops, intensity dims
4. Type "make it a clinical lab" → opposite of #3
5. Type "cathedral with stone walls except south wall which is glass" → per-wall differentiation
6. Type a nonsensical instruction ("make the ceiling purple and sideways") → graceful error, no crash
7. Apply 3 instructions in sequence → each builds on the previous state correctly
8. Click "Reset" after modifications → returns to original state exactly
9. Apply a preset → sliders update to match
10. Drag ceiling slider during an LLM modification → no conflict
11. Type an instruction for an unsupported factor → validation gate blocks it with explanation
12. Check FPS during multi-factor modification → ≥ 60fps
13. Type a very long instruction (50+ words) → LLM parses correctly
14. Type instructions in different phrasings ("raise roof" vs "higher ceiling" vs "ceiling at 4m") → all work
15. Export the modified glTF → file is valid and loads in Blender

---

## What you submit

| Item | What it is |
|---|---|
| `ka_vr_ai_modifier.html` | Working AI front-end with NL input + sliders + validation |
| LLM integration code | API call with constrained JSON output |
| Validation gate | Checks modifications against viability matrix |
| ≥ 5 research presets | With citations and IV explanations |
| 15-test results on 10 models | 150 test outcomes documented |
| Modification history log | Every LLM call: input text, output JSON, validation result |
| Material library | ≥ 10 PBR presets (wood, brick, concrete, glass, marble, tile, plaster, carpet, slate, metal) |
| Contracts + tests | Written BEFORE building |
| Demo video | 3-minute recording showing multi-instruction NL on 3 different models |
| File manifest | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 10 | Written BEFORE building. Specific. **(CONTRACT GATE)** |
| **LLM integration** | 15 | Constrained JSON output; multi-factor instructions work; per-wall addressing |
| **Validation gate** | 10 | Checks viability matrix; blocks unsupported; shows feedback |
| **Research presets** | 10 | ≥ 5 presets with citations; IVs correctly mapped to modifications |
| **Model coverage** | 15 | 15-test protocol on ≥ 10 diverse models; honest reporting |
| **Ruthless testing** | 10 | Adversarial inputs tested; graceful degradation documented |
| **Polish** | 5 | Slider sync, reset, export, modification history, FPS maintained |

> ⛔ **Contract gate**: If your AI front-end doesn't include the validation gate, or your 15-test results are fabricated, your work will not be integrated.

---

## Existing code you should know about

| Resource | What it gives you |
|---|---|
| `scratch/t3_ai_frontend_v2.html` | Working prototype with sliders, material swatches, NL parser, and FPS counter at 120fps |
| Your `ka_vr_viewer.html` from Task 2 | Your slider/swatch code — the AI front-end wraps this |
| Your `mesh_roles/*.json` from Task 1 | Scene introspection data source |
| Your factor viability matrix from Task 2 | Input to the validation gate |
| `Tagging_Contractor` registry | 330 manipulable tags across 8 classes — defines the parameter space |
| `Article_Eater/data/templates/` | 166 PNU templates — experimental conditions for presets |

---

## Why this matters

You are building the first tool that lets a neuroarchitecture researcher say "give me the Meyers-Levy high-ceiling condition on this office model" and get a modified 3D stimulus in seconds instead of weeks. No existing product does this. Every component uses proven technology — the innovation is the integration.
