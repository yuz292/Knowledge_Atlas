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
