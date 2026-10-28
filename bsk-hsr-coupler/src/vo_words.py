#!/usr/bin/env python3
"""VO lock + word timestamps + event retime.

usage: python src/vo_words.py [--model large-v3] [--apply]
  1. hashes and measures every file in audio/VO_LOCK.json (sha256, duration, sample rate)
  2. faster-whisper word timestamps (Korean) -> audio/VO_WORDS.json (world frames via place_F)
  3. for each event word: target event F = word onset F - lead(preferred), checked against [min,max] lead and the shot window
  4. --apply writes the new targets into src/rig_config.json events_target (world_F and local_F); then re-run the pipeline
Requires: pip install faster-whisper soundfile
"""
import json, os, sys, hashlib, argparse, unicodedata
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); AUD = os.path.join(ROOT, "audio")
ap = argparse.ArgumentParser(); ap.add_argument("--model", default="large-v3"); ap.add_argument("--apply", action="store_true")
args = ap.parse_args()
LOCKP = os.path.join(AUD, "VO_LOCK.json"); LOCK = json.load(open(LOCKP)); FPS = LOCK["fps"]
def norm(s): return unicodedata.normalize("NFC", "".join(ch for ch in s if ch.isalnum()))

# 1 measure
for key, f in LOCK["files"].items():
    p = os.path.join(AUD, f["file"])
    if not os.path.exists(p): f["status"] = "MISSING"; continue
    info = sf.info(p); f.update({"sha256": hashlib.sha256(open(p, "rb").read()).hexdigest(), "duration_s": round(info.duration, 4),
                                 "samplerate": info.samplerate, "channels": info.channels, "end_F": f["place_F"] + round(info.duration * FPS), "status": "OK"})

# 2 words
from faster_whisper import WhisperModel
model = WhisperModel(args.model, device="auto", compute_type="auto"); words = {}
for key, f in LOCK["files"].items():
    if f.get("status") != "OK": continue
    segs, _ = model.transcribe(os.path.join(AUD, f["file"]), language="ko", word_timestamps=True, vad_filter=False)
    words[key] = [{"w": w.word.strip(), "t0": round(w.start, 3), "t1": round(w.end, 3), "F0": f["place_F"] + round(w.start * FPS), "F1": f["place_F"] + round(w.end * FPS)}
                  for s in segs for w in s.words]
json.dump(words, open(os.path.join(AUD, "VO_WORDS.json"), "w"), ensure_ascii=False, indent=2)

# 3 overlaps between consecutive selected files
sel = LOCK["selection"]; used = []
for key in ("S1a", "S1b", "S2a", sel["S2b"], sel["S3a"], "S3b", "S5a", "S5b"):
    f = LOCK["files"][key]
    if f.get("status") == "OK": used.append((f["place_F"], f["end_F"], key))
used.sort(); report = {"overlaps": [], "events": {}, "violations": []}
for (a0, a1, ka), (b0, b1, kb) in zip(used, used[1:]):
    if a1 + 6 > b0: report["overlaps"].append(f"{ka} ends F{a1} but {kb} starts F{b0} (need >=6F gap)")
if used and used[-1][1] > 1260 - 15: report["violations"].append(f"last VO ends F{used[-1][1]} (loop tail needs >=15F silence before F1260)")

# 4 events
CFG = json.load(open(os.path.join(HERE, "rig_config.json"))); lead = LOCK["lead_frames"]
for test, evs in LOCK["event_words"].items():
    T = CFG[test]; win = LOCK["shot_windows"]["JP" if "shibata" in test else "SCH"]
    for ev, (slot, word) in evs.items():
        key = sel.get(slot, slot); hit = next((w for w in words.get(key, []) if norm(word) in norm(w["w"])), None)
        if hit is None: report["violations"].append(f"{ev}: word '{word}' not found in {key}"); continue
        tgt = hit["F0"] - lead["preferred"]; report["events"][ev] = {"word": hit["w"], "word_F": hit["F0"], "target_world_F": tgt}
        if not (win[0] <= tgt <= win[1]):
            alt = hit["F0"] - lead["max"]
            msg = f"{ev}: target F{tgt} outside shot window {win}"
            if win[0] <= alt <= win[1]: msg += f"; lead {lead['max']}F gives F{alt} (inside) -> use that"; report["events"][ev]["target_world_F"] = alt
            else: report["violations"].append(msg + " -> move place_F, switch variant, or adjust cut by <=6F"); continue
        local = report["events"][ev]["target_world_F"] - T["world_frame_start"] + 1
        report["events"][ev]["target_local_F"] = local
        if args.apply and ev in T["events_target"]:
            T["events_target"][ev].update({"world_F": report["events"][ev]["target_world_F"], "local_F": local, "source": f"VO_WORDS {key} '{hit['w']}' F{hit['F0']} - lead", "status": "LOCK"})
    E = T["events_target"][next(k for k in T["events_target"] if k.endswith("LOCKED"))]["local_F"]
    if E + 59 > T["bake_frames"]:
        report["violations"].append(f"{test}: G3 window needs bake_frames >= {E + 59} (now {T['bake_frames']})")
        if args.apply: T["bake_frames"] = E + 59
    if args.apply:   # keep the post-lock tension pull after the (possibly moved) lock event
        T["motion"]["tension_pull_frames"] = [E + 25, max(T["bake_frames"], E + 59)]
if args.apply: json.dump(CFG, open(os.path.join(HERE, "rig_config.json"), "w"), indent=2, ensure_ascii=False)
json.dump(LOCK, open(LOCKP, "w"), indent=2, ensure_ascii=False)
json.dump(report, open(os.path.join(AUD, "vo_sync_report.json"), "w"), ensure_ascii=False, indent=2)
print(json.dumps(report, ensure_ascii=False, indent=2))
sys.exit(1 if report["violations"] or report["overlaps"] else 0)
