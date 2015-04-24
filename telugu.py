# coding=utf-8
from __future__ import unicode_literals
import cmu
import devnagri

REVERSE_CONSONENTS = {
    'ब': 'బ',
    'भ': 'భ',
    'ह': 'హ',
    'ङ': 'ఙ',
    'ग': 'గ',
    'घ': 'ఘ',
    'द': 'ద',
    'ध': 'ధ',
    'ज': 'జ',
    'झ': 'ఝ',
    'ड': 'డ',
    'ढ': 'ఢ',
    'प': 'ప',
    'फ': 'ఫ',
    'र': 'ర',
    'ऱ': 'ఱ',
    'क': 'క',
    'ख': 'ఖ',
    'त': 'త',
    'थ': 'థ',
    'च': 'చ',
    'छ': 'ఛ',
    'ट': 'ట',
    'ठ': 'ఠ',
    'म': 'మ',
    'ण': 'ణ',
    'न': 'న',
    'ऩ': 'న',
    'व': 'వ',
    'ऴ': 'ళ',
    'ल': 'ల',
    'ळ': 'ళ',
    'स': 'స',
    'श': 'శ',
    'ष': 'ష',
    'य': 'య',
    'य़': 'య',
}

CONSONENTS = dict((v, k) for k, v in REVERSE_CONSONENTS.items())
HALF_CONSONENTS = dict(t + '్' for t in CONSONENTS)

VOWELS = {
    'అ': 'अ',
    'ఆ': 'आ',
    'ఇ': 'इ',
    'ఈ': 'ई',
    'ఉ': 'उ',
    'ఊ': 'ऊ',
    'ఏ': 'ए',
    'ఐ': 'ऐ',
    'ఓ': 'ओ',
    'ఔ': 'औ',
    'ఆ': 'ऑ',
}
REVERSE_VOWELS = dict((v, k) for k, v in VOWELS.items())

VOWELS_MATRA = {
    'అ': '',
    'ఆ': 'ా',
    'ఇ': 'ి',
    'ఈ': 'ీ',
    'ఉ': 'ు',
    'ఊ': 'ూ',
    'ఏ': 'ే',
    'ఐ': 'ై',
    'ఓ': 'ో',
    'ఔ': 'ౌ',
    'ఆ': 'ా',
    'అం': 'ం',
    'అః': 'కః',
}

REVERSE_VOWELS_MATRA = {
    '': '',
    'ा': 'ా',
    'ि': 'ి',
    'ी': 'ీ',
    'ु': 'ు',
    'ू': 'ూ',
    'े': 'ే',
    'ै': 'ై',
    'ो': 'ో',
    'ौ': 'ౌ',
    'ॉ': 'ా',
    'ं': 'ం',
    'ः': 'కః',
}

DIGITS = '౦౧౨౩౪౫౬౭౮౯'

REVERSE_MAPPING = REVERSE_CONSONENTS
REVERSE_MAPPING.update(REVERSE_VOWELS)

for i in range(10):
    REVERSE_MAPPING[str(i)] = REVERSE_MAPPING[devnagri.DIGITS[i]] = DIGITS[i]


def to_devnagri(text):
    pass


def from_devnagri(text):
    tel = []
    for h in text:
        tel.append(REVERSE_MAPPING.get(h, h))
    return "".join(tel)


def is_vowel(l):
    # print l, l in VOWELS
    return l in VOWELS


def is_consonent(l):
    # print l, l in CONSONENTS, l in HALF_CONSONENTS
    return l in CONSONENTS or l in HALF_CONSONENTS


def add_vowel(c, v):
    # print "add_vowel", c, v
    if c in HALF_CONSONENTS:
        c = c[:-1]
    # print "add_vowel", c, v, c+VOWELS_MATRA.get(v, v)
    return c+VOWELS_MATRA.get(v, v)


def trans_text(text):
    return from_devnagri(cmu.trans_text(text))


def main():
    import sys
    words = sys.argv[1:]

    output = file("out.txt", "w")

    for word in words:
        tel = trans_text(word)
        line = u"%s => %s\n" % (word, tel)
        output.write(line.encode("utf-8"))

if __name__ == "__main__":
    main()
