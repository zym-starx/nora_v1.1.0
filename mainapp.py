from tkinter import *
import asr
import nlp
import tts
import openingact
import mid_end_acts
from playsound import playsound
import time

# GUI
root = Tk()
root.title("Chatbot")
 
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
 
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
 
# Send function
def send():
    open_line = openingact.opening_act()
    nora_answer_tts = tts.tts(open_line)
    playsound(nora_answer_tts)
    txt.insert(END, "\n" + "Nora -> " + open_line)

    

    user_input = asr.asr()
    send = "You -> " + user_input
    txt.insert(END, "\n" + send)

    print(user_input)
    nora_answer = nlp.return_response(user_input)
    nora_answer_tts = tts.tts(nora_answer)
 
    playsound(nora_answer_tts)
    txt.insert(END, "\n" + "Nora -> " + nora_answer)
    
 
    e.delete(0, END)
 
 
lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Nora", font=FONT_BOLD, pady=10, width=20, height=1).grid(
    row=0)
 
txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
txt.grid(row=1, column=0, columnspan=2)
 
scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)
 
e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
e.grid(row=2, column=0)
 
send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
              command=send).grid(row=2, column=1)
 
root.mainloop()