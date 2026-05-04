# Manifest Rationale
**Student:** Yuxuan Zhang  
**Room Types:** Bathroom, Hallway/Corridor  
**Date:** 2026-04-30

---

## Bathroom — Range and Citation Justification

### ceiling_height_m (1.8–3.0 m, default 2.4 m)
Vartanian et al. (2015) studied ceiling heights between 2.4 m and 3.0 m and
found significant effects on beauty judgments and approach-avoidance decisions.
The lower bound of 1.8 m reflects the minimum building-code clearance for
habitable spaces in most jurisdictions and represents the strongest enclosure
condition studied. Meyers-Levy & Zhu (2007) found that ceilings below 2.4 m
prime concrete, detail-oriented processing — relevant to grooming tasks performed
in bathrooms. The upper bound of 3.0 m is set below the living-room maximum
because bathrooms rarely exceed this height in residential construction, keeping
the range empirically grounded.

### daylight_intensity (0.0–1.0, default 0.5)
Münch et al. (2020) identify bathrooms as a critical site for morning light
exposure that entrains the circadian system. The normalised 0–1 range maps to
the sun-contribution scalar in the Infinigen renderer. A default of 0.5 reflects
a frosted-glass window — the most common bathroom glazing — which admits
diffuse light without direct solar gain. Kaplan & Kaplan (1989) support the
inclusion of daylight as a restoration cue even in small enclosed spaces.

### tile_material_id (enum, default white_ceramic)
Ulrich (1991) identifies surface material as a primary wellness variable in
enclosed healthcare and hygiene spaces. The six enum values span the warm-cool
and light-dark axes that the literature identifies as relevant: white_ceramic
(clinical, high cleanliness perception), marble (luxury, low stress), terracotta
(warm, biophilic), dark_slate (low arousal). The enum is preferred over a
continuous index because tile materials are categorically distinct in the
Infinigen asset library and cannot be meaningfully interpolated.

### fixture_count (2–6, default 3)
Joye (2007) links object density to complexity perception and restorative
capacity. The minimum of 2 (toilet + sink) is the functional floor for any
bathroom. The maximum of 6 covers a full en-suite (toilet, sink, shower,
bathtub, towel rail, mirror). The default of 3 reflects a standard bathroom.
Values outside this range either produce a non-functional room (below 2) or
exceed the spatial capacity of a standard bathroom footprint (above 6).

### wall_warmth_index (0.0–1.0, default 0.4)
Ulrich (1991) reports warm material palettes reduce physiological stress markers
in enclosed spaces. The default of 0.4 (slightly cool) reflects the clinical
association of bathrooms with hygiene and cleanliness, which correlates with
cooler, lighter palettes. Meyers-Levy & Zhu (2007) provide further support for
the interaction between colour temperature and ceiling height on mood.

### biophilia_count (0–3, default 1)
Kaplan & Kaplan (1989) identify plant presence as a reliable restoration trigger.
The upper bound of 3 is set lower than in other room types because bathroom
footprints are typically 4–6 m², limiting the number of plants that can be
placed without causing clutter — which would reverse the restorative effect per
Joye (2007). A default of 1 reflects the common practice of a single small plant
on a shelf or windowsill.

---

## Hallway / Corridor — Range and Citation Justification

### ceiling_height_m (2.0–3.5 m, default 2.7 m)
Vartanian et al. (2015) is the primary citation. Their study found significant
effects of ceiling height on approach-avoidance decisions across the 2.4–3.0 m
band. The range is extended to 2.0 m at the lower end (minimum habitable
clearance) and 3.5 m at the upper end (grand civic corridor scale) to allow
exploration of enclosure effects beyond the residential band. The default of
2.7 m reflects the most common residential corridor height.

### corridor_width_m (0.9–2.4 m, default 1.2 m)
Vartanian et al. (2015) and Joye (2007) both identify spatial constriction as a
driver of avoidance responses. The minimum of 0.9 m is the ADA-compliant
minimum for single-occupancy passage. The maximum of 2.4 m represents a
generous gallery-width corridor. The default of 1.2 m is the standard residential
hallway width. This parameter has no direct equivalent in the living-room
manifest, making it the distinctive contribution of the hallway typology.

### wall_material_id (enum, default white_plaster)
Ulrich (1991) identifies material warmth as a primary wellness variable in
enclosed spaces. Five enum values are provided spanning the warm-cool and
texture axes. The enum is preferred over a continuous index for the same reason
as tile_material_id in the bathroom manifest: Infinigen's asset library treats
wall materials as categorically distinct.

### daylight_intensity (0.0–1.0, default 0.4)
Kaplan & Kaplan (1989) identify prospect-refuge balance as critical in corridor
design: a hallway that terminates in darkness produces refuge without prospect,
which reduces restoration. Münch et al. (2020) support daylight access as an
alertness cue. The default of 0.4 is lower than the living room (0.6) because
hallways typically have fewer and smaller windows.

### biophilia_count (0–4, default 1)
Kaplan & Kaplan (1989) and Ulrich (1991) support plant presence as a restoration
cue in transitional spaces. The upper bound of 4 is higher than the bathroom
because corridors are longer linear spaces that can accommodate plants at
intervals without clutter. The default of 1 reflects a single plant at the
corridor terminus, a common interior design practice.

### wall_warmth_index (0.0–1.0, default 0.5)
Meyers-Levy & Zhu (2007) show that warm palettes under lower ceilings can
partially compensate for enclosure-driven avoidance responses. Ulrich (1991)
provides the primary empirical basis for warmth as a wellness variable. The
default of 0.5 (neutral) reflects the fact that hallways serve diverse functions
and a neutral baseline is most generalisable.

---

## References (APA)

Joye, Y. (2007). Architectural lessons from environmental psychology: The case
of biophilic architecture. *Review of General Psychology, 11*(4), 305–328.
https://doi.org/10.1037/1089-2680.11.4.305

Kaplan, R., & Kaplan, S. (1989). *The experience of nature: A psychological
perspective.* Cambridge University Press.

Meyers-Levy, J., & Zhu, R. (2007). The influence of ceiling height: The effect
of priming on the type of processing that people use. *Journal of Consumer
Research, 34*(2), 174–186. https://doi.org/10.1086/519146

Münch, M., Wirz-Justice, A., Brown, S. A., Kantermann, T., Martiny, K.,
Stefani, O., Vetter, C., Wright, K. P., Wulff, K., & Skene, D. J. (2020).
The role of daylight for humans: Gaps in current knowledge. *Clocks & Sleep,
2*(1), 61–85. https://doi.org/10.3390/clockssleep2010008

Ulrich, R. S. (1991). Effects of interior design on wellness: Theory and recent
scientific research. *Journal of Health Care Interior Design, 3*, 97–109.

Vartanian, O., Navarrete, G., Chatterjee, A., Fich, L. B., Leder, H.,
Modroño, C., Rostrup, N., Skov, M., Corradi, G., & Nadal, M. (2015).
Architectural design and the brain: Effects of ceiling height and perceived
enclosure on beauty judgments and approach-avoidance decisions. *Journal of
Environmental Psychology, 41*, 10–18.
https://doi.org/10.1016/j.jenvp.2014.11.006
