import time
import cx_Oracle as co
from bs4 import BeautifulSoup
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('disable-gpu') # 가속 사용 x
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument('lang=ko_KR') # 가짜 플러그인 탑재
path = 'D:/devTools/Anaconda3/chromedriver.exe'
driver = webdriver.Chrome(path, options=chrome_options)

conn = co.connect('system/oracle@192.168.99.100:32764/xe', encoding='utf-8')

def printer(site, day, hour):
    print(f'*********{day} {hour}시 {site}차트*********')

def dr(site, day, hour, url):
    driver.get(url)
    driver.implicitly_wait(3)
    driver.get_screenshot_as_file(f'D:/workspace/VSCode/WebProject/screenshots/{site}{day}{hour}.jpg')

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    return soup

def saver(song):
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO HOTMUSIC_TOP (ID, SITE, DAY, HOUR, RANK, TITLE, ARTIST, IMAGE) VALUES(SEQ_NO.NEXTVAL, :1, :2, :3, :4, :5, :6, :7)" 
        cursor.execute(sql,song)
    except :
        sql = "INSERT INTO HOTMUSIC_TOP (ID, SITE, DAY, HOUR, RANK, TITLE, ARTIST) VALUES(SEQ_NO.NEXTVAL, :1, :2, :3, :4, :5, :6)" 
        cursor.execute(sql,song)
    conn.commit()

def bugs(day):
    site = 'bugs'
    lists = []
    hour = 0
    while hour <= 23:
        if 2 <= hour <= 5:
            hour = 6
        else:
            printer(site, day, hour)          
            url = f'https://music.bugs.co.kr/chart/track/realtime/total?chartdate=2019{day}&charthour={hour}'
            soup = dr(site, day, hour, url)
            table = soup.find('tbody')
            for r in table.find_all('tr'):
                for j,c in enumerate(r.find_all('td')):
                    if j==1:
                        rank =int(c.find('strong').text)
                    elif j==4:
                        for a, b in enumerate(c.find_all('a')):
                            if a==0:
                                artist = c.find('a').text.replace('"','').replace(' &',',')
                            elif a==1:
                                data = str(b).split('||')
                                data = data[1]+", "+data[3]
                                artist = data
                for k,q in enumerate(r.find_all('th')):
                    if k==0:
                        title =q.find('a').text.replace('ñ','n').replace('"','').replace(' &',',')
                row = [site, day, hour, rank, title, artist]
                saver(row)
        hour += 1
        time.sleep(1)
    driver.quit()

def melon(day):
    site = 'melon'
    lists = []
    hour = 0
    while hour <= 23:
        if 2 <= hour <= 5:
            hour = 6
        else:
            printer(site, day, hour)
            to = 50
            while to <= 100:
                if to == 50:
                    url = f'https://www.melon.com/chart/index.htm?dayTime=2019{day}{hour}'
                elif to == 100 :
                    url = f'https://www.melon.com/chart/index.htm?dayTime=2019{day}{hour}#params[idx]=51'
                soup = dr(site, day, hour, url)
                top = soup.select(f'tr.lst{to}')
                for song in top:
                    rank = song.find('span', {'class':'rank'}).text
                    title = song.find('div', {'class':'ellipsis rank01'}).text.replace('ñ','n').replace('"','').replace(' &',',')
                    artist = song.find('span', {'class':'checkEllipsis'}).text.replace('"','').replace(' &',',')
                    image = song.find('img').attrs['src'].replace('/melon/resize/120/quality/80/optimize','')
                    row = [site, day, hour, rank, title, artist, image]
                    saver(row)
                to += 50
        hour += 1
        time.sleep(1)
    driver.quit()

def genie(day):
    site = 'genie'
    lists = []
    hour = 0
    while hour <= 23:
        if 2 <= hour <= 5:
            hour = 6
        else:
            printer(site, day, hour)
            page = 1
            while page <= 2:
                url = f'https://www.genie.co.kr/chart/top200?ditc=D&ymd=2019{day}&hh={hour}&rtm=Y&pg={page}'
                soup = dr(site, day, hour, url)
                top = soup.select('tr.list')
                for song in top:
                    rank = song.find('td', {'class':'number'}).text.split('\n')[0].strip()
                    title = song.find('a', {'class':'title ellipsis'}).text.replace('ñ','n').replace('"','').replace(' &',',').strip()
                    artist = song.find('a', {'class':'artist ellipsis'}).text.replace('"','').replace(' &',',').strip()
                    row = [site, day, hour, rank, title, artist]
                    saver(row)
                page += 1
        hour += 1
        time.sleep(1)
    driver.quit()

if __name__=='__main__':
    today = '1218'

    # melon(today)
    # bugs(today)
    genie(today)
    conn.close()