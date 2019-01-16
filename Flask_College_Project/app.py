

from flask import Flask, render_template, request
from spellCheck import *
import language_check
import re
from spellchecker import SpellChecker
from gingerit.gingerit import GingerIt
import operator
import nltk
import time
# nltk.download()        # download nltk requirements for first time
from nltk.util import ngrams
import collections
import re
from nltk import bigrams
import itertools
# from nltk.corpus import stopwords
#

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        corrected = []
        candidate = {}
        input_list = []
        input_text = request.form['inputText']
        tool = language_check.LanguageTool('en-US')
        output_list = re.findall(r'\S+', input_text)
        # set(stopwords.words('english'))
        my_cand = {}
        # try:
        #     parser = GingerIt()
        #     real = parser.parse(input_text)
        # except Exception:
        #     real = None

        global unigram  # uni-gram dictionary
        unigram = {}
        global bigram  # bi-gram dictionary        # basic implementation
        bigram = {}
        global trigram  # bi-gram dictionary        # basic implementation
        trigram = {}

        with open('data/w2_.txt', 'r', encoding='ISO-8859-1') as f:
            for line in f:
                elements = line.rstrip().split("\t")
                bigram[(elements[1], elements[2])] = elements[0]

        with open('data/w3_.txt', 'r', encoding='ISO-8859-1') as f:
            for line in f:
                elements = line.rstrip().split("\t")
                trigram[(elements[1], elements[2], elements[3])] = elements[0]

        text = input_text
        text_list = text.split(' ')
        print(text_list)
        tokenize = nltk.word_tokenize(text)
        bigrams = ngrams(tokenize, 2)
        trigrams = ngrams(tokenize, 3)
        spell = SpellChecker()
        for word in text_list:
            print("Candidate", spell.candidates(word))
            print("Correct", spell.correction(word))

        for items in output_list:
            input_list.append(items)
            output_text = correction(items.lower())
            candidate_word = candidates(items.lower())
            candidate[items]= list(candidate_word)
            # candidate.append(candidate_word)
            corrected.append(output_text)
            print("Their: ", candidate.items())
            print("Their values: ", candidate.values())

        #
        # for items in output_list:
        #     candid = my_candidate(items.lower())
        #     my_cand[items] = list(candid)
        #     print("my candidates:", my_cand.items())
        #     print("my values:", my_cand.values())
        #     for item in my_cand.values():
        #         for i in range(0,len(item),4):
        #             print(item[i])

        i = 0
        all =[]
        for key, value in candidate.items():
            print(key)
            print(value)
            all.append(value)
            print(all)

        new = []
        partial={}
        for i in range(len(all)):
            if i < len(all)-1:
                permut = list(itertools.product(all[i], all[i+1]))
                print(permut)
                for items in permut:
                    try:
                        partial[items]=(bigram[items])
                        print("partial", partial)
                    except KeyError:
                        partial[items]=0
                new.append(partial.copy())
                partial.clear()
                print("bigram", new)
        res=''
        for i in range(len(new)):
            a = new[i]
            a = dict((k, int(v)) for k, v in a.items())
            b = max(a, key=a.get)
            print(b, a[(b)])
            if i == 0 :
                res = res + b[0] + " " + b[1]
            else:
                res = res + " " + b[1]

        print(res)

        corrected_string = " ".join(corrected)

        text = corrected_string
        matches = tool.check(text)
        context_correct = language_check.correct(text, matches).lower()

        result = request.form
        # context_correct = context(candidate)
        # print(real)
        # a = f_score()
        return render_template("home.html", input=input_text, input_list=input_list, output=corrected_string, candidate=candidate, real=res)

    elif request.method == 'GET':
        return render_template("home.html")


def context(candidate):
    # list of our text file, tokens
    # text = []
    global unigram  # uni-gram dictionary
    unigram = {}
    global bigram  # bi-gram dictionary        # basic implementation
    bigram = {}
    global trigram  # bi-gram dictionary        # basic implementation
    trigram = {}

    with open('data/w2_.txt', 'r', encoding='ISO-8859-1') as f:
        for line in f:
            elements = line.rstrip().split("\t")
            bigram[(elements[1], elements[2])] = elements[0]

    with open('data/w3_.txt', 'r', encoding='ISO-8859-1') as f:
        for line in f:
            elements = line.rstrip().split("\t")
            trigram[(elements[1], elements[2], elements[3])] = elements[0]

    for key, value in candidate.items():
        print(key)
        print(value)
    text = 'their are the trees'
    tokenize = nltk.word_tokenize(text)
    bigrams = ngrams(tokenize, 2)
    trigrams = ngrams(tokenize, 3)

    for bi in bigrams:
        try:
            print(bi[0], bi[1])
            print(bigram[(bi[0], bi[1])])
        except KeyError:
            print("No such key", KeyError)

        for tri in trigrams:
            try:
                print(tri[0], tri[1], tri[2])
                print(trigram[(tri[0], tri[1], tri[2])])
                print(trigram[("There", tri[1], tri[2])])
            except KeyError:
                print("No such key", KeyError)
    return 1


def f_score():
    with open('data/question.txt', 'r') as file1:
        text = file1.read()
    with open('data/right.txt', 'r') as file2:
        correct = file2.read()
    tokenize = nltk.word_tokenize(text)
    token = nltk.word_tokenize(correct)
    print(tokenize)
    print(token)
    TP, FP, FN, TN = 0
    for i in range(len(tokenize)):
        if tokenize[i] == token[i]:
            TP = TP + 1
        else:
            FP = FP + 1
    return TP


if __name__ == '__main__':
    app.run(debug=True)
