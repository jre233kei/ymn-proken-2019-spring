# -*- coding: utf-8 -*-

import sys
import subprocess as cmd
import fasttext as ft


def text2bow(obj, mod):

    # input: ファイルの場合はmod="file", input: 文字列の場合はmod="str"
    if mod == "file":
        morp = cmd.getstatusoutput("cat " + obj + " | mecab -Owakati")
    elif mod == "str":
        morp = cmd.getstatusoutput("echo " + obj + " | mecab -Owakati")
    else:
        print ("error!!")
        sys.exit(0)

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

    estimate = clf.predict_proba(texts=[bow], k=5)[0]

    for e in estimate:
        index = int(e[0][9])
        prob[index] = e[1]

    score = Scoring(prob)

    return score


def output(score):

    print ("Evaluation Score = " + str(score))

    if score < 1.8:
        print ("Result: negative--")
    elif score >= 1.8 and score < 2.6:
        print ("Result: negative-")
    elif score >= 2.6 and score < 3.4:
        print ("Result: neutral")
    elif score >= 3.4 and score < 4.2:
        print ("Result: positive+")
    elif score >= 4.2:
        print ("Result: positive++")
    else:
        print ("error")
        sys.exit(0)


def main(model):

    print ("This program is able to estimate to sentiment in sentence.")
    print ("Estimation Level:")
    print ("    negative-- < negative- < neutral < positive+ < positive++")
    print ("    bad    <---------------------------------------->    good")
    print ("Input:")

    while True:

        input_txt = input()

        if input_txt == "exit":
            print ("bye!!")
            sys.exit(0)

        score = SentimentEstimation(input_txt, model)

        output(score)


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