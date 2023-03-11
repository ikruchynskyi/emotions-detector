# emotions-detector
### Text processor which utilize https://huggingface.co/arpanghoshal/EmoRoBERTa pretrained model for emotional tone classification

## Local instalation. 

### Requirements:
Pythom 3.9.* with pip

### Local nstalation:

Install following dependencies manually or create requirements.txt file with the next content

```
transformers==4.26.*
tensorflow==2.11.*
```

Run 
```
pip install -r requirements.txt
```

Pipelines documentation:
https://huggingface.co/transformers/v4.10.1/main_classes/pipelines.html



### Docker installation

 ```
 docker build . -t emotion-image
 ```
 
```
docker run -dit --name emotions-detector -v "$(pwd)"/detector:/detector emotion-image
```

###Usage example:
```
docker exec -it emotions-detector python3 detector.py "I will stop doing buisness with you" "Your service is awfull" "Thank you for helping, Ill recomend you to friends"

text='I will stop doing buisness with you':{'label': 'annoyance', 'score': 0.6424481868743896}
text='Your service is awfull':{'label': 'excitement', 'score': 0.6927852034568787}
text='Thank you for helping, Ill recomend you to friends':{'label': 'gratitude', 'score': 0.9946815371513367}
```

### Web server 

Run webserver: python3 server.py HOST PORT

```
python3 server.py 127.0.0.1 8080
```

### API: 
**POST /analyze**

Request text example:
```
curl -sX POST 127.0.0.1:8080/analyze -d '{"text": "Some random text and sad"}' | json_pp
{
   "data" : "sadness",
   "status" : "success"
}

```

### Run with docker:

Please see example assuming that port 8080 will be used on the host and container environment

```
docker run -dit --name emotions-detector -p 8080:8080 -v "$(pwd)"/detector:/detector emotion-image
docker exec -it emotions-detector python3 server.py 127.0.0.1 8080

curl -sX POST emotions-detecto:8080/analyze -d '{"text": "Some random text and sad"}'
```

Pipelines documentation:
https://huggingface.co/transformers/v4.10.1/main_classes/pipelines.html
