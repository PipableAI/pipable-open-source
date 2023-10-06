from trl import SFTTrainer
from peft import LoraConfig
from transformers import TrainingArguments
from datasets import load_dataset
from data_preprocessor import DataProcessor


class SFT:
    def __init__(
        self,
        base_model,
        tokenizer,
        dataset_path,
        output_dir,
    ):
        self.base_model = base_model
        self.tokenizer = tokenizer
        self.dataset_path = dataset_path
        self.lora_hyperparameters = LoraConfig(**{
                            "lora_alpha": 16,
                            "r": 8,
                            "lora_dropout": 0.05,
                            "target_modules": ["q_proj", "v_proj"],
                            "bias": "none",
                            "task_type": "CAUSAL_LM"
                        })
        
        self.sft_hyperparameters = TrainingArguments(**{
                            "output_dir": output_dir,
                            "per_device_train_batch_size": 4,
                            "gradient_accumulation_steps": 2,
                            "per_device_eval_batch_size": 1,
                            "learning_rate": 1e-4,
                            "logging_steps": 10,
                            "max_steps": 500,
                            "save_steps": 10,
                            "group_by_length": False,
                            "lr_scheduler_type": "cosine",
                            "warmup_steps": 100,
                            "optim": "paged_adamw_32bit",
                            "bf16": True,
                            "remove_unused_columns": False,
                            "run_name": "sft_llama2"
                        })
        
        processed_data = DataProcessor(
            self.dataset_path , self.tokenizer,
        )

        self.trainer = SFTTrainer(
            model=self.base_model,
            tokenizer=self.tokenizer,
            peft_config=self.lora_hyperparameters,
            args=self.sft_hyperparameters,
            train_dataset=processed_data.train_dataset,
            packing=True
        ) 