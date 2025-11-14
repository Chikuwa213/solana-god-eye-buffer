import os
import requests
from flask import Flask, request, jsonify

# --- AIクローン・エンジン（神の目）戦略 ---
# --- オペレーション：『神託バッファ』 ---
# 設計者：ジェリー

# --- 兵器の初期化 ---
app = Flask(__name__)

# --- 最重要機密：作戦司令部の『新しい座標』---
# このURLは、後ほどRenderというクラウドサービスで設定する。
# これで、コードを世界に公開しても、URLが漏れることはない。
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# --- Heliusからの神託を受け止める、唯一の『門』 ---
@app.route('/webhook', methods=['POST'])
def helius_webhook_handler():
    # Heliusから送られてきた、全ての神託（JSONデータ）を受け取る。
    transactions = request.json
    print(f"[デバッグ] Heliusから神託を受信。データ数: {len(transactions)}")

    # もしDiscordのURLが設定されていなければ、作戦は実行不可能。
    if not DISCORD_WEBHOOK_URL:
        print("[緊急エラー] Discord Webhook URLが設定されていません。")
        return jsonify({"error": "Discord webhook URL not configured"}), 500

    # Heliusは複数の情報を一度に送ってくる。その一つ一つを解析する。
    for tx in transactions:
        # 我々が本当に知りたい『スワップ』の情報だけを抜き出す。
        if tx.get("type") == "SWAP" and tx.get("source") == "JUPITER":
            try:
                # --- 神託の翻訳開始 ---
                description = tx.get("description", "")
                
                # "User {SIGNER} swapped..." の形式から、行動者（神）のアドレスを抜き出す。
                signer = description.split(" ")[1] if description else "不明"
                
                # トークンの変動情報を取得
                token_transfers = tx.get("tokenTransfers", [])
                
                # 何を、何に、いくらで交換したのかを特定する。
                # 非常に複雑なデータの中から、本質だけを抜き出す魔法だ。
                from_token, to_token, from_amount, to_amount = None, None, None, None
                
                for transfer in token_transfers:
                    # 神のウォレットから出ていったトークン（売却したもの）
                    if transfer.get("fromUserAccount") == signer:
                        from_token = transfer.get("mint")
                        from_amount = transfer.get("tokenAmount")
                    # 神のウォレットに入ってきたトークン（購入したもの）
                    if transfer.get("toUserAccount") == signer:
                        to_token = transfer.get("mint")
                        to_amount = transfer.get("tokenAmount")

                # 必要な情報が揃っているか最終確認
                if from_token and to_token and from_amount and to_amount:
                    
                    # Solscanへのリンクを作成
                    solscan_link = f"https://solscan.io/tx/{tx.get('signature')}"
                    
                    # 司令部へ送る、最終報告書の作成
                    message = (
                        f"🚨 **神託受信：スワップ検知** 🚨\n"
                        f"**--------------------------------------**\n"
                        f"**神のアドレス:** `{signer}`\n"
                        f"**売却トークン:** `{from_token}`\n"
                        f"**売却量:** `{from_amount}`\n"
                        f"**購入トークン:** `{to_token}`\n"
                        f"**購入量:** `{to_amount}`\n"
                        f"**取引所:** `Jupiter`\n"
                        f"**--------------------------------------**\n"
                        f"**詳細確認:** [Solscanでトランザクションを追跡]({solscan_link})"
                    )
                    
                    # 作戦司令部へ、最終報告書を送信する。
                    payload = {"content": message}
                    requests.post(DISCORD_WEBHOOK_URL, json=payload)
                    print(f"[報告完了] {signer}のスワップを司令部へ伝達。")

            except Exception as e:
                print(f"[翻訳エラー] 神託の解析中にエラーが発生: {e}")

    # Heliusに対し、「任務完了」と返信する。
    return jsonify({"status": "success"}), 200

# --- サーバー起動の呪文 ---
if __name__ == "__main__":
    # Renderがこのサーバーを起動するために、この設定が必要。
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))