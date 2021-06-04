# katakana_syn

A tool to get the katakana synonyms of a japanese word using Japanese Wordnet.

# Usage
Python 3 or higher is required.

Download katakana_syn.py from this repository and wnjpn.db from http://compling.hss.ntu.edu.sg/wnja/index.en.html.

Put the downloaded files in the python project you want to use them.

# Example
## Python import
```python
from katakana_syn import get_most_frequent_synonym, get_most_frequent_synonyms

# Use get_most_frequent_synonyms to get a list of the most frequent katakana synonyms by zip_frequency

print(get_most_frequent_synonyms('概念'))
print(get_most_frequent_synonyms('起動'))
print(get_most_frequent_synonyms('勧告'))
print(get_most_frequent_synonyms('背広'))
print(get_most_frequent_synonyms('美的'))
print(get_most_frequent_synonyms('国際'))
print(get_most_frequent_synonyms('地域'))
```
The output of the above example is:
```
{'コンセプト': 4.24, 'コンセプション': 1.5}
{'スタート': 4.81}
{'アドヴァイス': 1.59, 'アドバイス': 4.28}
{'スーツ': 4.58, 'ツーピース': 2.1}
{'ビューティフル': 2.51}
{'インターナショナル': 3.52}
{'ゾーン': 4.17, 'エリア': 4.61, 'エリヤ': 2.32, 'リージョン': 4.33}
```

```python
# Use get_most_frequent_synonym to get the most frequent katakana synonym

print(get_most_frequent_synonym('概念'))
print(get_most_frequent_synonym('起動'))
print(get_most_frequent_synonym('勧告'))
print(get_most_frequent_synonym('背広'))
print(get_most_frequent_synonym('美的'))
print(get_most_frequent_synonym('国際'))
print(get_most_frequent_synonym('地域'))
```
The output of the above example is:
```
コンセプト
スタート
アドバイス
スーツ
ビューティフル
インターナショナル
エリア
```

# License
GPLv2

