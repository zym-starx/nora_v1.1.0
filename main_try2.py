from contextlib import closing
from tkinter import *
import asr
import nlp
import tts
import openingact
import mid_end_acts
from playsound import playsound
import time
import threading

TEXT_COLOR = "#FFFFFF"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

root = Tk()
root.title("Nora")
root.geometry("560x800")
cont = True
txt = Text(root, bg="#050910", fg=TEXT_COLOR, font=FONT, width=50, height=32)
txt.grid(row=1, column=0, columnspan=2)
scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)
lable1 = Label(root, bg="#D0C9D2", fg=TEXT_COLOR, text="Nora", font=FONT_BOLD, width=50, height=2).grid(row=0)
myLabel = Label(root, bg="#BAADBF", fg=TEXT_COLOR, text="Standby", font=FONT_BOLD, width=50, height=2).grid(row=2)

#open_line = ""
#closing_line = ""
#mid_line = ""
nora_answer = ""
user_input = ""

mode = "OP" # OP / MID / END / ASR / NLP / TTS
exmode = "OP"


def Listening(root):
    global myLabel
    myLabel = Label(root)
    myLabel.destroy()

    tex = "Listening..."
    myLabel = Label(root, bg="#79a57f", fg=TEXT_COLOR, text=tex, font=FONT_BOLD, width=50, height=2).grid(row=2)

def Not_listening(root):
    global myLabel
    myLabel = Label(root)
    myLabel.destroy()

    tex = "Listening..."
    myLabel = Label(root, bg="#BAADBF", fg=TEXT_COLOR, text=tex, font=FONT_BOLD, width=50, height=2).grid(row=2)

def Standby(root):
    global myLabel
    myLabel = Label(root)
    myLabel.destroy()

    tex = "Standby..."
    myLabel = Label(root, bg="#BAADBF", fg=TEXT_COLOR, text=tex, font=FONT_BOLD, width=50, height=2).grid(row=2)

def Speaking(root):
    global myLabel
    myLabel = Label(root)
    myLabel.destroy()

    tex = "Speaking..."
    myLabel = Label(root, bg="#3D5340", fg=TEXT_COLOR, text=tex, font=FONT_BOLD, width=50, height=2).grid(row=2)

def Opening(txt):
    global nora_answer
    nora_answer = openingact.opening_act()
    txt.insert(END, "\n" + "Nora -> " + nora_answer)

def ASR(txt):
    global user_input
    user_input = asr.asr()
    send = "You -> " + user_input
    txt.insert(END, "\n" + send)

def NLP():
    global nora_answer
    nora_answer = nlp.return_response(user_input)
    txt.insert(END, "\n" + "Nora -> " + nora_answer)

def TTS():
    global nora_answer
    nora_answer_tts = tts.tts(nora_answer)
    nora_answer_tts = "testsounds/" + nora_answer_tts
    time.sleep(1)
    playsound(nora_answer_tts)

def Mid(txt):
    global nora_answer
    nora_answer = mid_end_acts.mid_act()
    txt.insert(END, "\n" + "Nora -> " + nora_answer)

def Closing(txt):
    global nora_answer
    nora_answer = mid_end_acts.closing_act()
    txt.insert(END, "\n" + "Nora -> " + nora_answer)

def user_bye(user_input):
    user_input = str(user_input)
    global cont
    if (user_input.find("goodbye") != -1 or user_input.find("Goodbye") != -1):
        cont = False
    elif (user_input.find("good bye") != -1):
        cont = False
    else:
        cont = True

def empty():
    return

def main():
    global myLabel
    global mode, exmode, nora_answer, user_input, cont

    myLabel = Label(root)

    if(mode == "OP"):
        Standby(root)   
        root.after(1000, Opening, txt)
        exmode = "OP"
        mode = "TTS"

    elif(mode == "MID"):
        root.after(100, Mid, txt)
        exmode = "MID"
        mode = "TTS"
        Standby(root)

    elif(mode == "END"):
        root.after(100, Closing, txt)
        exmode = "END"
        mode = "TTS"
        Speaking(root)
    
    elif(mode == "ASR"):
        Listening(root)
        root.after(500, ASR, txt)
        Not_listening(root)
        exmode = "ASR"
        mode = "NLP"

    elif(mode == "NLP"):
        user_bye(user_input=user_input)

        if (cont == False):
            exmode = "NLP"
            mode = "END"
        else:
            root.after(500, NLP)
            exmode = "NLP"
            mode = "TTS"

    elif(mode == "TTS"):
        Speaking(root)
        root.after(100, TTS)

        if (exmode == "OP"):
            mode = "ASR"
        elif (exmode == "MID"):
            mode = "ASR"
        elif (exmode == "END"):
            mode = "none"
            time.sleep(5)
            root.destroy()
        elif (exmode == "NLP"):
            mode = "MID"

    root.after(1000, main)
    root.mainloop()

if __name__ == '__main__':
    main()


import os, shutil
folder = 'C:/zym/nora/nora_v1.1.0/testsounds'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))