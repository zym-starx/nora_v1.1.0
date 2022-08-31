from datetime import datetime
from datetime import time
import random as rnd


def mid_act():
    cont             = ["Is there anything else I can help you with?" , "Is there anything else?", "Is there something else I can help you with?", 
                            "Can I help you with something else?", "Do you need help with something else?", "Is there anything else I can assist you?",
                            "Do you need help with something else?"]

    index = rnd.randint(0, len(cont))
    dropbomb = cont[index-1]

    return dropbomb


def closing_act():
    cont             = ["Goodbye." , "Glad that I could help.", "Feel free to ask me anytime.", "I'm always here to help anytime",  
                            "See you again.", "See you later.", "Goodbye for now."]

    index = rnd.randint(0, len(cont))
    dropbomb = cont[index-1]

    return dropbomb