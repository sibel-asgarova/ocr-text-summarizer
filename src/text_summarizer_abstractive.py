from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "t5-small" 
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def summarize_text_t5(text):
    
    input_text = "summarize: " + text
    
 
    inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
    
 
    summary_ids = model.generate(inputs["input_ids"], max_length=300, num_beams=5, early_stopping=True)
    

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


