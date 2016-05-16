#coding=utf-8
from flask import render_template, Flask
from ics import icalendar
from urllib.request import urlopen
import datetime,time
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
    if temp >= datetime.time(7,30) and temp < timeTable(x[len(x)-1]):
        return True
    else:
        return False

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/cwb')
def cwbr():
    if timeRange(cwb) == True:
        return render_template("cwb.html",table = cwb, tableTit = "銅鑼灣平日時間表", Prev = printPrev(cwb), Next = printNext(cwb), check = timeRange(cwb) )
    else:
        return render_template("cwb.html",check = timeRange(cwb), table= cwb , tableTit ="銅鑼灣平日時間表")

@app.route('/cwbh')
def cwbhr():
    if timeRange(cwbh) == True:
        return render_template("cwbh.html",table = cwbh, tableTit = "銅鑼灣假日時間表", Prev = printPrev(cwbh), Next = printNext(cwbh), check = timeRange(cwbh))
    else:
        return render_template("cwbh.html",check = timeRange(cwbh), table= cwbh , tableTit ="鑼灣假日時間表")

@app.route('/northpoint')
def npr():
    if timeRange(np) == True:
        return render_template("np.html",table = np, tableTit = "北角平日時間表", Prev = printPrev(np), Next = printNext(np), check = timeRange(np))
    else:
        return render_template("np.html",check = timeRange(np), table= np , tableTit ="北角平日時間表")

@app.route('/northpointh')
def nphr():
    if timeRange(nph) == True:
        return render_template("nph.html",table = nph, tableTit = "北角假日時間表", Prev = printPrev(nph), Next = printNext(nph), check = timeRange(nph))
    else:
        return render_template("nph.html", check=timeRange(nph), table=nph, tableTit="北角假日時間表")

@app.route('/taikoo')
def tkr():
    if timeRange(tk) == True:
        return render_template("tk.html",table = tk, tableTit = "太古平日時間表", Prev = printPrev(tk), Next = printNext(tk), check = timeRange(tk))
    else:
        return render_template("tk.html", check=timeRange(tk), table=tk, tableTit="太古平日時間表")

@app.route('/taikooh')
def tkhr():
    if timeRange(tkh) == True:
        return render_template("tkh.html",table = tkh, tableTit = "太古假日時間表", Prev = printPrev(tkh), Next = printNext(tkh), check = timeRange(tkh))
    else:
        return render_template("tkh.html", check=timeRange(tkh), table=tkh, tableTit="太古假日時間表")

if __name__ == '__main__':
    app.run()
