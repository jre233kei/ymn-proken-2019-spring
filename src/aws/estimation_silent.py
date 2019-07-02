# -*- coding: utf-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/modules')

from janome.tokenizer import Tokenizer
import fasttext as ft

MODEL = '20190526_名詞のみ.bin'


def text2bow(obj, mod):

    t = Tokenizer()


    # words = " ".join(nagisa.tagging(obj))
    words = " ".join(t.tokenize(obj, wakati=True))
    words = words.replace('\n', '')

    return words


def Scoring(prob):

    score = 0.0
    for e in prob.keys():
        score += e*prob[e]

    return score


def SentimentEstimation(input_txt, clf):

    prob = {}

    bow = text2bow(input_txt, mod="str")

    estimate = clf.predict_proba(texts=[bow], k=5)[0]

    for e in estimate:
        index = int(e[0][9])
        prob[index] = e[1]

    score = Scoring(prob)
    return score


def main(text):

    model = ft.load_model(MODEL)
    score = SentimentEstimation(text, model)
    return score

if __name__ == "__main__":
    text = 'これはテストです。'
    print(main(text))
