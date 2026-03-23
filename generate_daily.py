"""
Poker Japan Daily - Automated daily generation script
Uses ANTHROPIC_API_KEY from GitHub Actions to generate content via Claude.
"""

import os
import anthropic
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
today = datetime.now(JST)
date_str = today.strftime("%Y年%m月%d日")
date_iso = today.strftime("%Y-%m-%d")

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PROMPT = f"""
あなたは日本ポーカー業界専門のトップ編集者です。
今日（{date_str}）の「Poker Japan Daily」の記事を、完全なHTML形式で生成してください。

【記事内容】
## 📰 今日のポーカーニュース
- 直近の海外トーナメント結果（Triton/WSOP/APT/WPT）を2〜3件
- 日本人プレイヤーの活躍があれば優先記載
- 業界ニュース

## 🎯 今日の戦略ワンポイント
- 実戦で使えるGTO or Exploit戦略、具体的なハンド例必須

## 🧠 今日のハンドクイズ
- スタック・ポジション・ボード明記の3沼、正解に✅

## 💰 今日のマインド・収支管理
- プロ思考を2〜3点

## 📊 今日の一言データ
- ROI・ITM率など数値ありの具体的統計

【HTMLデザイン】
- <!DOCTYPE html>から始まる単一ファイル
- ダークテーマ背景#0d0f14、ゴールド#e8c44a、ブルー#4a9fe8、グリーン#4ae87a
- max-width:720px、カード型、角丸と12px、レスポンシブ
- ヘッダーに「🂣 Poker Japan Daily」と{date_str}表示
- フッターに「Poker Japan Daily — 毎朝更新」
- system fontのみ使用、HTMLのみ出力

【ルール】日本語で出力、全体3〜5分、具体的な数値・ハンド必須
"""

print(f"[{date_str}] Generating Poker Japan Daily...")
message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=8192,
    messages=[{"role": "user", "content": PROMPT}]
)

html_content = message.content[0].text.strip()
if not html_content.startswith("<!DOCTYPE") and not html_content.startswith("<html"):
    import re
    m = re.search(r"```html\s*([\s\S]+?)```", html_content)
    if m:
        html_content = m.group(1).strip()

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Done: index.html ({len(html_content):,} chars)")
