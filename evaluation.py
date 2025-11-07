from transformers import Trainer, TrainingArguments, LlamaForCausalLM, LlamaTokenizer
from evaluate import load # get metrics here
from datasets import load_dataset
import numpy as np
import torch

# Load model and tokenizer
model_name = "baffo32/decapoda-research-llama-7B-hf"
model = LlamaForCausalLM.from_pretrained(model_name ,   
                                        load_in_8bit=True,
                                        dtype=torch.float16, # dtype will change in upcoming updates 
                                        device_map="auto",)
tokenizer = LlamaTokenizer.from_pretrained(model_name)

# Load your evaluation dataset
eval_dataset = load_dataset("json", data_files="file.jsonl") # Prepare evaluation dataset as a Dataset object


# Trainer receives token IDs and attention masks in tensor format.
# turn data into PyTorch tensors
eval_dataset.set_format(type="torch", columns=['input_ids', 'attention_mask', 'labels'])

training_args = TrainingArguments(
    dataloader_num_workers=2,
    output_dir="./lora-alpaca-output/",
    eval_strategy="steps",    
    fp16=True, 
    eval_steps=50,
    per_device_eval_batch_size=4, # micro-batch
    do_eval=True,
    report_to="wandb",
    run_name="test_run"
)

# Load METEOR and ROUGE 
meteor = load("meteor")
rouge = load("rouge")

# Trainer sends internally tuple EvalPrediction to get predictions or labels based on your dataset structure.
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    # Convert logits to token IDs by argmax if predictions are logits
    predictions = np.argmax(predictions, axis=-1) if predictions.ndim == 3 else predictions

    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # METEOR expects references as list of lists of refs per prediction
    meteor_score = meteor.compute(predictions=decoded_preds, references=[[r] for r in decoded_labels])["meteor"]
    rouge_scores = rouge.compute(predictions=decoded_preds, references=decoded_labels)
    
    return {
        "meteor": meteor_score,
        "rouge1": rouge_scores["rouge1"].mid.fmeasure,
        "rouge2": rouge_scores["rouge2"].mid.fmeasure,
        "rougeL": rouge_scores["rougeL"].mid.fmeasure,
    }

# Initialize Trainer with evaluation args and include compute metrics
trainer = Trainer(
    model=model,
    args=training_args,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# Run evaluation
eval_results = trainer.evaluate()
print(eval_results)
