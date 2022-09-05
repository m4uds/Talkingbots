from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import re
import torch
import numpy as np
import pyttsx3
import json
import amend_json

tokenizer_one = AutoTokenizer.from_pretrained("models/blenderbot-400M-distill")
model_one = AutoModelForSeq2SeqLM.from_pretrained("models/blenderbot-400M-distill")
tokenizer_two = AutoTokenizer.from_pretrained("models/DialoGPT-medium")
model_two = AutoModelForCausalLM.from_pretrained("models/DialoGPT-medium")


def next_response(message, model, tokenizer):
  inputs = tokenizer(message, return_tensors="pt")
  result = model.generate(**inputs)
  blender = tokenizer.decode(result[0])
  blender = re.search(r'<s> (.*?)</s>', blender).group(1)
  print("Blender: " + blender)
  amend_json.appendJSON("Blender: " + blender)
  
  #engine_blender.setProperty('voice', voices[10].id)
  #engine_blender.say(blender)
  #engine_blender.runAndWait()

  return blender


#dialio = "do you know how much energy was required to create us??"
dialio = amend_json.get_last()
dialio_last = dialio


#engine_dialio = pyttsx3.init() # object creation
#voices = engine.getProperty('voices')
#print(voices)

#engine_blender = pyttsx3.init() # object creation

#voices = engine_blender.getProperty('voices')
#engine_blender.setProperty('voice', voices[6].id)
#print(voices)

step = 0
blender_last = ""
while True:
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer_two.encode(next_response(dialio,model_one,tokenizer_one) + tokenizer_two.eos_token, return_tensors='pt')
    if new_user_input_ids == blender_last:
        new_user_input_ids = tokenizer_two.encode(next_response("",model_one,tokenizer_one) + tokenizer_two.eos_token, return_tensors='pt')
    
    # append the new user input tokens to the chat history
    if step > 0:
        
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) 
    else:
        bot_input_ids = new_user_input_ids 

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model_two.generate(bot_input_ids, max_length=5000, pad_token_id=tokenizer_two.eos_token_id)
    # pretty print last ouput tokens from bot
    dialio = tokenizer_two.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    if  dialio == "" or dialio == "I" or dialio == dialio_last:
        bot_input_ids = new_user_input_ids 
         # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model_two.generate(bot_input_ids, max_length=10000, pad_token_id=tokenizer_two.eos_token_id)
        # pretty print last ouput tokens from bot
        dialio = tokenizer_two.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
  

    dialio_last = dialio
    print("DialoGPT: "+ dialio)
    amend_json.appendJSON("DialoGPT: "+ dialio)
    step = step +1


    #engine_blender.setProperty('voice', voices[0].id)
    #engine_dialio.say(dialio)
    #engine_dialio.runAndWait()
