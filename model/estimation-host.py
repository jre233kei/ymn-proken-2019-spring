# -*- coding: utf-8 -*-

import MeCab
import fasttext as ft
import struct
import sys
import threading
import queue
import json

import tkinter
from tkinter import messagebox as tkMessageBox


MODEL = "../data/processing/20190526_名詞のみ.bin"

def text2bow(obj):
    mecab = MeCab.Tagger("-Ochasen")
    morp = mecab.parse(obj)

    words = morp[1]
    words = words.replace('\n', '')

    return words


def Scoring(prob):
    score = 0.0
    for e in prob.keys():
        score += e * prob[e]

    return score


def SentimentEstimation(input_txt, clf):
    prob = {}

    bow = text2bow(input_txt)

    # print(bow)
    estimate = clf.predict_proba(texts=[bow], k=5)[0]

    for e in estimate:
        index = int(e[0][9])
        prob[index] = e[1]

    score = Scoring(prob)
    return score


# Below is extension back-end


# On Windows, the default I/O mode is O_TEXT. Set this to O_BINARY
# to avoid unwanted modifications of the input/output streams.
if sys.platform == "win32":
    import os, msvcrt

    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)


# Helper function that sends a message to the webapp.
def send_message(message):
    """
    # Write message size.
    msg_size = ""
    msg_size = msg_size.decode(sys.stdout.encoding)
    # Write the message itself.
    sys.stdout.write(msg_size)
    """
    sys.stdout.write(message)
    msg_text = json.loads(message)["text"]
    score = SentimentEstimation(msg_text, model)
    # print(msg_text)
    sys.stdout.write(str(score))
    sys.stdout.flush()


# Thread that reads messages from the webapp.
def read_thread_func(queue_):
    message_number = 0
    while 1:
        # Read the message length (first 4 bytes).
        text_length_bytes = sys.stdin.buffer.read(4)

        if len(text_length_bytes) == 0:
            if queue_:
                queue_.put(None)
            sys.exit(0)

        # Unpack message length as 4 byte integer.
        text_length = struct.unpack('i', text_length_bytes)[0]

        # Read the text (JSON object) of the message.
        text = sys.stdin.buffer.read(text_length).decode("utf-8")

        if queue_:
            queue_.put(text)
        else:
            # In headless mode just send an echo message back.
            send_message('{"echo": %s}' % text)


if tkinter:
    class NativeMessagingWindow(tkinter.Frame):
        def __init__(self, queue_):
            self.queue_ = queue_

            tkinter.Frame.__init__(self)
            self.pack()

            self.text = tkinter.Text(self)
            self.text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
            self.text.config(state=tkinter.DISABLED, height=10, width=40)

            self.messageContent = tkinter.StringVar()
            self.sendEntry = tkinter.Entry(self, textvariable=self.messageContent)
            self.sendEntry.grid(row=1, column=0, padx=10, pady=10)

            self.sendButton = tkinter.Button(self, text="Send", command=self.onSend)
            self.sendButton.grid(row=1, column=1, padx=10, pady=10)

            self.after(100, self.processMessages)

        def processMessages(self):
            while not self.queue_.empty():
                message = self.queue_.get_nowait()
                if message == None:
                    self.quit()
                    return
                self.log("Received %s" % message)

            self.after(100, self.processMessages)

        def onSend(self):
            text = '{"text": "' + self.messageContent.get() + '"}'
            self.log('Sending %s' % text)
            try:
                send_message(text)
            except IOError:
                tkMessageBox.showinfo('Native Messaging Example',
                                      'Failed to send message.')
                sys.exit(1)

        def log(self, message):
            self.text.config(state=tkinter.NORMAL)
            self.text.insert(tkinter.END, message + "\n")
            self.text.config(state=tkinter.DISABLED)


def Main():

    if not tkinter:
        send_message('"tkinter python module wasn\'t found. Running in headless ' +
                     'mode. Please consider installing tkinter."')

        read_thread_func(None)
        sys.exit(0)

    queue_ = queue.Queue()

    main_window = NativeMessagingWindow(queue_)
    main_window.master.title('Native Messaging Example')

    thread = threading.Thread(target=read_thread_func, args=(queue_,))
    thread.daemon = True
    thread.start()

    main_window.mainloop()

    sys.exit(0)

"""

path = argvs[2]
test_text = open(path, 'r')

for t in test_text:
    true.append(int(t[0]))
    score = SentimentEstimation(t[1:], model)
    pred.append(score)
    print('true is : ' + t[0])
    print('pred is : ' + str(score))
    print('--')
"""

if __name__ == "__main__":
    model = ft.load_model(MODEL)

    Main()
