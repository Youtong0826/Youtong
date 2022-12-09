import discord
from core.bot import Bot

bot = Bot(
    intents = discord.Intents.all(),
    setting_path = "setting.json",
    command_prefix ="n!"
)

@bot.event
async def on_ready():
    print("bot is ready!!")

if __name__ == "__main__":
    bot.setup()
    bot.run(bot.token)