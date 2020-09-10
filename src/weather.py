import aiohttp
import asyncio
import time
import json
import datetime
import click
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_URL = os.environ.get("BASE_URL")
API_KEY = os.environ.get("API_KEY")
from functools import wraps
from src.Fetch import Fetcher as fetcher

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

@click.group()
def cli():
    pass

def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper

@cli.command(name="weather")
@click.argument("city",type=click.STRING)
@coro
async def weather(city):
    getRequest = await fetcher.get(f"{BASE_URL}q={city}&appid={API_KEY}")
    data = json.loads(getRequest)
    print(f"datetime : {datetime.datetime.now()}")
    print(f"city : {data['name']}")
    print(f"temperature : {data['main']['temp']}")
    print(f"weather : {data['weather'][0]['description']}")
    print(f"sunrise : {time.ctime(int(data['sys']['sunrise']))}")
    print(f"sunset : {time.ctime(int(data['sys']['sunset']))}")

if __name__ == '__main__':
    cli()

