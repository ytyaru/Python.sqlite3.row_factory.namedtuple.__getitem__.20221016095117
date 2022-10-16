import sqlite3
from collections import namedtuple
class NtLite:
    def __init__(self, path=':memory:'):
        self._path = path
        self._con = sqlite3.connect(path)
        self._con.row_factory = self._namedtuple_factory # sqlite3.Row
        self._cur = self._con.cursor()
    def __del__(self): self._con.close()
    def exec(self, sql, params=()): return self.con.execute(sql, params)
    def execm(self, sql, params=()): return self.con.executemany(sql, params)
    def execs(self, sql): return self.con.executescript(sql)
    def get(self, sql, params=()): return self.exec(sql, params).fetchone()
    def gets(self, sql, params=()): return self.exec(sql, params).fetchall()
    def _namedtuple_factory(self, cursor, row): return self._make_row_type(list(map(lambda d: d[0], cursor.description)))(*row)
    def _make_row_type(self, col_names): return self._set_getitem(namedtuple('Row', col_names))
    def _set_getitem(self, typ): #https://stackoverflow.com/questions/45326573/slicing-a-namedtuple
        def getitem(self, key):
            if isinstance(key, str): return getattr(self, key)
            else: return super(type(self), self).__getitem__(key)
        typ.__getitem__ = getitem
        return typ
    def commit(self): return self.con.commit()
    def rollback(self): return self.con.rollback()
    @property
    def con(self): return self._con
    @property
    def cur(self): return self._cur
    @property
    def path(self): return self._path

