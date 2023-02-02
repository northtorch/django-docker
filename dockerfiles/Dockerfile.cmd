FROM python:3.10-bullseye
WORKDIR /opt/app

# ----- Update apt packages -----
RUN apt-get update \
    && apt-get install -y libpq5 libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ----- Restore python packages -----
COPY requirements.txt /opt/app
RUN pip install -r requirements.txt

# ----- Copy all files -----
COPY ./ /opt/app/
COPY ./core/local_settings.py.docker /opt/app/core/local_settings.py
RUN mkdir /var/log/django

CMD bash -c "python manage.py migrate && python manage.py increment"
