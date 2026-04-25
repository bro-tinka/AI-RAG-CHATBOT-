## Step 1 : Once you have your docker file ready , go the project directory of your terminal

```bash
cd AI Chatbot
```

## Step2 : Build the image

```bash
docker build -t ragbot .
```
You can set image_name: ragbot or chatbot or my_bot whatsover

## Step3 : Run The image or Export to DockerHub

Wait before running this below command:
```bash
docker run -p 8000:7860 ragbot
```
Since you have set to get GEMINI_API_KEY from your environment variable, your container cant access host env variables ⚠

Run with setting environment variables for that temporary container
```bash
docker run -p 8000:7860 ragbot -e GEMINI_API_KEY = yourapikeyhere
```

You should see like:
Uvicorn running on http://0.0.0.0/7860
but clicking on that wont work,because 7860 is the port where contatiner is interacting
we have defined machine port as 8000 . Therefore acces it via:
http://localhost:8000


---

## 📜 License

This project is for educational and research purposes.

---

## 👤 Author

**bro-tinka**  
AI / ML Enthusiast | RAG Systems | Backend + AI Engineering | Automation

---

⭐ If you find this project useful, consider giving it a star on GitHub.
💝  Follow me on Linkedin : https://www.linkedin.com/in/trivendra-singh-bisht/

💚💙🧡💖❣💕💞💓💗💖💖💗💓💞💕💜💘🧡💙💚





