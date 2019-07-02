#!/usr/bin/env python
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# A simple native messaging host. Shows a Tkinter dialog with incoming messages
# that also allows to send message back to the webapp.

import struct
import sys
import threading
import MeCab
import fasttext as ft
import subprocess

MODEL = '../data/processing/20190526_名詞のみ.bin'

def text2bow(obj, mod):
    mecab = MeCab.Tagger("-Owakati")
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

# Python 3 compatibility
if sys.version_info[0] < 3:
    import Queue
else:
    import queue as Queue

# Python 3 compatibility
if sys.version_info[0] < 3:
    try:
        import Tkinter
        import tkMessageBox
    except ImportError:
        Tkinter = None
else:
    try:
        import tkinter as Tkinter
        from tkinter import messagebox
    except ImportError:
        Tkinter = None

# On Windows, the default I/O mode is O_TEXT. Set this to O_BINARY
# to avoid unwanted modifications of the input/output streams.
if sys.platform == "win32":
    import os
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)


# Helper function that sends a message to the webapp.
def send_message(message):
    # Write message size.
    msg_size = struct.pack('I', len(message))

    # For Python 3
    if not sys.version_info[0] < 3:
        msg_size = msg_size.decode(sys.stdout.encoding)

    sys.stdout.write(msg_size)

    # Write the message itself.
    sys.stdout.write(message)
    sys.stdout.flush()


# Thread that reads messages from the webapp.
def read_thread_func(queue):
    while 1:
        # Read the message length (first 4 bytes).
        # Python 3 compatibility
        if sys.version_info[0] < 3:
            text_length_bytes = sys.stdin.read(4)
        else:
            text_length_bytes = sys.stdin.buffer.read(4)

        if len(text_length_bytes) == 0:
            if queue:
                queue.put(None)
            sys.exit(0)

        # Unpack message length as 4 byte integer.
        text_length = struct.unpack("i", text_length_bytes)[0]

        # Read the text (JSON object) of the message.
        # Python 3 compatibility
        if sys.version_info[0] < 3:
            text = sys.stdin.read(text_length).decode("utf-8")
        else:
            text = sys.stdin.buffer.read(text_length).decode("utf-8")

        if queue:
            queue.put(text)
        else:
            # In headless mode just send an echo message back.
            send_message('{"echo": %s}' % text)


if Tkinter:
    class NativeMessagingWindow(Tkinter.Frame):
        def __init__(self, queue):
            self.queue = queue

            Tkinter.Frame.__init__(self)
            self.pack()

            self.text = Tkinter.Text(self)
            self.text.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
            self.text.config(state=Tkinter.DISABLED, height=10, width=40)

            self.messageContent = Tkinter.StringVar()
            self.sendEntry = Tkinter.Entry(self, textvariable=self.messageContent)
            self.sendEntry.grid(row=1, column=0, padx=10, pady=10)

            self.sendButton = Tkinter.Button(self, text="Send", command=self.on_send)
            self.sendButton.grid(row=1, column=1, padx=10, pady=10)

            self.after(100, self.process_messages)

        def process_messages(self):
            while not self.queue.empty():
                message = self.queue.get_nowait()
                if message is None:
                    self.quit()
                    return

                self.log("Received %s" % message)

                t_len = len(message) - 11
                #send_message(message)
                # str_ = message[9:9 + t_len]

                # SEND AGAIN
                #text = '{"text": "' + str_ + '"}'
                #send_message(text)

            self.after(100, self.process_messages)

        def on_send(self):
            text = '{"text":"' + self.messageContent.get() + '"}'
            self.log('Sending %s' % text)
            try:
                send_message(text)
            except IOError:
                tkMessageBox.showinfo('Native Messaging Example',
                                      'Failed to send message.')
                sys.exit(1)

        def log(self, message):
            self.text.config(state=Tkinter.NORMAL)
            self.text.insert(Tkinter.END, message + "\n")
            self.text.config(state=Tkinter.DISABLED)


def main():
    model = ft.load_model(MODEL)
    str_ = str(SentimentEstimation('Hello', model))
    text = '{"text": "' + str_ + '"}'
    send_message(text)

    if not Tkinter:
        send_message('"Tkinter python module wasn\'t found. Running in headless ' +
                     'mode. Please consider installing Tkinter."')
        read_thread_func(None)
        sys.exit(0)

    queue = Queue.Queue()

    main_window = NativeMessagingWindow(queue)
    main_window.master.title('Native Messaging Example')

    thread = threading.Thread(target=read_thread_func, args=(queue, ))
    thread.daemon = True
    thread.start()

    main_window.mainloop()

    sys.exit(0)


if __name__ == '__main__':
    main()