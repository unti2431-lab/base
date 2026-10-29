"""제동·거리 근거 계산 (R3). 영상의 모든 거리 수치는 이 파일 출력만 쓴다.

가정 (화면·설명란에 그대로 표기):
  - 감속도는 일정하다고 본다. 고속 비상제동 대표값 1.0 m/s^2
    (TGV 300 km/h -> 약 3.5 km, CRH 300 km/h -> 2.8~3.3 km 보고치와 정합: 0.99~1.25 m/s^2)
  - 보수 하한 0.8 m/s^2 (점착 저하·하강구배 여유)
  - 반응·제동 체결 시간 2 s (그 동안 등속)
  - 편성 길이 200 m (화면 비유 단위. Frecciarossa 1000 = 약 202 m)
실제 사고 열차의 제동 성능·구배·점착 조건을 재현한 값이 아니다.
"""
import json, sys

def stop(v_kmh, a, t_react=2.0):
    v = v_kmh / 3.6
    react = v * t_react
    brake = v * v / (2 * a)
    return {"v_kmh": v_kmh, "a_mps2": a, "react_m": round(react, 1),
            "brake_m": round(brake, 1), "total_m": round(react + brake, 1),
            "brake_s": round(v / a, 1), "trainsets_200m": round((react + brake) / 200, 2)}

rows = [stop(v, a) for v in (40, 137, 200) for a in (1.0, 0.8)]

# 보도 수치 정합: 08:36 운행 재개 지시 -> 08:53~54 충돌, 25 km
corridor = {}
for minutes in (17, 18):
    corridor[f"avg_kmh_{minutes}min"] = round(25 / (minutes / 60), 1)
corridor["minutes_at_40kmh"] = round(25 / 40 * 60, 1)   # 시계운전 상한으로 25 km를 갈 때
corridor["minutes_at_200kmh"] = round(25 / 200 * 60, 1)

out = {"assumption": {"a_main": 1.0, "a_conservative": 0.8, "t_react_s": 2.0, "trainset_m": 200},
       "stopping": rows, "corridor_25km": corridor,
       "screen_values": {  # 두 가정(a=1.0/0.8) 모두에서 참인 경계값만 화면·내레이션에 쓴다
           "N3_200kmh_over_km": 1.5,    # 1.65~2.04 km -> "1.5 km 넘게"
           "N7_40kmh_within_m": 100}}   # 84~99 m -> "100 m 안에"
s200 = [r["total_m"] for r in rows if r["v_kmh"] == 200]
s40 = [r["total_m"] for r in rows if r["v_kmh"] == 40]
assert min(s200) > out["screen_values"]["N3_200kmh_over_km"] * 1000
assert max(s40) < out["screen_values"]["N7_40kmh_within_m"]
json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
