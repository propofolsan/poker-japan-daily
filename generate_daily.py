"""
Poker Japan Daily - Automated daily generation script
Uses ANTHROPIC_API_KEY from GitHub Actions to generate content via Claude.
Generates a full modern media site with rich articles and real images.
"""

import os
import anthropic
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
today = datetime.now(JST)
date_str = today.strftime("%Y年%m月%d日")
date_iso = today.strftime("%Y-%m-%d")
date_display = today.strftime("%B %d, %Y")

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PROMPT = f"""あなたは日本のポーカーメディア「Poker Japan Daily」の編集長です。
今日は{date_str}です。今日の日刊ページを完全なHTML形式で生成してください。

━━━━━━━━━━━━━━━━━━━━━━━━━━
【重要：コンテンツ要件】
━━━━━━━━━━━━━━━━━━━━━━━━━━

■ トップ記事（FEATURED - 1本）
- 日本人プレイヤーの最新の国際大会での活躍に関する記事
- 800〜1200文字のしっかりした本文
- 大会名、賞金額、対戦相手、プレイの詳細を具体的に記述
- 出典リンクは実在の情報源名を記載

■ ブログ記事（ARTICLES - 4本以上）
各記事に以下を含む：
1. カテゴリタグ（RESULT / ANALYSIS / PLAYER / STRATEGY / LAW / TRITON / WSOP / JOPT）
2. 魅力的な見出し
3. 300〜500文字の要約文（薄い1行説明ではなく、読み応えのある内容）
4. 出典名と日付（{date_iso}付近の日付を使用）
5. 「続きを読む →」リンク

記事テーマ例：
- 国内トーナメント結果（JOPT, P1 GRANDPRIX, WPT Japan等）
- 海外での日本人プレイヤー活躍（Triton, WSOP, EPT, APT等）
- ポーカー法規制の動向
- 戦略分析記事
- プレイヤーインタビュー・プロフィール
- 業界トレンド分析

■ トーナメントセクション（2本以上）
- 直近のトーナメント結果の詳細
- 参加者数、賞金プール、優勝者情報

■ 海外日本人プレイヤーセクション（2本以上）
- WSOP, Triton, EPT等での日本人の成績
- 具体的な順位と賞金額

■ 規制・法律セクション（1本以上）
- アミューズメントポーカー規制の動向
- IR法案関連

■ サイドバー情報
- 今後のトーナメントスケジュール（5件以上、具体的な日付・会場）
- 関連リンク集

━━━━━━━━━━━━━━━━━━━━━━━━━━
【画像の使用 - 必須】
━━━━━━━━━━━━━━━━━━━━━━━━━━

以下のUnsplash画像URLを記事のサムネイルとして使用してください：

トップ記事用（大きい）:
https://images.unsplash.com/photo-1511193311914-0346f16efe90?w=1200&h=600&fit=crop
（ポーカーチップの画像）

記事サムネイル用（使い分けること）:
1. https://images.unsplash.com/photo-1596838132731-3301c3ef1986?w=600&h=400&fit=crop
   （カジノテーブル）
2. https://images.unsplash.com/photo-1541278107931-e006523892df?w=600&h=400&fit=crop
   （ポーカーカード）
3. https://images.unsplash.com/photo-1606167668584-78701c57f13d?w=600&h=400&fit=crop
   （カジノチップ）
4. https://images.unsplash.com/photo-1609743522653-52354461eb27?w=600&h=400&fit=crop
   （カードゲーム）
5. https://images.unsplash.com/photo-1587314168485-3236d6710814?w=600&h=400&fit=crop
   （ポーカー風景）
6. https://images.unsplash.com/photo-1518893063132-36e46dbe2428?w=600&h=400&fit=crop
   （カジノ雰囲気）
7. https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=600&h=400&fit=crop
   （イベント会場）
8. https://images.unsplash.com/photo-1504279577054-acfeccf8fc52?w=600&h=400&fit=crop
   （都市風景 - 法規制記事用）

各記事カードに必ず <img> タグでサムネイル画像を配置すること。
CSSグラデーションのプレースホルダーは絶対に使わないこと。

━━━━━━━━━━━━━━━━━━━━━━━━━━
【HTMLデザイン仕様 - 厳守】
━━━━━━━━━━━━━━━━━━━━━━━━━━

<!DOCTYPE html>から始まる完全な単一HTMLファイル。
以下のCSS変数を使用した白ベースのモダンデザイン：

```
:root {{
  --bg: #fafafa;
  --bg-card: #ffffff;
  --border: #e5e7eb;
  --text: #111827;
  --text-muted: #6b7280;
  --accent: #2563eb;
  --accent-light: #dbeafe;
  --green: #059669;
  --green-light: #d1fae5;
  --gold: #d97706;
  --gold-light: #fef3c7;
  --red: #dc2626;
  --radius: 8px;
  --radius-lg: 16px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
}}
```

レイアウト構造：
1. ヘッダー: ロゴ「♠ Poker Japan Daily」+ 「JAPANESE POKER NEWS & TOURNAMENT MEDIA」+ 緑の● AUTO UPDATE バッジ
2. ナビゲーション: TOP | ARTICLES | JAPANESE ABROAD | TOURNAMENTS | REGULATION | WORLD
3. ニュースティッカー: 横スクロールで直近のトーナメント日程表示
4. メインコンテンツ（左70%）+ サイドバー（右30%）のグリッドレイアウト
5. トップ記事: ダークグラデーションオーバーレイ付き大画像ヒーローカード
6. ブログ記事グリッド: 2列のカード型レイアウト、各カードにサムネイル画像
7. セクション別記事: TOURNAMENTS / JAPANESE ABROAD / REGULATION / WORLD
8. フッター: ダークグレー背景、ナビリンク

フォント: Google Fonts から Playfair Display（見出し用）+ Inter（本文英語）+ Noto Sans JP（本文日本語）

レスポンシブ対応:
- max-width: 1200px のコンテナ
- タブレット以下で1カラムに
- モバイルでカードが縦並びに

記事カードのデザイン:
- 白背景、border-radius: var(--radius-lg)、box-shadow: var(--shadow-md)
- サムネイル画像は object-fit: cover で統一的なサイズ
- カテゴリタグは小さなラベル（色分け）
- 出典＋日付をミューテッドカラーで表示
- 「続きを読む →」リンクをアクセントカラーで

━━━━━━━━━━━━━━━━━━━━━━━━━━
【出力ルール】
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. <!DOCTYPE html> から始めて完全なHTMLのみ出力（説明文やマークダウンコードブロック不要）
2. 日本語で記述
3. すべての記事に具体的な数値（賞金額、参加者数、順位等）を含める
4. 今日の日付は {date_str} として表示
5. 全体で少なくとも15,000文字以上のHTMLを生成すること（記事内容を充実させる）
6. img タグには alt 属性を必ず付ける
7. 画像が読み込めない場合のフォールバックとして、各imgの親要素に背景色を設定
"""

print(f"[{date_str}] Generating Poker Japan Daily...")
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    messages=[{"role": "user", "content": PROMPT}]
)

html_content = message.content[0].text.strip()

# Extract HTML from markdown code block if wrapped
if not html_content.startswith("<!DOCTYPE") and not html_content.startswith("<html"):
    import re
    m = re.search(r"```html\s*([sS]+?)```", html_content)
    if m:
        html_content = m.group(1).strip()

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Done: index.html ({len(html_content):,} chars")
