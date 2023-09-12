from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from app.predict.cabbage_data import send_random_number_cabbage
from app.predict.carrot_data import send_random_number_carrot
from app.predict.cucumber_data import send_random_number_cucumber
from app.predict.napa_cabbage_data import send_random_number_napa_cabbage
from app.predict.onion_data import send_random_number_onion
from app.predict.potato_data import send_random_number_potato
from app.predict.welsh_onion_data import send_random_number_welsh_onion
from app.predict.young_pumpkin_data import send_random_number_young_pumpkin

app = FastAPI()

load_dotenv()
origins = os.getenv('origins')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-origins")
def read_root():
    return os.getenv('origins')


def create_farm_produce_price():
    scheduler = BlockingScheduler()

    scheduler.add_job(send_random_number_cabbage, 'interval', hours=24, minutes=0, seconds=0, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')
    scheduler.add_job(send_random_number_carrot, 'interval', hours=24, minutes=0, seconds=10, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')
    scheduler.add_job(send_random_number_cucumber, 'interval', hours=24, minutes=0, seconds=10, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')
    scheduler.add_job(send_random_number_napa_cabbage, 'interval', hours=24, minutes=0, seconds=10, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')
    scheduler.add_job(send_random_number_onion, 'interval', hours=24, minutes=0, seconds=10, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')
    scheduler.add_job(send_random_number_potato, 'interval', hours=24, minutes=0, seconds=10, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')
    scheduler.add_job(send_random_number_welsh_onion, 'interval', hours=24, minutes=0, seconds=10, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')
    scheduler.add_job(send_random_number_young_pumpkin, 'interval', hours=24, minutes=0, seconds=10, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')

    scheduler.start()


create_farm_produce_price()


# def test1():
#     print("양배추")
#
# def test2():
#     print("당근")
#
# def test3():
#     print("오이")
#
# def test4():
#     print("배추")
#
# def test5():
#     print("양파")
#
# def test6():
#     print("감자")
#
# def test7():
#     print("대파")
#
# def test8():
#     print("애호박")

@app.get("/get-cabbage-price")
def get_cabbage_price_start():
    scheduler = BlockingScheduler()

    scheduler.add_job(send_random_number_cabbage, 'interval', hours=24, minutes=0, seconds=0, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')

    scheduler.start()


@app.get("/get-carrot-price")
def get_carrot_price_start():
    scheduler = BlockingScheduler()

    scheduler.add_job(send_random_number_carrot, 'interval', hours=24, minutes=0, seconds=0, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')

    scheduler.start()


@app.get("/get-cucumber-price")
def get_cucumber_price_start():
    scheduler = BlockingScheduler()

    scheduler.add_job(send_random_number_cucumber, 'interval', hours=24, minutes=0, seconds=0, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')

    scheduler.start()


@app.get("/get-napa-cabbage-price")
def get_napa_cabbage_price_start():
    scheduler = BlockingScheduler()

    scheduler.add_job(send_random_number_napa_cabbage, 'interval', hours=24, minutes=0, seconds=0,
                      timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')

    scheduler.start()


@app.get("/get-onion-price")
def get_onion_price_start():
    scheduler = BlockingScheduler()

    scheduler.add_job(send_random_number_onion, 'interval', hours=24, minutes=0, seconds=0, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')

    scheduler.start()


@app.get("/get-potato-price")
def get_potato_price_start():
    scheduler = BlockingScheduler()

    scheduler.add_job(send_random_number_potato, 'interval', hours=24, minutes=0, seconds=0, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')

    scheduler.start()


@app.get("/get-welsh-onion-price")
def get_welsh_onion_price_start():
    scheduler = BlockingScheduler()

    scheduler.add_job(send_random_number_welsh_onion, 'interval', hours=24, minutes=0, seconds=0, timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')

    scheduler.start()


@app.get("/get-young-pumpkin-price")
def get_young_pumpkin_price_start():
    scheduler = BlockingScheduler()

    scheduler.add_job(send_random_number_young_pumpkin, 'interval', hours=24, minutes=0, seconds=0,
                      timezone='Asia/Seoul',
                      start_date='2023-09-06 14:45:00')

    scheduler.start()
