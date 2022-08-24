
import io
import librosa
from time import time
import numpy as np
import IPython.display as ipd
import grpc
import requests

# NLP proto
import jarvis_api.jarvis_nlp_core_pb2 as jcnlp
import jarvis_api.jarvis_nlp_core_pb2_grpc as jcnlp_srv
import jarvis_api.jarvis_nlp_pb2 as jnlp
import jarvis_api.jarvis_nlp_pb2_grpc as jnlp_srv

# ASR proto
import jarvis_api.jarvis_asr_pb2 as jasr
import jarvis_api.jarvis_asr_pb2_grpc as jasr_srv

# TTS proto
import jarvis_api.jarvis_tts_pb2 as jtts
import jarvis_api.jarvis_tts_pb2_grpc as jtts_srv
import jarvis_api.audio_pb2 as ja

channel = grpc.insecure_channel('localhost:50051')

jarvis_asr = jasr_srv.JarvisASRStub(channel)
jarvis_nlp = jnlp_srv.JarvisNLPStub(channel)
jarvis_cnlp = jcnlp_srv.JarvisCoreNLPStub(channel)
jarvis_tts = jtts_srv.JarvisTTSStub(channel)

# Use the TextTransform API to run the punctuation model
req = jcnlp.TextTransformRequest()
req.model.model_name = "jarvis_punctuation"
req.text.append("add punctuation to this sentence")
req.text.append("do you have any red nvidia shirts")
req.text.append("i need one cpu four gpus and lots of memory "
                "for my new computer it's going to be very cool")

nlp_resp = jarvis_cnlp.TransformText(req)
print("TransformText Output:")
print("\n".join([f" {x}" for x in nlp_resp.text]))

# Use the TokenClassification API to run a Named Entity Recognition (NER) model
# Note: the model configuration of the NER model indicates that the labels are
# in IOB format. Jarvis, subsequently, knows to:
#   a) ignore 'O' labels
#   b) Remove B- and I- prefixes from labels
#   c) Collapse sequences of B- I- ... I- tokens into a single token

req = jcnlp.TokenClassRequest()
req.model.model_name = "jarvis_ner"     # If you have deployed a custom model with the domain_name
                                        # parameter in ServiceMaker's `jarvis-build` command then you should use
                                        # "jarvis_ner_<your_input_domain_name>" where <your_input_domain_name>
                                        # is the name you provided to the domain_name parameter.

req.text.append("Jensen Huang is the CEO of NVIDIA Corporation, "
                "located in Santa Clara, California")
resp = jarvis_cnlp.ClassifyTokens(req)

print("Named Entities:")
for result in resp.results[0].results:
    print(f"  {result.token} ({result.label[0].class_name})")

:
# Submit a TextClassRequest for text classification.
# Jarvis NLP comes with a default text_classification domain called "domain_misty" which consists of
# 4 classes: meteorology, personality, weather and nomatch

request = jcnlp.TextClassRequest()
request.model.model_name = "jarvis_text_classification_domain"       # If you have deployed a custom model
                                        # with the `--domain_name` parameter in ServiceMaker's `jarvis-build` command
                                        # then you should use "jarvis_text_classification_<your_input_domain_name>"
                                        # where <your_input_domain_name> is the name you provided to the
                                        # domain_name parameter. In this case the domain_name is "domain"
request.text.append("Is it going to snow in Burlington, Vermont tomorrow night?")
request.text.append("What causes rain?")
request.text.append("What is your favorite season?")
ct_response = jarvis_cnlp.ClassifyText(request)
print(ct_response)