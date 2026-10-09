#!/usr/bin/env python3
"""beats.json 규칙 검사. 실패하면 exit 1.

검사 항목
  G-B1 컷이 frame_range를 빈틈·겹침 없이 덮는다
  G-B2 사건 간격(컷 경계 포함) <= max_event_gap_frames
  G-B3 내레이션 발화 속도 <= max_syllables_per_sec (reading의 한글 음절 기준)
  G-B4 내레이션끼리 겹치지 않는다
  G-B5 명사가 들리는 추정 프레임에 그 대상이 현재 컷에서 이미 보인다
사용: python3 tools/check_beats.py [beats.json] [--json out.json]
"""
import json
import re
import sys
from pathlib import Path

HANGUL = re.compile(r"[가-힣]")


def syllables(s):
    return len(HANGUL.findall(s))


def cut_at(cuts, f):
    for c in cuts:
        if c["frames"][0] <= f <= c["frames"][1]:
            return c
    return None


def main():
    args = sys.argv[1:]
    out = None
    if "--json" in args:
        i = args.index("--json")
        out = args[i + 1]
        del args[i:i + 2]
    path = Path(args[0]) if args else Path(__file__).resolve().parent.parent / "src/config/beats.json"
    d = json.loads(path.read_text(encoding="utf-8"))
    fps, (f0, f1), r = d["fps"], d["frame_range"], d["rules"]
    cuts = d["cuts"]
    res, log = {}, []

    # G-B1
    ok, nxt = True, f0
    for c in cuts:
        a, b = c["frames"]
        if a != nxt or b < a:
            ok = False
            log.append(f"B1 {c['id']}: 시작 {a}, 기대 {nxt}")
        nxt = b + 1
    if nxt != f1 + 1:
        ok = False
        log.append(f"B1 끝 프레임 {nxt - 1}, 기대 {f1}")
    res["G-B1_cut_coverage"] = ok

    # G-B2
    marks = sorted({e["f"] for c in cuts for e in c["events"]} | {c["frames"][0] for c in cuts} | {f1 + 1})
    gaps = [(b - a, a, b) for a, b in zip(marks, marks[1:])]
    worst = max(gaps)
    res["G-B2_max_event_gap"] = worst[0] <= r["max_event_gap_frames"]
    log.append(f"B2 최대 사건 간격 {worst[0]}F ({worst[0] / fps:.2f}s) @F{worst[1]}–F{worst[2]}")
    for c in cuts:
        for e in c["events"]:
            if not c["frames"][0] <= e["f"] <= c["frames"][1]:
                res["G-B2_max_event_gap"] = False
                log.append(f"B2 {c['id']} 사건 F{e['f']}가 컷 범위 밖")

    # G-B3, G-B4, G-B5
    rate_ok, overlap_ok, noun_ok = True, True, True
    prev_end = 0
    for n in d["narration"]:
        a, b = n["frames"]
        dur = (b - a + 1) / fps
        syl = syllables(n["reading"])
        rate = syl / dur
        flag = "OK" if rate <= r["max_syllables_per_sec"] else "FAST"
        rate_ok &= flag == "OK"
        log.append(f"B3 {n['id']} {syl}음절 / {dur:.2f}s = {rate:.2f}음절/s {flag}")
        if a <= prev_end:
            overlap_ok = False
            log.append(f"B4 {n['id']} 시작 F{a} <= 이전 끝 F{prev_end}")
        prev_end = b
        for nn in n["nouns"]:
            pos = n["reading"].find(nn["reading"])
            if pos < 0:
                noun_ok = False
                log.append(f"B5 {n['id']} reading에 '{nn['reading']}' 없음")
                continue
            heard = a + round(syllables(n["reading"][:pos]) / syl * (b - a))
            c = cut_at(cuts, heard)
            seen = [e["f"] for e in c["events"] if nn["key"] in e.get("reveals", []) and e["f"] <= heard]
            good = bool(seen)
            noun_ok &= good
            log.append(f"B5 {n['id']} '{nn['reading']}'({nn['key']}) 추정 청취 F{heard} in {c['id']}"
                       f" → 노출 {('F' + str(min(seen))) if seen else '없음'} {'OK' if good else 'FAIL'}")
    res["G-B3_speech_rate"] = rate_ok
    res["G-B4_no_overlap"] = overlap_ok
    res["G-B5_noun_visible_first"] = noun_ok

    for line in log:
        print(line)
    allpass = all(res.values())
    print(json.dumps({"PASS": res, "ALL": allpass}, ensure_ascii=False, indent=2))
    if out:
        Path(out).write_text(json.dumps({"PASS": res, "ALL": allpass, "log": log}, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    sys.exit(0 if allpass else 1)


if __name__ == "__main__":
    main()
