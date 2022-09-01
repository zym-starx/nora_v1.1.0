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

#open_line = ""
#closing_line = ""
nora_answer = ""
#mid_line = ""
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

def TTS(nora_answer):
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

def user_bye(user_input, cont):
    user_input = str(user_input)
    if (user_input.find("goodbye") or user_input.find("Goodbye")):
        cont = False
    else:
        cont = True

def main():
    root = Tk()
    root.title("Nora")
    root.geometry("560x800")
    cont = True
    did_open = False
    myLabel = Label(root)

    lable1 = Label(root, bg="#D0C9D2", fg=TEXT_COLOR, text="Nora", font=FONT_BOLD, width=50, height=2).grid(row=0)

    txt = Text(root, bg="#050910", fg=TEXT_COLOR, font=FONT, width=50, height=32)
    txt.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)

    myLabel = Label(root, bg="#BAADBF", fg=TEXT_COLOR, text="Standby", font=FONT_BOLD, width=50, height=2).grid(row=2)


    if(mode == "OP"):
        Standby(root)   
        root.after(1000, Opening)
        exmode = "OP"
        mode = "TTS"

    elif(mode == "MID"):
        root.after(500, Mid)
        exmode = "MID"
        mode = "TTS"
        Speaking()

    elif(mode == "END"):
        root.after(500, Closing)

        exmode = "END"
        mode = "TTS"
    
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
        root.after(500, TTS, nora_answer)
        Not_listening()

        if (exmode == "OP"):
            mode = "ASR"
        elif (exmode == "MID"):
            mode = "ASR"
        elif (exmode == "END"):
            mode = "none"
            root.destroy()
        elif (exmode == "NLP"):
            mode = "ASR"

    root.mainloop()

if __name__ == '__main__':
    main()