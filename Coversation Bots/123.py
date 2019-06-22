#ZADANIE 1,3
import numpy
from random import random, randrange

input = 'pracowałem kiedyś w warzywniaku'

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
        line = line.split(' ')
        vec = []
        for word in line[1:-1]:
            vec.append(float(word))
        vec = numpy.array(vec, dtype='single')
        base_vectors[line[0]] = vec

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

used_verb = False

for word in input:
    if word in verb_past_m_rev:
        used_verb = verb_past_f[verb_past_m_rev[word]]

if not used_verb:
    for word in input:
        base = word
        if word in base_form:
            base = base_form[word]
        if base in verb_past_f and word.endswith('łaś'):
            used_verb = verb_past_f[base]

input_base = []

for word in input:
    if word in base_form:
        input_base.append(base_form[word])
    else:
        input_base.append(word)

print(input)
print(input_base)
print(used_verb)

if used_verb:
    candidates = []

    for phrase in phrases:
        if used_verb in phrase:
            candidates.append(phrase)

    answer = candidates[0]
    best_score = 0
    for candidate in candidates:

        candidate = candidate.split(' ')
        candidate_base = []

        for word in candidate:
            if word in base_form:
                candidate_base.append(base_form[word])
            else:
                candidate_base.append(word)

        print(candidate)
        print(candidate_base)
        score = 0
        sum = set()
        inter = set()

        for word in input_base:
            sum.add(word)
            if word in candidate_base:
                inter.add(word)

        for word in candidate_base:
            sum.add(word)

        sum_score = 0
        inter_score = 0

        for word in sum:
            if word in idf:
                sum_score += idf[word]
            else:
                sum_score += 15

        for word in inter:
            if word in idf:
                inter_score += idf[word]
            else:
                sum_score += 15

        score = inter_score/sum_score
        print(score)

        if score > best_score:
            best_score = score
            answer = candidate


#ZADANIE 2
    me = False
    for word in answer:
        if word == 'Ja' or word == 'ja':
            me = True

    if not me and randrange(2) == 0:
        for word in range(len(answer)):
            if answer[word] in verb_past_f_rev:
                answer[word] = 'ja ' + answer[word]

    choice = randrange(3)

    if choice == 0:
        answer[0] = 'Jeżeli chodzi o mnie , to ' + answer[0].lower()

    if choice == 1:
        answer[0] = 'Bardzo ciekawe . ' + answer[0]

    if choice == 2:
        answer[-1] = answer[-1] + ' A co po za tym u ciebie ?'

    odp = ''
    for word in answer:
        odp += word + ' '

    print(odp)