#######----------- LAYER 1 : base image  + user + env_path + workdir----------###############
FROM python:3.10-slim
# Create non-root user
RUN useradd -m -u 1000 user1
# creates user "user1" with home dir (-m) and specific UID 1000 (-u)
USER user1
# in environment variables: Add local pip bin to PATH 
ENV PATH="/home/user1/.local/bin:$PATH"
# Set working directory
WORKDIR /chatbot


#######-----------  LAYER 2 : requirements copy & Run ----------###############
COPY --chown=user1 requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
pip install --no-cache-dir -r requirements.txt



#######-----------  LAYER 3 : Copy Source Code + files ----------###############
COPY --chown=user1 . /chatbot



# Expose 
EXPOSE 7860
# CMD 
CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "7860"]



