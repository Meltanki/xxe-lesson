FROM python:latest
WORKDIR /xxe_lesson
ADD . /xxe_lesson
RUN pip install -r requirements.txt
CMD ["python","app.py"]