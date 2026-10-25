"""4단 텔레스코픽 붐: 실린더 1개 + 신장/회수 와이어 2조 기구학 풀이와 독립 검증.

좌표: 붐 축 방향 x(기초붐 S1 로컬). d(t)=실린더 스트로크.
각 단 Sk는 앞 단 위에서 d만큼 미끄러짐 -> 월드(S1 기준) 변위 = (k-1)*d.
와이어는 직선 2구간 + 시브 180도 감김(pi*r)으로 해석적으로 배치한다.
"""
import numpy as np

CFG = dict(
    stroke=1.0,        # m, 실린더 최대 스트로크
    sheave_r=0.09,     # m, 시브 피치 반경
    sec_len=3.0,       # m, 각 단 길이(단순화: 동일)
    tail_off=0.15,     # m, 다음 단 꼬리 고정점이 그 단 후단에서 앞쪽으로 떨어진 거리
    anchor_off=0.40,   # m, 앞 단 고정점이 그 단 후단에서 앞쪽으로 떨어진 거리
    fps=30, frames=1080,
)

def section_x(d, k):
    """Sk 후단의 S1 기준 x. S1=0, S2=d, S3=2d, S4=3d (겹침 초기값은 0으로 단순화)."""
    return (k - 1) * d

def ext_rope(d, k, c):
    """k단(시브 보유)이 k-1단 고정점 -> k단 앞머리 시브 -> k+1단 꼬리 를 잇는 신장 와이어."""
    anchor = section_x(d, k - 1) + c['anchor_off']
    sheave = section_x(d, k) + c['sec_len']            # 앞머리 시브 중심
    tail = section_x(d, k + 1) + c['tail_off']
    return (sheave - anchor) + (sheave - tail) + np.pi * c['sheave_r'], sheave

def ret_rope(d, k, c):
    """k+1단 꼬리 -> k단 후단 시브 -> k-1단 앞쪽 고정점 를 잇는 회수 와이어."""
    sheave = section_x(d, k)                            # 후단 시브 중심
    tail = section_x(d, k + 1) + c['tail_off']
    anchor = section_x(d, k - 1) + c['sec_len'] - 0.2
    return (tail - sheave) + (anchor - sheave) + np.pi * c['sheave_r'], sheave

def master_d(n, c):
    t = np.arange(n) / c['fps']
    T = t[-1]
    s = 0.5 - 0.5 * np.cos(2 * np.pi * t / T)           # 0 -> 1 -> 0 루프
    return c['stroke'] * s

def verify(c=CFG):
    d = master_d(c['frames'], c)
    out = {}
    for k in (2, 3):                                    # 시브는 S2, S3 에 있음
        Le, _ = ext_rope(d, k, c)
        Lr, _ = ret_rope(d, k, c)
        out[f'ext_rope_S{k}_len_dev_mm'] = float(np.ptp(Le) * 1e3)
        out[f'ret_rope_S{k}_len_dev_mm'] = float(np.ptp(Lr) * 1e3)
    # 시브 회전: 와이어 상대속도 = 시브 대비 꼬리 속도 = d' -> omega = d'/r
    dd = np.gradient(d) * c['fps']
    theta = np.cumsum(dd / c['sheave_r']) / c['fps']
    out['sheave_max_rev'] = float(theta.max() / (2 * np.pi))
    out['world_ratio_S2_S3_S4'] = [float(section_x(c['stroke'], k) / c['stroke']) for k in (2, 3, 4)]
    out['PASS'] = all(v < 0.5 for kk, v in out.items() if kk.endswith('_mm'))
    return out

if __name__ == '__main__':
    import json
    print(json.dumps(verify(), indent=2, ensure_ascii=False))
