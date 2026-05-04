# Extension Proposal: Classroom

## 1. Target Room Type and Closest Existing Infinigen Entity

**Target room type:** Classroom  
**Closest existing Infinigen entity:** `infinigen.entities.Office`

The Office entity is the closest match because both room types are knowledge-work
environments with rows of work surfaces, overhead lighting, and a front-facing
focal wall. The Office entity already exposes `ceiling_height_m`, `desk_density`,
and `daylight_intensity` — three of the seven parameters needed for a classroom.

---

## 2. Gap Analysis

The Office entity cannot express the following classroom-specific requirements:

- **Fixed row seating orientation:** Office desks are placed freely; classroom
  desks must face a single focal wall containing a board or screen.
- **Instructor zone:** Classrooms have a distinct front zone (podium, whiteboard,
  projector screen) absent from the Office entity.
- **Seating capacity scalar:** Classrooms pack seats more densely than offices
  and require a student-count parameter rather than a desk-density float.
- **Board/display surface:** The front wall requires a writable or projectable
  surface entity not present in the Office asset library.
- **Acoustic treatment:** Classrooms require sound-absorbing ceiling or wall
  panels that affect both visual appearance and the acoustic simulation layer.

---

## 3. Proposed New Parameters

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "ka://manifests/classroom.v1.proposed",
  "title": "Classroom Parameter Manifest (Proposed)",
  "description": "Seven knobs for a classroom extending infinigen.entities.Office.",
  "infinigen_entity": "infinigen.entities.Office",
  "status": "proposed",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "ceiling_height_m": {
      "type": "number",
      "minimum": 2.4,
      "maximum": 4.0,
      "default": 3.0,
      "unit": "m",
      "status": "proposed",
      "description": "Floor-to-ceiling clear height of the classroom.",
      "citation": "Vartanian et al. (2015); Meyers-Levy & Zhu (2007)",
      "rationale": "Higher ceilings in classrooms promote abstract thinking and
creative problem-solving. Meyers-Levy & Zhu (2007) found that ceilings above
2.7m shift cognition toward relational processing, beneficial for learning."
    },
    "student_capacity": {
      "type": "integer",
      "minimum": 10,
      "maximum": 60,
      "default": 30,
      "unit": "count",
      "status": "proposed",
      "description": "Number of student seats placed in forward-facing rows.",
      "citation": "Joye (2007)",
      "rationale": "Seating density controls perceived crowding and cognitive
load. Joye (2007) links object and occupant density to complexity perception
and reduced restorative capacity in learning environments."
    },
    "daylight_intensity": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "default": 0.6,
      "unit": "normalised",
      "status": "proposed",
      "description": "Scalar on natural light contribution through side windows.",
      "citation": "Münch et al. (2020); Kaplan & Kaplan (1989)",
      "rationale": "Daylight in classrooms modulates student alertness and
circadian entrainment during daytime learning. Münch et al. (2020) identify
morning daylight as the primary alertness regulator in knowledge-work settings."
    },
    "board_type": {
      "type": "string",
      "enum": ["whiteboard", "blackboard", "projector_screen", "smartboard"],
      "default": "whiteboard",
      "unit": "categorical",
      "status": "proposed",
      "description": "Type of display surface on the front focal wall.",
      "citation": "Ulrich (1991)",
      "rationale": "The front-wall surface material affects perceived formality
and visual contrast. Ulrich (1991) identifies surface contrast and material
finish as contributors to cognitive engagement in work environments."
    },
    "wall_warmth_index": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "default": 0.45,
      "unit": "normalised",
      "status": "proposed",
      "description": "0 = cool institutional palette; 1 = warm wood-tone palette.",
      "citation": "Ulrich (1991); Meyers-Levy & Zhu (2007)",
      "rationale": "Wall colour temperature interacts with ceiling height to
modulate mood and cognitive engagement. Ulrich (1991) links warm palettes to
reduced stress in enclosed learning environments."
    },
    "biophilia_count": {
      "type": "integer",
      "minimum": 0,
      "maximum": 6,
      "default": 2,
      "unit": "count",
      "status": "proposed",
      "description": "Number of plant entities placed around the classroom perimeter.",
      "citation": "Kaplan & Kaplan (1989); Ulrich (1991)",
      "rationale": "Indoor greenery in classrooms is a robust restoration cue
that reduces fatigue during extended learning sessions. Kaplan & Kaplan (1989)
identify nature contact as the primary driver of attention restoration."
    },
    "acoustic_panel_coverage": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "default": 0.3,
      "unit": "normalised",
      "status": "proposed",
      "description": "Fraction of ceiling and upper-wall area covered by sound-absorbing panels.",
      "citation": "Joye (2007)",
      "rationale": "Acoustic panel density affects both visual texture and the
acoustic simulation layer. Joye (2007) identifies noise and reverberation as
cognitive-load drivers in learning environments; panel coverage is the primary
architectural control."
    }
  },
  "required": ["ceiling_height_m", "student_capacity", "daylight_intensity"]
}
```

---

## 4. Implementation Hooks

The following Infinigen source files would need editing to implement this entity:

- `infinigen/entities/office.py` — base class to subclass or extend for
  `Classroom`; add `student_capacity`, `board_type`, and `acoustic_panel_coverage`
  parameters to the `__init__` signature.
- `infinigen/core/constraints/example_solver/room/predefined.py` — add
  `classroom` to the room-type registry with forward-facing desk constraint.
- `infinigen/assets/seating/` — add or tag a `classroom_chair` asset with
  forward-facing orientation lock.
- `infinigen/assets/wall_decorations/` — add `whiteboard`, `blackboard`,
  `projector_screen`, and `smartboard` assets for the front focal wall.
- `infinigen/assets/ceiling/` — add `acoustic_panel` asset controlled by the
  `acoustic_panel_coverage` scalar.
- `infinigen/examples/configs_indoor/classroom.gin` — new gin config file
  specifying classroom-specific defaults and constraints.

---

## 5. Literature Backing

**Vartanian et al. (2015)** — justifies `ceiling_height_m` range 2.4–4.0 m;
their study found significant approach-avoidance and beauty effects across the
2.4–3.0 m band, extended upward to 4.0 m for large lecture halls.

**Meyers-Levy & Zhu (2007)** — justifies the default of 3.0 m for
`ceiling_height_m`; ceilings above 2.7 m promote relational, abstract thinking
beneficial for learning tasks.

**Joye (2007)** — justifies `student_capacity` (10–60) and
`acoustic_panel_coverage`; crowding and noise are the two dominant cognitive-load
drivers in classroom environments.

**Münch et al. (2020)** — justifies `daylight_intensity` default of 0.6;
morning daylight is the primary circadian and alertness regulator for students
during daytime classes.

**Kaplan & Kaplan (1989)** — justifies `biophilia_count` (0–6); attention
restoration theory predicts that nature contact reduces directed-attention
fatigue during extended learning sessions.

**Ulrich (1991)** — justifies `wall_warmth_index` and `board_type`; material
warmth and surface contrast are identified as primary wellness and engagement
variables in knowledge-work environments.
