#!/usr/bin/env python3
"""R8(R006 컷 구조) 내레이션 비트 파일 생성: 현재 대본(current)과 제안 대본(proposed)."""
import json, sys
from pathlib import Path

SHOTS = [("S01", 1, 90), ("S02", 91, 198), ("S03", 199, 288), ("S04", 289, 396), ("S05", 397, 504),
         ("S06", 505, 603), ("S07", 604, 702), ("S08", 703, 810), ("S09", 811, 900)]

def cuts(s03_subject, tunnel_in_s02):
    reveal = {"S01": ["E5", "EMU370"], "S02": ["E5"], "S03": ["TUNNEL", s03_subject], "S04": ["EMU370"],
              "S05": ["E5", "BOGIE"], "S06": ["E5", "WHEEL"], "S07": ["E5", "PANTO"], "S08": ["EMU370"],
              "S09": ["E5", "EMU370"]}
    out = []
    for sid, a, b in SHOTS:
        ev = [{"f": a, "what": f"{sid} 시작", "reveals": reveal[sid]}, {"f": (a + b) // 2, "what": f"{sid} 중간 사건"}]
        if sid == "S02" and tunnel_in_s02:
            ev.append({"f": 135, "what": "원경에 터널 후드 진입", "reveals": ["TUNNEL"]})
        out.append({"id": sid, "frames": [a, b], "events": sorted(ev, key=lambda e: e["f"])})
    return out

CURRENT = [
    ("L1", [4, 86], "이 두 열차, 코부터 다릅니다.", "이 두 열차, 코부터 다릅니다.", []),
    ("L2", [95, 194], "E5의 긴 코에는, 터널을 고려한 설계가 담겼죠.", "이오의 긴 코에는, 터널을 고려한 설계가 담겼죠.",
     [{"key": "E5", "reading": "이오"}]),
    ("L3", [203, 284], "터널 진입 순간, 공기가 압축되기 때문입니다.", "터널 진입 순간, 공기가 압축되기 때문입니다.",
     [{"key": "TUNNEL", "reading": "터널"}]),
    ("L4", [293, 392], "EMU-370도 공기저항을 줄이려 앞머리를 다듬죠.", "이엠유 삼칠공도 공기저항을 줄이려 앞머리를 다듬죠.",
     [{"key": "EMU370", "reading": "이엠유"}]),
    ("L5", [401, 500], "차체 아래의 대차는 무게를 받치고,", "차체 아래의 대차는 무게를 받치고,", [{"key": "BOGIE", "reading": "대차"}]),
    ("L6", [509, 599], "바퀴와 레일은 맞닿아 힘을 전달합니다.", "바퀴와 레일은 맞닿아 힘을 전달합니다.", [{"key": "WHEEL", "reading": "바퀴"}]),
    ("L7", [608, 698], "지붕 위 팬터그래프는 전기를 받아오죠.", "지붕 위 팬터그래프는 전기를 받아오죠.", [{"key": "PANTO", "reading": "팬터"}]),
    ("L8", [707, 806], "공기, 힘, 전기. 모두 맞춰야 하는 설계.", "공기, 힘, 전기. 모두 맞춰야 하는 설계.", []),
    ("L9", [815, 896], "얼굴은 달라도, 속도를 만드는 건 열차 전체입니다.", "얼굴은 달라도, 속도를 만드는 건 열차 전체입니다.", []),
]

PROPOSED = [
    ("P1", [4, 86], "신칸센 E5, 한국 EMU-370. 코부터 다릅니다.", "신칸센 이오, 한국 이엠유 삼칠공. 코부터 다릅니다.",
     [{"key": "E5", "reading": "신칸센"}, {"key": "EMU370", "reading": "이엠유"}]),
    ("P2", [95, 284], "E5의 코는 무려 15미터. 터널에 들어갈 때 밀린 공기가, 출구에서 폭음으로 터지는 걸 줄이려는 거죠.",
     "이오의 코는 무려 십오 미터. 터널에 들어갈 때 밀린 공기가, 출구에서 폭음으로 터지는 걸 줄이려는 거죠.",
     [{"key": "E5", "reading": "이오"}, {"key": "TUNNEL", "reading": "터널"}]),
    ("P3", [293, 392], "EMU-370의 코는 10.2미터. 돌고래를 닮았죠.", "이엠유 삼칠공의 코는 십쩜이 미터. 돌고래를 닮았죠.",
     [{"key": "EMU370", "reading": "이엠유"}]),
    ("P4", [401, 500], "E5 대차엔, 흔들림을 스스로 잡는 액티브 서스펜션.", "이오 대차엔, 흔들림을 스스로 잡는 액티브 서스펜션.",
     [{"key": "E5", "reading": "이오"}, {"key": "BOGIE", "reading": "대차"}]),
    ("P5", [509, 599], "최고 속도에선, 바퀴가 1초에 30바퀴 넘게 돕니다.", "최고 속도에선, 바퀴가 일 초에 삼십 바퀴 넘게 돕니다.", [{"key": "WHEEL", "reading": "바퀴"}]),
    ("P6", [608, 698], "팬터그래프는 이 속도에도 전선을 놓치면 안 되죠.", "팬터그래프는 이 속도에도 전선을 놓치면 안 되죠.",
     [{"key": "PANTO", "reading": "팬터"}]),
    ("P7", [707, 806], "개발 중인 EMU-370, 목표는 370킬로.", "개발 중인 이엠유 삼칠공, 목표는 삼백칠십 킬로.",
     [{"key": "EMU370", "reading": "이엠유"}]),
    ("P8", [815, 896], "62년 신칸센의 320, 넘어설까요?", "육십이 년 신칸센의 삼백이십, 넘어설까요?", [{"key": "E5", "reading": "신칸센"}]),
]

def build(lines, s03_subject, tunnel_in_s02):
    return {"fps": 30, "frame_range": [1, 900], "rules": {"max_event_gap_frames": 90, "max_syllables_per_sec": 7.5},
            "cuts": cuts(s03_subject, tunnel_in_s02),
            "narration": [{"id": i, "frames": f, "text": t, "reading": r, "nouns": n} for i, f, t, r, n in lines]}

out = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent)
(out / "beats_r8_current.json").write_text(json.dumps(build(CURRENT, "EMU370", False), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(out / "beats_r8_proposed.json").write_text(json.dumps(build(PROPOSED, "E5", True), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
