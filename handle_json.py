import json
import os
from time import gmtime, strftime


def appendJSON(input_string):

    log_file = f = open('conversation_log.json')
    data =  json.load(log_file)
    time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    data["Conversation"].append({time_now: input_string})
    with open('conversation_log.json', 'w') as nf:
        json.dump(data, nf)
    if len(data["Conversation"]) > 5 :
        with open('conversation.json', "w") as nf:
            json.dump(data["Conversation"][-5:], nf)


#appendJSON("no thanks")
def get_last():
    log_file = f = open('conversation_log.json')
    data =  json.load(log_file)
    data = data["Conversation"][-1]
    for key, value in data.items():
        return(value)


