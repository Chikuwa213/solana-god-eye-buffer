import os
import requests
from flask import Flask, request, jsonify

# --- AIクローン・エンジン（神の目）戦略 ---
# --- 最終形態：ハイブリッド・ゲートキーパー ---

app = Flask(__name__)
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 【門番の仕事1】UptimeRobotからの生存確認 (GET)
# これにより、サーバーは常に「起きてます」と返事をし、スリープを防ぐ。
@app.route('/', methods=['GET'])
def wake_up_call():
    return "I am awake. The God Eye is active.", 200

# 【門番の仕事2】Heliusからの神託受信 (POST)
# ここでスワップ情報を解析し、Discordへ報告する。
@app.route('/', methods=['POST'])
def helius_oracle():
    if not DISCORD_WEBHOOK_URL:
        print("[緊急エラー] Discord Webhook URLが設定されていません。")
        return jsonify({"error": "Config missing"}), 500

    try:
        transactions = request.json
        # データがリストでない場合の保険
        if not isinstance(transactions, list):
            transactions = [transactions]

        print(f"[デバッグ] 神託受信。データ数: {len(transactions)}")

        for tx in transactions:
            # スワップのみを対象とする
            if tx.get("type") == "SWAP":
                description = tx.get("description", "")
                source = tx.get("source", "UNKNOWN")
                signature = tx.get("signature", "")
                
                # 神のアドレスを特定
                signer = "不明"
                if "swapped" in description:
                    # "User XXXXX swapped..." の形式から抽出
                    parts = description.split(" ")
                    if len(parts) > 1:
                        signer = parts[1]

                # トークン情報の抽出
                token_transfers = tx.get("tokenTransfers", [])
                from_token = "???"
                to_token = "???"
                from_amt = 0
                to_amt = 0

                for transfer in token_transfers:
                    # 売ったもの（神の口座から出たもの）
                    if transfer.get("fromUserAccount") == signer:
                        from_token = transfer.get("mint", "???")
                        from_amt = transfer.get("tokenAmount", 0)
                    # 買ったもの（神の口座に入ったもの）
                    if transfer.get("toUserAccount") == signer:
                        to_token = transfer.get("mint", "???")
                        to_amt = transfer.get("tokenAmount", 0)

                # 報告メッセージの作成
                solscan_link = f"https://solscan.io/tx/{signature}"
                
                msg = (
                    f"🚨 **神託受信：スワップ検知** 🚨\n"
                    f"**----------------------------------**\n"
                    f"**神:** `{signer}`\n"
                    f"**場所:** `{source}`\n"
                    f"**売却:** `{from_amt}` (`{from_token}`)\n"
                    f"**購入:** `{to_amt}` (`{to_token}`)\n"
                    f"**----------------------------------**\n"
                    f"**証拠:** [Solscanで追跡]({solscan_link})"
                )

                # Discordへ送信
                requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})
                print(f"[報告完了] {signer} のスワップを通知しました。")

    except Exception as e:
        print(f"[エラー] 処理中に問題発生: {e}")
        # エラーが起きてもHeliusには「OK」を返して、再送地獄を防ぐ
        
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))