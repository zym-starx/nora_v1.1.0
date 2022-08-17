from datetime import datetime
from datetime import time
import random as rnd


def opening_act():
    ## creating an opening line for Nora 
    ## for the first open up

    now = datetime.now()

    a = time(5,0,0)
    b = time(12,0,0)
    c = time(18,0,0)
    d = time(21,0,0)
    e = time(23,59,59)
    f = time(2,0,0)

    nowtime = now.time()
    current_time = now.strftime("%H:%M:%S")

    morning             = ["Good morning!" , "Rise and shine!", "Top of the morning to you.", 
                            "Good day.", "Isn't it a beautiful day today?"]
    afternoon           = ["Good afternoon!", "Have a good afternoon."]
    evening             = ["Good evening.", "Have a good evening."]
    night               = ["Good night.", "It looks like a good afternoon.", "Nighty night."]
    late_night          = ["Isn't it a bit late?", "Good night."]
    greetings_before    = ["Hi!", "Hello.", "Hey!"]
    greetings_after     = ["How are you today?", "How is it going?", "How are you?"]
    helpscript          = ["How can I help you?", "How may I help?", "Do you need something?", 
                            "What can I do for you?", "Want me to help you with something?"]

    dropbomb = ""

    if ("05:00:00" < current_time < "12:00:00"):
        index1 = rnd.randint(0, len(greetings_before))
        index2 = rnd.randint(0, len(morning))
        index3 = rnd.randint(0, len(helpscript))

        dropbomb = dropbomb + " " + greetings_before[index1-1] +  " " + morning[index2-1] +  " " + helpscript[index3-1]

    elif ("12:00:00" < current_time < "17:00:00"):
        index1 = rnd.randint(0, len(greetings_before))
        index2 = rnd.randint(0, len(afternoon))
        index3 = rnd.randint(0, len(helpscript))

        dropbomb = dropbomb +  " " + greetings_before[index1-1] +  " " + afternoon[index2-1] +  " " + helpscript[index3-1]

    elif ("17:00:00" < current_time < "20:00:00"):
        index1 = rnd.randint(0, len(greetings_before))
        index2 = rnd.randint(0, len(evening))
        index3 = rnd.randint(0, len(helpscript))

        dropbomb = dropbomb +  " " + greetings_before[index1-1] +  " " + evening[index2-1] +  " " + helpscript[index3-1]

    elif ("20:00:00" < current_time or current_time < "02:00:00"):
        index1 = rnd.randint(0, len(greetings_before))
        index2 = rnd.randint(0, len(night))
        index3 = rnd.randint(0, len(helpscript))

        dropbomb = dropbomb +  " " + greetings_before[index1-1] +  " " + night[index2-1] +  " " + helpscript[index3-1]

    elif ("02:00:00" < current_time < "05:00:00"):
        index1 = rnd.randint(0, len(greetings_before))
        index2 = rnd.randint(0, len(late_night))
        index3 = rnd.randint(0, len(helpscript))

        dropbomb = dropbomb +  " " + greetings_before[index1-1] +  " " + late_night[index2-1] +  " " + helpscript[index3-1]

    return dropbomb