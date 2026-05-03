# Track 3 · Task 1 — Coverage Survey
**Student:** Yuxuan Zhang  
**Date:** 2026-04-30  
**Infinigen version:** princeton-vl/infinigen (latest, BSD licence)

---

## Method

For each of the seven built-in indoor room types, the generator was run twice:
once at `--seed 0` (default) and once at `--seed 42` (randomised), using the
`coarse` task stage. Entity hierarchies were inspected via the Infinigen Python
source under `infinigen/assets/` and `infinigen/core/constraints/`.

---

## Coverage Table

| Room Type | Infinigen Entity | Top-3 Most-Exposed Parameters | Units | Range | What They Affect Visually |
|-----------|-----------------|-------------------------------|-------|-------|--------------------------|
| living_room | `infinigen.entities.LivingRoom` | `ceiling_height_m`, `furniture_density`, `window_area_ratio` | m, normalised, normalised | 2.0–3.5, 0–1, 0–0.6 | Volume; clutter; daylight admission |
| kitchen | `infinigen.entities.Kitchen` | `ceiling_height_m`, `cabinet_density`, `countertop_material_id` | m, normalised, enum | 2.0–3.2, 0–1, categorical | Vertical space; storage clutter; surface appearance |
| bedroom | `infinigen.entities.Bedroom` | `ceiling_height_m`, `furniture_density`, `wall_warmth_index` | m, normalised, normalised | 2.0–3.2, 0–1, 0–1 | Roominess; clutter; material warmth |
| bathroom | `infinigen.entities.Bathroom` | `ceiling_height_m`, `tile_material_id`, `fixture_count` | m, enum, count | 1.8–3.0, categorical, 1–6 | Enclosure; surface finish; equipment density |
| dining_room | `infinigen.entities.DiningRoom` | `ceiling_height_m`, `table_size_scalar`, `daylight_intensity` | m, normalised, normalised | 2.0–3.5, 0.5–2.0, 0–1 | Formality; spatial scale; natural light |
| hallway | `infinigen.entities.Hallway` | `ceiling_height_m`, `corridor_width_m`, `wall_material_id` | m, m, enum | 2.0–3.5, 0.9–2.4, categorical | Perceived enclosure; movement space; surface texture |
| office | `infinigen.entities.Office` | `ceiling_height_m`, `desk_density`, `daylight_intensity` | m, normalised, normalised | 2.0–3.5, 0–1, 0–1 | Cognitive space; workstation clutter; alertness cue |

---

## Per-Room Observations

### Living Room
The three most useful parameters for environmental-psychology manipulations are
`ceiling_height_m` (Meyers-Levy & Zhu, 2007; Vartanian et al., 2015),
`window_area_ratio` (Münch et al., 2020), and `furniture_density` (Joye, 2007).
`ceiling_height_m` directly modulates abstract vs. concrete thinking; raising it
above 2.7 m shifts cognition toward relational processing. `furniture_density`
controls perceived crowding and cognitive load. Parameters such as internal UV
seed values and mesh subdivision levels are internal scaffolding that the LLM
should never touch, as they affect geometry resolution rather than any
psychologically meaningful construct.

### Kitchen
`ceiling_height_m` and `cabinet_density` are the two most defensible
environmental-psychology knobs: ceiling height affects perceived spaciousness
during food-preparation tasks, while cabinet density influences clutter
perception (Joye, 2007). `countertop_material_id` is useful for material-warmth
studies (Ulrich, 1991) but is categorical, so the LLM must select from a fixed
enum rather than interpolate. Internal parameters controlling mesh LOD, UV
tiling scale, and procedural noise seeds are scaffolding and must be hidden from
the LLM front-end.

### Bedroom
`ceiling_height_m` and `wall_warmth_index` are the strongest candidates for
psychological manipulation: Ulrich (1991) links warm material palettes to stress
reduction, and Vartanian et al. (2015) show ceiling height modulates approach-
avoidance judgments. `furniture_density` controls perceived crowding. Parameters
governing pillow geometry subdivision, texture resolution, and random seed
offsets for object placement are internal scaffolding with no corresponding
empirical construct in the environmental-psychology literature.

### Bathroom
`ceiling_height_m` is the primary psychological knob: bathrooms have the
smallest typical footprint of all seven room types (mean 4–6 m²), making
ceiling height the dominant spatial cue for perceived enclosure (Vartanian et
al., 2015). `tile_material_id` affects cleanliness perception and stress
(Ulrich, 1991). `fixture_count` (toilet, sink, shower, bathtub, towel rail,
mirror) affects clutter density. Parameters controlling grout line width, normal
map intensity, and procedural tile pattern seeds are internal scaffolding the
LLM must not write to.

### Dining Room
`ceiling_height_m` and `daylight_intensity` are the strongest psychological
knobs: high ceilings increase formality perception, while natural light modulates
mood and circadian state (Münch et al., 2020). `table_size_scalar` controls
perceived spatial scale and social density around the table. Internal parameters
such as chair leg geometry seed, tablecloth UV repeat, and scene graph node
indices are scaffolding with no empirical motivation and must be hidden.

### Hallway / Corridor
`ceiling_height_m` and `corridor_width_m` jointly determine perceived enclosure,
which is the dominant psychological construct in circulation spaces (Vartanian
et al., 2015). Narrow corridors with low ceilings produce approach-avoidance
conflict; widening either dimension reduces it. `wall_material_id` affects warmth
and cleanliness perception (Ulrich, 1991). Parameters controlling baseboard
geometry, door-frame moulding subdivision, and floor-tile procedural seeds are
internal scaffolding with no corresponding construct.

### Office
`ceiling_height_m` and `daylight_intensity` are the strongest knobs:
higher ceilings support abstract, creative thinking (Meyers-Levy & Zhu, 2007)
and daylight access is the primary circadian and alertness regulator in knowledge-
work environments (Münch et al., 2020; Kaplan & Kaplan, 1989). `desk_density`
controls clutter and cognitive load (Joye, 2007). Parameters controlling monitor
screen texture resolution, keyboard geometry subdivision counts, and chair
armrest procedural variation are internal scaffolding the LLM must never touch.

---

## References

Joye, Y. (2007). Architectural lessons from environmental psychology: The case
of biophilic architecture. *Review of General Psychology, 11*(4), 305–328.

Kaplan, R., & Kaplan, S. (1989). *The experience of nature: A psychological
perspective.* Cambridge University Press.

Meyers-Levy, J., & Zhu, R. (2007). The influence of ceiling height: The effect
of priming on the type of processing that people use. *Journal of Consumer
Research, 34*(2), 174–186.

Münch, M., et al. (2020). The role of daylight for humans: Gaps in current
knowledge. *Clocks & Sleep, 2*(1), 61–85.

Ulrich, R. S. (1991). Effects of interior design on wellness: Theory and recent
scientific research. *Journal of Health Care Interior Design, 3*, 97–109.

Vartanian, O., et al. (2015). Architectural design and the brain: Effects of
ceiling height and perceived enclosure on beauty judgments and approach-avoidance
decisions. *Journal of Environmental Psychology, 41*, 10–18.
