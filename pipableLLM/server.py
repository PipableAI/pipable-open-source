from flask import Flask, request
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import AutoPeftModelForCausalLM
from accelerate import Accelerator
from datetime import date
import re

from sft import SFT

app = Flask(__name__)

model = AutoModelForCausalLM.from_pretrained(
    "./checkpoints/llama-7b-text-to-sql/final_merged_checkpoint",
    device_map={"": Accelerator().local_process_index},
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
    load_in_8bit=True
)


infer_tokenizer = AutoTokenizer.from_pretrained(
    "./checkpoints/base-llama-7b-chat-hf", trust_remote_code=True, use_fast=False
)

infer_tokenizer.pad_token = infer_tokenizer.eos_token
infer_tokenizer.padding_side = "right"

train_tokenizer = AutoTokenizer.from_pretrained(
    "./checkpoints/base-llama-7b-chat-hf",
    trust_remote_code=True,
    use_fast=False,
    add_eos_token=True,
)

train_tokenizer.pad_token = train_tokenizer.eos_token
train_tokenizer.padding_side = "right"

def process_output(output):
    """
    Process the output to remove the prompt.
    """
    return output.split("[/INST]")[1]

def parse_create_table(query):
    table_name_match = re.search(r'CREATE TABLE (\w+) \((.*?)\)', query)
    
    if table_name_match:
        table_name = table_name_match.group(1)
        column_defs = table_name_match.group(2)
        
        columns = [col.strip() for col in column_defs.split(',')]
        
        schema = f"table schema: {table_name}:"
        for col in columns:
            col_match = re.match(r'(\w+) (\w+)', col)
            if col_match:
                col_name = col_match.group(1)
                col_type = col_match.group(2)
                schema += f' "{col_name}" [ {col_type.upper()}]'
        
        return schema

def parse_prompt(context, question):
    llm_input = "[INST] Here is a database schema: "
    for table in context.split(';'):
        llm_input += parse_create_table(table) + " "
    
    llm_input += "Please write me a syntactically correct SQL statement that answers the following question:"
    llm_input += question + "[/INST]"

    return llm_input


@app.route("/generate", methods=["POST"])
def generate():
    """
    Generate a text from a given prompt.
    """
    data = request.json
    context = data.get("context").strip()
    question = data.get("question").strip()
    prompt = parse_prompt(context, question)
    input_ids = infer_tokenizer([prompt], return_tensors="pt").to("cuda")
    generated_ids = model.generate(**input_ids)
    output = infer_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    torch.cuda.empty_cache()

    output = process_output(output).strip()

    return {"output": output}


@app.route("/train", methods=["POST"])
def train():
    """
    Train the model on a given dataset.
    """
    global model

    data = request.json
    dataset_path = data.get("dataset_path")
    output_dir = f"./checkpoints/{date.today()}"

    try:
        sft = SFT(model, train_tokenizer, dataset_path, output_dir)

        sft.trainer.train()
        sft.trainer.save_model(output_dir)
        sft.trainer.model.save_pretrained(f"{output_dir}/final_checkpoint")

        del model
        torch.cuda.empty_cache()

        model = AutoPeftModelForCausalLM.from_pretrained(
            f"{output_dir}/final_checkpoint",
            device_map={"": Accelerator().local_process_index},
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
        ).to("cuda")

        model = model.merge_and_unload()
        output_merged_dir = f"{output_dir}/final_merged_checkpoint"
        model.save_pretrained(output_merged_dir)

        del model
        torch.cuda.empty_cache()

        model = AutoModelForCausalLM.from_pretrained(
            output_merged_dir,
            device_map={"": Accelerator().local_process_index},
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            load_in_8bit=True
        )

        return {"status": "success", "message": "Model trained successfully."}

    except Exception as e:
        return {"status": "error", "message": str(e)}
