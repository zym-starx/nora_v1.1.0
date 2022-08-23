# required imports
import io
import librosa
from time import time
import numpy as np
import IPython.display as ipd
import grpc
import requests

import riva_api.riva_nlp_pb2 as rnlp
import riva_api.riva_nlp_pb2_grpc as rnlp_srv

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

#def answer_question(question):
#    '''
#    This function takes in a question, embeds it and looks for paragraphs that would be semantically
#    most similar. It then takes top 10 of such paragraphs and concatenates them to create a context.
#    
#    We then ship the context over to Riva, to the Triton inference server and print the output
#    '''
#    #query_embedding = model.encode(question)
#    #similarities = util.pytorch_cos_sim(query_embedding, paragraph_embeddings)
##
#    #context = ''
#    #for idx in similarities.argsort()[0].flip(0)[:10]:
#    #    context += paragraphs[idx]
#
#    channel = grpc.insecure_channel('localhost:50051')
#    riva_nlp = rnlp_srv.RivaLanguageUnderstandingStub(channel)
#    req = rnlp.NaturalQueryRequest()
#    req.query = question
#    req.context = context
#    resp = riva_nlp.NaturalQuery(req)
#
#    print(f"Query: {question}")
#    print(f"Answer: {resp.results[0].answer}")
#
#answer_question("How are you doing today?")


query = {
    "intent" : "",
    "domain" : "",

    "O" : "",
    "weathertime" : "today",
    "weatherplace" : "ankara",
    "temperatureunit" : "",
    "current_location" : "",
    "wind_speed_unit" : "",
    "rainfallunit" : "",
    "snowunit" : "",
    "alert_type" : "",
    "weatherforecastdaily" : ""
}

class nlp_query:
    intent = ""
    slots = []
    domain = ""


def analyze_intent():
    channel = grpc.insecure_channel('localhost:50051')
    riva_nlp = rnlp_srv.RivaLanguageUnderstandingStub(channel)

    text = "Is it cloudy in New York next week?"

    req = rnlp.AnalyzeIntentRequest()
    req.query = str(text)
    req.options.domain = "weather"
    
    # The <domain_name> is appended to "riva_intent_" to look for a model "riva_intent_<domain_name>"
    # So the model "riva_intent_<domain_name>" needs to be preloaded in riva server.
    # In this case the domain is weather and the model being used is "riva_intent_weather-misc".

    resp = riva_nlp.AnalyzeIntent(req)

    #try:
    #    req = rnlp.AnalyzeIntentRequest()
    #    req.query = str(text)
    #    # The <domain_name> is appended to "riva_intent_" to look for a model "riva_intent_<domain_name>"
    #    # So the model "riva_intent_<domain_name>" needs to be preloaded in riva server.
    #    # In this case the domain is weather and the model being used is "riva_intent_weather-misc".
    #    req.options.domain = "weather"
    #    resp = riva_nlp.AnalyzeIntent(req)
    #except Exception as inst:
    #    # An exception occurred
    #    print("[Riva NLU] Error during NLU request")
    #    return {'riva_error': 'riva_error'}

    string_resp = ""
    string_resp = str(resp)
    
    #print(type(string_resp))
    #print(string_resp)
    #line.replace("class_name: ", "")
    #line.replace('""', "")
    #print(line)

    main = ""

    #for line in string_resp.splitlines():
    #    if line == "intent {":
    #        main = "intent"
    #        for x in range(3):
    #            if "class_name:" in line:
                    
    smth = string_resp.split("}")

    for x in smth:
        main = ""
        token = ""
        class_name = ""
        if x.find('  token: "?"') != -1:
            continue

        for line in x.splitlines():
            if line == "":
                continue
            elif line == "slots {":
                main = "slot"
            elif line == "intent {":
                main = "intent"
            elif line == 'domain_str: "weather"':
                main = "domain"
            else:
                if line.find("token") != -1:
                    line = line.replace("token: ", "")
                    line = line.replace('"', "")
                    line = line.replace('   ', "")
                    line = line.replace(' ', "")
                    if line == "?":
                        continue
                    else:
                        token = line

                elif line.find("class_name:") != -1:
                    line = line.replace("class_name: ", "")
                    line = line.replace('"', "")
                    line = line.replace('   ', "")
                    line = line.replace(' ', "")
                    class_name = line
                
                else:
                    continue
        
        if main == "slot":
            query[class_name] = token
        elif main == "intent":
            query['intent'] = class_name
        elif main == "domain":
            query['domain'] = class_name

    #for x in query:
    #    print(x , " -> ", query[x], "\n")


        




def analyze_entities():
    channel = grpc.insecure_channel('localhost:50051')
    riva_nlp = rnlp_srv.RivaLanguageUnderstandingStub(channel)

    text = "Have you ever heard of 'Among Us' Gregory?"

    req = rnlp.AnalyzeEntitiesRequest()
    req.query = str(text)

    resp = riva_nlp.AnalyzeEntities(req)
    print(resp)
    
    
def classify_text():
    channel = grpc.insecure_channel('localhost:50051')
    riva_nlp = rnlp_srv.RivaLanguageUnderstandingStub(channel)

    query = "Have you ever heard of 'Among Us' Gregory?"

    req = rnlp.TextClassRequest()
    req.text(query)
   

    resp = riva_nlp.ClassifyText(req)
    print(resp)

#classify_text()

analyze_intent()