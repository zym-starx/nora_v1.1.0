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

def Opening():
    global open_line
    open_line = openingact.opening_act()

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
    print("\n" + "Nora -> " + nora_answer)
    time.sleep(1)
    playsound(nora_answer_tts)

def Mid():
    global mid_line
    mid_line = mid_end_acts.mid_act()

def Closing():
    global closing_line  
    closing_line = mid_end_acts.closing_act()

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

    if(did_open == False):
        Speaking(root)    
        root.after(1000, Opening)
        root.after(1000, TTS, open_line)
        did_open = True
        Not_listening(root)
        

    if(cont == True):
        Listening(root)
        root.after(500, ASR, txt)
        Not_listening(root)
        root.after(500, NLP)
        Speaking(root)
        root.after(500, TTS, nora_answer)

        root.after(500, Mid)
        root.after(500, TTS, mid_line)
    else:
        root.after(500, Closing)


    

    root.mainloop()

if __name__ == '__main__':
    main()