#ZADANIE 4b
import numpy
import math
from operator import itemgetter, attrgetter

input = 'czytałem'

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


base_vectors.pop('532219')

input_vector = False
input = input.lower()

print("done")
print(input)

mx = [(-2, '-1')]
base_input = base_vectors[base_form[input]]
dlg = math.sqrt(numpy.dot(base_input, base_input))
print(base_form[input])

for vector in base_vectors:
    if vector in verb_past_f:
        vec = numpy.dot(base_input, base_vectors[vector])
        lg = math.sqrt(numpy.dot(base_vectors[vector], base_vectors[vector]))
        mx.append((vec/(dlg*lg), verb_past_f[vector]))
        mx = sorted(mx,key=itemgetter(0))
        if len(mx) > 5:
            mx.pop(0)
print(mx)
