import torch

def extract_text(path: str):
    with open(path, "rb") as f:
        raw_data = f.read()

        raw_data = str(raw_data).replace("\\", "")
        raw_data = raw_data.replace("b", "").replace(">", "").replace("<", "")
        raw_data = raw_data.replace("/", "").replace("%", "").replace("@", "")
        raw_data = raw_data.replace("[", "").replace("]", "")
        
        heads = raw_data[:1000]
        tails = raw_data[len(raw_data)-1000:]
        total_str = str(heads+tails)
        return total_str


def tokenize_function(text: str, tokenizer):
    return tokenizer(text, padding="max_length", truncation=True, return_tensors="pt")


def signature_check(file_path: str, tokenizer, model):
    text = extract_text(file_path)
    tokenized_input = tokenize_function(text, tokenizer)
    result = model(**tokenized_input)

    logits = result.logits
    check = torch.argmax(logits)
    return bool(not check.item())
