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
