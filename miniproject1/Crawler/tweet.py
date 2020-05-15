import cx_Oracle as co
import time
import datetime as dt
from bs4 import BeautifulSoup
from selenium import webdriver

conn = co.connect('system/oracle@192.168.99.100:32764/xe', encoding='utf-8')

def selector(day):
    cursor = conn.cursor()
    sql = f"SELECT distinct TITLE, ARTIST FROM HOTMUSIC_TOP WHERE HOUR='10' AND DAY={day} AND SITE='bugs'"
    cursor.execute(sql)
    keyword = cursor.fetchall()
    return keyword

def saver(tweet):
    cursor = conn.cursor()
    sql = 'INSERT INTO HOTMUSIC_TWEET (ID, T_TITLE, T_ARTIST, T_DAY, T_COUNT) VALUES(SEQ_NO.NEXTVAL, :1, :2, :3, :4)'
    cursor.execute(sql, tweet)
    conn.commit()

day = '1218'
tmp = selector(day)
for i in range(0,len(tmp)):
    keyword = tmp[i][0] + tmp[i][1]

    startdate=dt.date(year=2019,month=12,day=17)
    untildate=dt.date(year=2019,month=12,day=18)
    enddate=dt.date(year=2019,month=12,day=18)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('disable-gpu') # 가속 사용 x
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('lang=ko_KR') # 가짜 플러그인 탑재
    path = 'D:/devTools/Anaconda3/chromedriver.exe'
    driver = webdriver.Chrome(path, options=chrome_options)

    totalfreq=[]
    while not enddate==startdate:
        url=f'https://twitter.com/search?q={keyword}%20since%3A{startdate}%20until%3A{untildate}&amp;amp;amp;amp;amp;amp;lang=eg'
        driver.get(url)
        driver.implicitly_wait(2)
        driver.get_screenshot_as_file(f'D:/workspace/VSCode/WebProject/screenshots/tweet/tweet{day}{keyword}.jpg')
        html = driver.page_source
        soup=BeautifulSoup(html,'lxml')
        
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while True:
            wordfreq=0
            tweets=soup.find_all("p", {"class": "TweetTextSize"})
            wordfreq+=len(tweets)
                
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            newHeight = driver.execute_script("return document.body.scrollHeight")
            
            if newHeight != lastHeight:
                html=driver.page_source
                soup=BeautifulSoup(html,'html.parser')
                tweets=soup.find_all("p", {"class": "TweetTextSize"})
                wordfreq=len(tweets)
            else:
                startdate=untildate
                untildate+=dt.timedelta(days=1)
                tweet = [tmp[i][0], tmp[i][1], day, wordfreq]
                saver(tweet)
                break
            lastHeight = newHeight
    driver.quit()