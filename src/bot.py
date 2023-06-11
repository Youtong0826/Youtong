import discord
import sys

from core.bot import Bot

bot = Bot(
    intents = discord.Intents.all(),
    setting_path = "setting.json",
    command_prefix = "n!"
)

@bot.event
async def on_ready():
    print("bot is ready!!")
    print("python version:", sys.version[0:9]) 
    print("pycord version:", discord.__version__[0:5])

if __name__ == "__main__":
    bot.setup()
    bot.run(bot.token)