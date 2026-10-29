#!/usr/bin/env python3
"""FLOW_A_R2.md 의 프롬프트 블록에서 [LOCK] 태그를 LOCKS.md 본문으로 바꿔
붙여 넣을 완성 프롬프트를 prompts/out/K##_{CLEAN,INFO,MP4}.txt 로 쓴다.

LOCK 문구는 LOCKS.md 한 곳에서만 고친다. 이 스크립트는 복사만 한다.
사용: python3 prompts/build_prompts.py [--src prompts/FLOW_A_R2.md]
"""
import argparse, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent


def load_locks(path):
    text = path.read_text(encoding="utf-8")
    locks = {}
    # "## [TAG]" 헤딩(뒤에 ← 주석이 붙을 수 있음) 다음 첫 ``` 블록이 본문
    for m in re.finditer(r"^## (\[[^\]]+\])[^\n]*\n(.*?)```\n(.*?)```", text, re.S | re.M):
        tag, body = m.group(1), m.group(3).strip()
        locks[tag] = body
    return locks


def iter_prompts(md):
    cut = None
    kind = None
    for block in re.split(r"(```.*?```)", md, flags=re.S):
        if block.startswith("```"):
            if cut and kind:
                yield cut, kind, block.strip("`").strip("\n")
                kind = None
            continue
        h = re.findall(r"^### (K\d\d)", block, re.M)
        if h:
            cut = h[-1]
        k = re.findall(r"\*\*(CLEAN|INFO|MP4)\b", block)
        kind = k[-1] if k else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(HERE / "FLOW_A_R2.md"))
    ap.add_argument("--locks", default=str(HERE / "LOCKS.md"))
    ap.add_argument("--out", default=str(HERE / "out"))
    a = ap.parse_args()

    locks = load_locks(pathlib.Path(a.locks))
    out = pathlib.Path(a.out)
    out.mkdir(exist_ok=True)
    md = pathlib.Path(a.src).read_text(encoding="utf-8")

    unresolved, written = [], []
    for cut, kind, body in iter_prompts(md):
        for tag, text in locks.items():
            body = body.replace(tag, text)
        left = re.findall(r"\[[A-Z][A-Z —\-]+LOCK[^\]]*\]", body)
        if left:
            unresolved.append((cut, kind, left))
        p = out / f"{cut}_{kind}.txt"
        p.write_text(body.strip() + "\n", encoding="utf-8")
        written.append(p.name)

    print(f"locks: {sorted(locks)}")
    print(f"written {len(written)}: {' '.join(written)}")
    if unresolved:
        print("UNRESOLVED:", unresolved)
        sys.exit(1)


if __name__ == "__main__":
    main()
