from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import re
import torch
import numpy as np
import json
import handle_json
    #load models
tokenizer_blender = AutoTokenizer.from_pretrained("models/blenderbot-400M-distill")
model_blender = AutoModelForSeq2SeqLM.from_pretrained("models/blenderbot-400M-distill")
tokenizer_Dialo = AutoTokenizer.from_pretrained("models/DialoGPT-medium")
model_Dialo = AutoModelForCausalLM.from_pretrained("models/DialoGPT-medium") 
chat_history = False
chat_history_ids = []

def blenderBot(message):
  inputs = tokenizer_blender(message, return_tensors="pt")
  result = model_blender.generate(**inputs)
  blender = tokenizer_blender.decode(result[0])
  blender_output = re.search(r'<s> (.*?)</s>', blender).group(1)
  return blender_output

def dailoGPT(message, chat_history):
    
    return dialio_output 


def main(chat_history):
    
    last_blender = ""
    last_dialo = ""
    ###############
    # first response
    ###############
    last_response = handle_json.get_last()
    print(last_response)

    if last_response.startswith("DialoGPT"):
        blender = blenderBot(last_response)
        handle_json.appendJSON("Blender: " + blender)
    else:
        blender = last_response
        new_input_ids = tokenizer_Dialo.encode((blender) + tokenizer_Dialo.eos_token, return_tensors='pt')
        chat_history_ids = model_Dialo.generate(new_input_ids, max_length=20000, pad_token_id=tokenizer_Dialo.eos_token_id)
        # pretty print last ouput tokens from bot
        dialo = tokenizer_Dialo.decode(chat_history_ids[:, new_input_ids.shape[-1]:][0], skip_special_tokens=True)
        handle_json.appendJSON("DialoGPT: "+ dialo)
    
    x = True
    while x == False:
        
        blender_last = blender
        blender = blenderBot(dialo)
        if blender != blender_last:
            handle_json.appendJSON("Blender: " + blender)
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
        chat_history_ids = model_Dialo.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer_Dialo.eos_token_id)
        # pretty print last ouput tokens from bot
        dialo = tokenizer_Dialo.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        if dialo != dialo_last:
            handle_json.appendJSON("DialoGPT: " + dialo)
        else:
            print("DialoGPT confused")
            x = False
        print("+")















if __name__ == "__main__":
   while True:
     main(False)