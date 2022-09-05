from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import re


tokenizer_one = AutoTokenizer.from_pretrained("models/blenderbot-400M-distill")
model_one = AutoModelForSeq2SeqLM.from_pretrained("models/blenderbot-400M-distill")
tokenizer_two = AutoTokenizer.from_pretrained("models/blenderbot-400M-distill")
model_two = AutoModelForSeq2SeqLM.from_pretrained("models/blenderbot-400M-distill")


def next_response(message, model, tokenizer):
  inputs = tokenizer(message, return_tensors="pt")
  result = model.generate(**inputs)
  blender = tokenizer.decode(result[0])
  blender = re.search(r'<s> (.*?)</s>', blender).group(1)
  print(blender)

  return blender

blender = "hey, what's your name?"
while True:
    
    next_response(blender,model_one,tokenizer_one)
    next_response(blender,model_two,tokenizer_two)