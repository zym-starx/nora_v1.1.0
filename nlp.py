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




def analyze_intent():
    channel = grpc.insecure_channel('localhost:50051')
    riva_nlp = rnlp_srv.RivaLanguageUnderstandingStub(channel)

    text = "How is the weather in New York tomorrow?"

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
    
    print(type(string_resp))
    print(string_resp)


    for line in string_resp.splitlines():
        if line == "intent {":
            for x in range(3) and line in string_resp.splitlines():



    ##include <iostream>
    ##include <vector>
    #using namespace std;
#
#
    #string line;
    #struct nlp_object{
    #    string intent;
    #    vector<pair<string,string>> slots;
    #    string domain;
    #};
#
    #nlp_object query;
#
    #while(line = getline(input)){
    #    if(line == "intent {"){
    #        for (int i = 0; i < 3; i++){
    #            line = getline(input);
    #            line = 
    #        }
    #    }
    #}

                


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