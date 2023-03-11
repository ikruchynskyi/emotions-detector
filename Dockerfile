FROM python:3.9.6

RUN pip install transformers==4.26.1 tensorflow==2.11.0
WORKDIR /detector
CMD python3

