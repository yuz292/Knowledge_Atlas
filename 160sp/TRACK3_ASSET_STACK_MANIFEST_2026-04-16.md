# Track 3 Asset Stack Manifest

Date: 2026-04-16

This manifest assumes the Track 3 submission contract is:

- final runtime: **A-Frame / WebXR**
- editing and cleanup: **Blender**
- preferred asset format: **`.glb` / `.gltf`**

## Starter Set

### 1. Smoke-test environment

Use this before importing any external model.

- **A-Frame environment component**
  - purpose: instant browser sanity check
  - why: confirms that camera, movement, and scene boot are working before students debug asset problems
  - output: one minimal `scene.html`
  - source:
    - https://aframe.io/docs/1.7.0/introduction/
    - https://github.com/supermedium/aframe-environment-component

### 2. Room shell sources

Use these to build the benchmark corpus.

- **Sketchfab downloadable interiors**
  - purpose: candidate room shells
  - preferred format: `.glb`
  - use only when the model has:
    - clear license
    - inspectable hierarchy
    - realistic scale
    - separate walls / floor / ceiling / openings when possible
  - source:
    - https://sketchfab.com/

- **TurboSquid free interiors**
  - purpose: fallback room-shell source
  - preferred format: `.fbx` or `.obj`, then export cleaned `.glb` from Blender
  - use only if hierarchy and materials survive import cleanly
  - source:
    - https://www.turbosquid.com/Search/3D-Models/free/room

### 3. Materials and lighting

- **Poly Haven HDRIs**
  - purpose: neutral sky and lighting reference
  - use for:
    - soft daylight
    - overcast daylight
    - neutral studio lighting
  - source:
    - https://polyhaven.com/

- **Poly Haven textures**
  - purpose: walls, flooring, wood, stone, concrete, fabric
  - use for:
    - floor swaps
    - wall-material changes
    - texture-manipulation conditions
  - source:
    - https://polyhaven.com/

### 4. Furniture and interior props

- **Quaternius Ultimate House Interior Pack**
  - purpose: modular interior parts, doors, windows, kitchen and bathroom pieces
  - strongest use: furnishing or completing benchmark rooms
  - source:
    - https://quaternius.com/packs/ultimatehomeinterior.html

- **Quaternius Ultimate Furniture Pack**
  - purpose: chairs, tables, beds, storage, common room furniture
  - strongest use: controlled density or furniture-layout variations
  - source:
    - https://quaternius.com/packs/ultimatefurniture.html

- **Kenney 3D assets**
  - purpose: very lightweight fallback props for early testing
  - strongest use: placeholder objects and low-complexity scene proofs
  - source:
    - https://kenney.nl/assets

- **Poly Pizza CC0 search**
  - purpose: ad hoc small props when a room needs one or two missing objects
  - caution: quality and style vary, so keep it supplementary
  - source:
    - https://poly.pizza/

### 5. AI-generated assets

- **Meshy / Tripo**
  - purpose: isolated props only
  - examples:
    - single chair
    - lamp
    - plant
    - side table
  - avoid using them as the shared benchmark room source
  - source:
    - https://www.meshy.ai/
    - https://www.tripo3d.ai/

## Selection Rules

Every asset admitted to the benchmark set should be checked for:

1. **format portability**
   - can it end as `.glb`?

2. **scale sanity**
   - do doors, tables, and room dimensions look approximately real?

3. **hierarchy quality**
   - are the major architectural components separable?

4. **material editability**
   - can walls / floors / key props be retextured cleanly?

5. **condition usefulness**
   - can the room support at least two controlled manipulations?

## First Bundle To Assemble

If building the first shared student bundle now, assemble:

1. one minimal A-Frame starter scene
2. one neutral room shell
3. one second room shell with stronger openings or light variation
4. one small furniture pack
5. two Poly Haven textures
6. one daylight HDRI
7. one overcast or neutral HDRI
8. one short room-selection checklist

## Do Not Treat As Required

Do not make these mandatory until they actually exist as supported course infrastructure:

- `KA-Rooms`
- Unreal `.uasset` pipelines
- `vr_scenes`
- Unity `.unity` baseline scenes
- Unity-only instrumentation scripts

## Next Collection Step

The clean next move is to create a local `track3_assets/` folder and populate it with:

```text
track3_assets/
  smoke_test/
  rooms/
  props/
  textures/
  skies/
  docs/
```

Then every imported item should be normalized through Blender and re-exported to `.glb` wherever possible.
