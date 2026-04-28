# Track 3: VR Studio — All Tasks

**Track overview:** You will build a pipeline that lets neuroarchitecture researchers modify 3D interior environments through natural language. Starting from openly licensed 3D models — or generating new ones from photographs with World Labs Marble — you will curate a library of VR-ready rooms, build a real-time viewer with slider controls for 8 environmental manipulation classes, and wire up an AI front-end that turns instructions like "make this a cozy library with 4m ceilings and wood on the north wall" into instant 3D scene modifications. (*VR Studio* is the in-house name for this end-to-end VR content pipeline.)

**Three tasks, one pipeline:**

| Task | What you build | Points |
|---|---|---|
| Task 1 | Collect and catalog at least 20 VR-ready 3D models with per-wall mesh annotations | 75 points |
| Task 2 | Convert to VR and test factors by hand — real-time sliders, 10 models x 8 factors, path-traced lighting | 75 points |
| Task 3 | AI front-end — natural language to validated parametric scene modification | 75 points |

**Contract gate (all tasks):** Every task requires a written contract listing inputs, processing, outputs, success conditions, and a test checklist.

**Speed:** Three.js scene modifications run at **120+ fps**. Path-traced lighting (light bouncing realistically between surfaces) converges in roughly 2 seconds on any modern laptop.

---

# Track 3 - Task 1: Collect and Catalog VR-Ready 3D Interior Models

**Track:** VR Studio
**Points:** 75
**What you will have when you finish:** A curated library of at least 20 VR-ready 3D interior models in glTF or GLB format (glTF is the open 3D-scene file standard; GLB is its single-file binary form). Each model is scored against 8 manipulation classes, cataloged in a Google Sheet with viability scores, and shipped with a *mesh annotation file* — a JSON file that maps every mesh in the model to its semantic role (ceiling, wall_north, floor, window, and so on).

---

## The big picture

The Knowledge Atlas stores evidence that specific environmental features alter human cognition and affect. Researchers have already manipulated these features experimentally:

| Manipulation Class | Registry tags | What researchers change |
|---|---|---|
| **Geometry** (ceiling height, volume, enclosure) | 46 tags | Ceiling height >= 3.0m vs <= 2.4m; room proportions; isovist area (the area visible from a single viewpoint) |
| **Lighting** (intensity, spectrum, direction) | 33 tags | Illuminance (lux); color temperature (2700K-6500K); daylight vs artificial |
| **Materials** (surface texture, roughness) | 13 tags | Wood vs concrete vs glass; natural-material ratio; texture density |
| **Color** (hue, warmth, saturation) | 5 tags | Warm vs cool palettes; color diversity; chroma levels |
| **Biophilic elements** (plants, water, nature views) | 6 tags | Plant count; window-view content (greenery vs built-up) |
| **Furniture layout** (density, arrangement) | 17 tags | Seating count; sociopetal vs sociofugal arrangement; clutter density |
| **Acoustic properties** | 5 tags | Acoustic privacy; natural sound sources |
| **Visual complexity** (detail, order, fractals) | 22 tags | Fractal dimension; symmetry; ornament density |

To test these relationships in VR, researchers need 3D rooms where each factor can be **varied independently while the others stay fixed**. Your job is to collect models that make this possible.

---

## What makes a model "VR-ready"

Not every 3D model can be modified parametrically. ("Parametric" here means the geometry, lights, and materials are exposed as named parameters that code can edit at runtime.) These constraints are hard:

### Constraint 1: Separable named meshes

The ceiling must be a **separate mesh** from the walls. Each wall must be individually identifiable. This rules out:
- Photogrammetry scans (one fused mesh) — NO
- "Baked" models (one mesh with a texture atlas) — NO
- Architectural models with separate, named objects — YES

**Test:** Open the model in Blender (the free open-source 3D editor) and check the Outliner panel. Named objects like "Ceiling", "Wall_North", "Floor" mean the model is viable. A single object called "mesh_001" means it is not.

### Constraint 2: PBR materials, not baked textures

Models must use **PBR material slots** — physically-based rendering channels (base color, roughness, metalness) that a renderer interprets at draw time — rather than a single pre-baked lightmap painted onto the geometry. PBR is what lets you swap materials at runtime.

### Constraint 3: Architectural scale

Models must use **real-world units** (meters). To raise a ceiling by 1m you need to know its actual height, and VR immersion breaks the moment scale is wrong.

### Constraint 4: VR-compatible polygon count

For WebXR at 72 fps or higher: under 500K polygons per scene, under 20 unique materials, textures no larger than 4096 x 4096.

### Constraint 5: Open license

CC0, CC-BY, or CC-BY-SA. Reject "editorial use only" and "All Rights Reserved."

---

## Phase 1: Find model sources

> **Contract objective:** "I want a tested, documented list of 3D-model sources I can use to collect VR-ready interior models."
> **Contract is with:** 3D-model repositories and their APIs.
> **Prompt hint:** *"I need 5+ sources of openly licensed architectural-interior 3D models in glTF, GLB, FBX, or OBJ format. For each source, give me license, API availability, format, and whether models have separable meshes. Test one search per source."*

Write YOUR OWN contract. Include Inputs, Processing, Outputs, Success Conditions.

### Starting points

- **Sketchfab** — CC-licensed, API available, downloads as glTF, many architectural interiors.
- **3D Warehouse** — SketchUp models with groups and components; export through Blender.
- **BlenderKit** — Free tier; meshes are separable out of the box.
- **TurboSquid** (free section) — Check the license on every model.
- **Poly Haven** — CC0; excellent HDRIs and a handful of room models.
- **CGTrader** (free section) — Mixed quality; check the license.

### Advanced source: World Labs Marble (image to 3D world)

[World Labs Marble](https://marble.worldlabs.ai/) uses spatial AI to build explorable 3D worlds from a single photograph, text prompt, or video. Instead of downloading someone else's model, you photograph a real room and generate a 3D version of it. This route matters for neuroarchitecture: [Champalimaud Foundation and King's College London already use Marble to generate patient-specific VR environments for OCD exposure therapy](https://www.worldlabs.ai/case-studies/3-health-systems).

#### Step 1: Generate a world

**Option A - Web UI (easiest start):**
Visit [marble.worldlabs.ai](https://marble.worldlabs.ai/), click Create, upload an interior photo or type a text prompt, and wait about 5 minutes.

**Option B - API (automatable, required for batch processing):**

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

**Generation times:** Text or image to panorama, about 30 seconds. Panorama to full world, about 5 minutes. High-quality mesh export, about 1 hour.

#### Step 2: Export the mesh

In the Marble web viewer, click Export and choose **High-quality mesh (GLB)**. The job runs server-side for about an hour and produces:
- A **600K-triangle mesh** with texture maps
- A **1M-triangle mesh** with vertex colors
- Both in GLB format (loadable in Blender and Three.js)

> **Important:** The exported mesh is a **single fused object** — walls, ceiling, and floor share one continuous surface. You cannot select individual walls yet. Step 3 fixes that.

#### Step 3: Segment the fused mesh into separate architectural elements

To make the Marble export parametrically modifiable, split that single surface into individual objects (ceiling, walls, floor, furniture) and assign PBR materials to each. This step is core to the assignment — **you must use at least one of the AI-assisted approaches below**, not do everything by hand.

---

### Controlling Blender: manual, AI-assisted, and fully automated

There are four ways to segment meshes in Blender, ranging from fully manual to fully automated. Pick whichever you like, but **document which approach you used and evaluate its accuracy.**

#### Approach A - Manual segmentation in Blender (~30-45 min per model)

This is the baseline; every student should know how to do it even after automating it later.

1. Import the GLB: `File -> Import -> glTF 2.0`.
2. Enter Edit Mode (`Tab`).
3. Select ceiling faces: `Select -> Select All by Trait -> Normal` (faces pointing downward).
4. Separate them: `Mesh -> Separate -> Selection` (`P`).
5. Rename the new object "Ceiling" in the Outliner.
6. Repeat for floor (upward normals), each wall (by face orientation), and furniture.
7. Assign PBR materials to every separated object.
8. Export: `File -> Export -> glTF 2.0`.

**Effectiveness:** 100% accurate but slow. Use it for your first one or two models to learn the geometry, then automate.

---

#### Approach B - BlenderMCP: Claude or Cursor controls Blender through MCP (recommended)

[**BlenderMCP**](https://github.com/ahujasid/blender-mcp) (20.7k stars, MIT license) connects Blender to Claude through the [Model Context Protocol](https://modelcontextprotocol.io/). Claude can see your Blender viewport, run Python code, create or modify or delete objects, apply materials, and download Poly Haven assets — all by chatting in natural language.

**Why this is the most powerful option:** Unlike BlenderGPT, BlenderMCP feeds the LLM **viewport screenshots**, so it can see what it just did and correct mistakes. It also pulls HDRIs and materials from Poly Haven, which feeds straight into our VR pipeline.

**Setup:**
1. Install `uv`: `brew install uv` (Mac) or `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` (Windows).
2. Download `addon.py` from the [repo](https://github.com/ahujasid/blender-mcp) and install it in Blender: `Edit -> Preferences -> Add-ons -> Install`.
3. In the Blender sidebar (`N`), open the "BlenderMCP" tab and click "Connect to Claude".
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

**Then tell Claude or Cursor:**
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

**Effectiveness:** Roughly 85-90% accurate on rectangular rooms. The LLM sees the viewport and self-corrects. Irregular rooms may still need manual cleanup. Expect 2-3 prompts per model. Total time: about 10-15 minutes per model, verification included.

**Other capabilities relevant to T3:**
- Pull Poly Haven HDRIs and materials directly (useful for Task 2 lighting).
- Generate 3D models through the Hyper3D Rodin integration.
- Export scene information as JSON for the AI front-end.

---

#### Approach C - BlenderGPT: natural language inside Blender (~10 min per model)

[**BlenderGPT**](https://github.com/gd3kr/BlenderGPT) (4.9k stars, MIT license) is a Blender add-on that takes natural language, sends it to GPT-4, gets back Blender Python (`bpy`) code, and runs that code inside Blender.

**Setup:** Download the ZIP from GitHub, install it via `Edit -> Preferences -> Add-ons -> Install`, and paste your OpenAI API key into the add-on preferences. Open the sidebar (`N`) and find the "GPT-4 Assistant" tab.

**Key difference from BlenderMCP:** BlenderGPT runs entirely inside Blender (no external MCP server) but has **no viewport awareness** — it cannot see what it just did. It writes code blind, based only on your description. So it works well when you describe geometry precisely (face normals, coordinates) but cannot self-correct visual mistakes.

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
-> 'Wall_West', positive X normal -> 'Wall_East'."
```

```
"Assign a new Principled BSDF material to each separated object.
Set Ceiling base color to (0.9, 0.9, 0.9), Floor to (0.4, 0.4, 0.4),
all walls to (0.85, 0.82, 0.75). Set roughness 0.7 for all."
```

**Effectiveness:** About 80% on rectangular rooms. Without viewport feedback, errors stack up — you will need to inspect the result in Blender and fix problems by hand. Total time: about 10-15 minutes per model.

---

#### Approach D - Headless Blender Python script (fully automated, no AI required)

This is the fastest option for batch processing. Write the segmentation logic once as a Python script, then run it headlessly (no GUI) on every model:

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

Run it: `blender --background --python segment_marble_export.py -- marble_room.glb room_segmented.glb`.

Batch every model: `for f in marble_exports/*.glb; do blender --background --python segment_marble_export.py -- "$f" "segmented/$(basename $f)"; done`.

**Effectiveness:** About 75-80% on simple rectangular rooms. The script fails on L-shaped rooms, angled walls, curved surfaces, and rooms where furniture faces look like wall faces. It has no visual judgment — it works purely from geometry. **You must inspect every output in Blender and fix misclassified faces by hand.** This is the ruthless validation step.

**Advantage:** Zero cost, zero API keys; processes 20 models in under 5 minutes. The human review step is where you earn the grade.

---

### Which approach should you use?

| Approach | Stars | API cost | Sees viewport? | Batch mode? | Accuracy | Best for |
|---|---|---|---|---|---|---|
| **A: Manual** | — | $0 | N/A (you are the eyes) | No | 100% | Learning; fixing AI errors |
| **B: BlenderMCP** | 20.7k | Claude API | Yes (screenshots) | No | ~85-90% | Best single-model workflow |
| **C: BlenderGPT** | 4.9k | OpenAI API | No | No | ~80% | Quick iteration in Blender |
| **D: Headless script** | — | $0 | No | Yes | ~75-80% | Batch-processing 20 models |

**Recommended workflow:** Run **Approach D** to batch-segment every model, then **inspect each one in Blender** and use **Approach A or B** to fix the failures. Document every correction — that record is your ruthless validation data.

#### Marble pricing

| Plan | Worlds/month | Mesh export | Cost |
|---|---|---|---|
| **Free** | 4 | None | $0 |
| **Standard** | 12 | Collider mesh | Check [pricing page](https://marble.worldlabs.ai/pricing) |
| **Pro** | 25 | High-quality mesh + commercial rights | Check [pricing page](https://marble.worldlabs.ai/pricing) |
| **Max** | 75 | Everything | Check [pricing page](https://marble.worldlabs.ai/pricing) |
| **API** | Pay-per-use (credits) | Through API | [API pricing](https://docs.worldlabs.ai/api/pricing) |

For this assignment, the **Free plan** (4 worlds) is enough to try the workflow, and the **Standard plan** covers 12 Marble-generated rooms. Use Sketchfab for the rest.

Use Marble for at least 3 of your 20 models so you demonstrate the photo-to-3D-to-parametric pipeline.

**Deliverable:** `model_sources.json`

---

## Phase 2: Collect and evaluate at least 20 models

For every model, score it against all 8 manipulation classes. Can you actually change the ceiling? Swap the wall material? Modify individual walls independently?

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
| `pbr_materials` | Yes/No — uses PBR workflow? |
| `realistic_scale` | Yes/No — meters, not arbitrary units? |
| `individual_walls` | Yes/No — can you select and modify each wall independently? |
| `ceiling_modifiable` | Yes/No |
| `lighting_modifiable` | Yes/No — are lights separate objects? |
| `materials_modifiable` | Yes/No |
| `windows_identifiable` | Yes/No — can you find and resize window meshes? |
| `furniture_separable` | Yes/No — is furniture separate from architecture? |
| `viability_score` | 0-8 (count of modifiable classes) |
| `resolution` | Low / Medium / High |
| `naturalness` | 1-5 (visual realism) |
| `notes` | Issues, conversion needed, what is missing |

### Minimum bar

- At least 20 models total
- At least 10 with viability score >= 4
- At least 5 different room types
- At least 3 different sources

---

## Phase 3: Create mesh annotation files

For each model, write a `mesh_roles.json` that maps every mesh name to its semantic role. The AI front-end in Task 3 reads this file to know which mesh to modify.

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

> **Every wall must carry a `wall_id`** (north/south/east/west or left/right/back/front). This is what enables per-wall material and geometry changes.

---

## Phase 4: Write a ruthless validation prompt

Before you call any model "ready," test it with a **ruthless prompt** — an adversarial instruction designed to break things.

### What a ruthless prompt is

A ruthless prompt is an AI instruction that probes every failure mode. Instead of asking "does it work?" you ask "in exactly what ways does it fail?" The structure:

> *"You are a hostile QA engineer. Your job is to find every way this 3D-model catalog entry could be wrong, misleading, or unusable. For model {model_id}:*
> 1. *Open the model in Blender. Count the actual meshes and compare them to mesh_roles.json. Are any missing or mislabeled?*
> 2. *Try to move the ceiling mesh up by 1 meter. Does the room still look right? Do walls gap?*
> 3. *Try to change the north wall's material to a different color. Does only that wall change, or do others change too (shared material)?*
> 4. *Check every material — is it PBR, or a baked texture that can't be swapped?*
> 5. *Measure the room in Blender. Does it match room_dimensions in the JSON?*
> 6. *Is the model oriented correctly (Y-up or Z-up)? Does the 'north' wall actually face north?*
> *Report every discrepancy you find."*

Write a ruthless validation prompt for your catalog. Run it on at least 5 models. Document everything that broke.

---

## What you submit

| Item | What it is |
|---|---|
| `model_sources.json` | At least 5 sources, at least 3 tested |
| Google Sheet catalog | At least 20 models with all columns filled |
| `models/` directory | All glTF/GLB files |
| `mesh_roles/` directory | One `mesh_roles.json` per model |
| Conversion scripts | Any Blender scripts you used for format conversion |
| Ruthless validation report | Results of running the adversarial prompt on at least 5 models |
| Contracts + tests | Written BEFORE building |
| File manifest | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 15 | Written BEFORE collecting. Specific success conditions. **(CONTRACT GATE)** |
| **Model sources** | 10 | At least 5 sources, at least 3 tested, licenses documented |
| **Model catalog** | 15 | At least 20 models, at least 10 viable, at least 5 room types, viability scores accurate |
| **Mesh annotations** | 15 | Per-wall IDs present, roles correct, dimensions measured |
| **Ruthless validation** | 10 | Run on at least 5 models, failures documented, fixes applied |
| **Verification** | 10 | Spot-checked claims, caught discrepancies |

> STOP **Contract gate**: If your contracts and tests are missing or vague, the VR pipeline will not be able to use your models. Write real contracts with real success conditions.

---

## Existing code you should know about

| Repo / File | What it gives you |
|---|---|
| `Tagging_Contractor/core/trs-core/v0.2.8/registry/registry_v0.2.8.json` | 424 tags; 330 are continuous or ordinal and represent manipulable environmental features |
| `Article_Eater/data/templates/` | 166 PNU templates showing what IVs researchers actually manipulate (ceiling height, lighting, materials, etc.) |
| `Outcome_Contractor/contracts/oc_export/outcome_vocab.json` | 839 effect terms — the dependent variables these manipulations affect |
| `160sp/context/context_vr_production.md` | VR-production context, including the K-ATLAS evidence model and scene specification format |
| [World Labs Marble](https://marble.worldlabs.ai/) | Photo or text to 3D world generation; [API docs](https://docs.worldlabs.ai/api); [SparkJS](https://sparkjs.dev/) for Gaussian Splat rendering |
| [BlenderMCP](https://github.com/ahujasid/blender-mcp) (20.7k stars) | Claude or Cursor controls Blender through MCP; viewport-aware AI control with Poly Haven integration |
| [BlenderGPT](https://github.com/gd3kr/BlenderGPT) (4.9k stars) | Natural language to Blender Python code execution inside Blender; no viewport awareness |
| Blender CLI: `blender --background --python script.py` | Run segmentation/conversion scripts headlessly (no GUI); batch-process all models |

---

## Reuse

The model library and mesh annotations you build here are infrastructure for the next two tasks. Task 2 takes your catalog of viable models and tests their factor-by-factor modifications by hand in A-Frame. Task 3 reads your `mesh_roles.json` files so the AI front-end knows which mesh to modify when a researcher says "the north wall." Accurate annotations now save hours of debugging then.

---

# Track 3 - Task 2: VR Conversion and Manual Factor Testing

**Track:** VR Studio
**Prerequisite:** Task 1 (your 20+ models with mesh annotations)
**Points:** 75
**What you will have when you finish:** At least 10 of your models loaded into A-Frame with verified, real-time slider controls for all 8 manipulation classes, plus a *factor viability matrix* — a model x factor table that proves which modifications work on which models.

---

## The big picture

You cataloged 20+ 3D models and annotated their meshes. Now you need to **prove** those annotations are correct by loading the models into a VR-capable viewer and testing every modification class by hand. This is not a demo; it is validation engineering.

### Why A-Frame, not Unity or Unreal

| Platform | Learning curve | Verdict |
|---|---|---|
| **A-Frame** (WebXR) | HTML and JS; loads glTF natively; runs in the browser; zero install | USE THIS |
| **Unity** | C#; 2+ weeks of onboarding; heavy project files | Too slow for 6 weeks |
| **Unreal** | C++ or Blueprint; steepest curve; massive files | Not feasible |

You already know HTML and JavaScript from Tracks 1 and 2. A-Frame wraps Three.js, so a glTF loads with a single HTML tag. Modifications are JavaScript property assignments and run at **120+ fps** (verified by prototype).

---

## Phase 1: Build the interactive viewer

> **Contract objective:** "I want an HTML page that loads any of my glTF models and exposes real-time slider controls for each manipulation class."
> **Contract is with:** Your glTF models, your `mesh_roles.json` annotations, and the Three.js / A-Frame API.

Write YOUR OWN contract. Include Inputs, Processing, Outputs, Success Conditions.

### The viewer must support

**Real-time sliders (continuous, instant feedback):**

| Slider | What it controls | Range |
|---|---|---|
| Ceiling height | `ceiling` mesh position.y + wall scale | 2.0m - 6.0m |
| Wall roughness | Material roughness on selected wall(s) | 0.0 - 1.0 |
| Light intensity | Main light + ambient intensity | 0.1 - 3.0 |
| Color temperature | Light color mapped from Kelvin | 2700K - 6500K |
| Window scale | Window mesh scale | 0.2x - 3.0x |
| Partition depth | Refuge partition visibility + depth | 0.0m - 2.5m |

**Discrete selectors (click to apply):**

| Selector | What it controls | Options |
|---|---|---|
| Wall material swatches | Wall color + roughness | Plaster, Brick, Concrete, Wood, White, Glass, Slate |
| Floor material swatches | Floor color + roughness | Hardwood, Carpet, Tile, Polished |
| Wall selector | Which wall(s) the change hits | All, North, South, East, West, Individual |

**Per-wall selection is critical.** The user must be able to click "North Wall" and change only that wall's material. This depends on the `wall_id` mapping you wrote in Task 1.

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

**Speed:** These are JavaScript property changes. No re-rendering, no recompilation. Measured at **120 fps** in our prototype. Slider dragging feels instantaneous.

### Lighting quality requirement

Basic Three.js lights (DirectionalLight + AmbientLight) produce flat, unrealistic scenes — no light bounce, no color bleeding, no ambient occlusion. For research stimuli that is unacceptable: 33 of the registry's lighting tags describe properties of **indirect** light.

Your viewer must implement **at least one** of these lighting upgrades:

| Level | Technique | What it adds | Implementation | Laptop requirement |
|---|---|---|---|---|
| **Level 2 (minimum)** | HDRI environment map + tone mapping | Realistic ambient light from every direction; reflections on glossy surfaces | Load a `.hdr` file from Poly Haven, set `scene.environment`, use `ACESFilmicToneMapping`. About 20 lines. | Any laptop, 120 fps |
| **Level 3 (expected)** | + Screen-space ambient occlusion (SSAO) | Corners and crevices darken naturally; large realism boost | Add `SSAOPass` from Three.js post-processing. About 40 lines. | Any laptop, 60-90 fps |
| **Level 5 (stretch)** | Path tracing through `three-gpu-pathtracer` | Full global illumination: light bounces between surfaces, color bleeds from colored walls onto the ceiling, soft shadows, caustics | Replace `renderer.render()` with `pathTracer.renderSample()`. About 20 lines. See the [Interior Scene demo](https://gkjohnson.github.io/three-gpu-pathtracer/example/bundle/interior.html). | Any laptop with WebGL 2 (every modern laptop). Renders progressively: noisy during interaction, converges to clean in about 2 seconds when you stop. **No harder to implement than Level 2 — the library does the work.** |

**Verified empirically:** The `three-gpu-pathtracer` [Interior Scene demo](https://gkjohnson.github.io/three-gpu-pathtracer/example/bundle/interior.html) runs on standard laptop GPUs (MacBook Air M1 and up). It uses WebGL 2 (not WebGPU), renders at half resolution while you interact (`renderScale: 0.5`), and reaches 38 samples (visually clean) within about 30 seconds at rest. At 370+ samples the result is publication-quality. The library has 1.7k GitHub stars, 2,332 commits, an MIT license, and active maintenance.

**The interactive UX for path tracing:**

```
SLIDER DRAG:     Scene goes noisy (like the Blender viewport) — still responsive
SLIDER RELEASE:  pathTracer.updateMaterials() + pathTracer.reset()
                 Image converges to clean GI in ~2 seconds
EXPORT:          Capture the converged frame as the research stimulus
```

**HDRI sources (all CC0, free):**

| Source | What you need |
|---|---|
| [Poly Haven](https://polyhaven.com/hdris) | Filter the "indoor" category. Download at least 3 HDRIs at different color temperatures (warm interior, neutral studio, cool overcast). |
| [Ambient CG](https://ambientcg.com) | CC0 HDRIs plus matching PBR material textures |

---

## Phase 2: Test each model x each factor

Load each of your top 10 models (viability score >= 4) and test all 8 manipulation classes systematically.

### The factor viability matrix

For each model x factor combination, record:

| | Geometry | Lighting | Materials | Color | Biophilic | Furniture | Acoustic | Complexity |
|---|---|---|---|---|---|---|---|---|
| Model 1 | OK | OK | partial | OK | NO | OK | n/a | partial |
| Model 2 | OK | OK | OK | OK | OK | OK | n/a | OK |
| ... | | | | | | | | |

Legend:
- OK — Works correctly (visual change is clearly visible)
- partial — Partially works (e.g., a shared material affects multiple walls)
- NO — Does not work (e.g., no separate ceiling mesh)
- n/a — Not applicable (e.g., no acoustic meshes to modify)

### Testing protocol for each factor

**For every modification on every model:**
1. Set the slider to its **lowest** value (e.g., ceiling = 2.0m).
2. Take a screenshot.
3. Set the slider to its **highest** value (e.g., ceiling = 6.0m).
4. Take a screenshot.
5. Record: did it work? What broke? How long did the modification take?

### The extended manipulation class (beyond the 5 original factors)

Your viewer should also support these where the model allows:

| Class | What to test | How to implement |
|---|---|---|
| **Window placement** | Move a window mesh from one wall to another | Re-parent the window to a different wall mesh; update position |
| **Furniture density** | Show or hide furniture meshes | Toggle `mesh.visible` on furniture-role meshes |
| **View content** | Change what is visible through the window | Swap the window mesh's emissive texture or backdrop |
| **Partition walls** | Add or remove internal dividers | Toggle visibility on partition-role meshes |
| **Floor-plan proportions** | Make the room wider or narrower | Scale floor + walls + ceiling on the X or Z axis |

---

## Phase 3: Write ruthless validation tests

For each model you tested, write a **ruthless prompt** that an AI cannot pass unless the viewer actually works:

> *"Load model SKF_office_001 in the viewer. Run these 12 tests in sequence:*
> 1. *Set ceiling to 2.0m. Is the ceiling visually at desk height? If not, the scale is wrong.*
> 2. *Set ceiling to 5.0m. Do the walls extend to meet it, or is there a gap?*
> 3. *Select ONLY the north wall. Change it to brick. Verify: south, east, and west walls are unchanged.*
> 4. *Set color temperature to 2700K. Does the room look warm? Set to 6500K. Does it look clinical?*
> 5. *Set window scale to 3.0x. Does the window mesh overlap adjacent walls?*
> 6. *Set window scale to 0.2x. Is the window still visible, or does it disappear?*
> 7. *Change the floor to marble (roughness 0.15). Does it look reflective?*
> 8. *Hide all furniture meshes. Is only the architecture left?*
> 9. *Watch the FPS counter while dragging a slider. Does it stay >= 60 fps throughout?*
> 10. *Push every slider to an extreme value at once. Does anything z-fight or overlap?*
> 11. *Reset to defaults. Does the model return to its original state exactly?*
> 12. *Open the browser console. Are there any JavaScript errors?*
> *Report pass or fail for each test."*

Run this on **every model** you test. The results feed straight into the factor viability matrix.

---

## What you submit

| Item | What it is |
|---|---|
| `ka_vr_viewer.html` | Interactive viewer with sliders, material swatches, and per-wall selection |
| Factor viability matrix | 10 models x 8 factors, each marked OK / partial / NO |
| Before-and-after screenshots | One pair per factor per model (at least 80 screenshots total) |
| Ruthless validation results | Pass or fail for the 12-test protocol on each model |
| Modification log | What broke at scale and how you fixed it |
| Contracts + tests | Written BEFORE building |
| File manifest | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 10 | Written BEFORE building. Specific. **(CONTRACT GATE)** |
| **Viewer functionality** | 20 | All 8 factors controllable; per-wall selection works; sliders respond in real time |
| **Model coverage** | 15 | At least 10 models tested, at least 5 room types |
| **Factor viability matrix** | 15 | Accurate, supported by screenshots, failures documented |
| **Ruthless validation** | 10 | 12-test protocol run on all models, results honest |
| **Verification** | 5 | Caught problems, documented fixes |

> STOP **Contract gate**: If your viewer omits per-wall selection or your viability matrix is fabricated, your work will not be integrated.

---

## Existing code you should know about

| Resource | What it gives you |
|---|---|
| `scratch/t3_ai_frontend_v2.html` | Working prototype with sliders, material swatches, FPS counter, and NL parser — study this before building |
| A-Frame documentation (aframe.io) | Entity-component system, glTF loading, light components |
| Three.js GLTFLoader docs | How to traverse loaded glTF scene graphs |
| Your `mesh_roles/*.json` from Task 1 | The mesh-to-role mappings the viewer consumes |

---

## Reuse

This viewer becomes the testing harness for Task 3's AI front-end. Every slider you wire here turns into a parameter the LLM can drive through natural language, and your factor viability matrix tells Task 3 exactly which modifications are safe to expose for each model. Without an honest matrix, the AI front-end will silently apply requests that the geometry cannot honor.

---

# Track 3 - Task 3: AI Front-End for Parametric Scene Modification

**Track:** VR Studio
**Prerequisite:** Task 2 (working viewer with sliders + factor viability matrix)
**Points:** 75
**What you will have when you finish:** A web-based tool where a researcher types a natural-language instruction such as "make this a warm, cozy library with 4-meter ceilings and exposed brick on the north wall," and the system modifies the 3D scene in real time. Every change is checked against your factor viability matrix before it is applied.

---

## The big picture

In Task 2 you built sliders and swatches that modify 3D scenes in real time. But sliders force the user to know *which* parameter to change and *what value* to set. A researcher who wants to study "cozy versus clinical environments" should not have to set ceiling=2.6m, CCT=2700K, walls=wood, roughness=0.6, and lighting=0.8 by hand. They should just say it.

**No existing product does this.** Veras, DecorAI, and Decory produce 2D images, not modified 3D models. Meshy and Luma generate new models, not parametric modifications of existing ones. You are building something genuinely new — but every component uses proven technology.

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
    │  - Is ceiling modifiable? OK     │
    │  - Is north wall selectable? OK  │
    │  - Block unsupported mods NO     │
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

**Key insight:** The LLM does NOT generate 3D geometry. It maps natural language onto a small, constrained JSON schema. Your Task 2 code does the actual 3D manipulation.

---

## Phase 1: Build the scene introspector

The *scene introspector* is a function that surveys whatever model is currently loaded and produces a structured summary the LLM can read. The LLM needs to know what room it is editing before it can decide what to change.

> **Contract objective:** "I want a function that reads a loaded glTF scene and its mesh_roles.json and produces a structured summary the LLM can understand."

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
- [ ] Produces valid JSON for any loaded model
- [ ] Correctly identifies which walls are individually selectable
- [ ] Reports current ceiling height, material colors, and light settings
- [ ] Lists which modifications this specific model supports

---

## Phase 2: Wire up the LLM parameter extractor

The *LLM parameter extractor* turns a free-form sentence into the exact JSON the scene modifier expects. The system prompt is the contract — it defines every field the LLM is allowed to emit.

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

**Why `responseMimeType: 'application/json'` matters:** It forces the LLM to emit valid JSON — no markdown wrapping, no explanation text. If the JSON is invalid, you get a hard error you can catch.

### Multi-instruction parsing

A single user input can specify changes across all 8 factors at once:

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

Apply all modifications **atomically**, in a single render frame. The user sees one transition, not a sequence of individual changes.

---

## Phase 3: Build the validation gate

Before applying any LLM output, validate it against your Task 2 factor viability matrix.

```javascript
function validateModifications(mod, viabilityMatrix, modelId) {
  const model = viabilityMatrix[modelId];
  const errors = [];
  const validated = {};

  for (const [key, value] of Object.entries(mod)) {
    if (key === 'ceiling_height' && model.geometry !== 'OK') {
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
- Modifications that were applied
- Modifications that were degraded (e.g., per-wall fell back to all-wall)
- Modifications that were blocked (this model does not support them)

---

## Phase 4: Build presets from the research literature

Create at least 5 presets drawn from real neuroarchitecture experimental conditions:

| Preset | Based on | Modifications |
|---|---|---|
| **Meyers-Levy High Ceiling** | Meyers-Levy & Zhu (2007), ceiling height x creativity | ceiling=3.5m, walls=white, light_cct=5000K |
| **Meyers-Levy Low Ceiling** | Same study, low condition | ceiling=2.4m, walls=white, light_cct=5000K |
| **Biophilic Restoration** | Browning et al. (2014) | wall_north_color=green tones, window_scale=2.5, floor=wood |
| **Prospect-Dominant** | Appleton (1975), prospect-refuge | window_scale=3.0, ceiling=4.0m, partition_depth=0 |
| **Refuge-Dominant** | Same theory, refuge condition | window_scale=0.4, ceiling=2.4m, partition_depth=2.0 |
| **Clinical Control** | Standard lab environment | ceiling=2.7m, walls=white, light_cct=6500K, floor=tile |

Each preset must cite the original paper and explain which IV it manipulates.

---

## Phase 5: Test on 10+ diverse models

Test the AI front-end on **at least 10 different models** of varied style:
- At least 2 offices, 2 residential, 1 classroom, 1 healthcare, 1 retail or hospitality, 3 other
- Include at least 2 "difficult" models (low viability score) so you can test graceful degradation

### The 15-test ruthless protocol

For each model, run this validation suite:

1. Type "raise the ceiling to 5 meters" — ceiling moves, walls extend, no gaps.
2. Type "change the north wall to brick" — only the north wall changes.
3. Type "make it warm and cozy" — ceiling lowers, CCT drops, intensity dims.
4. Type "make it a clinical lab" — opposite of #3.
5. Type "cathedral with stone walls except south wall which is glass" — per-wall differentiation works.
6. Type a nonsensical instruction ("make the ceiling purple and sideways") — graceful error, no crash.
7. Apply 3 instructions in sequence — each builds on the previous state correctly.
8. Click "Reset" after modifications — returns to original state exactly.
9. Apply a preset — sliders update to match.
10. Drag the ceiling slider during an LLM modification — no conflict.
11. Type an instruction targeting an unsupported factor — the validation gate blocks it with an explanation.
12. Watch FPS during a multi-factor modification — stays >= 60 fps.
13. Type a very long instruction (50+ words) — LLM still parses correctly.
14. Type the same intent in different phrasings ("raise roof" vs "higher ceiling" vs "ceiling at 4m") — all work.
15. Export the modified glTF — file is valid and reopens in Blender.

---

## What you submit

| Item | What it is |
|---|---|
| `ka_vr_ai_modifier.html` | Working AI front-end with NL input, sliders, and validation |
| LLM integration code | API call with constrained JSON output |
| Validation gate | Checks modifications against the viability matrix |
| At least 5 research presets | With citations and IV explanations |
| 15-test results on 10 models | 150 test outcomes documented |
| Modification history log | Every LLM call: input text, output JSON, validation result |
| Material library | At least 10 PBR presets (wood, brick, concrete, glass, marble, tile, plaster, carpet, slate, metal) |
| Contracts + tests | Written BEFORE building |
| Demo video | 3-minute recording showing multi-instruction NL on 3 different models |
| File manifest | `git diff --name-only HEAD` and `git status --short` |

---

## Grading (75 points)

| Criterion | Points | What we check |
|---|---|---|
| **Contracts + tests** | 10 | Written BEFORE building. Specific. **(CONTRACT GATE)** |
| **LLM integration** | 15 | Constrained JSON output; multi-factor instructions work; per-wall addressing |
| **Validation gate** | 10 | Checks the viability matrix; blocks unsupported modifications; shows feedback |
| **Research presets** | 10 | At least 5 presets with citations; IVs correctly mapped to modifications |
| **Model coverage** | 15 | 15-test protocol on at least 10 diverse models; honest reporting |
| **Ruthless testing** | 10 | Adversarial inputs tested; graceful degradation documented |
| **Polish** | 5 | Slider sync, reset, export, modification history, FPS maintained |

> STOP **Contract gate**: If your AI front-end omits the validation gate, or your 15-test results are fabricated, your work will not be integrated.

---

## Existing code you should know about

| Resource | What it gives you |
|---|---|
| `scratch/t3_ai_frontend_v2.html` | Working prototype with sliders, material swatches, NL parser, and FPS counter at 120 fps |
| Your `ka_vr_viewer.html` from Task 2 | Your slider and swatch code — the AI front-end wraps it |
| Your `mesh_roles/*.json` from Task 1 | Scene-introspection data source |
| Your factor viability matrix from Task 2 | Input to the validation gate |
| `Tagging_Contractor` registry | 330 manipulable tags across 8 classes — defines the parameter space |
| `Article_Eater/data/templates/` | 166 PNU templates — experimental conditions for presets |

---

## Why this matters

You are building the first tool that lets a neuroarchitecture researcher say "give me the Meyers-Levy high-ceiling condition on this office model" and get a modified 3D stimulus in seconds rather than weeks. No existing product does this. Every component uses proven technology — the innovation is in the integration.
