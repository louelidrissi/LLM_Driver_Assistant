from transformers import AutoTokenizer
from thefuzz import fuzz
#print("AutoTokenizer", AutoTokenizer) 
import json


'''
    Determine max cut-off length.
    Tokenize and truncate data
    Save output as jsonl.
'''
# Debugging 
#import os
#for name, value in os.environ.items():
#    print("name",f"{name}: {value}")
#print(globals())  # shows all global variables and their values


# Debugging
#import inspect
#print("hf_tokenizer:", convert)
#print("type:", type(convert))
#print("defined in:", inspect.getsourcefile(convert) if callable(convert) else "Not callable")

# Legacy does not work with fast tokenization. Default is Legacy.
# Pass folder with .model file for llama
tokenizer = AutoTokenizer.from_pretrained("/Users/louelidrissi/LLM/decapoda-research-llama-7B-hf",legacy=True, use_fast=False)

# Debugging
#tokenizer.save_pretrained("./decapoda-research-llama-7B-hf")
#print("type", type(tokenizer)) 


jsonl_file_path = "reduced_training.jsonl"
testing_jsonl_file_path = "reduced_testing.jsonl"
train_on_input = True 

def find_max_length(jsonl_path):
    max_length = 0
    
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            instruction = data.get("instruction", "")
            input_text = data.get("input", "")
            output = data.get("output", "")
            if input_text.strip() == "":
                # new lines after each part of the prompt for proper tokenization
                prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output}\n"
            else:
                # new lines after each part of the prompt for proper tokenization
                prompt = (
                    f"### Instruction:\n{instruction}\n\n"
                    f"### Input:\n{input_text}\n\n"
                    f"### Response:\n{output}\n"
                )
            tokens = tokenizer(prompt, truncation=False)

            if not train_on_input:
                print("add eos")
                add_eos(tokens, cutoff_len=256)
            else:
                pass
            
            token_len = len(tokens["input_ids"])
            if token_len > max_length:
                max_length = token_len
    return max_length

def save_tokenized_jsonl(jsonl_path, output_path, cutoff_len):
    with open(jsonl_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
        for line in fin:
            data = json.loads(line)
            instruction = data.get("instruction", "")
            input_text = data.get("input", "")
            output = data.get("output", "")
            if input_text.strip() == "":
                # new lines after each part of the prompt for proper tokenization
                prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output}\n"
            else:
                # new lines after each part of the prompt for proper tokenization
                prompt = (
                    f"### Instruction:\n{instruction}\n\n"
                    f"### Input:\n{input_text}\n\n"
                    f"### Response:\n{output}\n"
                )
            tokens = tokenizer(prompt, max_length=cutoff_len, truncation=True, padding=False)
            
            if not pass_test(prompt, tokens):
                break

            if not train_on_input:
                print("masked and eos")
                add_eos(tokens, cutoff_len)
                labels = mask_input(prompt, tokens, cutoff_len)
            else:
                labels = tokens["input_ids"].copy

            tokenized_data = {
                "input_ids": tokens["input_ids"],
                "attention_mask": tokens["attention_mask"],
                "labels": tokens["input_ids"].copy(),
                "prompt": prompt
            }
            # fout.write each item from the dictionary as a new line 
            fout.write(json.dumps(tokenized_data) + "\n")

def pass_test(prompt, tokens):
    # Detokenize for testing puposes
    detokenized_text = tokenizer.decode(tokens["input_ids"], skip_special_tokens=True)
    
    # Find similarity ratio
    similarity = fuzz.ratio(prompt, detokenized_text)
    
    # add repr() to show string with spaces included
    if similarity < 100:
        print(f"Warning: Low similarity ({similarity}%) between original prompt and detokenized text.")
        print("Original prompt:", repr(prompt))
        print("Detokenized text:", repr(detokenized_text))
        return False 
    return True

def add_eos(tokens, cutoff_len):
    # Add EOS token if not present and mark it in attention mask 
    if tokens["input_ids"][-1] != tokenizer.eos_token_id and len(tokens["input_ids"]) < cutoff_len:
        tokens["input_ids"].append(tokenizer.eos_token_id)
        tokens["attention_mask"].append(1)
    return 

def mask_input(prompt, tokens, cutoff_len):
    # Mask input tokens in "labels" with -100 to ignore loss on input part
    user_prompt_ids = tokenizer(prompt, max_length=cutoff_len, truncation=True, padding=False).input_ids
    user_len = len(user_prompt_ids)
    
    labels = tokens["input_ids"].copy()
    labels[:user_len] = [-100] * user_len 
    return labels

def find_max_cutoff():
    cutoff_train = find_max_length(jsonl_file_path)
    #print("Max length:",  cutoff_train)
    cutoff_test = find_max_length(testing_jsonl_file_path)
    #print("Max length:", cutoff_test )
    return max(cutoff_train, cutoff_test)

def tokenize_truncate_training(max_len):
    output_jsonl_file_path = "tokenized_output.jsonl"
    save_tokenized_jsonl(jsonl_file_path,  output_jsonl_file_path, max_len)
    print("done with training")
    return 

def tokenize_truncate_testing(max_len):
    testing_output_jsonl_file_path = "testing_tokenized_output.jsonl"
    save_tokenized_jsonl(testing_jsonl_file_path,  testing_output_jsonl_file_path, max_len)
    print("done with testing")
    return 

def main():
    # extend cutoff length for assurance
    max_cutoff = find_max_cutoff()+3
    print(max_cutoff)
    tokenize_truncate_training(max_cutoff)
    tokenize_truncate_testing(max_cutoff)

main()