# Splat Capture Notes

**Student:** Yuxuan Zhang
**Date:** 2026-05-03
**Room type captured:** Bathroom

## Capture Details
- **Device:** iPhone (video-based capture)
- **Cloud service:** Polycam (free tier)
- **Processing time:** approximately 3 minutes
- **Output format:** GLB (free tier; .splat export requires paid tier)

## Process
Walked around the bathroom for approximately 45 seconds, sweeping the camera
slowly to cover all four walls, the floor, and the ceiling.

## Script Execution
splat_to_hdri.py raised a SyntaxError at line 123 (bytes/nonbytes literal
mix, Python 3.11 compatibility issue). A stub HDR was written per the scaffold
specification.

## Surface Quality Assessment
- **Wall tiles:** Clean capture, good geometry and colour fidelity
- **Floor tiles:** Clean capture, minimal noise
- **Ceiling:** Slightly noisy due to uniform white surface
- **Mirror:** Highly noisy, reflective surfaces confuse the SH fitter

## Failed Retries
None. Single capture attempt was sufficient.
