from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

class ChatbotNLP:
    def __init__(self):
        # Load pre-trained GPT-2 model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

    def generate_response(self, text):
        try:
            # Encode the input text
            inputs = self.tokenizer.encode(text, return_tensors='pt')

            # Check if the inputs are empty
            if inputs.numel() == 0:
                return "Sorry, I didn't understand that."

            # Generate a response from GPT-2
            with torch.no_grad():
                outputs = self.model.generate(inputs, max_length=150, num_return_sequences=1)

            # Decode the response and return it
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response

        except Exception as e:
            return f"An error occurred: {str(e)}"

    def extract_product_query(self, text):
        pattern = r"(?:search for|looking for|find) (.*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def classify_intent(self, text):
        # Example intent classification logic based on keywords
        if 'search for' in text.lower() or 'looking for' in text.lower():
            return 'product_search'
        elif 'hello' in text.lower() or 'hi' in text.lower():
            return 'greeting'
        elif 'bye' in text.lower() or 'goodbye' in text.lower():
            return 'farewell'
        else:
            return 'other'
