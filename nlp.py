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


