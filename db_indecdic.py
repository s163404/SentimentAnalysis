# -*- coding: utf-8 -*-
'''

東北大乾・鈴木研究室・日本語評価極性辞書(名詞編)をDB化
単語, 極性, 極性の値(-1 or 1)のタプル

'''

import sqlite3
from contextlib import closing

dbname = 'dicdatabase.db'
filepath = "Dic/pn.csv.m3.120408.trim"

# with構文 -> ファイル操作のopen, close処理を実行
# 参考 https://docs.python.jp/3/library/contextlib.html
with closing(sqlite3.connect(dbname)) as conn:
    # さらにCursorオブジェクトを作成
    # Cursorオブジェクトを使ってDBに対してコマンドを実行できる
    c = conn.cursor()

# テーブル作成
    c.execute("drop table indecdic")
    create_table = '''create table indecdic (
                        word varchar(64), polarity varchar(32), value integer)'''
    c.execute(create_table)

# 辞書ファイルを単語, 極性, 値のタプルでテーブルに挿入
    # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
    # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
    # タプルで渡す．
    insertform = 'insert into indecdic (word, polarity, value) values (?,?,?)'

    # 名詞辞書
    with open(filepath, 'r', encoding="utf-8") as file:
        for l in file.readlines():
            l = l.split('\t')   # タブ文字削除

            if l[1] == "p":
                pol = "ポジティブ"
                value = 1
            elif l[1] == "e":
                pol = "ニュートラル"
                value = 0
            elif l[1] == "n":
                pol = "ネガティブ"
                value = -1

            info = (l[0], pol, value)       # 単語, 極性, 値
            c.execute(insertform, info)


 # 変更をDBへ保存
    conn.commit()

    select_sql = 'select * from indecdic limit 10'
    for row in c.execute(select_sql):
        print(row)