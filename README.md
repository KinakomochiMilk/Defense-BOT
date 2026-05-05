# Defense-BOT / Discord Defense System

連投荒らしや未認証ユーザーのメッセージを自動で管理・防衛するDiscordボットです。
ボット自身の誤作動防止（ホワイトリスト制）や、複数サーバーでの独立運用に対応しています。

---

## 主な機能

* **連投検知 & BAN**
  1秒間に10回以上の発言をしたユーザー/ボットを自動BAN

* **メッセージ一掃**
  BANと同時に過去7日間の全メッセージを削除

* **未認証ユーザー制限**
  特定のロールを持つユーザーの発言を即座に削除し、警告を表示

* **ホワイトリスト**
  指定したロールを持つボットは防衛対象から除外

* **管理者保護**
  管理者権限を持つユーザーは防衛対象外

---

## セットアップ

### 環境変数

.env ファイルを作成し、以下を設定してください。
ただし、.envファイルを読み込めない場合は直接書き込むこともできます。コメントアウトを確認してください。

BOT_TOKEN=あなたのボットトークン
LOG_CH_ID=ログ出力用チャンネルID
SAFE_BOT_ROLE_ID=信頼するボットのロールID
UNAUTHORIZED_ROLE_ID=未認証ユーザーのロールID

---

### 実行方法

Python 3.8以上と discord.py が必要です。
```
pip install discord.py
python main.py
```
---

## ライセンス

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
