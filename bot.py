import os

import asyncio
import requests
from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

API_URL = ""

# Define the intents for the bot
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!logue") or message.content.startswith("@Polylogue"):
        print("User interacted with bot")

    await bot.process_commands(message)


@bot.command()
async def logue(ctx):
    try:
        # This assumes bot is not already connected to the voice channel
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
            await channel.connect()
            print(f"{bot.user.name} has connected to voice channel {channel.name}")
        else:
            await ctx.send(
                f"{ctx.author.name}, you are not connected to a voice channel."
            )
            return

        print(f"{ctx.author} has invoked !logue")

        # Start the conversation loop
        await transcribe_and_respond(ctx)

    except Exception as e:
        print(f"Error occurred: {e}")


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        print(f"{bot.user.name} has disconnected from voice channel.")
    else:
        await ctx.send("I'm not connected to a voice channel.")


async def transcribe_and_respond(ctx):
    while True:
        try:
            # Get the transcript
            response = requests.get(f"{API_URL}/transcribe")
            response.raise_for_status()  # Raises exception if not a 2XX response
            transcript = response.json().get("transcript", "")

            # Call /create API
            response = requests.post(
                f"{API_URL}/create", data={"transcript": transcript}
            )
            response.raise_for_status()

            # If /create decides, raise bot's hand
            if response.json().get("raise_hand", False):
                await raise_hand(ctx)

            # Check if user interacted with bot
            if user_interacted_with_bot():
                # Call /speak API
                response = requests.post(f"{API_URL}/speak", data={"text": transcript})
                response.raise_for_status()

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            # Wait for 10 seconds before next iteration
            await asyncio.sleep(10)


async def raise_hand(ctx):
    # Sending a message to the channel associated with the voice channel
    await ctx.send("Polylogue has something to say...")


def user_interacted_with_bot():
    # Placeholder for user interaction check
    print("Check if user interacted with bot")
    return False


bot.run(TOKEN)
