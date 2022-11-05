import discord

from core.classes import CogExtension

class Manage(CogExtension):
    black_role = []
    
    @discord.application_command()
    async def manage_role(self,ctx):
        pass

def setup(bot):
    bot.add_cog(Manage(bot))