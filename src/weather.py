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
# @click.option('--celcius',default=False,is_flag=True,type=click.BOOL, help='Temperatur Celcius')
# @click.option('--fahrenheit',default=False,is_flag=True,type=click.BOOL, help='Temperatur Fahrenheit ')
# @click.option('--kelvin',default=False,is_flag=True,type=click.BOOL, help='Temperatur Kelvin')
# @click.option('--temp',default=False,is_flag=True,type=click.BOOL, help='Menampilkan Temperatur dan cuaca')
@click.option("--cities")
@coro
async def weather(city, cities):

    if cities:
        print(f"datetime : {datetime.datetime.now()}")
        for city in cities:
            data = json.loads(await fetcher.get(f"{BASE_URL}q={city}&appid={API_KEY}"))
            print("----------------------------------------------")
            getRequest = await fetcher.get(f"{BASE_URL}q={city}&appid={API_KEY}")
            data = json.loads(getRequest)
            print(f"datetime : {datetime.datetime.now()}")
            print(f"city : {data['name']}")
            print(f"temperature : {data['main']['temp']}")
            print(f"weather : {data['weather'][0]['description']}")
            print(f"sunrise : {time.ctime(int(data['sys']['sunrise']))}")
            print(f"sunset : {time.ctime(int(data['sys']['sunset']))}")

    else :
        getRequest = await fetcher.get(f"{BASE_URL}q={city}&appid={API_KEY}")
        data = json.loads(getRequest)
        print(f"datetime : {datetime.datetime.now()}")
        print(f"city : {data['name']}")
        print(f"temperature : {data['main']['temp']}")
        print(f"weather : {data['weather'][0]['description']}")
        print(f"sunrise : {time.ctime(int(data['sys']['sunrise']))}")
        print(f"sunset : {time.ctime(int(data['sys']['sunset']))}")



@cli.command(name="dailyforecast")
@click.argument("city",default=False,type=click.STRING)
@click.option('--days',default=False,is_flag=True,type=click.BOOL)
@coro
async def dailyforecast(city,days):
    if days:
        print("processing ...")
        getRequest = await fetcher.get(f"{BASE_URL}q={city}&appid={API_KEY}")
        data = json.loads(getRequest)
        print("done ...")
        data = json.loads(data)
        list_data = list(data['list'])
        filename = f"{datetime.datetime.now()}_{city}.json"
        f = open(filename, "w")
        f.write(json.dumps(list_data,indent=1))
        f.close() 
        print("saved into",filename)
    else:
        getRequest = await fetcher.get(f"{BASE_URL}q={city}&appid={API_KEY}")
        data = json.loads(getRequest)
        list_data = list(data['list'])
        # print(data['list'][0]['dt_txt'].split(' ')[0].split('-')[2])
        filterData = filter(lambda ndata: datetime.datetime.fromtimestamp(ndata['dt']).strftime("%d") == datetime.datetime.fromtimestamp(list_data[0]['dt']).strftime("%d"),list_data)
        
        for i in filterData:
            date=datetime.datetime.now()
            temperature = f"{i['weather'][0]['main']}, {i['weather'][0]['description']}"
            print(temperature)

if __name__ == '__main__':
    cli()

