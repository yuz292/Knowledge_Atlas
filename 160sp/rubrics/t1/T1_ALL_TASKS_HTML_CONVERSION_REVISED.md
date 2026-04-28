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
