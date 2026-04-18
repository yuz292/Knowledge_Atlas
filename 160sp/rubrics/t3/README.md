# Track 3 — VR rubric overview

*Last updated: 2026-04-17*

## Track-level allocation (75 points)

| Deliverable | Span | Hardness | Points | Rubric file |
|-------------|:----:|:--------:|-------:|-------------|
| T3.a Unity environment + hello-scene commit | Week 3 | Easy | 5 | `T3.a_hello_scene.md` |
| T3.b First interactive scene (one T1-framework mapping) | Weeks 3–4 | Medium | 10 | `T3.b_first_scene.md` |
| T3.c Second scene + reusable component library | Weeks 4–5 | Medium-hard | 12 | `T3.c_second_scene.md` |
| T3.d Performance pass — 72 Hz on target hardware | Week 5 | Hard | 10 | `T3.d_performance.md` |
| T3.e User-study pilot (n = 3) with pre/post survey | Weeks 6–7 | Hard | 15 | `T3.e_user_pilot.md` |
| T3.f Polish + documentation for Fall handoff | Weeks 7–8 | Medium-hard | 13 | `T3.f_polish.md` |
| T3.g Final demo + reflection | Week 8 | Easy | 10 | `T3.g_final_demo.md` |
| **Total** | | | **75** | |

## Primary signals the AI grader reads

- `git log` in `160sp/tracks/t3/{student_id}/`: commit count, diff stats, files touched.
- Unity `.scene` and `.prefab` files: the grader reads the YAML representation to check scene composition and component count.
- Profiler JSON output (for T3.d): frame-time distribution.
- Screencast MP4 / video URL (for T3.b, T3.c, T3.g): the grader receives a student-written transcript describing what happens in the video, plus the video itself for the instructor / TA audit.
- Survey data + write-up (for T3.e): structured CSV in the repo plus prose interpretation.

## Track-specific conventions

- **VR demo aesthetics are not AI-graded.** The grader checks interaction fidelity (does the button actually toggle the light? does the gaze-target move the highlight?) via the student's written scene-log, not via visual inspection. Aesthetic judgements are instructor-only at T3.g.
- **Performance is measurable.** T3.d requires 72 Hz at 95th percentile on the target hardware (Quest 3 by default); this is a hard numeric threshold in the rubric.
- **User-study ethics.** T3.e requires IRB-equivalent class protocol: consent form, anonymised data, pilot-n of 3 (instructor-cleared for class use, not publication).
