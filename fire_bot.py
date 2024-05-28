import discord
import asyncio
import datetime
import os
from embed import create_embed
from dotenv import load_dotenv, dotenv_values
from db_ops import *
from datetime import datetime, timezone, time
import logging
from discord.ext import commands, tasks

load_dotenv()

target_channel_id = 887066573498634280

intents = discord.Intents.default()
intents.reactions = True
intents.message_content = True
intents.members = True

create_tables()

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def setup_hook():
    weekly_post.start()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
@bot.event
async def on_reaction_add(reaction, _):
    if reaction.emoji == "🔥":
        handle_reaction_add(reaction)
@bot.event
async def on_reaction_remove(reaction, _):
    if reaction.emoji == "🔥":
        handle_reaction_remove(reaction, False)
@bot.event
async def on_reaction_clear(_, reactions):
    for reaction in reactions:
        if reaction.emoji == "🔥":
            handle_reaction_remove(reaction, True)
@bot.event
async def on_reaction_clear_emoji(reaction):
    if reaction.emoji == "🔥":
        handle_reaction_remove(reaction, True)

@tasks.loop(hours=168)
async def weekly_post():
    embeds = []
    
    top_three = fetch_top_three_messages()
    for rank, row in enumerate(top_three):
        message_id, channel_id, fire_count = row
        try:
            message_channel = bot.get_channel(channel_id)
            if message_channel is None:
                print("msg channel not found")
                return
            msg = await message_channel.fetch_message(message_id)
            embeds.append(create_embed(msg, rank+1, fire_count))
            
        except discord.NotFound:
            print("channel not found")
        except discord.Forbidden:
            print("channel forbidden")
        except discord.HTTPException as e:
            print("exception")
    print("sending embeds")
    
    post_channel = bot.get_channel(target_channel_id)
    await post_channel.send(embeds=embeds)

@weekly_post.before_loop
async def before_weekly_post():
    await bot.wait_until_ready()
    # Calculate the time until the next weekly post (e.g., every Monday at 6 PM)
    now = datetime.now(timezone.utc)
    target_time = datetime.combine(now.date(), time(hour=19, minute=18), timezone.utc)  # 6:00 PM UTC
    seconds_until_target = (target_time - now).total_seconds()

    #TODO: replace 0 with seconds_until_target
    await asyncio.sleep(0)

handler = logging.FileHandler(filename='discord,log', encoding='utf-8', mode='w')
bot.run(os.getenv("TOKEN"), log_handler=handler)
