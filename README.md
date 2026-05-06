# 整体院誠天 東加古川院 — 1週間-1kg ダイエットLINE講座 LP

40〜50代女性のための、教育型ロングLP。理学療法士・筒井智久院長監修の無料LINE講座への導線。

## Stack

- 静的HTML / CSS / Vanilla JS（ビルドなし）
- 日本語フォント: Noto Serif JP（見出し）, Noto Sans JP（本文）
- ホスティング: Cloudflare Pages

## Local

```sh
python3 -m http.server 8765
# → http://localhost:8765/
```

## Files

```
index.html              # 全セクション
assets/css/styles.css   # デザイントークン + 全スタイル
assets/js/script.js     # スクロールリベール / フローティングCTA
assets/images/          # 33枚の画像（最適化済み）
```

## Deploy

```sh
npx wrangler pages deploy . --project-name=tsutsui-lp
```
