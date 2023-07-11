# Importing libraries
import discord
from discord.ext import commands
import os
import requests


intents = discord.Intents.all()
intents.members = True
# Discord bot Initialization
client = commands.Bot(command_prefix = '!', intents=intents)


BOTTOKEN = TOKEN

# This event happens when the bot gets run
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")


# This event happens when a message gets sent
@client.command(pass_context = True)
async def join(ctx):
      if not ctx.message.author.voice:
            await ctx.send('You aren"t in a voice channel')
      else:
            channel = ctx.message.author.voice.channel
      await channel.connect()


@client.command(pass_context = True)
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
         await voice_client.disconnect()
    else:
         await ctx.send("The bot is not connected to a voice channel.")


@client.command(pass_context = True)
async def say(ctx, *, message):
      
      # print(message)
      
      CHUNK_SIZE = 1024
      url = "https://api.elevenlabs.io/v1/text-to-speech/{api_key}"

      headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": xi_api_key
      }

      data = {
      "text": message,
      "model_id": "eleven_monolingual_v1",
      "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
      }
      }

      response = requests.post(url, json=data, headers=headers)
      with open('output.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                  if chunk:
                        f.write(chunk)

      server = ctx.message.guild
      voice_channel = server.voice_client
      async with ctx.typing():
                  filename = 'output.mp3'

                  def delete_file(error):
                        os.remove(filename)

                  voice_channel.play(discord.FFmpegPCMAudio(executable = "C:\\ProgramData\\chocolatey\\bin\\ffmpeg.exe", source=filename), after=delete_file)

      
client.run(BOTTOKEN)