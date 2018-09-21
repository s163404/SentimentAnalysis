
# -*- coding: utf-8 -*-

import MeCab

m = MeCab.Tagger("-Ochasen")
print(m.parse("SMAPの中居正広あるいはグラードンあるいは恋ダンス"))

