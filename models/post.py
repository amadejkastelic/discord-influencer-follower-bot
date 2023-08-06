import datetime
import io
import typing
from dataclasses import dataclass


@dataclass
class Post:
    pk: str
    mentions: typing.List[str]
    links: typing.List[str]
    hashtags: typing.List[str]
    locations: typing.List[str]
    author: typing.Optional[str] = None
    buffer: typing.Optional[io.BytesIO] = None
    created: typing.Optional[datetime.datetime] = None

    def __str__(self) -> str:
        return (
            '🧑🏻‍🎨 Author: {author}\n'
            '📅 Created: {created}\n'
            '🧑‍🤝‍🧑 Mentions: {mentions}\n'
            '🗺️ Locations: {locations}\n'
            '📍 Hashtags: {hashtags}\n'
            '⛓️ Links: {links}\n'
        ).format(
            author=self.author or '❌',
            created=self.created.strftime('%H:%M · %b %-d, %Y') if self.created else '❌',
            mentions=', '.join(self.mentions) if self.mentions else '❌',
            locations=', '.join(self.locations) if self.locations else '❌',
            hashtags=', '.join(self.hashtags) if self.hashtags else '❌',
            links=', '.join(self.links) if self.links else '❌',
        )

    def _human_format(self, num: int) -> str:
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
