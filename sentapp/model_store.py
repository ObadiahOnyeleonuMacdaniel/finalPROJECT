# sentapp/model_store.py
from transformers import pipeline

# Model name you gave
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"

print("Loading Hugging Face pipeline (this may take a while the first time)...")
sent_pipeline = pipeline("sentiment-analysis", model=MODEL_NAME, tokenizer=MODEL_NAME)
print("Model loaded and ready!")
