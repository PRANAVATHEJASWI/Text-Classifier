import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

tokenizer = AutoTokenizer.from_pretrained("Pranavathejaswi/Text_Classifier")
model = AutoModelForSequenceClassification.from_pretrained("Pranavathejaswi/Text_Classifier").to(device)

def get_prediction(text):
    encoding = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=128)
    encoding = {k: v.to(device) for k, v in encoding.items()}

    outputs = model(**encoding)
    logits = outputs.logits

    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())
    probs = probs.detach().numpy()
    label = np.argmax(probs, axis=-1)

    if label == 1:
        return {
            'sentiment': 'Positive',
            'probability': probs[1]
        }
    else:
        return {
            'sentiment': 'Negative',
            'probability': probs[0]
        }
