import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
from transformers import pipeline
from transformers import logging as hf_logging

#Disable logging
hf_logging.set_verbosity_error()

class Analyzer:

    def __init__(self):
        self.__pipeline = None

    def analyze(self, text, model='arpanghoshal/EmoRoBERTa'):
        if self.__pipeline is None:
            self.__pipeline = pipeline('sentiment-analysis', model=model)
        text = self.__normalize(text)
        return self.__pipeline(text)

    def __normalize(self, text):
        return "".join(ch for ch in text if ch.isalnum() or ch == " ")

