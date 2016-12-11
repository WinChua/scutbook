# -*- coding: utf8 -*-
#! /usr/bin/python
from parse import args
from datetime import date, timedelta
import json

today = date.today()
if args.date:
    year, month, day = map(int, args.date.split("-"))
    date_range = [date(year, month, day)]
elif args.range:
    args.range[-1] += 1
    date_range = map(lambda day: date(today.year, today.month, day), range(*args.range))
elif args.today:
    date_range = [today]
else:
    date_range = map(lambda delta: today + timedelta(delta), range(args.length))
with open(args.config_file) as f:
    user = json.load(f)
place_ids = ["4825",
             "4806",
             "946",
             "939"
             ]
place = place_ids[args.place]
class Setting(object):
    pass

setting = Setting()
setting.action = args.action
setting.user = user
if setting.action == 'query':
    setting.date_range = date_range
    setting.place = place
else :
    if args.date:
        year, month, day = map(int, args.date.split("-"))
        day = date(year, month, day)
    setting.date = day
    setting.place = place
    setting.floorid = args.floorid
    setting.ydtime = args.ydtime
    if setting.date is None or setting.place is None or setting.floorid is None or setting.ydtime is None:
        print u"book定场必须指定日期，时间，场地编号"
