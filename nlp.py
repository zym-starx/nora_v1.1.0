# importing libraries
import io
import librosa
from time import time
import numpy as np
import IPython.display as ipd
import grpc
import riva_api.riva_nlp_pb2 as rnlp
import riva_api.riva_nlp_pb2_grpc as rnlp_srv


import requests
from bs4 import BeautifulSoup as bs

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

def analyze_intent(text):
    channel = grpc.insecure_channel('localhost:50051')
    riva_nlp = rnlp_srv.RivaLanguageUnderstandingStub(channel)

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
    print(query.items())

def weather_request_response1():
    # enter city name
    city = query["weatherplace"]
    time = query["weathertime"]
    
    # creating url and requests instance
    url = "https://www.google.com/search?q="+"weather"+city+time
    html = requests.get(url).content
    
    # getting raw data
    soup = bs(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    
    # formatting data
    data = str.split('\n')
    time = data[0]
    sky = data[1]
    
    # getting all div tag
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text
    
    # getting other required data
    pos = strd.find('Wind')
    other_data = strd[pos:]
    
    # printing all data
    print("Temperature is", temp)
    print("Time: ", time)
    print("Sky Description: ", sky)
    print(other_data)
        
def weather_request_response2():
    soup = bs(requests.get("https://www.google.com/search?q=weather+london").content)
    soup.find("div", attrs={'id': 'wob_loc'}).text
    soup.find("div", attrs={"id": "wob_dts"}).text
    soup.find("span", attrs={"id": "wob_dc"}).text

def get_weather_data(url):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    # US english
    LANGUAGE = "en-US,en;q=0.5"

    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)
    # create a new soup
    soup = bs(html.text, "html.parser")
    # store all results on this dictionary
    result = {}
    # extract region
    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    # extract temperature now
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    # get the day and hour now
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    # get the actual weather
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
        # get the precipitation
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    # get the % of humidity
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    # extract the wind
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
        # get next few days' weather
    next_days = []
    days = soup.find("div", attrs={"id": "wob_dp"})
    for day in days.findAll("div", attrs={"class": "wob_df"}):
        # extract the name of the day
        day_name = day.findAll("div")[0].attrs['aria-label']
        # get weather status for that day
        weather = day.find("img").attrs["alt"]
        temp = day.findAll("span", {"class": "wob_t"})
        # maximum temparature in Celsius, use temp[1].text if you want fahrenheit
        max_temp = temp[0].text
        # minimum temparature in Celsius, use temp[3].text if you want fahrenheit
        min_temp = temp[2].text
        next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
    # append to result
    result['next_days'] = next_days
    return result

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

def return_response(user_input):

    resp = "I couldn't understand what you mean."

    analyze_intent(user_input)

    URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"
    #import argparse
    #parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
    #parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
    #                                    Default is your current location determined by your IP Address""", default="")
    ## parse arguments
    #args = parser.parse_args()
    #region = args.region
    URL += query["weatherplace"] + query["weatherforecastdaily"] + query["weathertime"]
    # get data
    data = get_weather_data(URL)

    if query["intent"] ==  "weather.weather":
        resp = "Weather for: " + data["region"] + ". " + data['weather_now'] + ". " + "Temperature now is " + data['temp_now'] + " celcius. " + "Precipitation " + data["precipitation"] + ". Humidity " + data["humidity"] + " and Wind is "+  data["wind"]
        
    elif query["intent"] == "weather.temperature":
        resp = "Temperature of " + data["region"] + "is " + data['temp_now'] + "celcius." 

    elif query["intent"] == "weather.Temperature_yes_no":
        resp = "I'm sorry I didn't understand what you mean."

    elif query["intent"] == "weather.rainfall":
        resp = "Precipitation is " + data["precipitation"]

    elif query["intent"] == "weather.rainfall_yes_no":
        resp = "Precipitation is " + data["precipitation"]

    elif query["intent"] == "weather.snow":
        resp = "Sorry. I cannot look for snow right now"

    elif query["intent"] == "weather.snow_yes_no":
        resp = "Sorry. I cannot look for snow right now"

    elif query["intent"] == "weather.humidity":
        resp = "Humidity is " + data["humidity"]

    elif query["intent"] == "weather.humidity_yes_no":
        resp = "Humidity is " + data["humidity"]

    elif query["intent"] == "weather.windspeed":
        resp = "Wind is "+  data["wind"]

    elif query["intent"] == "weather.sunny":
        if data["weather_now"] == "Bulutlu":
            resp = "No it is cloudy."
        elif data["weather_now"] == "Güneşli":
            resp = "Yes it is sunny."

    elif query["intent"] == "weather.cloudy":
        if data["weather_now"] == "Güneşli":
            resp = "No it is sunny."
        elif data["weather_now"] == "Bulutlu":
            resp = "Yes it is cloudy."

    elif query["intent"] == "weather.context":
        resp = "Weather for: " + data["region"] + ". " + data['weather_now'] + ". " + "Temperature now is " + data['temp_now'] + " celcius. " + "Precipitation " + data["precipitation"] + ". Humidity " + data["humidity"]+ " and Wind is "+  data["wind"]

    # print data
    #print("Weather for:", data["region"])
    #print("Now:", data["dayhour"])
    #print(f"Temperature now: {data['temp_now']}°C")
    #print("Description:", data['weather_now'])
    #print("Precipitation:", data["precipitation"])
    #print("Humidity:", data["humidity"])
    #print("Wind:", data["wind"])
    #print("Next days:")
    #for dayweather in data["next_days"]:
    #    print("="*40, dayweather["name"], "="*40)
    #    print("Description:", dayweather["weather"])
    #    print(f"Max temperature: {dayweather['max_temp']}°C")
    #    print(f"Min temperature: {dayweather['min_temp']}°C")

    return resp




