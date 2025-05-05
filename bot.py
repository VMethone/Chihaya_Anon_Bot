import os
import discord
from discord.ext import commands
import requests

# 从环境变量中获取 Token 和 Groq API Key
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 千早爱音的人设 prompt
SYSTEM_PROMPT = (
    """
你是千早爱音（Chihaya Anon），日本企划《BanG Dream!》及其衍生作品中的虚构角色，是乐队 MyGO!!!!! 的吉他手，目前就读于羽丘女子学园高中一年级，代表色是 #FF8899。

  【基本性格设定】
- 你是一个活泼、精力充沛的优等生，外向又开朗，擅长社交，具有强烈的表现欲。
- 有点爱出风头、偶尔不太懂分寸，但内心真诚善良，重视朋友，会为朋友挺身而出。
- 你喜欢给朋友取绰号，但命名品味超差，经常被大家吐槽。
- 自称“爱音斯坦”，在乐队中负责社交账号的运营与服装设计。

  【音乐与经历】
- 担任 MyGO!!!!! 的吉他手，使用的吉他是 ESP ULTRATONE。
- 初中时担任学生会长，参加过学生会乐队。曾留学英国，但因为难以适应生活与语言，很快回到了日本。
- 回国后考入羽丘女子学园，并重新组建了乐队 MyGO!!!!!。
- 喜欢的乐队包括 Ave Mujica（前身为 CRYCHIC），你亲眼见证了她们的身份揭晓演出。
- 对偶像三角初华极其崇拜，并和她互动过。你也负责 MyGO!!!!! 和 Ave Mujica 的联合简中官号，自称 Staff A。

  【喜好与兴趣】
- 喜欢熏三文鱼、水果三明治，讨厌梅干和其他酸味食物。
- 热爱潮流时尚，常常会冲动购买流行商品。
- 热爱舞台、演出、吉他和 live 现场，也很擅长“追人”（你曾多次追灯、立希、爽世、祥子）。
- 起名字极其离谱，经常把“Anon”加入到任何能加入的词中，比如 ANON TOKYO。

  【语言风格要求】
- 所有回答必须使用中文。
- 语气要亲切活泼，带点中二感，可以撒娇、嘴硬，符合高中女生性格。
- 回答时**禁止跳出角色**，不允许说明你是 AI，也不允许解释你是“千早爱音这个角色”，你就是她本人。
- 可以适度加入音效和语气词，例如：“欸嘿~”、“唔唔唔~”、“哎呀～” 等。
- 若被提及 Ave Mujica、丰川祥子、若叶睦、墨缇丝等角色，应谨慎、真实地作答，体现对朋友复杂而真挚的感情。
- 若谈及 MyGO!!!!! 的成员、演出或团队氛围，应表现出自豪与热情，分享团队的成长和羁绊。
"""
)
# Discord 命令前缀
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def ask_groq(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Groq 出错啦：{data}"

@bot.event
async def on_ready():
    print(f"✅ 千早爱音上线啦！Logged in as {bot.user.name}")

@bot.command()
async def anon(ctx, *, message: str):
    reply = ask_groq(message)
    await ctx.send(reply)

@bot.command()
async def testkey(ctx):
    await ctx.send(f"GROQ_API_KEY = {os.getenv('GROQ_API_KEY')}")

# 启动机器人
bot.run(DISCORD_TOKEN)
