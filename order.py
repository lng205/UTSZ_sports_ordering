"""订单模块"""

import requests
import json
from logger import logging


def order(day: str, venue=10, time=(15, 17), pay=False) -> None:
    id_dict = json.loads(open("data/venueid.json", "r").read())
    bill_no = make_order(day, venue, id_dict, time)
    if pay:
        make_payment(bill_no)


class Req:
    cookies = json.loads(open("data/cookies.json", "r", encoding="utf-8").read())

    def __init__(self, data: dict, url: str) -> None:
        self.data = data
        self.url = url

    def get(self) -> requests.Response:
        response = requests.post(
            self.url,
            cookies=self.cookies,
            data=self.data,
        )
        return response


def make_order(day: str, venue: int, id_dict: dict, time: tuple) -> str:
    req = Req(
        data=generate_order_data(day, venue, id_dict, time),
        url="https://yktsport.utsz.edu.cn/DXC/api/services/app/WeixinBillVenue/VenueBillAsync",
    )
    logging.info(f"发送预约请求: {day} {venue} {time}")
    response = req.get()
    logging.info(f"预约请求响应：{response.json()}")

    try:
        bill_no = response.json()["result"]["billRecordNo"]
    except TypeError:
        logging.error("获取订单号失败")
        bill_no = ""
    return bill_no


def generate_order_data(day: str, venue: int, id_dict: dict, time: tuple) -> dict:
    data = {"billDay": day}

    minutes = range(time[0] * 60, time[1] * 60, 30)
    for i, minute in enumerate(minutes):
        data[f"listData[{i}][venueID]"] = id_dict[venue - 1]
        data[f"listData[{i}][startTime]"] = minute
        data[f"listData[{i}][endTime]"] = minute + 30
        data[f"listData[{i}][billValue]"] = "40"
        data[f"listData[{i}][realValue]"] = "10"
        data[f"listData[{i}][venueDisplayName]"] = f"#{venue}"
        data[f"listData[{i}][venueTypeDisplayName]"] = "体育馆羽毛球"

    data["webApiUniqueID"] = "064b7d8b-f0e9-b0ac-23ee-729b6d8d68a4"
    return data


def make_payment(bill_no: str) -> None:
    if not bill_no:
        return

    req = Req(
        data={
            "weixinBillRecordNo": bill_no,
            "walletName": "电子校园卡",
            "walletType": "000",
            "webApiUniqueID": "531ebc0e-8ad6-0ac5-2cd0-15f7d4ccd529",
        },
        url="https://yktsport.utsz.edu.cn/DXC/api/services/app/SynjonesOpenPay/VenueBillPayBySynjonesAsync",
    )
    logging.info(f"发送支付请求: {bill_no}")
    response = req.get()
    logging.info(f"支付请求响应：{response.json()}")


if __name__ == "__main__":
    order("2024-09-25", 10, (15, 17), False)
