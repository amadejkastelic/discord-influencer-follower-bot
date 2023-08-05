import sqlite3


class InfluencerDB(object):
    def __init__(self):
        self.conn = sqlite3.connect('post.db')
        cur = self.conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS post(pk)')
        cur.close()
        self.conn.commit()

    def mark_seen(self, pk: int) -> None:
        cur = self.conn.cursor()
        cur.execute('INSERT INTO post VALUES(?)', [str(pk)])
        cur.close()
        self.conn.commit()

    def is_seen(self, pk: int) -> bool:
        cur = self.conn.cursor()
        res = cur.execute('SELECT pk FROM post WHERE pk=?', [str(pk)]).fetchall()
        cur.close()
        self.conn.commit()
        return len(res) > 0
