# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the required files to the working directory
COPY bot.py .
COPY time_helper.py .
COPY weather_helper.py .

RUN wget https://bulk.openweathermap.org/sample/city.list.json.gz
RUN gzip -d city.list.json.gz

# command to run on container start
CMD [ "python", "./bot.py" ] 
