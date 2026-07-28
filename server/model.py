from transformers import pipeline
import os



class AIModelAgent:
    def __init__(self):

        print("Loading local DistilBERT Transformer weights from disk...")
        
        # We use a fast, stable text classification model checkpoint
        self.classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
        print("🟢 AI Engine successfully loaded and ready for memory arrays.")

    def classify_log(self,text_paylog):
        prediction = self.classifier(text_paylog)

        return prediction


AiModel = AIModelAgent()



        
    
