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
