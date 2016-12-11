#-*- coding: utf8 -*-
#! /usr/bin/python
import argparse
from os.path import dirname, join
basename = dirname(__file__)
usage = u'''
华工北校区羽毛球场查询脚本, 默认查询包含当天在内一周西区体育场16：00～22：00场次
'''
parser = argparse.ArgumentParser(description=usage)
parser.add_argument("action", choices = ("query", "book"), help = u"指定查询或者预订")
parser.add_argument("-r", "--range", type=int, nargs=2, 
                    dest="range", help='specify the start and the end date of query')
parser.add_argument("-t", "--today", action="store_true",
                    dest='today', help=u'设置查询日期为当天')
parser.add_argument("--config", dest='config_file',
                    help=u'指定用户配置文件', default=join(basename, "config.json"))
parser.add_argument("-l", "--length", dest='length',
                    help=u'如果today没有被设置, 指定查询天数, 默认是10天', type=int, default=10)
parser.add_argument("-p", "--place", choices = range(4), default = 0, 
                    help = u"指定查询/预订场地, 0 为 西区下午, 1 为 海丽文体中心下午, 2 为西区上午, 3 为海丽文体中心上午",
                    type = int, dest = 'place')
parser.add_argument("-d", "--date", dest = "date", 
                    help = u"指定查询/预订日期")
parser.add_argument("-f", "--floor.id", dest = "floorid", help = u"指定场地编号")
parser.add_argument("-y", "--ydtime", dest = "ydtime", help = u"指定预订时间")
args = parser.parse_args()
