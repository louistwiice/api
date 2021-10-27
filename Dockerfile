FROM python:3.8.6

ENV APP_ROOT /src
ENV CONFIG_ROOT /config

RUN mkdir ${CONFIG_ROOT}
COPY requirements.txt ${CONFIG_ROOT}/requirements.txt
RUN pip install -r ${CONFIG_ROOT}/requirements.txt

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]