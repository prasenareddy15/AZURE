from transformers import AutoTokenizer, AutoModelForCausalLM
import os

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

model_name = "microsoft/phi-3-mini-4k-instruct"

print("Downloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Downloading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="cpu"
)

print("Model loaded successfully.")