FROM python:3.8-slim-buster

WORKDIR /xxe_lesson
ADD . /xxe_lesson

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD ["app.py"]