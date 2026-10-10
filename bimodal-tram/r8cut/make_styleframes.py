# 인포그래픽·오버레이 스타일 시안 (편집 MG 제작 기준 참고용, 최종 그래픽 아님)
import sys, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A = sys.argv[1]; O = sys.argv[2]
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
f = lambda s: ImageFont.truetype(F, s)
W, H = 1920, 1080
INK = (14, 22, 28); PAPER = (236, 234, 228); CYAN = (64, 214, 214); AMBER = (238, 170, 60); RED = (232, 84, 70); WHITE = (255, 255, 255)
def load(n):
    return Image.open(f"{A}/{n}").convert('RGB').resize((W, H), Image.LANCZOS)
def badge(d, txt='AI 재현'):
    w = d.textlength(txt, font=f(26)) + 28
    d.rounded_rectangle((W - 60 - w, 50, W - 60, 92), 8, fill=(0, 0, 0, 150))
    d.text((W - 60 - w + 14, 56), txt, font=f(26), fill=WHITE)
def chip(d, x, y, txt, size=40, fill=(0, 0, 0, 170), fg=WHITE, accent=CYAN):
    w = d.textlength(txt, font=f(size)) + 44
    d.rounded_rectangle((x, y, x + w, y + size + 30), 10, fill=fill)
    d.rectangle((x, y, x + 6, y + size + 30), fill=accent)
    d.text((x + 26, y + 13), txt, font=f(size), fill=fg)
    return w
def dashed(d, p0, p1, dash=28, gap=18, **kw):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0); n = int(L // (dash + gap)) + 1
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        d.line((x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b), **kw)

# SF1 C001 고스트 레일
im = load('LOOP_WHEEL_L_FHD_UPSCALED.jpg'); ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
for (a, b) in [((-200, 1080), (1920, 640)), ((300, 1080), (1920, 800))]:
    dashed(d, a, b, width=10, fill=(*CYAN, 230))
cx, cy = 1180, 860
d.line((cx - 70, cy - 70, cx + 70, cy + 70), fill=(*RED, 255), width=16); d.line((cx - 70, cy + 70, cx + 70, cy - 70), fill=(*RED, 255), width=16)
chip(d, 120, 120, '레일 없음', 56, accent=RED)
badge(d)
Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB').save(f"{O}/SF1_C001_ghost_rails.jpg", quality=90)

# SF2 C022 휠 원더링 누적선 + 분포곡선
im = load('WET_CLEAN_L_FHD_UPSCALED.jpg'); ov = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(ov)
random.seed(4)
for yc in (330, 750):
    for i in range(46):
        y = yc + random.gauss(0, 34)
        d.line((0, y, 1500, y), fill=(*CYAN, 60), width=5)
d.rectangle((1500, 0, W, H), fill=(*INK, 215))
for yc in (330, 750):
    pts = [(1820 - 230 * math.exp(-((y - yc) / 46) ** 2), y) for y in range(yc - 160, yc + 161, 4)]
    d.line([(1820, yc - 160)] + pts + [(1820, yc + 160)], fill=(*CYAN, 255), width=5)
    d.line((1820, yc - 170, 1820, yc + 170), fill=(*WHITE, 120), width=2)
d.text((1530, 40), '바퀴 위치 분포', font=f(32), fill=WHITE)
d.text((1530, 1000), '개념도 · 수치 없음', font=f(24), fill=(*WHITE, 170))
chip(d, 80, 470, '휠 원더링  Wheel Wandering', 48)
d.rounded_rectangle((80, 60, 470, 130), 10, fill=(0, 0, 0, 160)); d.text((104, 74), '통과 46 / N회', font=f(38), fill=WHITE)
d.rectangle((0, 990, 1500, 1060), fill=(*INK, 190))
d.text((80, 1006), '매 통과는 직선 · 좌우 위치만 다름 · 원리 비교, 실험 결과 아님', font=f(26), fill=WHITE)
Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB').save(f"{O}/SF2_C022_wheel_wandering.jpg", quality=90)

# SF3 C033 탄성 vs 잔류 (풀 CG)
im = Image.new('RGB', (W, H), INK); d = ImageDraw.Draw(im, 'RGBA')
d.text((120, 90), '눌렸다가 돌아오는 변화와는 다릅니다', font=f(56), fill=PAPER)
for k, (x0, title, resid, col) in enumerate([(120, '탄성 변형 · 돌아옴', 0, CYAN), (1000, '소성 변형 · 일부 남음', 1, AMBER)]):
    d.rounded_rectangle((x0, 230, x0 + 800, 900), 18, outline=(*PAPER, 60), width=3)
    d.text((x0 + 40, 260), title, font=f(44), fill=col)
    base = 520; d.line((x0 + 40, base, x0 + 760, base), fill=(*PAPER, 120), width=3)
    d.text((x0 + 40, 820), '시간 →  (통과 1회)', font=f(28), fill=(*PAPER, 160))
    pts = []
    for i in range(0, 721, 6):
        t = i / 720
        dip = 230 * math.exp(-((t - 0.4) / 0.11) ** 2)
        r = (90 * (1 - math.exp(-max(0, t - 0.4) / 0.05)) if resid and t > 0.4 else 0)
        y = base + (dip if t <= 0.4 else max(dip, r))
        pts.append((x0 + 40 + i, y))
    d.line(pts, fill=col, width=7)
    if resid:
        d.line((x0 + 560, base, x0 + 560, base + 90), fill=(*AMBER, 255), width=3)
        d.text((x0 + 580, base + 20), '남는 변형', font=f(32), fill=AMBER)
d.text((120, 960), '개념도 · 눈금·수치 없음', font=f(28), fill=(*PAPER, 150))
im.save(f"{O}/SF3_C034_elastic_vs_residual.jpg", quality=90)

# SF4 C041~ 청라 타임라인 (배경 KF05 흐림)
im = load('KF05_L_FHD_UPSCALED.jpg').filter(ImageFilter.GaussianBlur(22)); ov = Image.new('RGBA', (W, H), (*INK, 205)); d = ImageDraw.Draw(ov)
d.text((120, 90), '청라 바이모달 트램 · 당시 기관 발표', font=f(52), fill=PAPER)
y = 560; d.line((120, y, 1800, y), fill=(*PAPER, 180), width=4)
nodes = [(220, '2017.06', '도입계획', '인천경제청', 0), (560, '2018.02', 'GRT 개통 발표', '바이모달 4월 예정 · 자기유도 2020 이후', 0),
         (900, '2018.04.18', '네 대 투입 발표', '4.21 운행 예정', 0), (1180, '2018.06', '후속 공지', '운행개시 언급', 0),
         (1440, '2020 이후', '자동유도', '당시 계획', 1), (1720, '2020.12', '기관 설명', '보강·개선 / 일부 누유 보수', 0)]
for x, dt, t1, t2, plan in nodes:
    if plan:
        for a in range(0, 360, 30): d.arc((x - 22, y - 22, x + 22, y + 22), a, a + 15, fill=AMBER, width=5)
    else:
        d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=CYAN)
    d.text((x - d.textlength(dt, font=f(34)) / 2, y - 90), dt, font=f(34), fill=PAPER)
    d.text((x - d.textlength(t1, font=f(32)) / 2, y + 40), t1, font=f(32), fill=AMBER if plan else WHITE)
    if t2: d.text((x - d.textlength(t2, font=f(24)) / 2, y + 88), t2, font=f(24), fill=(*PAPER, 190))
for i in range(4): d.rounded_rectangle((835 + i * 34, 700, 860 + i * 34, 740), 5, fill=(*CYAN, 230))
d.ellipse((120, 880, 146, 906), fill=CYAN); d.text((160, 876), '발표된 시행', font=f(28), fill=PAPER)
for a in range(0, 360, 30): d.arc((380, 880, 406, 906), a, a + 15, fill=AMBER, width=4)
d.text((420, 876), '당시 계획', font=f(28), fill=PAPER)
d.text((120, 980), '편집 요약 · 원문 화면 아님 | 출처: 인천경제청 2017.06.26·2018.02.05 / 인천교통공사 2018.04.18·06.11 / 2020.12.03', font=f(24), fill=(*PAPER, 170))
Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB').save(f"{O}/SF4_C042_cheongna_timeline.jpg", quality=90)
print('ok')
