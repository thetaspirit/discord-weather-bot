# set base image (host OS)
FROM python:3.9.2-slim-buster

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN apt-get update && apt-get install -y build-essential && pip install -r requirements.txt && apt-get remove -y build-essential && apt-get autoremove -y && apt-get install -y wget

# copy the required files to the working directory
COPY bot.py .
COPY time_helper.py .
COPY weather_helper.py .
COPY assets.py .

RUN wget https://bulk.openweathermap.org/sample/city.list.json.gz

RUN apt-get remove -y wget && apt-get autoremove -y

RUN gzip -d city.list.json.gz

# command to run on container start
CMD [ "python3", "bot.py" ] 
