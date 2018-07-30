import os
import time

while True:
    os.system('source activate py3 & cd github/Music_classification_by_lyric/NCT_Crawler/ & scrapy crawl NCT')
    time.sleep(600)