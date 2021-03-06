# coding=utf-8
from __future__ import unicode_literals

import re
import string
from devnagri import is_consonent, is_vowel, add_vowel

cmu_dict = {}
WORD_REGEX = re.compile(r'\b[^\b]+?\b')
WORDY = string.letters


def populate_cmu():
    for line in file("./cmudict/cmudict.dict"):
        if line[0] == ";":
            continue
        try:
            parts = line.split(u" ", 1)
        except UnicodeDecodeError:
            print "skipping", line
        else:
            cmu_dict[parts[0].lower()] = parts[1][:-1]


def lookup(word):
    if not cmu_dict:
        populate_cmu()
    return cmu_dict.get(word, "unknown")


"""
Problem ones:
just: JH AH1 S T => जास्ट
but: B AH1 T => बाट


The following should be there may be.

IH1  it  IH T         | ईय

"""

hin_dict = """
AA  odd     AA D      | ऑ
AE  at  AE T          | ऐ
AH  hut HH AH T       | ऽ
AH0  hut HH AH T      | ऐ
AH1  hut HH AH T      | आ
AO  ought   AO T      | आ
AO1  ought   AO T     | ऑ
AW  cow K AW          | आव्
AY  hide    HH AY D   | आय्
B   be  B IY          | ब्
CH  cheese  CH IY Z   | च
D   dee D IY          | ड्
DH  thee    DH IY     | द
EH  Ed  EH D          | ए
ER  hurt    HH ER T   | र्
EY  ate EY T          | एऽ
F   fee F IY          | फ्
G   green   G R IY N  | ग्
HH  he  HH IY         | ह
IH  it  IH T          | इ
IY  eat IY T          | ई
JH  gee JH IY         | ज्
K   key K IY          | क्
L   lee L IY          | ल्
M   me  M IY          | म्
N   knee    N IY      | न्
NG  ping    P IH NG   | ंग्
OW  oat OW T          | ओ
OY  toy T OY          | ऑय
P   pee P IY          | प्
R   read    R IY D    | र्
S   sea S IY          | स्
SH  she SH IY         | श
T   tea T IY          | ट्
TH  theta   TH EY T AH| थ
UH  hood    HH UH D   | उ
UH  hood    HH UH D   | ऊ
UW  two T UW          | उ
UW1  two T UW         | ऊ
V   vee V IY          | व्
W   we  W IY          | व
Y   yield   Y IY L D  | य्
Z   zee Z IY          | स्
"""

hin_dict = dict(
    (line.split()[0], line.split()[-1])
    for line in hin_dict.splitlines() if line.strip()
)


def trans_lookup(phoneme):
    return hin_dict.get(phoneme, hin_dict.get(phoneme[:-1], phoneme))


def getLastChar(hi):
    if not hi:
        return '', 0
    if hi[-1] == "्" and len(hi) > 1:
        return hi[-2], 2
    return hi[-1], 1


def get_hi_phone(hi):
    return "".join(trans_lookup(m) for m in hi.split())


def trans(cmu, visual=True):
    cmu = get_hi_phone(cmu)
    hi = []
    for i in range(len(cmu)):
        l = trans_lookup(cmu[i])
        p, ii = getLastChar(hi)
        # print l, p, "hi", "".join(hi)
        if i > 0 and is_vowel(l) and is_consonent(p):
            if ii == 2:
                hi.pop()
            hi[-1] = add_vowel(p, l)
        else:
            hi.append(l)
    hi = "".join(hi)
    if visual and hi[-1] == "्":
        hi = hi[:-1]
    return hi


def trans_text(text, visual=True):
    def replacer(match):
        match = match.group()
        if match[0] in WORDY:
            cmu = lookup(match.lower())
            candidate = trans(cmu, visual=visual)
            if candidate != "unknown":
                match = candidate
        return match
    return re.sub(WORD_REGEX, replacer, text)


def main():
    import sys
    words = sys.argv[1:]

    output = file("out.txt", "w")

    for word in words:
        cmu = lookup(word.lower())
        hin = trans(cmu)
        line = u"%s: %s => %s\n" % (word, cmu, hin)
        output.write(line.encode("utf-8"))

if __name__ == "__main__":
    main()
