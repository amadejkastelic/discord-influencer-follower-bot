import datetime
import io
import typing
from dataclasses import dataclass


@dataclass
class Post:
    pk: int
    url: typing.Optional[str] = None
    author: typing.Optional[str] = None
    description: typing.Optional[str] = None
    views: typing.Optional[int] = None
    likes: typing.Optional[int] = None
    buffer: typing.Optional[io.BytesIO] = None
    spoiler: bool = False
    created: typing.Optional[datetime.datetime] = None

    def __str__(self) -> str:
        return (
            '📕 Description: {description}\n'
            '🧑🏻‍🎨 Author: {author}\n'
            '📅 Created: {created}\n'
        ).format(
            author=self.author or '❌',
            created=self.created.strftime('%H:%M · %b %-d, %Y') if self.created else '❌',
            description=self.description or '❌',
        )

    def _human_format(self, num: int) -> str:
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
