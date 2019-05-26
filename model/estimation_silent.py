# -*- coding: utf-8 -*-

import sys
import subprocess as cmd
import MeCab
import fasttext as ft
from sklearn.metrics import mean_squared_error


def text2bow(obj, mod):

    # input: ファイルの場合はmod="file", input: 文字列の場合はmod="str"

    """
    if mod == "file":
        morp = cmd.getstatusoutput("cat " + obj + " | mecab -Owakati")
    elif mod == "str":
        morp = cmd.getstatusoutput("echo " + obj + " | mecab -Owakati")
    else:
        print ("error!!")
        sys.exit(0)
    """

    mecab = MeCab.Tagger("-Ochasen")
    morp = mecab.parse(obj)

    # print(morp)

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


def main(model):

    true = []
    pred = []

    path = '../data/processing/test.txt'
    test_text = open(path, 'r')

    for t in test_text:
        true.append(int(t[0]))
        score = SentimentEstimation(t[1:], model)
        pred.append(score)
        print('true is : ' + t[0])
        print('pred is : ' + str(score))
        print('--')

    print(mean_squared_error(true, pred))


if __name__ == "__main__":

    argvs = sys.argv

    _usage = """--                                                                                                                                                       
Usage:                                                                                                                                                                   
    python estimation.py [model]                                                                                                                                         
Args:                                                                                                                                                                    
    [model]: The argument is a model for sentiment estimation that is trained by fastText.                                                                               
""".rstrip()

    if len(argvs) < 2:
        print (_usage)
        sys.exit(0)

    model = ft.load_model(argvs[1])

    main(model)