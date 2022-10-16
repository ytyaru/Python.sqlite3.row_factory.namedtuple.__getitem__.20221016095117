【Python】sqlite3.connect.row_factoryでnamedtuple型にする薄いラッパーを書いた2

　`__getitem__`を使い`['列名']`のように参照することもできるようにした。前回のままだと列名を変数にしたいとき`getattr(row, '列名')`と書く必要があった。それを`['列名']`と書けるようにした。

<!-- more -->

# ブツ

* [リポジトリ][]

[リポジトリ]:https://github.com/ytyaru/Python.sqlite3.row_factory.namedtuple.__getitem__.20221016095117
[sqlite3]:https://docs.python.org/ja/3/library/sqlite3.html
[row_factory]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Connection.row_factory
[sqlite3.Row]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Row
[__getitem__]:https://docs.python.org/ja/3/reference/datamodel.html#object.__getitem__
[cursor.description]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.description
[namedtuple]:https://docs.python.org/ja/3/library/collections.html#collections.namedtuple
[dataclass]:https://docs.python.org/ja/3/library/dataclasses.html
[mypy]:https://github.com/python/mypy

## 実行

```sh
NAME='Python.sqlite3.row_factory.namedtuple.__getitem__.20221016095117'
git clone https://github.com/ytyaru/$NAME
cd $NAME/src
./test-ntlite.py
./example-2.py
./example.py
```

## コード例

```python
#!/usr/bin/env python3
# coding: utf8
import os
from ntlite import NtLite
path = 'my.db'
if os.path.isfile(path): os.remove(path)
db = NtLite(path)
db.exec("create table users(id integer, name text);")
db.execm("insert into users values(?,?);", [(0,'A'),(1,'B')])
assert 2 == db.get("select count(*) num from users;").num
rows = db.gets("select * from users;")
assert 0   == rows[0].id
assert 'A' == rows[0].name
assert 1   == rows[1].id
assert 'B' == rows[1].name

assert 0   == rows[0]['id']
assert 'A' == rows[0]['name']
assert 1   == rows[1]['id']
assert 'B' == rows[1]['name']

assert 0   == rows[0][0]
assert 'A' == rows[0][1]
assert 1   == rows[1][0]
assert 'B' == rows[1][1]
```

# 前回までの課題

　前回のままだと列名を変数にしたいとき`getattr(row, '列名')`と書く必要があった。[sqlite3.Row][]なら`row['列名']`と書けるのに。

ファクトリ|参照方法
----------|--------
デフォルト|`row[0]`
[sqlite3.Row][]|`row['列名']`
[前回][]([namedtuple][])|`row.列名`

[list]:
[namedtuple]:
[sqlite3.Row]:

# やったこと

　`['列名']`でも参照できるようにした。

　[__getitem__][]を使い`[キー]`で参照されたときの挙動を実装する。

```python
def getitem(self, key):
    if isinstance(key, str): return getattr(self, key)
    else: return super(type(self), self).__getitem__(key)
```

　`[キー]`の書式で与えられるキーは整数のときもあれば文字列のときもある。そこでキーの型によって処理を分岐するようにした。現状デフォルト状態では位置を整数で渡すと実行される。それを`super(type(self), self).__getitem__(key)`で実行している。`super()`のくだりが冗長だが、やっていることはただ親クラスの[namedtuple][]を参照してるだけ。

# コード

## ntlite.py

```python
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
```

　テストケースも追加した。それぞれの参照方法で参照されることを確認した。また、SQL文で列名が大文字で書かれていても戻り値の[namedtuple][]では小文字になることも確認した。SQLでは大文字・小文字の区別がない。でもPythonでは区別するし、変数名は小文字にするのが通例。なので期待通り。特に何も実装する必要もなかった。

### 失敗例

　最初は[namedtuple][]型を継承して[__getitem__][]をオーバーライドしようとした。以下のように。でも、できなかった。

```python
from collections import namedtuple
class NamedTupleDict(namedtuple):
    def __getitem__(self, key):
        if isinstance(key, str): return getattr(self, key)
        else: return super(type(self), self).__getitem__(key)
```
```python
from typing import NamedTuple
class NamedTupleDict(NamedTuple):
    def __getitem__(self, key):
        if isinstance(key, str): return getattr(self, key)
        else: return super(type(self), self).__getitem__(key)
```

　以下のようにならできるらしい。

```python
class NamedTupleDict(namedtuple('Some' 'id name')):
```

　でも列名が固定されてしまう。可変にしたい。

### 今回

　なので今回はクラスを動的に生成した。SQL文で受け取った列名を引数にして[namedtuple][]型を生成した。これで列名を可変にできる。

```python
namedtuple('Row', col_names)
```

　あとはそのクラスに自作の[__getitem__][]をセットすれば任意の列をもったRowクラスの完成。

```python
typ.__getitem__ = getitem
```

　最後に`sqlite3.connect.row_factory`にセットする関数で、自作クラスのインスタンスを返す。一行に圧縮したのでわかりづらいが、`(*row)`のところが`Row(*row)`という意味。`Row`は自作クラスで、`namedtuple('Row', col_names)`の戻り値。

```python
self._make_row_type(list(map(lambda d: d[0], cursor.description)))(*row)
```

　ちなみに`list(...)`の所は[cursor.description][]を使ってSQL文の列名を取得している。

# 所感

　[sqlite3][]の薄いラッパー[namedtuple][]編はこれで完成。

　気になるのは[dataclass][]。[namedtuple][]よりも新しいが、何が違うのか。たぶん型アノテーションが必須なところが違うのだろう。でも、どうせ[mypy][]で[unittest][]コードがチェックできないし、ヌケモレが起こりうるなら型チェックされたか不安。そんなもののために労力を割いても仕方ない。というわけで[namedtuple][]さえ使えればいい。

　ただ、[dataclass][]も動的に生成できるのかな？　勉強のために試してみてもいいかもしれない。

　それができたら`row_factory`を配列、辞書、[namedtuple][]、[dataclass][]で選択できるようにすると良さそう。

