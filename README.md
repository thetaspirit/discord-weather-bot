# discord-weather-bot
fun fact: most if not all of this was written in spacevim ide!

## requirements sources
aiohttp: version 3.7.4 https://pypi.org/project/aiohttp/<br>
async-timeout: version 3.0.1 https://pypi.org/project/async-timeout/<br>
attrs: verison 20.3.0 https://pypi.org/project/attrs/<br>
chardet: version 4.0.0 https://pypi.org/project/chardet/<br>
discord.py: version 1.6.0 https://pypi.org/project/discord.py/<br>
dotfiles: version 0.6.4 https://pypi.org/project/dotfiles/<br>
idna: version 3.1 https://pypi.org/project/idna/<br>
multidict: version 5.1.0 https://pypi.org/project/multidict/<br>
python-dotenv: version 0.15.0 https://pypi.org/project/python-dotenv/<br>
yarl: version 1.6.3 https://pypi.org/project/yarl/<br>
requests: version 2.25.1 https://pypi.org/project/requests/<br>

## city data
`city.list.json.gz` was downloaded [here](http://bulk.openweathermap.org/sample/).  need to unzip before program can use it.

## Running

There are two ways to run this program: with Docker, and without it (native). I recommend using the Docker image, as it is more portable. I won't reply to any bugs saying "this doesn't work on Windows / MacOS / Haiku".

### Docker

Download the provided `docker-compose.yml` file, and open it with your preferred text editor. Set the bot prefix to a character (default is `?`), and set the bot token. [Don't know how to get a token?](https://www.writebots.com/discord-bot-token/)

Install Docker Compose by following the instructions [here](https://docs.docker.com/compose/install/).

Start the bot with `docker-compose up -d`, and check to make sure that it's running with `docker ps`. If it isn't running, run `docker-compose up` to see debug output, and ensure that you've set all of the proper information in the `docker-compose.yml` file.

Invite your bot to the server(s) of your choice. [Don't know how?](https://discordjs.guide/preparations/adding-your-bot-to-servers.html).

### Native

Download and install the latest Python 3 from [here](https://www.python.org/downloads/). Download the source code of this program by going to the [releases page](https://github.com/thetaspirit/discord-weather-bot/releases) and downloading the .zip or .tar.gz file of the latest version. If you're not sure what to download, download the .zip file. Extract the file to somewhere you know.

Create a virtual environment with `python3 -m venv venv`, and activate it with `source venv/bin/activate`. If you are on Windows or just want to know more about virtual environments, check out the documentation [here](https://docs.python.org/3/tutorial/venv.html) on running a virtual environment.

Install the requirements with `pip3 install -r requirements.txt`.

Copy the file `sample.env` to a file called `.env`, and fill in the prefix and token. Read the section on Docker to learn how to get the token.

Run the program with `python3 bot.py`, and have it run in the background.

