from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

print("Loading model...")
model_name = "pszemraj/grammar-synthesis-small"  # <- new model link

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
model.eval()

if torch.cuda.is_available():
    model.to("cuda")
    print("Using GPU.")
else:
    print("Using CPU.")

def correct_grammar(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example test
text = "He go to school everyday. She not like maths. I eat food yesterday"
corrected = correct_grammar(text)
print("Original:", text)
print("Corrected:", corrected)
