from tkinter import *
import asr
import nlp
import tts
import openingact
from playsound import playsound
import time

loop = TRUE

while(loop):
    open_line = openingact.opening_act()
    nora_answer_tts = tts.tts(open_line)
    nora_answer_tts = "testsounds/" + nora_answer_tts
    time.sleep(3)
    print("\n" + "Nora -> " + open_line)
    playsound(nora_answer_tts)

    time.sleep(2)

    user_input = asr.asr()
    send = "You -> " + user_input
    print("\n" + send)

    print(user_input)
    nora_answer = nlp.return_response(user_input)
    nora_answer_tts = tts.tts(nora_answer)
    nora_answer_tts = "testsounds/" + nora_answer_tts
    time.sleep(3)
    print("\n" + "Nora -> " + nora_answer)
    playsound(nora_answer_tts)

    user_input = asr.asr()
    send = "You -> " + user_input
    print("\n" + send)
