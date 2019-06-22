#ZADANIE 4
import numpy
import math
from operator import itemgetter, attrgetter

input = 'ja lubię algebrę i bigos'

phrases = open('personal_corpora.txt', 'r', encoding='utf8').read().splitlines()

idf_lines = open('word_idf.txt', 'r', encoding='utf8').read().splitlines()
idf = {}

for rate in idf_lines:
    rate = rate.split(' ')
    idf[rate[0]] = float(rate[1])

base_form_lines = open('superbazy.txt', 'r', encoding='utf8').read().splitlines()
base_form = {}

for line in base_form_lines:
    line = line.split(' ')
    base_form[line[0]] = line[1]

base_vectors = {}

with open('poleval_base_vectors.txt', 'r', encoding='utf8') as base_vectors_lines:
    for line in base_vectors_lines:
        #print('line: ' + line)
        line = line.split(' ')
        #print(line[1:])
        vec = []
        for word in line[1:-1]:
            vec.append(float(word))
        vec = numpy.array(vec, dtype='single')
        #print(line[0], vec)
        base_vectors[line[0]] = vec
        #print(line)


verb_past_m_lines = open('verb_czytalem.txt', 'r', encoding='utf8').read().splitlines()
verb_past_f_lines = open('verb_czytalam.txt', 'r', encoding='utf8').read().splitlines()

verb_past_m = {}
verb_past_f = {}
verb_past_m_rev = {}
verb_past_f_rev = {}

for line in verb_past_m_lines:
    line = line.split(' ')
    verb_past_m[line[0]] = line[1]
    verb_past_m_rev[line[1]] = line[0]

for line in verb_past_f_lines:
    line = line.split(' ')
    verb_past_f[line[0]] = line[1]
    verb_past_f_rev[line[1]] = line[0]

input = input.split(' ')
base_vectors.pop('532219')

ads_lines = open('reklamy.txt', 'r', encoding='utf8').read().splitlines()

ads_vectors = []
ads = []

for line in ads_lines:
    line = line.split(' ')
    phrase = []
    vector = False
    for word in line:
        word = word.strip('.?,!():;"')
        word = word.lower()
        word_vector = False

        if word != '':
            if word in base_form:
                word = base_form[word]
            if word in base_vectors:
                scalar = 17
                if word in idf:
                    scalar = idf[word]
                word_vector = scalar*base_vectors[word]
                phrase.append(word)

        if word_vector is not False:
            if vector is not False:
                vector = numpy.add(word_vector, vector)
            else:
                vector = word_vector

    ads.append(phrase)
    ads_vectors.append(vector)

input_vector = False
for word in input:
    word = word.strip('.?,!():;"')
    word = word.lower()
    word_vector = False
    if word != '':
        if word in base_form:
            word = base_form[word]
        if word in base_vectors:
            scalar = 17
            if word in idf:
                scalar = idf[word]
            word_vector = scalar * base_vectors[word].copy()
            phrase.append(word)

        if word_vector is not False:
            if input_vector is not False:
                input_vector = numpy.add(word_vector, input_vector)
            else:
                input_vector = word_vector

print("done")
print(input)

mx = [(-2, '-1')]
dlg = math.sqrt(numpy.dot(input_vector, input_vector))
for i in range(len(ads_vectors)):
    vector = ads_vectors[i]
    vec = numpy.dot(input_vector, vector)
    lg = math.sqrt(numpy.dot(vector, vector))
    mx.append((vec/(abs(dlg*lg)), ads_lines[i]))
    mx = sorted(mx, key=itemgetter(0))
    if len(mx) > 5:
        mx.pop(0)
print(mx)

'''
mx = [(-2,'-1')]
kuk = base_vectors['kukułka']
dlg = math.sqrt(numpy.dot(kuk, kuk))
for vector in base_vectors:
    vec = numpy.dot(kuk, base_vectors[vector])
    lg = math.sqrt(numpy.dot(base_vectors[vector], base_vectors[vector]))
    if vec > mx[0][0]:
        mx.append((vec/(abs(dlg*lg)),vector))
        mx = sorted(mx,key=itemgetter(0))
    if len(mx) > 10:
        mx.pop(0)
print(mx)
'''
