FROM python:3.11

# Install curl
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

    
ENV TZ=America/Vancouver
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 

CMD [ "python3", "main.py" ]