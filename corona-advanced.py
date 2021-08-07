from csv import DictReader
from datetime import date, timedelta
import json
import requests
import os
from pyecharts.charts import Map, Timeline
from pyecharts import options as opts
from pyecharts.globals import ThemeType

confirm = requests.get('https://raw.fastgit.org/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
death = requests.get('https://raw.fastgit.org/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recover = requests.get('https://raw.fastgit.org/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
os.system('rm -rf confirm.csv death.csv recover.csv confirm.json death.json recover.json')
fc = open('confirm.csv', 'x', encoding = 'utf-8')
fd = open('death.csv', 'x', encoding = 'utf-8')
fr = open('recover.csv', 'x', encoding = 'utf-8')
fc.write(confirm.text)
fd.write(death.text)
fr.write(recover.text)
fc.close()
fd.close()
fr.close()
jsnc = []
jsnd = []
jsnr = []
fjsnc = open('confirm.json', 'x', encoding = 'utf-8')
fjsnd = open('death.json', 'x', encoding = 'utf-8')
fjsnr = open('recover.json', 'x', encoding = 'utf-8')
fc = open('confirm.csv', 'r', encoding = 'utf-8')
fd = open('death.csv', 'r', encoding = 'utf-8')
fr = open('recover.csv', 'r', encoding = 'utf-8')
rdc = DictReader(fc)
rdd = DictReader(fd)
rdr = DictReader(fr)

for row in rdc:
    jsnc.append(row)

for row in rdd:
    jsnd.append(row)

for row in rdr:
    jsnr.append(row)

json.dump(jsnc, fjsnc)
json.dump(jsnd, fjsnd)
fjsnc.close()
fjsnd.close()
print('Information is stored in json format if needed')
dead = {}
conf = {}
rcov = {}
dates = []
delta = timedelta(1)
start = date(2020, 1, 22)
end = date.today() - delta
while start != end:
    dates.append(str(start.month) + '/' + str(start.day) + '/' + str(start.year % 100))
    start = start + delta

flag = False
total = 0
country = ''
countries = []
usflag = False
allafter = 0
for dat in dates:
    conf[dat] = {}
    dead[dat] = {}
    rcov[dat] = {}
    for elem in jsnc:
        if elem['Country/Region'] == 'Summer Olympics 2020':
            continue
        if elem['Country/Region'] == 'US':
            elem['Country/Region'] = 'United States'
        if elem['Country/Region'] == 'Korea, South':
            elem['Country/Region'] = 'Dem. Rep. Korea'
        if elem['Country/Region'] == 'Congo (Brazzaville)':
            elem['Country/Region'] = 'Congo'
        if elem['Country/Region'] == 'Congo (Kinshasa)':
            elem['Country/Region'] = 'Dem. Rep. Congo'
        if elem['Country/Region'] == 'South Sudan':
            elem['Country/Region'] = 'S. Sudan'
        if elem['Country/Region'] == 'Central African Republic':
            elem['Country/Region'] = 'Central African Rep.'
        if elem['Province/State'] == 'Greenland':
            elem['Country/Region'] = 'Greenland'
            elem['Province/State'] = ''
        if elem['Country/Region'] not in countries:
            countries.append(elem['Country/Region'])
        if elem['Province/State'] == '':
            if elem['Country/Region'] not in conf[dat].keys():
                conf[dat][elem['Country/Region']] = {}
            conf[dat][elem['Country/Region']]['total'] = elem[dat]
            if 'children' not in conf[dat][elem['Country/Region']].keys():
                conf[dat][elem['Country/Region']]['children'] = None
            if flag == True:
                flag = False
                conf[dat][country]['total'] = total
                total = 0
                country = ''
        else:
            if elem['Country/Region'] != country and country != '':
                flag = False
                conf[dat][country]['total'] = total
                total = 0
                country = ''
            if flag == True:
                total = total + int(elem[dat])
            if flag == False:
                flag = True
                country = elem['Country/Region']
                conf[dat][country] = {}
                conf[dat][country]['children'] = []
            conf[dat][country]['children'].append({elem['Province/State'] : elem[dat]})
    for elem in jsnd:
        if elem['Country/Region'] == 'Summer Olympics 2020':
            continue
        if elem['Country/Region'] == 'US':
            elem['Country/Region'] = 'United States'
        if elem['Country/Region'] == 'Korea, South':
            elem['Country/Region'] = 'Dem. Rep. Korea'
        if elem['Country/Region'] == 'Congo (Brazzaville)':
            elem['Country/Region'] = 'Congo'
        if elem['Country/Region'] == 'Congo (Kinshasa)':
            elem['Country/Region'] = 'Dem. Rep. Congo'
        if elem['Country/Region'] == 'South Sudan':
            elem['Country/Region'] = 'S. Sudan'
        if elem['Country/Region'] == 'Central African Republic':
            elem['Country/Region'] = 'Central African Rep.'
        if elem['Province/State'] == 'Greenland':
            elem['Country/Region'] = 'Greenland'
            elem['Province/State'] = ''
        if elem['Country/Region'] not in countries:
            countries.append(elem['Country/Region'])
        if elem['Province/State'] == '':
            if elem['Country/Region'] not in dead[dat].keys():
                dead[dat][elem['Country/Region']] = {}
            dead[dat][elem['Country/Region']]['total'] = elem[dat]
            if 'children' not in dead[dat][elem['Country/Region']].keys():
                dead[dat][elem['Country/Region']]['children'] = None
            if flag == True:
                flag = False
                dead[dat][country]['total'] = total
                total = 0
                country = ''
        else:
            if elem['Country/Region'] != country and country != '':
                flag = False
                dead[dat][country]['total'] = total
                total = 0
                country = ''
            if flag == True:
                total = total + int(elem[dat])
            if flag == False:
                flag = True
                country = elem['Country/Region']
                dead[dat][country] = {}
                dead[dat][country]['children'] = []
            dead[dat][country]['children'].append({elem['Province/State'] : elem[dat]})
    for elem in jsnr:
        if elem['Country/Region'] == 'Summer Olympics 2020':
            continue
        if elem['Country/Region'] == 'US':
            elem['Country/Region'] = 'United States'
        if elem['Country/Region'] == 'Korea, South':
            elem['Country/Region'] = 'Dem. Rep. Korea'
        if elem['Country/Region'] == 'Congo (Brazzaville)':
            elem['Country/Region'] = 'Congo'
        if elem['Country/Region'] == 'Congo (Kinshasa)':
            elem['Country/Region'] = 'Dem. Rep. Congo'
        if elem['Country/Region'] == 'South Sudan':
            elem['Country/Region'] = 'S. Sudan'
        if elem['Country/Region'] == 'Central African Republic':
            elem['Country/Region'] = 'Central African Rep.'
        if elem['Province/State'] == 'Greenland':
            elem['Country/Region'] = 'Greenland'
            elem['Province/State'] = ''
        if dat == '12/13/20' and elem['Country/Region'] == 'United states':
            usflag = True
        if usflag == True and elem['Country/Region'] == 'United states':
            elem[dat] = elem['12/13/20']
        if elem['Country/Region'] not in countries:
            countries.append(elem['Country/Region'])
        if elem['Province/State'] == '':
            if elem['Country/Region'] not in rcov[dat].keys():
                rcov[dat][elem['Country/Region']] = {}
            rcov[dat][elem['Country/Region']]['total'] = elem[dat]
            if 'children' not in rcov[dat][elem['Country/Region']].keys():
                rcov[dat][elem['Country/Region']]['children'] = None
            if flag == True:
                flag = False
                rcov[dat][country]['total'] = total
                total = 0
                country = ''
        else:
            if elem['Country/Region'] != country and country != '':
                flag = False
                rcov[dat][country]['total'] = total
                total = 0
                country = ''
            if flag == True:
                total = total + int(elem[dat])
            if flag == False:
                flag = True
                country = elem['Country/Region']
                rcov[dat][country] = {}
                rcov[dat][country]['children'] = []
            rcov[dat][country]['children'].append({elem['Province/State'] : elem[dat]})

timeline = (
    Timeline(init_opts=opts.InitOpts(page_title='Coronavirus', theme=ThemeType.LIGHT))
)
timeline2 = (
    Timeline(init_opts=opts.InitOpts(page_title='Coronavirus', theme=ThemeType.LIGHT))
)
timeline3 = (
    Timeline(init_opts=opts.InitOpts(page_title='Coronavirus', theme=ThemeType.LIGHT))
)
for i in range(len(dates)):
    dat = dates[i]
    czipped = []
    dzipped = []
    rzipped = []
    for cntry in countries:
        czipped.append((cntry, conf[dat][cntry]['total']))
        dzipped.append((cntry, dead[dat][cntry]['total']))
        rzipped.append((cntry, rcov[dat][cntry]['total']))
    map = (
        Map()
        .add('Confirmed', czipped, 'world')
        .set_series_opts(label_opts=opts.LabelOpts(position='right'))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=[
            {'min':10000000, 'label':'10000000+', 'color':'#f26522'},
            {'min':1000000, 'max':9999999, 'color':'#102b6a'},
            {'min':500000, 'max':999999, 'color':'#411445'},
            {'min':100000, 'max':499999, 'color':'#003a6c'},
            {'min':50000, 'max':99999, 'color':'#494e8f'},
            {'min':6000, 'max':49999, 'color':'#130c0e'},
            {'min':2000, 'max':5999, 'color':'#401c44'},
            {'min':300, 'max':1999, 'color':'#78331e'},
            {'min':150, 'max':299, 'color':'#7a1723'},
            {'min':90, 'max':149, 'color':'#a7324a'},
            {'min':40, 'max':89, 'color':'#d93a49'},
            {'min':20, 'max':39, 'color':'#f8aba6'},
            {'min':0, 'max':19, 'color':'#feeeed'}
        ]))
    )
    map2 = (
        Map()
        .add('Dead', dzipped, 'world')
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=[
            {'min':100000, 'label':'100000+', 'color':'#f26522'},
            {'min':50000, 'max':99999, 'color':'#003a6c'},
            {'min':13000, 'max':49999, 'color':'#494e8f'},
            {'min':1000, 'max':12999, 'color':'#130c0e'},
            {'min':500, 'max':999, 'color':'#401c44'},
            {'min':250, 'max':499, 'color':'#78331e'},
            {'min':150, 'max':249, 'color':'#7a1723'},
            {'min':90, 'max':149, 'color':'#a7324a'},
            {'min':40, 'max':89, 'color':'#d93a49'},
            {'min':20, 'max':39, 'color':'#f8aba6'},
            {'min':0, 'max':19, 'color':'#feeeed'}
        ]))
    )
    map3 = (
        Map()
        .add('Recovered', rzipped, 'world')
        .set_series_opts(label_opts=opts.LabelOpts(position='right'))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=[
            {'min':10000000, 'label':'10000000+', 'color':'#009ad6'},
            {'min':1000000, 'max':9999999, 'color':'#00ae9d'},
            {'min':500000, 'max':999999, 'color':'#78a355'},
            {'min':100000, 'max':499999, 'color':'#5c7a29'},
            {'min':50000, 'max':99999, 'color':'#a3cf62'},
            {'min':6000, 'max':49999, 'color':'#b2d235'},
            {'min':2000, 'max':5999, 'color':'#7fb80e'},
            {'min':300, 'max':1999, 'color':'#007d65'},
            {'min':150, 'max':299, 'color':'#007947'},
            {'min':90, 'max':149, 'color':'#1d953f'},
            {'min':40, 'max':89, 'color':'#84bf96'},
            {'min':20, 'max':39, 'color':'#abc88b'},
            {'min':0, 'max':19, 'color':'#cde6c7'}
        ]))
    )
    timeline.add(map, dat)
    timeline2.add(map2, dat)
    timeline3.add(map3, dat)
timeline.add_schema(play_interval=50)
timeline.render('Corona-confirms.html')
timeline2.add_schema(play_interval=50)
timeline2.render('Corona-deaths.html')
timeline3.add_schema(play_interval=50)
timeline3.render('Corona-recoveries.html')
print('Generated graphs')
print('Done')