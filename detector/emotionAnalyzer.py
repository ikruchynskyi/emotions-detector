import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
from transformers import pipeline
from transformers import logging as hf_logging

#Disable logging
hf_logging.set_verbosity_error()

emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')
def analyze(text):
    return  emotion(text)
