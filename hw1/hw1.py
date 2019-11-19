import csv
import datetime
import sys

## step 1, filter to valid data (TX, no double dates in expired_month, time)
valid_data = []
with open(sys.argv[1], encoding='big5') as f:
    rows = csv.reader(f)
    for row in rows:
        if row[1] == '商品代號' or row[3] == '成交時間':
            continue

        good_name = row[1][0:2]
        if good_name != 'TX':
            continue

        dates = row[2]
        if dates[6] != ' ':
            continue

        time = int(row[3])
        if time >= 84500 and time <= 134500:
            valid_data.append(row)

## step *, calculate the right day
the_day = valid_data[0][0]
year = the_day[0:4]
month = the_day[4:6]
day = the_day[6:8]

## step 2, predict the valid month
d = datetime.datetime(int(year), int(month), int(day))
no_week = (d.day-1)//7 + 1
no_day = d.weekday() # 0~6

if no_week > 3 or (no_week == 3 and no_day > 2):
    month = int(month) + 1
    if month > 12:
        year = int(year) + 1
        month = 1

month = int(month)
if month < 10:
    month = str('0')+str(month)

valid_month = str(year)+str(month)

## step3, filter to valid month
final_data = []
for row in valid_data:
    expired_month = row[2]
    expired_month = expired_month[0:6]
    if expired_month == valid_month:
        final_data.append(row)

High = -10000
Low = 10000000
for i in range(0, len(final_data)):
    deal_price = int(final_data[i][4])
    if i == 0:
        Open = deal_price
    elif i == len(final_data)-1:
        Close = deal_price

    if deal_price > High:
        High = deal_price

    if deal_price < Low:
        Low = deal_price

print(Open, High, Low, Close)
