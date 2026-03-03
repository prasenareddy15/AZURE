import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model

MODEL_NAME = "microsoft/phi-3-mini-4k-instruct"
DATA_PATH = "data/credit_risk_dataset.jsonl"


def format_example(example):
    return {
        "text": example["prompt"] + "\n\n" + example["completion"]
    }


def main():

    print("Loading dataset...")
    dataset = load_dataset("json", data_files=DATA_PATH)["train"]

    # CPU sanity test: small subset
    dataset = dataset.select(range(100))
    dataset = dataset.map(format_example)

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    def tokenize_function(example):
        return tokenizer(
            example["text"],
            truncation=True,
            max_length=1024,
            padding="max_length"
        )

    dataset = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)

    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="cpu",
        torch_dtype=torch.float32
    )

    print("Applying LoRA...")
    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["qkv_proj", "o_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(model, lora_config)

    training_args = TrainingArguments(
        output_dir="./models/lora-credit-risk",
        per_device_train_batch_size=1,
        num_train_epochs=1,
        logging_steps=10,
        save_strategy="no",
        learning_rate=2e-4,
        fp16=False
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )

    print("Starting training...")
    trainer.train()

    print("Saving LoRA adapter...")
    model.save_pretrained("./models/lora-credit-risk")

    print("Training complete.")


if __name__ == "__main__":
    main()