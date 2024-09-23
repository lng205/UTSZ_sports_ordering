import requests
import json
import argparse

ID = json.loads(open('data/venueid.json', 'r').read())

ORDER_URL = 'https://yktsport.utsz.edu.cn/DXC/api/services/app/WeixinBillVenue/VenueBillAsync'
PAYMENT_URL = 'https://yktsport.utsz.edu.cn/DXC/api/services/app/SynjonesOpenPay/VenueBillPayBySynjonesAsync'

class Req:
    """
    Send a post request.
    """
    cookies = json.loads(open('data/cookies.json', 'r').read())
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


def make_order(billday:str, venue_number: int, id_dict: dict, time: tuple[int, int]) -> None:
    response = Req(
        data = generate_order_data(billday, venue_number, id_dict, time),
        url=ORDER_URL
    ).get().json()

    print(response)
    result = response["result"]
    if not result:
        print(f'Failed to make order for venue #{venue_number} at {time[0]}:00-{time[1]}:00')
        return

    payment_response = Req(
        data = {
            'weixinBillRecordNo': result["billRecordNo"],
            'walletName': '电子校园卡',
            'walletType': '000',
            'webApiUniqueID': '531ebc0e-8ad6-0ac5-2cd0-15f7d4ccd529',
        },
        url=PAYMENT_URL
    ).get().json()
    print(payment_response)

def generate_order_data(billday:str, venue_number: int, id_dict: dict, time: tuple[int, int]) -> dict:
    data = {'billDay': billday}

    minutes = range(time[0]*60, time[1]*60, 30)
    for i, minute in enumerate(minutes):
        data[f'listData[{i}][venueID]'] = id_dict[venue_number - 1]
        data[f'listData[{i}][startTime]'] = minute
        data[f'listData[{i}][endTime]'] = minute + 30
        data[f'listData[{i}][billValue]'] = '40'
        data[f'listData[{i}][realValue]'] = '10'
        data[f'listData[{i}][venueDisplayName]'] = f'#{venue_number}'
        data[f'listData[{i}][venueTypeDisplayName]'] = '体育馆羽毛球'

    data['webApiUniqueID'] = '064b7d8b-f0e9-b0ac-23ee-729b6d8d68a4'
    return data

if __name__ == '__main__':
    make_order('2024-09-25', 10, ID, (15, 16))