import io
import os
import requests
import typing

import instagrapi

from models import post


class InstagramClientSingleton(object):
    INSTANCE: typing.Optional['_InstagramClient'] = None

    @classmethod
    def get_instance(cls) -> '_InstagramClient':
        if not cls.INSTANCE:
            cls.INSTANCE = _InstagramClient()

        return cls.INSTANCE


class _InstagramClient(object):
    def __init__(self):
        self.client = instagrapi.Client()
        username, password = os.getenv('INSTAGRAM_CREDENTIALS').split(':')
        self.client.login(username, password)

    def get_user_id(self, username: str) -> int:
        return int(self.client.user_id_from_username(username=username))

    def get_stories(self, user_id: int) -> typing.List[post.Post]:
        stories = []
        for story in self.client.user_stories(user_id=user_id):
            match story.media_type:
                case 1:
                    url = str(story.thumbnail_url)
                case 2:
                    url = str(story.video_url)

            with requests.get(url=url) as resp:
                buffer = io.BytesIO(resp.content)

            stories.append(
                post.Post(
                    pk=story.pk,
                    author=story.user.username,
                    created=story.taken_at.astimezone(),
                    mentions=[mention.user.full_name for mention in story.mentions],
                    links=[str(link.webUri) for link in story.links],
                    hashtags=[hashtag.hashtag.name for hashtag in story.hashtags],
                    locations=[f'{location.location.name} - {location.location.city}' for location in story.locations],
                    buffer=buffer,
                )
            )

        return stories
