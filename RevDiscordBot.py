# config["CLIENT"] = {"Sesson_ID": str(LoginDataSD['Data'])}
# SessionID = config["CLIENT"]["Sesson_ID"]

from configparser import ConfigParser

import discord
from discord.ext import commands

config = ConfigParser()
config.read("Config.ini")

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"{bot.user} has Connected to Discord !")
        print(f"{str(len(synced))} Commands Synced")
    except Exception as Error:
        print(Error)


# PROFILE Command Start
@bot.tree.command(name="profile", description="Buy the Demo")
async def Profile(interaction: discord.Interaction):
    await interaction.response.send_message(f"Your User ID is {interaction.user.id}")


# PROFILE Command End


# HELP Command Start
@bot.tree.command(name="help", description="Helps With The Command")
async def Help(interaction: discord.Interaction):
    pass


# HELP Command Ends

bot.run(config["DISCORD"]["TOKEN"])
