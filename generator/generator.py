import os
from google import genai

# client get api key from : environment variable `GEMINI_API_KEY`

#MODELS YOU CAN USE 
model1 =  "gemini-flash-latest"
model2 =  "gemini-pro-latest"
model3 =  "gemini-flash-lite-latest"

class LLMGenerator:
    def __init__(self, api_key=None, model_name = "gemini-2-nano-2"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY daalo bhai!")
        self.client = genai.Client(api_key=api_key)
        

    def generate_answer(self, query, context):

        prompt = f"""
                You are a helpful AI assistant.
                Answer the question strictly using the context below.
                If the answer is not present in the context, reply and say: "I don't have enough information from the uploaded PDF(s)."

                Context:
                {context}

                Question:
                {query}

                """

        try:
            response = self.client.models.generate_content(
                    model=model1, 
                    contents=prompt
                    )
            print("answered by model:",{model1})
            return response.text
            
        except Exception as e:
            print("Model 1 failed : ",e)

        try:
            response = self.client.models.generate_content(
                    model=model2,
                    contents=prompt
                    )
            print("answered by model:",{model2})
            return response.text
            
        except Exception as e:
            print("Model 2 failed : ",e)

        try:
            response = self.client.models.generate_content(
                    model=model3, 
                    contents=prompt
                    )
            print("answered by model:",{model3})
            return response.text
            
        except Exception as e:
            print("Model 3 failed : ",e)

        return "LLMs are under heavy load! Please try later!"
