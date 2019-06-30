#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import MeCab
import fasttext as ft
import subprocess


class XXX:
    def main2(self):
        subprocess.check_output(shell=True)
        #return sys.version
        return ''.join([i for i in sys.version.split()])

MODEL = '../data/processing/20190526_名詞のみ.bin'


def text2bow(obj, mod):
    mecab = MeCab.Tagger("-Ochasen")
    morp = mecab.parse(obj)
    words = morp[1]
    words = words.replace('\n','')

    return words

def Scoring(prob):

    score = 0.0
    for e in prob.keys():
        score += e*prob[e]

    return score


def SentimentEstimation(input_txt, clf):

    prob = {}

    bow = text2bow(input_txt, mod="str")

    # print(bow)
    estimate = clf.predict_proba(texts=[bow], k=5)[0]

    for e in estimate:
        index = int(e[0][9])
        prob[index] = e[1]

    score = Scoring(prob)
    return score


def main1(text):
    model = ft.load_model(MODEL)
    score = SentimentEstimation(text, model)
    return score


if __name__ == "__main__":

    main1("HELLO")
