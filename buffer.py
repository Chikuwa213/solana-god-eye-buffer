import os
import requests
from flask import Flask, request, jsonify

# --- AIクローン・エンジン（神の目）戦略 ---
# --- オペレーション：『神託バッファ』 ---
# --- 最終形態：覚醒 ---
# 設計者：ジェリー

app = Flask(__name__)
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

@app.route('/', methods=['POST'])
def helius_webhook_handler():
    transactions = request.json
    print(f"[デバッグ] Heliusから神託を受信。データ数: {len(transactions)}")

    if not DISCORD_WEBHOOK_URL:
        print("[緊急エラー] Discord Webhook URLが設定されていません。")
        return jsonify({"error": "Discord webhook URL not configured"}), 500

    for tx in transactions:
        # あらゆる取引所の『スワップ』を、神託として、認識する。
        if tx.get("type") == "SWAP":
            try:
                # --- 神託の、最終翻訳、開始 ---
                description = tx.get("description", "")
                source = tx.get("source", "不明な取引所")
                
                # 行動者（神）のアドレスを、安全に、抜き出す。
                signer = ""
                if "swapped" in description:
                    signer = description.split(" ")[1]

                token_transfers = tx.get("tokenTransfers", [])
                
                from_token_symbol, to_token_symbol = "不明", "不明"
                from_amount, to_amount = 0, 0
                
                # 生の神託から、本質だけを、抜き出す。
                for transfer in token_transfers:
                    if transfer.get("fromUserAccount") == signer:
                        from_token_symbol = transfer.get("mint")
                        from_amount = transfer.get("tokenAmount")
                    if transfer.get("toUserAccount") == signer:
                        to_token_symbol = transfer.get("mint")
                        to_amount = transfer.get("tokenAmount")

                # 全ての情報が、完璧に、揃っている場合のみ、報告する。
                if signer and from_token_symbol != "不明" and to_token_symbol != "不明":
                    solscan_link = f"https://solscan.io/tx/{tx.get('signature')}"
                    
                    # 司令部へ送る、最終完成版の、報告書。
                    message = (
                        f"🚨 **神託受信：スワップ検知** 🚨\n"
                        f"**----------------------------------**\n"
                        f"**神:** `{signer}`\n"
                        f"**取引所:** `{source}`\n"
                        f"**売却:** `{from_amount}` **{from_token_symbol}**\n"
                        f"**購入:** `{to_amount}` **{to_token_symbol}**\n"
                        f"**----------------------------------**\n"
                        f"**証拠:** [Solscanで確認]({solscan_link})"
                    )
                    
                    payload = {"content": message}
                    requests.post(DISCORD_WEBHOOK_URL, json=payload)
                    print(f"[報告完了] {signer}のスワップを司令部へ伝達。")

            except Exception as e:
                print(f"[最終翻訳エラー] 神託の解析中に致命的なエラー: {e}")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))