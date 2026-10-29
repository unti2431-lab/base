BSK-HSR-COUPLER R10 DELTA (overlay)
Unzip INTO the existing BSK-HSR-COUPLER folder (same parent), overwrite = yes.
Contains only what changed in R10:
  src/spring_helix.py            (new, L07 helix spring)
  src/build_schB.py              (R9-2 materials + helix spring)
  src/build_shibataA.py          (helix spring)
  src/rig_config.json            (TEST A camera distance 1.6 m)
  src/encode_preview.sh          (first-frame fix)
  review/shibA_key4s_R91_F80-199.mp4 (+ _stress2M, _contact)   L05 540p
  review/schB_key4s_R92_F60-179.mp4  (+ _stress2M, _contact)   L06 540p
  review/R09_1, R09_2, R10_L07 CHANGELOG.md
  audio/VO_LOCK.TEMPLATE.json, LOCKS.md, TASKS.json, REPORT.md, CCL_R10_DELTA.md, OPUS_BRIEF_R10.md, START_HERE.md
Check after unzip: src/build_schB.py must contain "spring_helix"; rig_config test_A_shibata.camera.distance must be 1.6
