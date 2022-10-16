[ja](./README.ja.md)

# sqlite3.row_factory.namedtuple.__getitem__

Write a thin wrapper that returns SQLite3 select result as namedtuple type.

<!--

# DEMO

* [demo](https://ytyaru.github.io/Python.sqlite3.row_factory.namedtuple.__getitem__.20221016095117/)

![img](https://github.com/ytyaru/Python.sqlite3.row_factory.namedtuple.__getitem__.20221016095117/blob/master/doc/0.png?raw=true)

# Features

* sales point

-->

# Requirement

* <time datetime="2022-10-16T09:51:14+0900">2022-10-16</time>
* [Raspbierry Pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 4 Model B Rev 1.2
* [Raspberry Pi OS](https://ja.wikipedia.org/wiki/Raspbian) buster 10.0 2020-08-20 <small>[setup](http://ytyaru.hatenablog.com/entry/2020/10/06/111111)</small>
* bash 5.0.3(1)-release
* Python 3.10.5

```sh
$ uname -a
Linux raspberrypi 5.10.103-v7l+ #1529 SMP Tue Mar 8 12:24:00 GMT 2022 armv7l GNU/Linux
```

# Installation

```sh
git clone https://github.com/ytyaru/Python.sqlite3.row_factory.namedtuple.__getitem__.20221016095117
```

# Usage

## unit test

```sh
cd Python.sqlite3.row_factory.namedtuple.__getitem__.20221016095117/src
./test-ntlite.py
```

## import

```python
from ntlite import NtLite
```

## new

```python
db = NtLite() # :memory:
```
```python
db = NtLite('./db/my.sqlite3')
```

## API

method|call sqlite3 method
------|-------------------
`exec`|[execute][]
`execm`|[executemany][]
`execs`|[executescript][]
`get`|[execute][] + [fetchone][]
`gets`|[execute][] + [fetchall][]

[execute]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.execute
[executemany]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.executemany
[executescript]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Connection.executescript
[fetchone]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.fetchone
[fetchall]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.fetchall
[fetchmany]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.fetchmany

## reference column

```python
row = db.get("select id, name num from users where id=5;")
row.id    #=> 5
row['id'] #=> 5
row[0]    #=> 5
```

[row_factory][]|reference
---------------|---------
default|`row[0]`
[sqlite3.Row][]|`row[0]`, `row['列名']`
[previous][]([namedtuple][])|`row[0]`, `row.列名`
This work([namedtuple][],[__getitem__][])|`row[0]`, `row.列名`, `row['列名']`

[previous]:https://github.com/ytyaru/Python.sqlite3.row_factory.namedtuple.20221015151253
[sqlite3]:https://docs.python.org/ja/3/library/sqlite3.html
[row_factory]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Connection.row_factory
[sqlite3.Row]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Row
[__getitem__]:https://docs.python.org/ja/3/reference/datamodel.html#object.__getitem__
[cursor.description]:https://docs.python.org/ja/3/library/sqlite3.html#sqlite3.Cursor.description
[namedtuple]:https://docs.python.org/ja/3/library/collections.html#collections.namedtuple
[dataclass]:https://docs.python.org/ja/3/library/dataclasses.html
[mypy]:https://github.com/python/mypy

## example

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

<!--

# Note

* important point

-->

# Author

ytyaru

* [![github](http://www.google.com/s2/favicons?domain=github.com)](https://github.com/ytyaru "github")
* [![hatena](http://www.google.com/s2/favicons?domain=www.hatena.ne.jp)](http://ytyaru.hatenablog.com/ytyaru "hatena")
* [![twitter](http://www.google.com/s2/favicons?domain=twitter.com)](https://twitter.com/ytyaru1 "twitter")
* [![mastodon](http://www.google.com/s2/favicons?domain=mstdn.jp)](https://mstdn.jp/web/accounts/233143 "mastdon")

# License

This software is CC0 licensed.

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.en)

