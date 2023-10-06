from datasets import load_dataset
from tqdm import tqdm
from trl.trainer import ConstantLengthDataset
import re

class DataProcessor:
    def __init__(self, dataset_path, tokenizer):
        self.dataset_path = dataset_path
        self.tokenizer = tokenizer

        dataset = load_dataset("json", data_files={"train": self.dataset_path})

        train_dataset = dataset["train"]
        chars_per_token = self.chars_token_ratio(train_dataset)
        print(f"The character to token ratio of the dataset is: {chars_per_token:.2f}")

        self.train_dataset = ConstantLengthDataset(
            self.tokenizer,
            train_dataset,
            formatting_func=self.prepare_sample_text,
            infinite=True,
            chars_per_token=chars_per_token,
        )

    def parse_create_table(self, query):
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

    def parse_prompt(self, context, question):
        llm_input = "[INST] Here is a database schema: "
        for table in context.split(';'):
            llm_input += self.parse_create_table(table) + " "
        
        llm_input += "Please write me a syntactically correct SQL statement that answers the following question:"
        llm_input += question + "[/INST]"

        return llm_input

    def prepare_sample_text(self, example):
        """
        Prepare a sample text from the dataset.
        """
        return f"{self.parse_prompt(example['context'], example['question'])} {example['answer']}"

    def chars_token_ratio(self, dataset, nb_examples=400):
        """
        Estimate the average number of characters per token in the dataset.
        """

        total_characters, total_tokens = 0, 0
        for _, example in tqdm(
            zip(range(nb_examples), iter(dataset)), total=nb_examples
        ):
            text = self.prepare_sample_text(example)
            total_characters += len(text)
            if self.tokenizer.is_fast:
                total_tokens += len(self.tokenizer(text).tokens())
            else:
                total_tokens += len(self.tokenizer.tokenize(text))

        return total_characters / total_tokens