import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient()
#songs = client.kugou_db.songs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0"
}

def get_info(url):

    wb_data = requests.get(url)

    soup = BeautifulSoup(wb_data.text,'html.parser')

    ranks = soup.select(".pc_temp_num")

    titles = soup.select(".pc_temp_songname")
    song_times = soup.select(".pc_temp_time")

    for rank,title,song_time in zip(ranks,titles,song_times):
        data = {
            'rank': rank.get_text().strip(),
            'title': title.get_text(),
            'song_time': song_time.get_text().strip()
        }
        print(data)
        print("--------------------------------------------------------------")


if __name__ == "__main__":
    urls = ["http://www.kugou.com/yy/rank/home/{}-8888.html?from=rank".format(str(i)) for i in range(1,24)]
    for url in urls:
        get_info(url)
        #time.sleep(1)