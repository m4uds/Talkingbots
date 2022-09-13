from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import re
import torch
import numpy as np
import json
import handle_json
import random



tokenizer_Dialo = AutoTokenizer.from_pretrained("models/DialoGPT-medium")
model_Dialo = AutoModelForCausalLM.from_pretrained("models/DialoGPT-medium") 
tokenizer_blender = AutoTokenizer.from_pretrained("models/blenderbot-400M-distill")
model_blender = AutoModelForSeq2SeqLM.from_pretrained("models/blenderbot-400M-distill")

def temp():
    random_num = random.randint(5,85)
    print(random_num)
    return random_num


def main(message):
    

    new_input_ids = tokenizer_Dialo.encode((message) + tokenizer_Dialo.eos_token, return_tensors='pt')
    chat_history_ids = model_Dialo.generate(new_input_ids, max_length=100, pad_token_id=tokenizer_Dialo.eos_token_id, do_sample=True, top_k=200, top_p=1.5, temperature=0.75)
    # pretty print last ouput tokens from bot
    dialo = tokenizer_Dialo.decode(chat_history_ids[:, new_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return dialo
    




def blenderBot(message):
    if len(message) > 128:
        message = message[:128]
        print(message)
    inputs = tokenizer_blender(message, return_tensors="pt")
    result = model_blender.generate(**inputs, output_scores=True, top_k=100, top_p=0.5, temperature=1, num_beams= temp())
    blender = tokenizer_blender.decode(result[0])
    blender_output = re.search(r'<s> (.*?)</s>', blender).group(1)
    return blender_output













if __name__ == "__main__":
   while True:
     #print("DALIO: "+ main("who are you?"))
     print("BLENDER: "+blenderBot("who are you?"))