FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /project

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONBREAKPOINT=ipdb.set_trace
COPY ./entrypoint.sh .
#STOPSIGNAL SIGINT
#
ENTRYPOINT ["./entrypoint.sh"]
