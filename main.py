import asyncio as asyncio

import discord
from discord import Game, Embed

import SECRETS
import STATICS
from commands import cmd_ping, cmd_autorole

client = discord.Client()


commands = {

    "ping": cmd_ping,
    "autorole": cmd_autorole,

}


@client.event
@asyncio.coroutine
def on_ready():
    print("Bot is logged in successfully. Running on servers:\n")
    [(lambda s: print("  - %s (%s)" % (s.name, s.id)))(s) for s in client.servers]
    yield from client.change_presence(game=Game(name="This is just for tutorial purposes!"))


@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith(STATICS.PREFIX):
        invoke = message.content[len(STATICS.PREFIX):].split(" ")[0]
        args = message.content.split(" ")[1:]
        if commands.__contains__(invoke):
            yield from commands.get(invoke).ex(args, message, client, invoke)
        else:
            yield from client.send_message(message.channel, embed=Embed(color=discord.Color.red(), description=("The command `%s` is not valid!" % invoke)))


@client.event
@asyncio.coroutine
def on_member_join(member):
    yield from client.send_message(member, "**Hey %s!**\n\nWelcome on the official nice super cool *%s* discord server from %s!\n\nIf you want, you can write a little bit about you in the %s channel!\n\nNow have a nice day!" % (member.name, member.server.name, discord.utils.get(member.server.channels, id="332163979365580801").mention, member.server.owner.mention))
    role = cmd_autorole.get(member.server)
    if not role == None:
        yield from client.add_roles(member, role)
        try:
            yield from client.send_message(member, "\n\nYou got automatically assigned the role **" + role.name + "**!")
        except Exception:
            yield from client.send_message(member, "Sorry, but the bot has no permissions to automatically assing you the role **" + role.name + "**.")
            raise Exception



client.run(SECRETS.TOKEN)