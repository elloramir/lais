FROM python:3.10-slim-buster

# important for django timezone
ARG TZ='America/Fortaleza'
# set the working directory to /app
WORKDIR /app
# copy the current directory contents into the container at /app
COPY . .

RUN \
	# configure timezone
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
	# install python deps
	pip install -r requirements.txt

EXPOSE 8000