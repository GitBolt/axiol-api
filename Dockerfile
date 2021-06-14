FROM python:3

COPY /axiolapi /main 

WORKDIR /main

RUN pip install fastapi uvicorn uvloop requests cloudinary pymongo matplotlib

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}