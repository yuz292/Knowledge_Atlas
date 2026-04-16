# Track 3 Platform And Asset Decision

Date: 2026-04-16

## Decision

Track 3 should be treated as an **A-Frame / WebXR submission track**.

Unity and Unreal may still be useful for prototyping, visual comparison, or later headset-heavy work, but they are not the right primary contract for the current course website or weekly deliverables.

## Why

The current Track 3 pages do not agree:

- `ka_track3_setup.html` says the working path is Blender now and Unreal later, with a future `KA-Rooms` pipeline.
- `ka_track3_hub.html` says the instructor baseline is Unity 2022 LTS with OpenXR and a `vr_scenes` repo.
- `ka_track3_resources.html` seeds Unity assets and C# scripts.
- `ka_vr_assignment.html` says final Track 3 deliverables must be standalone HTML scenes built in A-Frame and runnable in a browser.

Only the A-Frame contract is coherent with the student submission requirement. It is also the only path currently compatible with lightweight review, GitHub submission, and browser-based testing.

## What A-Frame Is

A-Frame is a browser-based 3D / VR framework built on top of WebGL and three.js.

It is not a layer that runs inside Unity or Unreal.

It is best understood as a different runtime choice:

- **A-Frame**: browser-first, lightweight, easiest to review and submit
- **Unity**: engine-based, stronger tooling, heavier setup and build process
- **Unreal**: highest visual ambition, heaviest setup, most fragile course path right now

The same source assets can often move across these systems if they are kept in engine-neutral formats such as `.glb`, `.gltf`, `.obj`, `.fbx`, and standard texture maps.

## Practical Recommendation

For Spring 160 Track 3, the primary working stack should be:

1. **A-Frame / WebXR**
   - final scene runtime
   - final deliverable format
   - easiest testing path

2. **Blender**
   - asset inspection
   - scale correction
   - mesh cleanup
   - material cleanup
   - export to `.glb`

3. **Engine-neutral asset libraries**
   - room shells
   - props
   - textures
   - skyboxes / HDRIs

4. **Unity / Unreal**
   - optional prototyping only
   - never the primary student contract unless the site is explicitly rewritten around that

## Asset Stack To Collect

### Tier 1: Zero-friction setup and smoke-test assets

Use these first because they remove dependency on external binary repos.

- A-Frame primitives
  - chairs, walls, boxes, ceilings, windows, and dividers can be approximated with basic geometry for early testing
- A-Frame environment component
  - useful for instant sanity checks that a scene boots and the camera/navigation work

### Tier 2: Neutral room and material assets

These should be preferred because they are portable and low-friction.

- Poly Haven
  - HDRIs for sky and lighting reference
  - PBR textures for walls, floors, wood, concrete, fabric
- Downloadable `.glb` or `.gltf` interiors from Sketchfab
  - use only models with clear licensing and clean hierarchy
- Select free room shells from TurboSquid only when the mesh quality is good enough

### Tier 3: Props and furniture

These are useful for condition variation without rebuilding entire rooms.

- Kenney
  - simple, lightweight CC0-style game assets for fast testing
- Quaternius
  - larger CC0 packs with furniture and interior pieces
- Poly Pizza
  - CC0 models, often convenient for smaller props

### Tier 4: AI-generated additions

Use these narrowly.

- Meshy
- Tripo

These are best for isolated props or decorative objects, not for the benchmark room corpus itself. AI-generated full rooms are too unreliable as the canonical shared benchmark set.

## What To Avoid As Core Dependencies

- `KA-Rooms` as a required Track 3 starter
  - local repo exists but does not currently contain a usable Unreal project
- `vr_scenes` as a required Track 3 starter
  - no local repo or seeded baseline scene was found in `/Users/davidusa/REPOS`
- Unity-only scripts such as `GazeLogger.cs` as the main student instrumentation contract
  - these contradict the A-Frame submission path

## Minimum Coherent Starter Bundle

If I were normalizing Track 3 immediately, I would build the starter bundle around:

1. one bare A-Frame template scene
2. one simple room shell `.glb`
3. two skyboxes or HDRIs
4. one small furniture pack
5. one short validation checklist
6. one example `assets/` folder layout

Suggested structure:

```text
track3_assets/
  starter_scene/
    scene.html
  rooms/
    simple_room_shell.glb
  props/
    chair.glb
    table.glb
    plant.glb
  textures/
    wood_floor_01/
    plaster_wall_01/
  skies/
    neutral_studio.hdr
    outdoor_softlight.hdr
  docs/
    LICENSE_NOTES.md
    ROOM_SELECTION_CHECKLIST.md
```

## Immediate Page Changes Needed

These should be treated as a cleanup set:

- `ka_track3_setup.html`
  - keep Blender
  - remove any implication that students must wait for Unreal infrastructure
  - add the browser-first A-Frame starter path explicitly
- `ka_track3_hub.html`
  - remove Unity as the baseline contract
  - rewrite verification around browser load, console-clean render, navigation, and logging checks
- `ka_track3_resources.html`
  - replace Unity scene and C# script examples with A-Frame starter scenes, asset packs, and browser-side logger examples
- `track3_hub.html`
  - remove the phrase `Unreal-ready experimental rooms` unless that remains a prototype-only note

## Operational Rule

If an asset cannot be exported to or used from a browser-runnable A-Frame scene with reasonable effort, it should not be treated as a core Track 3 dependency.
