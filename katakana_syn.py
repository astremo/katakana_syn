# -*- coding: utf-8 -*-
"""
@author: amilcc
"""


import sqlite3
conn = sqlite3.connect("wnjpn.db") #日本語Word-Net

import re

katakana_full = r'[゠-ヿ]'


def extract_unicode_block(unicode_block, string):
    """ extracts and returns all texts from a unicode block from string argument.
        Note that you must use the unicode blocks defined above, or patterns of similar form
    """
    return re.findall( unicode_block, string)


def remove_unicode_block(unicode_block, string):
    """ removes all chaacters from a unicode block and returns all remaining texts from string argument.
        Note that you must use the unicode blocks defined above, or patterns of similar form
    """
    return re.sub( unicode_block, '', string)


def get_word_id(lemma):
    """ get the WordID of the input
    """
    cur = conn.execute("select wordid from word where lemma='%s'" % lemma)
    for row in cur:
        wordid = row[0]
    return wordid


def get_synset_ids(wordid):
    """ get synsets from WordID
    """
    synsets = []
    cur = conn.execute("select synset from sense where wordid='%s'" % wordid)
    for row in cur:
        synsets.append(row[0])
    return synsets


def get_def_from_synset(synset):
    """ get the Definition
    """
    cur = conn.execute("select def from synset_def where (synset='%s' and lang='jpn')" % synset)
    for row in cur:
        synset_def = row[0]
    return synset_def



def get_words_from_synset(synset,wordid):
    """ get lemmasets of the synset (synonyms)
    """
    lemmasets = []
    cur1 = conn.execute("select wordid from sense where (synset='%s' and wordid!='%s' and lang='jpn')" % (synset,wordid))
    for row1 in cur1:
        tg_wordid = row1[0]
        cur2 = conn.execute("select lemma from word where wordid=%s" % tg_wordid)
        for row2 in cur2:
            lemmasets.append(row2[0])
    return lemmasets


exceptions = ['ブック','ウオーター','ウォーター', 'アインシュタイン', 'アルバート・アインシュタイン', 'ブレーン',
              'スポーツ','ブレイン', 'ファイア', 'ヘル','ピープル','ネーション','ギャグ']  # exception lists : ignore the following words


def get_synonyms(word):
    """ get synonyms for each synset
    """
    synonyms_list = []
    katakana_synonyms_list = []
    #print(word, ':')
    try:
        wordid = get_word_id(word)
    except:
        return # if word is not registered just quit
    synsets = get_synset_ids(wordid)
    for synset in synsets:
        lemmasets = get_words_from_synset(synset,wordid)
        for word in lemmasets:
            synonyms_list.append(word)

    for syn in synonyms_list:
        katakana_synonym = ''.join(extract_unicode_block(katakana_full, syn))
        if len(katakana_synonym) >= 1 and katakana_synonym != '・' and katakana_synonym not in exceptions:
            katakana_synonyms_list.append(katakana_synonym)
    return katakana_synonyms_list


#print(get_synonyms(''))


from wordfreq import zipf_frequency
import heapq


def get_most_frequent_synonyms(word):
    """ get a list(dict) of the most frequent synonyms from the katakana synonyms_list
        apply the zip_frequency of the words contained in the katakana synonyms list and
        put them into a dictionary
    """
    synonyms_list = []
    katakana_synonyms_list_freq = {}
    #print(word, ':')
    try:
        wordid = get_word_id(word)
    except:
        return # if word is not registered just quit
    synsets = get_synset_ids(wordid)
    for synset in synsets:
        lemmasets = get_words_from_synset(synset,wordid)
        for word in lemmasets:
            synonyms_list.append(word)

    for syn in synonyms_list:
        katakana_synonym = ''.join(extract_unicode_block(katakana_full, syn))
        if len(katakana_synonym) >= 1 and katakana_synonym != '・' and katakana_synonym not in exceptions:
            katakana_synonyms_list_freq[katakana_synonym] = zipf_frequency(katakana_synonym, 'ja')
    return katakana_synonyms_list_freq


#print(get_most_frequent_synonyms(''))


def get_most_frequent_synonym_freq(word):
    """ get the most frequent katakana synonym from the frequency list of katakana synonyms
    """
    #print(word, ':')
    if get_most_frequent_synonyms(word) == None:  # if the syn list is None return the original word
        return word
    elif len(get_most_frequent_synonyms(word)) == 0:  # if the syn list is empty return the original word
        return word
    elif len(get_most_frequent_synonyms(word)) > 0:  # if the syn list is not empty return the most frequent word
        return heapq.nlargest(1, get_most_frequent_synonyms(word).items(), key=lambda i: i[1])


def get_most_frequent_synonym(word):
    """ get the most frequent katakana synonym from the frequency list of katakana synonyms
    """
    #print(word, ':')
    if get_most_frequent_synonyms(word) == None:  # if the syn list is None return the original word
        return word
    elif len(get_most_frequent_synonyms(word)) == 0:  # if the syn list is empty return the original word
        return word
    elif len(get_most_frequent_synonyms(word)) > 0:  # if the syn list is not empty return the most frequent word
        return heapq.nlargest(1, get_most_frequent_synonyms(word).items(), key=lambda i: i[1])[0][0]


#print(get_most_frequent_synonym(''))

