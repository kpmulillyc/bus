#coding=utf-8
from flask import render_template, Flask
from ics import icalendar
from urllib.request import urlopen
import datetime
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)





cwb = ['07:30', '07:45', '08:00', '08:10', '08:20', '08:30', '08:40', '08:50', '09:00', '09:15', '09:30', '09:45',
       '10:00', '10:15'
    , '10:30', '10:45', '11:00', '11:15', '11:30', '11:45', '12:15', '12:45', '13:00', '13:30', '14:00', '14:15',
       '14:30',
       '14:45', '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30', '16:45', '17:00', '17:15', '17:30',
       '17:45', '18:00',
       '18:15', '18:30', '18:45', '19:00', '19:15', '19:30', '20:00', '20:30', '21:00']

np = ['07:30', '07:50', '08:10', '08:30', '08:50', '09:20', '09:50', '10:20', '10:50', '11:20', '11:40', '12:00',
      '12:20', '13:50', '14:20', '14:50', '15:20', '15:50', '16:20',
      '16:50', '17:20', '17:50', '18:20', '18:50', '19:20', '19:50', '20:20', '20:50']

tk = ['07:30', '08:00', '08:30', '09:00', '09:45', '10:30', '11:15', '13:00', '13:45', '14:30', '15:15', '16:00',
      '16:45', '17:30', '18:15', '19:00']

cwbh = ['08:00', '08:20', '08:40', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '14:00',
        '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00',
        '18:30', '19:00', '19:30', '20:00', '20:30', '21:00']

nph = ['08:10', '08:30', '08:50', '09:20', '09:50', '10:20', '10:50', '11:20', '11:50', '12:20', '12:50', '13:50',
       '14:20', '14:50', '15:20', '15:50', '16:20', '16:50', '17:20', '17:50', '18:20', '18:50']

tkh = ['09:45', '10:30', '11:15', '13:00', '13:45', '14:30', '15:15', '16:00', '16:45', '17:30', '18:15', '19:00']


def get_localtime():
    temp = datetime.datetime.now()
    return datetime.datetime.time(temp)

def timeTable(x):
    temp = datetime.datetime.strptime(x,'%H:%M')
    return datetime.datetime.time(temp)

def diffInMin(x):
    minTimenow = (get_localtime().hour * 60 * 60) + (get_localtime().minute * 60 ) + get_localtime().second
    minTimebus = (timeTable(x).hour * 60 * 60) + (timeTable(x).minute * 60 )
    return minTimenow - minTimebus

def calAll(x):
    u = 0
    temp = []
    for i in x:
       temp.append(diffInMin(x[u]))
       u+=1
    return temp

def isHoliday():
    url = 'http://www.1823.gov.hk/common/ical/tc.ics'
    c = icalendar.Calendar(urlopen(url).read().decode('utf-8'))
    e= icalendar.Event()
    result = False
    today = datetime.date.today()
    e.begin = today.strftime("%Y%m%d") + " 00:00:00"
    for i in c.events:
        if e.begin == i.begin:
            result = True
            break
    if today.weekday() == 6:
        result = True
    return result

def preBus(x):
    temp = min(n for n in calAll(x) if n > 0)
    return calAll(x).index(temp)

def nextBus(x):
    temp = max(n for n in calAll(x) if n < 0)
    return calAll(x).index(temp)

def printNext(x):
    return (x[nextBus(x)])

def printPrev(x):
    return (x[preBus(x)])

def timeRange(x):
    temp = datetime.datetime.now().time()
    if temp >= timeTable('00:00') and temp < timeTable(x[0]):
        return 1
    elif temp > timeTable(x[0]) and temp < timeTable(x[len(x)-1]):
        return 2
    else:
        return 3

def tmrIsHoliday():
    url = 'http://www.1823.gov.hk/common/ical/tc.ics'
    c = icalendar.Calendar(urlopen(url).read().decode('utf-8'))
    e= icalendar.Event()
    result = False
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(1)
    e.begin = tomorrow.strftime("%Y%m%d") + " 00:00:00"
    for i in c.events:
        if e.begin == i.begin:
            result = True
            break
    if today.weekday() == 5:
        result = True
    return result

def nearestBustime():
    if isHoliday() is False:
        if timeRange(cwb) is 2:
            x = printNext(cwb)
        else:
            x = '23:59'
        if timeRange(np) is 2:
            y = printNext(np)
        else:
            y = '23:59'
        if timeRange(tk) is 2:
            z = printNext(tk)
        else:
            z = '23:59'
        minimum = min(x,y,z)
        if x == y ==  z:
            return cwb
        elif x is y <= minimum:
            return cwb
        elif y is z <= minimum:
            return np
        elif x is z <= minimum:
            return cwb
        elif minimum is x:
            return cwb
        elif minimum is y:
            return np
        else:
            return tk
    else:
        if timeRange(cwbh) is 2:
            x = printNext(cwbh)
        else:
            x = '23:59'
        if timeRange(nph) is 2:
            y = printNext(nph)
        else:
            y = '23:59'
        if timeRange(tkh) is 2:
            z = printNext(tkh)
        else:
            z = '23:59'
        minimum = min(x,y,z)
        if x == y == z:
            return cwbh
        elif x is y <= minimum:
            return cwbh
        elif y is z <= minimum:
            return nph
        elif x is z <= minimum:
            return cwbh
        elif minimum is x:
            return cwbh
        elif minimum is y:
            return nph
        else:
            return tkh

def nearestBusName():
    if isHoliday() is False:
        if timeRange(cwb) is 2:
            x = printNext(cwb)
        else:
            x = '23:59'
        if timeRange(np) is 2:
            y = printNext(np)
        else:
            y = '23:59'
        if timeRange(tk) is 2:
            z = printNext(tk)
        else:
            z = '23:59'
        minimum = min(x, y, z)
        if x == y ==  z:
            return "all"
        elif x is y <= minimum:
            return "cn"
        elif y is z <= minimum:
            return "nt"
        elif x is z <= minimum:
            return "ct"
        elif minimum is x:
            return "cwb"
        elif minimum is y:
            return "np"
        else:
            return "tk"
    else:
        if timeRange(cwbh) is 2:
            x = printNext(cwbh)
        else:
            x = '23:59'
        if timeRange(nph) is 2:
            y = printNext(nph)
        else:
            y = '23:59'
        if timeRange(tkh) is 2:
            z = printNext(tkh)
        else:
            z = '23:59'
        minimum = min(x, y, z)
        if x == y == z:
            return "all"
        elif x is y <= minimum:
            return "cn"
        elif y is z <= minimum:
            return "nt"
        elif x is z <= minimum:
            return "ct"
        elif minimum is x:
            return "cwb"
        elif minimum is y:
            return "np"
        else:
            return "tk"

app = Flask(__name__)
@app.route('/')
def hello_world():
    if isHoliday() is False:
        if timeRange(cwb) is 1:
            return render_template("index.html", Next = cwb[0], title = "all")
        elif timeRange(cwb) is 2:
            return render_template("index.html", Next = printNext(nearestBustime()), title = nearestBusName())
        else:
            if tmrIsHoliday() is True:
                return render_template("index.html", Next = cwbh[0], title = "cwb")
            else:
                return render_template("index.html", Next = cwb[0], title = "all")
    else:
        if timeRange(cwbh) is 1:
            return render_template("index.html", Next=cwbh[0], title="cwb")
        elif timeRange(cwbh) is 2:
            return render_template("index.html", Next=printNext(nearestBustime()), title=nearestBusName())
        else:
            if tmrIsHoliday() is True:
                return render_template("index.html", Next=cwbh[0], title="cwb")
            else:
                return render_template("index.html", Next=cwb[0], title="all")

@app.route('/cwb')
def cwbr():
    if isHoliday() is False:
        if timeRange(cwb) is 1:
            return render_template("cwb.html", table = cwb, tableTit = "銅鑼灣平日時間表", check = False, Next = cwb[0])
        elif timeRange(cwb) is 2:
            return render_template("cwb.html", table = cwb, tableTit = "銅鑼灣平日時間表", Prev = printPrev(cwb), Next = printNext(cwb), check = True)
        else:
            if tmrIsHoliday() is True:
                return render_template("cwb.html", check = False, table = cwbh, tableTit = "銅鑼灣假日時間表", Next = cwbh[0])
            else:
                return render_template("cwb.html", check = False, table = cwb, tableTit = "銅鑼灣平日時間表", Next = cwb[0])
    else:
        if timeRange(cwbh) is 1:
            return render_template("cwb.html", table=cwbh, tableTit="銅鑼灣假日時間表", check=False, Next=cwbh[0])
        elif timeRange(cwbh) is 2:
            return render_template("cwb.html", table=cwbh, tableTit="銅鑼灣假日時間表", Prev=printPrev(cwbh), Next=printNext(cwbh),
                                   check=True)
        else:
            if tmrIsHoliday() is True:
                return render_template("cwb.html", check=False, table=cwbh, tableTit="銅鑼灣假日時間表", Next=cwbh[0])
            else:
                return render_template("cwb.html", check=False, table=cwb, tableTit="銅鑼灣平日時間表", Next=cwb[0])

@app.route('/northpoint')
def npr():
    if isHoliday() is False:
        if timeRange(np) is 1:
            return render_template("np.html", table=np, tableTit="北角平日時間表", check=False, Next=np[0])
        elif timeRange(np) is 2:
            return render_template("np.html", table=np, tableTit="北角平日時間表", Prev=printPrev(np), Next=printNext(np),
                                   check=True)
        else:
            if tmrIsHoliday() is True:
                return render_template("np.html", check=False, table=nph, tableTit="北角假日時間表", Next=nph[0])
            else:
                return render_template("np.html", check=False, table=np, tableTit="北角平日時間表", Next=np[0])
    else:
        if timeRange(nph) is 1:
            return render_template("np.html", table=nph, tableTit="北角假日時間表", check=False, Next=nph[0])
        elif timeRange(nph) is 2:
            return render_template("np.html", table=nph, tableTit="北角假日時間表", Prev=printPrev(nph),
                                   Next=printNext(nph),
                                   check=True)
        else:
            if tmrIsHoliday() is True:
                return render_template("np.html", check=False, table=nph, tableTit="北角假日時間表", Next=nph[0])
            else:
                return render_template("np.html", check=False, table=np, tableTit="北角平日時間表", Next=np[0])

@app.route('/taikoo')
def tkr():
    if isHoliday() is False:
        if timeRange(tk) is 1:
            return render_template("tk.html", table=tk, tableTit="太古平日時間表", check=False, Next=tk[0])
        elif timeRange(tk) is 2:
            return render_template("tk.html", table=tk, tableTit="太古平日時間表", Prev=printPrev(tk), Next=printNext(tk),
                                   check=True)
        else:
            if tmrIsHoliday() is True:
                return render_template("tk.html", check=False, table=tkh, tableTit="太古假日時間表", Next=tkh[0])
            else:
                return render_template("tk.html", check=False, table=tk, tableTit="太古平日時間表", Next=tk[0])
    else:
        if timeRange(tkh) is 1:
            return render_template("tk.html", table=tkh, tableTit="太古假日時間表", check=False, Next=tkh[0])
        elif timeRange(tkh) is 2:
            return render_template("tk.html", table=tkh, tableTit="太古假日時間表", Prev=printPrev(tkh),
                                   Next=printNext(tkh),
                                   check=True)
        else:
            if tmrIsHoliday() is True:
                return render_template("tk.html", check=False, table=tkh, tableTit="太古假日時間表", Next=tkh[0])
            else:
                return render_template("tk.html", check=False, table=tk, tableTit="太古平日時間表", Next=tk[0])

if __name__ == '__main__':
    app.run()
