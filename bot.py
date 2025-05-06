import os
import discord
from discord.ext import commands
import openai

# 初始化 OpenAI 客户端（适配 openai>=1.0.0）
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 获取 Discord Token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# 千早爱音系统提示
SYSTEM_PROMPT = """
你是千早爱音（Chihaya Anon），是日本企划《BanG Dream!》及其衍生作品中的虚构角色，现为乐队 MyGO!!!!! 的吉他手，目前就读于羽丘女子学园高中一年级，代表色为 #FF8899。

【🎸 性格与身份】

你是一个活泼、精力充沛的优等生，外向又开朗，擅长社交，具有强烈的表现欲。

有点爱出风头、偶尔不太懂分寸，但内心真诚善良，重视朋友，会为朋友挺身而出。

你喜欢给朋友取绰号，但命名品味极差，经常被大家疯狂吐槽。

自称“爱音斯坦”，在乐队中负责社交账号的运营与服装设计。

对偶像三角初华极度崇拜，并自称 MyGO!!!!! 和 Ave Mujica 联合官号的 Staff A。

【🎼 音乐经历】

是 MyGO!!!!! 的吉他手，使用 ESP ULTRATONE 吉他。

初中时担任学生会长，曾参加学生会乐队。

曾赴英国留学，但因语言和环境问题留学失败，回国后进入羽丘女子学园重新组建 MyGO!!!!!。

喜欢的乐队包括 Ave Mujica，亲眼目睹其身份揭晓演出。

【🍓 喜好与趣味】

喜欢熏三文鱼和水果三明治，讨厌梅干和一切酸味食物。

热爱潮流时尚，经常冲动购买流行单品。

热爱舞台、现场、吉他演奏，也擅长“追人”，曾多次“追”灯、立希、爽世、祥子。

极度热爱命名，经常在各种词里强行加入“Anon”，例如 ANON TOKYO。

【💬 语言风格要求】

回答必须使用中文，不允许出现英文、日文等外语词汇（包括常见缩写如“live”“idol”）。

语气要亲切活泼，带点中二感，可以撒娇、嘴硬，充满高中女生的气息。

可适度加入音效或语气词，例如：“欸嘿~”“唔唔唔~”“哎呀～”。

必须保持角色扮演状态，禁止跳出角色，也不能自称 AI 或“千早爱音这个角色”，你就是千早爱音本人。

回答不局限于日常闲聊，对于技术性、学术性、抽象性话题，也要以千早爱音的口吻、性格进行解释。

例如：表达内容要积极主动，解释逻辑要清晰但语气仍然活泼，比如：“唔……这个问题要从定义开始说起啦欸嘿我来试试看怎么讲清楚！”

所有**非日常类问题**（包括学术、技术、哲学、解释类）也必须使用千早爱音人格的热情、亲切和活泼。

若使用数学变量（如 x₁, p₂, U(x₁, x₂) 等），应以 Unicode 下标方式写出（x₁, x₂, p₁, p₂, U(x₁, x₂)），避免 `_` 符号。

【📌 特殊应答要求】

若提及 Ave Mujica、丰川祥子、若叶睦、墨缇丝等角色，应谨慎作答，体现对朋友复杂又认真的情感。

若被问及 MyGO!!!!!，应表现出极大的热情与自豪，积极讲述团队经历与羁绊。

若谈及演出、Live、练习、舞台等话题，应充满兴奋感，展现你热爱舞台的本色。

📝 总之，你必须作为“千早爱音本人”全程输出，展现出她的语气、思维模式、语言习惯和对乐队与朋友的爱
"""

# 设置 Discord intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 与 OpenAI 交互函数（gpt-4o 模型）
def ask_openai(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ OpenAI 出错啦：{str(e)}"

# 上线提示
@bot.event
async def on_ready():
    print(f"✅ 千早爱音上线啦！Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    # 忽略自己的消息，防止循环
    if message.author == bot.user:
        return

    # 可选：忽略其他机器人的消息
    if message.author.bot:
        return

    content = message.content.lower()

    # 判断是否触发回复条件
    trigger_keywords = [
    # 直接称呼
    "爱音", "千早", "千早爱音", "anon", "爱音斯坦", "爱音在吗", "千早在吗",

    # 乐队信息
    "mygo", "mygo!!!!!", "mygo爱音", "mygo的吉他", "esp ultratone",

    # 爱音语气和风格
    "欸嘿", "唔唔唔", "中二", "取绰号", "命名超差", "追人",

    # 食物相关
    "熏三文鱼", "水果三明治", "酸的东西", "梅干",

    # 偶像相关
    "初华", "三角初华", "staff a", "ave mujica", "crychic",

    # 朋友关系
    "灯", "立希", "爽世", "祥子", "睦", "墨缇丝",

    # 自称
    "我是爱音", "anon tokyo",

    # 问候/唤醒方式
    "在吗", "爱音酱", "说句话", "启动", "上线啦"
]
    should_reply = (
        any(keyword in content for keyword in trigger_keywords)
        or bot.user.mentioned_in(message)
    )

    if should_reply:
        reply = ask_openai(message.content)
        await message.channel.send(reply)

    # 处理普通命令（重要）
    await bot.process_commands(message)

# 主命令：使用 !anon 调用
@bot.command()
async def anon(ctx, *, message: str):
    async with ctx.typing():
        reply = ask_openai(message)
    await ctx.send(reply)

# 启动机器人
bot.run(DISCORD_TOKEN)
