FROM python:3

#ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pipenv

RUN mkdir /code
WORKDIR /code


COPY requirements.txt /code/

#RUN pip install -r requirements.txt
# RUN pipenv --no-site-packages venv
# RUN . venv/bin/activate
COPY Pipfile  /code/
COPY Pipfile.lock /code/
RUN pipenv install --system --deploy --verbose


COPY ./docker-entrypoint.sh /docker-entrypoint.sh
#RUN chmod +x . /docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]


EXPOSE 8000

COPY . /code/