import discord
from discord.ext import tasks
import asyncio
from collections import deque
import time
import os

# 環境変数から読み込むか、右側の文字列を自分のサーバーのIDに書き換えてください。（任意部分は書かなくても動作しますが、書くことを推奨します。）
BOT_TOKEN        = os.getenv("BOT_TOKEN")        or "YOUR_BOT_TOKEN_HERE"
LOG_CH_ID        = int(os.getenv("LOG_CH_ID")    or 0) # ログ出力先のチャンネルID(任意)
SAFE_BOT_ROLE_ID = int(os.getenv("SAFE_BOT_ROLE_ID") or 0) # 信頼するボット用ロールID(任意)
UNAUTHORIZED_ROLE_ID   = int(os.getenv("UNAUTHORIZED_ROLE_ID")   or 0) # 制限ロールID(任意)

# 防衛しきい値（デフォルト：1秒間に10回発言でBAN）
LIMIT_TIME = 1.0
LIMIT_COUNT = 10

class DefenseSystem(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True
        intents.moderation = True
        
        super().__init__(intents=intents)
        self.history = {}

    async def setup_hook(self):
        self.clear_cache.start()
        print(f"防衛システム稼働中: {self.user}")

    @tasks.loop(minutes=30)
    async def clear_cache(self):
        """メモリ節約のため古いキャッシュを定期的にクリア"""
        self.history.clear()
        import gc
        gc.collect()

    async def on_message(self, message):
        if message.author == self.user or not message.guild:
            return
        if message.author.guild_permissions.administrator:
            return

        if any(role.id == SAFE_BOT_ROLE_ID for role in message.author.roles):
            return

        if any(role.id == UNAUTHORIZED_ROLE_ID for role in message.author.roles):
            try:
                await message.delete()
                if not message.author.bot:
                    await message.channel.send(
                        f"注意: {message.author.mention} さん、発言は許可されていません。",
                        delete_after=15
                    )
                return 
            except Exception:
                return

        gid = message.guild.id
        uid = message.author.id
        now = time.time()

        if gid not in self.history:
            self.history[gid] = {}
        if uid not in self.history[gid]:
            self.history[gid][uid] = deque(maxlen=LIMIT_COUNT)

        user_times = self.history[gid][uid]
        user_times.append(now)

        if len(user_times) >= LIMIT_COUNT and (now - user_times[0]) <= LIMIT_TIME:
            await self.execute_defense(message)

    async def execute_defense(self, message):
        """BAN実行およびメッセージの一掃"""
        try:
            await message.author.ban(
                reason=f"連投検知: {LIMIT_COUNT}msg/{LIMIT_TIME}s",
                delete_message_seconds=604800
            )

            log_ch = self.get_channel(LOG_CH_ID)
            if log_ch:
                target_type = "Bot(未認可)" if message.author.bot else "ユーザー"
                embed = discord.Embed(
                    title="自動防衛システム作動が作動しました。",
                    description=f"対象: **{message.author}** ({message.author.mention})\n種別: {target_type}",
                    color=discord.Color.red(),
                    timestamp=message.created_at
                )
                embed.add_field(name="処置", value="BANおよび過去7日分の全メッセージ削除", inline=False)
                embed.add_field(name="理由", value=f"短時間（{LIMIT_TIME}秒以内）での異常な連続発言", inline=False)
                await log_ch.send(embed=embed)

        except Exception as e:
            print(f" 防衛アクション失敗 (権限を確認してください): {e}")

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or LOG_CH_ID == 0:
        print("注意： 必要事項が設定されていません。必要事項を書き換えてください。")
    else:
        client = DefenseSystem()
        client.run(BOT_TOKEN)