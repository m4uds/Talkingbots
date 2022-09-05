from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import re
import torch
import numpy as np
import json
import handle_json
import random
def temp():
    random_num = random.random()
    
    random_num = round(random_num, 2)
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
  inputs = tokenizer_blender(message, return_tensors="pt")
  result = model_blender.generate(**inputs, output_scores=True)
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
        blender = blenderBot(last_response)
        handle_json.appendJSON("Blender: " + blender)
        print("Blender: " + blender)
    
    blender = last_response
    new_input_ids = tokenizer_Dialo.encode((blender) + tokenizer_Dialo.eos_token, return_tensors='pt')
    chat_history_ids = model_Dialo.generate(new_input_ids, max_length=100, pad_token_id=tokenizer_Dialo.eos_token_id, do_sample=True, top_k=100, top_p=0.7, temperature=0.96)
    # pretty print last ouput tokens from bot
    dialo = tokenizer_Dialo.decode(chat_history_ids[:, new_input_ids.shape[-1]:][0], skip_special_tokens=True)
    handle_json.appendJSON("DialoGPT: "+ dialo)
    print("DialoGPT: "+ dialo)
    
    
    for step in range(5):
        
        blender_last = blender
        blender = blenderBot(dialo)
        if blender != blender_last:
            handle_json.appendJSON("Blender: " + blender)
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
        chat_history_ids = model_Dialo.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer_Dialo.eos_token_id, top_k=100, top_p=0.7, temperature= temp())
        # pretty print last ouput tokens from bot
        dialo = tokenizer_Dialo.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        if dialo != dialo_last:
            handle_json.appendJSON("DialoGPT: " + dialo)
            print("DialoGPT: "+ dialo)
        else:
            print("DialoGPT confused")
            x = False
        print("+")















if __name__ == "__main__":
   while True:
     main(False)