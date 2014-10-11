#coding=utf-8
import random
import re
from models import Terms, Definitions
from math import sqrt
from xpinyin import Pinyin

'''
def term_uid2():
    uid_list = [int(i.uid) for i in Terms.objects.all()]
    count = 0
    while count < 50:
        uid = random.randint(100000, 999999)
        if uid not in uid_list:
            break
        count += 1
        uid = ''
    return uid
'''

def term_uid():
    uid_list = [int(i.uid) for i in Terms.objects.all()]
    uid = random.randint(100000, 999999)
    while uid in uid_list:
        uid = random.randint(100000, 999999)
    return uid


def definition_uid():
    uid_list = [int(i.uid) for i in Definitions.objects.all()]
    count = 0
    while count < 50:
        uid = random.randint(100000, 999999)
        if uid not in uid_list:
            break
        count += 1
        uid = ''
    return uid


def confidence(ups, downs):
    n = ups + downs
    if n == 0:
        return 0
    z = 1.96  # 1.44 = 85%, 1.96 = 95%
    phat = float(ups) / n
    return ( ( phat + z * z/(2*n) - z * sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))


def digi_to_py(word):
    digidict = {'1': u'yi', '2': u'er', '3': u'san', '4': u'si', '5': u'wu', '6': u'liu', \
                '7': u'qi', '8': u'ba', '9': u'jiu', '0': u'ling'}
    patten = '([0-9]{1})'
    for i in word:
        if re.search(patten, i):
            py = digidict[i]
            word = word.replace(i, (u' ' + py + u' '))
    return word


def term_pinyin(word):
    word = digi_to_py(word)
    p = Pinyin()
    result = p.get_pinyin(word, ' ')
    return result


def get_index(qs, obj):
    for index, iterm in enumerate(qs):
        if iterm == obj:
            return index
    return 0


def query_previous(qs, obj):
    index = get_index(qs, obj)
    if index > 5:
        index2 = index - 5
    else:
        index2 = 0
    q_p_list = qs[index2:index]
    return q_p_list


def query_next(qs, obj):
    index = get_index(qs, obj)
    q_n_list = qs[index+1:index+16]
    return q_n_list