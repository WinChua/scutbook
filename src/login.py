#! /usr/bin/python
# -*- coding: utf8 -*-
import requests
import urllib
import sys
from bs4 import BeautifulSoup as BS
import re
from test import setting


def login(user):
    login_url = 'http://116.57.72.197:9099/sports/users/login'
    user['loginMode'] = "1"
    login_res = requests.post(login_url, data=user)
    return login_res



def query(login_res, date, place):
    query = 'http://116.57.72.197:9099/sports/reserve/enFloors'
    query_data = {
        "id": place,  # haili zaoshang
        "datetime": date.strftime("%Y-%m-%d"),
        "ydkssj": "08:00",
        "ydjssj": "22:00"
    }

    query_re = requests.post(query, data=query_data, cookies=login_res.cookies)

    pattern = re.compile(r"\[([0-9]*)\].*?([0-9]{1,2})<")
    timebox = BS(query_re.content).findAll(class_="timelistbox")
    num_ids = map(lambda x: pattern.findall(str(x.h5))[0], timebox)

    get_num = 'http://116.57.72.197:9099/sports/reservezd/reserveInfo'
    results = []
    for num, id in num_ids:
        get_num_data = {"id": num}
        get_num_re = requests.post(get_num,
                                   data=get_num_data, cookies=login_res.cookies)
        times = BS(get_num_re.content)
        tds = times.findAll("td")
        if tds:
            results.append((id, num, map(lambda x: x.text, tds)))
##            print id, num
##            for td in tds:
##                print td.text
    return results, num_ids
time_map = {
    "8":"08:00--09:00",
   "9":"09:00--10:00",
    "10":"10:00--11:00",
    "11":"11:00--12:00",
    "12":"12:00--13:00",
    "13":"13:00--14:00",
    "14":"14:00--15:00",
    "15":"15:00--16:00",
    "16":"16:00--18:00",
    "18":"18:00--20:00",
    "20":"20:00--22:00"
}
    
def book(login_res, place, datetime, ydtime, num):
    result, num_ids = query(login_res, datetime, place)
    result_dict = {num: (place_code, times) for num, place_code, times in result}
    if isinstance(num, int):
        num = str(num)
    for n, tmp in result_dict.items():
        print n, tmp[-1]
    if num not in result_dict:
        print u"该时间段该场地无空闲时间"
        return
    place_code, times = result_dict[num]
    time_code = map(lambda x: int(x.split(":")[0]), times)
    if int(ydtime) in time_code:
        _book(login_res, place_code, datetime.isoformat(),"0,"+time_map[ydtime], place)
    else:
        print u"该时间段没有空闲场次"

floor_id_test = "1460"
datetime_test = "2016-12-17"
ydtime_test = "0,08:00--09:00"
def _book(login_res, floor_id, datetime, ydtime, place):
    dateIndex_url = "http://116.57.72.197:9099/sports/reservezd/dateIndex?id=" + place
    dateIndex = requests.get(dateIndex_url, cookies = login_res.cookies)
    book_url = "http://116.57.72.197:9099/sports/reservezd/editydtime"
    book_get_param = {"floorid":floor_id,"datetime":datetime}
    book_url = book_url + "?" + urllib.urlencode(book_get_param)
    book = requests.get(book_url, cookies = login_res.cookies)
    bs = BS(book.content)
    code = bs.find("input", attrs = {"name":"code"})['value']
#    update_url = "http://116.57.72.197:9099/sports/reservezd/update?datetime=2016-12-17&ydtime=0,08:00--09:00"
    update_url = "http://116.57.72.197:9099/sports/reservezd/update"
    update_get_param = {"datetime": datetime, "ydtime": ydtime}
    update_url = update_url + "?" + urllib.urlencode(update_get_param)
    update_post_param = {"floor.id": floor_id,
                         "sno":"201620108279",
                         "realSno":"",
                         "flag":"0",
                         "computeFeeMode.id":"",
                         "code":"",
                         "account":"103062",
                         "opentime": ydtime,
                         "lxr": "cy",
                         "lxdh": "13660270454",
                         "memo":""
                         }
    update_post_param['code'] = code
#    data = '''floor.id:1460
#sno:201620108279        
#realSno:
#flag:0
#computeFeeMode.id:
#code:20161210232908199145
#account:103062
#opentime:08:00--09:00
#lxr:cy
#lxdh:13660270454
#memo:'''
#    data = filter(bool, data.split("\n"))
#    data = dict(map(lambda x: x.split(":", 1), data))
#    data['code'] = code
    
    r = requests.post(update_url, data = update_post_param, cookies = login_res.cookies)
    print "book OK"
    return r


place_name = {
    "4825":u"西区体育场",
    "946": u"西区体育场",
    "4806": u"海丽文体中心",
    '939': u'海丽文体中心'
}
def query_date_range(login_res, date_range, place):
    results = []
    for date in date_range:
        result, num_ids = query(login_res, date, place)
        print date.isoformat(), 'done'
        results.append((date, result))
    return results


def show(results, place):
    print u"场地:", place_name[place]
    print ''
    for date, result in results:
        print date.isoformat(), u"星期"+str(date.isoweekday())
        for id, num, texts in result:
            print "\t" + id + u"号场", num
            print "\t\t" + "\n\t\t".join(texts)
        print 
    return



def main():
    login_res = login(setting.user)
    if setting.action == "query":
        results = query_date_range(login_res, setting.date_range, setting.place)
        show(results, setting.place)
        return login_res, results
    else:
        book(login_res, place = setting.place, datetime = setting.date, ydtime = setting.ydtime, num = setting.floorid)
##    for date in date_range:
##        print date.isoformat(), 'is', u'星期', date.isoweekday()
##        result = query(login_res, date, place)
##        show(result, place)
##


if __name__ == "__main__":
    main()
