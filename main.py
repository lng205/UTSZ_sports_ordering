#!python3.12.6
# -*- coding: utf-8 -*-
"""主程序入口"""
from order import order
from timer import timer
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('target_day', type=str, help='日期（YYYY-MM-DD）')
    parser.add_argument('venue_number', type=int, nargs='?', default=10, help='场号（1-25）')
    parser.add_argument('start_time', type=int, nargs='?', default=15, help='开始时间（0-24）')
    parser.add_argument('end_time', type=int, nargs='?', default=17, help='结束时间（0-24）')
    args = parser.parse_args()

    timer(args.target_day)
    order(args.target_day, args.venue_number, (args.start_time, args.end_time), True)

if __name__ == '__main__':
    main()