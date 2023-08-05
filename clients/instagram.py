import datetime
import io
import os
import requests
import typing

import instaloader

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
        self.client = instaloader.Instaloader(
            user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0'
        )
        if os.path.exists('instagram.sess'):
            self.client.load_session_from_file(username='amadejkastelic', filename='instagram.sess')

    def get_user_id(self, username: str) -> int:
        return instaloader.Profile.from_username(context=self.client.context, username=username).userid

    def get_stories(self, user_id: int, not_before: datetime.timedelta) -> typing.List[post.Post]:
        now = datetime.datetime.now().astimezone()
        stories = []
        for story in self.client.get_stories(userids=[user_id]):
            for item in story.get_items():
                if item.date_local > (now - not_before):
                    stories.append(self._build_post_from_story(story=item))

        return stories

    def _build_post_from_story(self, story: instaloader.StoryItem) -> post.Post:
        if story.is_video:
            url = story.video_url
        else:
            url = story.url

        with requests.get(url=url) as resp:
            return post.Post(
                author=story.owner_profile.username,
                description=story.caption,
                buffer=io.BytesIO(resp.content),
                created=story.date_local,
            )
