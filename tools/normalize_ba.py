#!/usr/bin/env python3
"""
ba-1.png 〜 ba-5.png の統一フォーマット化スクリプト。

- 共通サイズ：幅1080px、高さは中身に合わせて 800〜1200px の範囲に収める
- 背景色：#fffaf3（既存LPデザイントークン --bg-card と同色）
- 内側マージン：24px
- 元画像のアスペクト比は保持（letterbox 風、白背景で囲む）
- 元のキャプション・数値テキストはそのまま保持（リサイズのみ）
- 元ファイルは上書き保存・PNG最適化
"""
from PIL import Image
from pathlib import Path
import sys

DIR = Path(__file__).resolve().parent.parent / "assets" / "images"
TARGET_W = 1080
H_MIN = 800
H_MAX = 1200
BG = (255, 250, 243)  # #fffaf3
PAD = 24


def process(file: Path) -> tuple[tuple[int, int], tuple[int, int], int, int]:
    """Returns (orig_size, new_size, orig_bytes, new_bytes)."""
    orig_bytes = file.stat().st_size
    img = Image.open(file).convert("RGB")
    ow, oh = img.size

    # 1. 横幅 1080-2*PAD にフィット
    inner_w = TARGET_W - 2 * PAD
    scale = inner_w / ow
    new_w = inner_w
    new_h = int(oh * scale)

    # 2. 縦が H_MAX を超えるなら、縦を H_MAX-2*PAD に合わせて再計算
    inner_h_max = H_MAX - 2 * PAD
    if new_h > inner_h_max:
        scale = inner_h_max / oh
        new_h = inner_h_max
        new_w = int(ow * scale)

    # 3. 縦が H_MIN-2*PAD 未満なら、 H_MIN に揃える（上下に余白）
    canvas_h = max(new_h + 2 * PAD, H_MIN)

    img_resized = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (TARGET_W, canvas_h), BG)
    # 中央配置
    px = (TARGET_W - new_w) // 2
    py = (canvas_h - new_h) // 2
    canvas.paste(img_resized, (px, py))

    canvas.save(file, optimize=True)
    return (ow, oh), canvas.size, orig_bytes, file.stat().st_size


def main() -> int:
    rows = []
    for i in range(1, 6):
        f = DIR / f"ba-{i}.png"
        if not f.exists():
            print(f"!! {f} not found, skipping", file=sys.stderr)
            continue
        orig, new, ob, nb = process(f)
        rows.append((f.name, orig, new, ob, nb))

    # 結果表示
    print(f"{'file':10} | {'orig WxH':>13} | {'new WxH':>13} | {'orig KB':>8} | {'new KB':>8}")
    print("-" * 70)
    for name, orig, new, ob, nb in rows:
        print(
            f"{name:10} | {orig[0]:>5}x{orig[1]:<6} | {new[0]:>5}x{new[1]:<6} | "
            f"{ob // 1024:>6} KB | {nb // 1024:>6} KB"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
