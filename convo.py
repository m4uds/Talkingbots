from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import re
import torch
import numpy as np
import json
import handle_json
import random
from time import gmtime, strftime, sleep
import datetime



#appendJSON("no thanks")
def get_last():
    log_file = f = open('conversation_log.json')
    data =  json.load(log_file)
    data = data["Conversation"][-1]
    for key, value in data.items():
        return(value)

print("innit begins")

def temp():
    random_num = random.randint(5,85)
    print(random_num)
    return random_num

#load models
tokenizer_blender = AutoTokenizer.from_pretrained("models/blenderbot-400M-distill")
model_blender = AutoModelForSeq2SeqLM.from_pretrained("models/blenderbot-400M-distill")
tokenizer_Dialo = AutoTokenizer.from_pretrained("models/DialoGPT-medium")
model_Dialo = AutoModelForCausalLM.from_pretrained("models/DialoGPT-medium") 
chat_history = False
chat_history_ids = []

def blenderBot(message):
    if len(message) > 128:
        message = message[:128]
        print(message)
    inputs = tokenizer_blender(message, return_tensors="pt")
    result = model_blender.generate(**inputs, output_scores=True, top_k=100, top_p=0.5, temperature=1, num_beams= temp())
    blender = tokenizer_blender.decode(result[0])
    blender_output = re.search(r'<s> (.*?)</s>', blender).group(1)
    return blender_output




def main(chat_history):
    
    last_blender = ""
    last_dialo = ""
    ###############
    # first response
    ###############
    last_response = handle_json.get_last()
    print(last_response)

    if last_response.startswith("DialoGPT"):
        blender = blenderBot("last_response")
        appendJSON("Blender: " + blender)
        print("Blender: " + blender)
    
    blender = last_response
    new_input_ids = tokenizer_Dialo.encode((blender) + tokenizer_Dialo.eos_token, return_tensors='pt')
    chat_history_ids = model_Dialo.generate(new_input_ids, max_length=100, pad_token_id=tokenizer_Dialo.eos_token_id, do_sample=True, top_k=100, top_p=0.7, temperature=0.96)
    # pretty print last ouput tokens from bot
    dialo = tokenizer_Dialo.decode(chat_history_ids[:, new_input_ids.shape[-1]:][0], skip_special_tokens=True)
    appendJSON("DialoGPT: "+ dialo)
    print("DialoGPT: "+ dialo)
    
    
    for step in range(5):
        
        
      
        
        
        
        blender_last = blender
        blender = blenderBot(dialo)
         
        if blender != blender_last:
            ts_ago = seconds_since_last_TS()
            if ts_ago < 10:
                sleep(10-ts_ago)
            appendJSON("Blender: " + blender)
            print("Blender: " + blender)
        else:
            print("blender confused")
            x = False
        
        
        dialo_last = dialo
        new_input_ids = tokenizer_Dialo.encode((blender) + tokenizer_Dialo.eos_token, return_tensors='pt')
        # append the new input tokens to the chat history
        if chat_history == True:
            bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) 
        else:
            bot_input_ids = new_input_ids
        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model_Dialo.generate(new_input_ids, max_length=100, pad_token_id=tokenizer_Dialo.eos_token_id, do_sample=True, top_k=200, top_p=1.5, temperature=0.75)
    
        # pretty print last ouput tokens from bot
        dialo = tokenizer_Dialo.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        if dialo != dialo_last:
            ts_ago = seconds_since_last_TS()
            if ts_ago < 10:
                sleep(10-ts_ago)
            appendJSON("DialoGPT: " + dialo)
            print("DialoGPT: "+ dialo)
        else:
            print("DialoGPT confused")
            x = False
        print("+")




def appendJSON(input_string):

    log_file = f = open('conversation_log.json')
    data =  json.load(log_file)
    time_now = str(datetime.datetime.now())
    data["Conversation"].append({time_now: input_string})
    with open('conversation_log.json', 'w') as nf:
        json.dump(data, nf)
    if len(data["Conversation"]) > 5 :
        with open('conversation.json', "w") as nf:
            json.dump(data["Conversation"][-5:], nf)




def seconds_since_last_TS():
    log_file = f = open('conversation_log.json')
    data =  json.load(log_file)
    data = data["Conversation"][-1]
    for key, value in data.items():
        
        last_time = datetime.datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f")
        time_now = datetime.datetime.now()
        seconds = (time_now - last_time).seconds
        seconds = float(seconds)
        print(seconds)
        return(seconds)
        
        
        print("Seconds since last: " + str(seconds))
        
        return(seconds)





if __name__ == "__main__":
   while True:
     main(False)