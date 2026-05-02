import requests

class LLMGenerator:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"

    def generate_answer(self, query, context):
       
        prompt = f"""
            You are a helpful AI assistant.

            Use the context to answer the question.
            If the answer is partially available, try to infer reasonably.
            Only say "I don't have enough information" if absolutely nothing relevant exists.

            Context:
            {context}

            Question:
            {query}
            """
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": "qwen2.5:3b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                answer = data.get("response", "").strip()

                if answer:
                    print("Answered by local LLM (Ollama)")
                    return answer

                return "Local model returned empty response."

            return f"Local LLM request failed: {response.status_code}"

        except Exception as e:
            return f"Local LLM (Ollama) error: {str(e)}"