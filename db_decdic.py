# -*- coding: utf-8 -*-
'''

東北大乾・鈴木研究室・日本語評価極性辞書(用言編)をDB化
単語, 極性, 極性の値(-1 or 1)のタプル

'''

import sqlite3
from contextlib import closing

dbname = 'dicdatabase.db'
filepath = "Dic/wago.121808.pn.txt"

# with構文 -> ファイル操作のopen, close処理を実行
# 参考 https://docs.python.jp/3/library/contextlib.html
with closing(sqlite3.connect(dbname)) as conn:
    # さらにCursorオブジェクトを作成
    # Cursorオブジェクトを使ってDBに対してコマンドを実行できる
    c = conn.cursor()

# テーブル作成
    c.execute("drop table decdic")
    create_table = '''create table decdic (
                        word varchar(64), polarity varchar(32), value integer)'''
    c.execute(create_table)

# 辞書ファイルを単語, 極性, 値のタプルでテーブルに挿入
    # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
    # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
    # タプルで渡す．
    insertform = 'insert into decdic (word, polarity, value) values (?,?,?)'

    # 用言辞書
    with open(filepath, 'r', encoding="utf-8") as file:
        for l in file.readlines():
            l = l.split('\t')   # タブ文字削除
            l[1] = l[1].replace(' ', '').replace('\n', '')  # 単語中のスペースと改行削除
            if l[0].split('（')[0] == "ポジ":
                pol = "ポジティブ"
                value = 1
            else:
                pol = "ネガティブ"
                value = -1

            info = (l[1], pol, value)       # 単語, 極性, 値
            c.execute(insertform, info)


 # 変更をDBへ保存
    conn.commit()

    select_sql = 'select * from decdic limit 10'
    for row in c.execute(select_sql):
        print(row)