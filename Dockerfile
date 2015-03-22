FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD . /code

RUN rm -rf staticfiles/*

ENV DJANGO_SETTINGS_MODULE=jointbtc.settings.docker
ENV GENERATE_WALLET=True
ENV BLOCKCHAIN_API_CODE=""
EXPOSE 8000

RUN python manage.py collectstatic --noinput
CMD python manage.py runserver 0.0.0.0:8000