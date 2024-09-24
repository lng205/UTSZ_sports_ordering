"""定时模块"""
import time
from datetime import datetime, timedelta
from logger import logging

def timer(target_day: str) -> None:
    """
    sleep until 22:00 on two days before target_day.
    target_day format: 'YYYY-MM-DD'
    """
    target = datetime.strptime(target_day, '%Y-%m-%d')
    target = target - timedelta(days=2)
    target = target.replace(hour=22, minute=0, second=0)
    delta = target - datetime.now()
    if delta.total_seconds() > 0:
        logging.info(f'等待 {delta.days} 天 {delta.seconds//3600} 小时 {delta.seconds%3600//60} 分钟')
        time.sleep(delta.total_seconds())

if __name__ == '__main__':
    timer('2024-09-27')