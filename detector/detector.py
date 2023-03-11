import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
from transformers import pipeline
from transformers import logging as hf_logging

#Disable logging
hf_logging.set_verbosity_error()

emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')
for text in sys.argv[1:]:
	emotion_labels = emotion(text)
	print(f'{text=}:{emotion_labels[0]}')

