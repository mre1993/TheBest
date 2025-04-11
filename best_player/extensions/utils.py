from . import jalali
from django.utils import timezone


def jalali_converter(time):
    time = timezone.localtime(time)

    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_list = list(jalali.Gregorian(time_to_str).persian_tuple())
    months = [
        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند",
    ]
    time_to_list[1] = months[time_to_list[1] - 1]
    output = f"{time_to_list[2]} {time_to_list[1]} {time_to_list[0]} ساعت {time.hour}:{time.minute}"
    return output


import requests


def send_otp(code, phone_number):
    api_key = "your_api_key"
    sender = "your_sender"
    url = f"https://api.sms-webservice.com/api/V3/Send?ApiKey={api_key}&Text={code}&Sender={sender}&Recipients={phone_number}"

    payload = {}
    headers = {}
    print("*\n" * 5, code, "*\n" * 5)
    # try:
    #     response = requests.get(url, headers=headers, data=payload)
    #     response.raise_for_status()
    #     print(response.text)
    # except requests.exceptions.HTTPError as err:
    #     print(err)