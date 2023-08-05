import asyncio
import logging
import os
import random

import discord

import db
import utils
from clients import instagram

emoji = ['😼', '😺', '😸', '😹', '😻', '🙀', '😿', '😾', '😩', '🙈', '🙉', '🙊', '😳']


class DiscordClient(discord.Client):
    async def on_ready(self):
        logging.info(f'Logged on as {self.user}')

    async def setup_hook(self) -> None:
        self.instagram_story_task = self.loop.create_task(self.instagram_story_task())

    async def on_message(self, message: discord.Message):
        pass

    async def instagram_story_task(self):
        client = instagram.InstagramClientSingleton.get_instance()
        user_id = client.get_user_id(os.getenv('INSTAGRAM_USERNAME'))

        database = db.InfluencerDB()

        await self.wait_until_ready()

        channel = self.get_channel(int(os.getenv('DISCORD_CHANNEL_ID')))
        while not self.is_closed():
            for story in client.get_stories(user_id=user_id):
                if database.is_seen(pk=story.pk):
                    continue
                file = None
                if story.buffer:
                    file = discord.File(
                        fp=story.buffer,
                        filename=f'file{utils.guess_extension_from_buffer(buffer=story.buffer)}',
                    )
                await channel.send(
                    content=f'A new story from your favorite influencer {random.choice(emoji)}.\n{str(story)}',
                    file=file,
                    suppress_embeds=True,
                )
                database.mark_seen(pk=story.pk)

            await asyncio.sleep(300)


intents = discord.Intents.default()
intents.message_content = True
client = DiscordClient(intents=intents)

api_key = os.environ.get('DISCORD_API_TOKEN')
if not api_key:
    raise RuntimeError('DISCORD_API_TOKEN environment variable not set, please set it to a valid value and try again.')

client.run(api_key)
