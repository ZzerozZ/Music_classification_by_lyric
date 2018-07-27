import scrapy
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import time



class NCT(scrapy.Spider):
    name = 'NCT'
    def start_requests(self):
        waitting = pd.read_csv('/home/nghia/Desktop/NCT/NCT/waitting.txt', header=None).values.ravel() 
        crawled = pd.read_csv('/home/nghia/Desktop/NCT/NCT/crawled.txt', header=None).values.ravel()
        for url in waitting:
            if url not in crawled:
                open('/home/nghia/Desktop/NCT/NCT/crawled.txt', 'a+').write(url+'\n')
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        crawled = pd.read_csv('/home/nghia/Desktop/NCT/NCT/crawled.txt', header=None).values.ravel()
        with open ('Song/'+ response.url.split('/')[-1].split('.')[0]+'.txt', 'w') as f:
            # Type:
            soup = bs(response.xpath("/html[1]/body[1]/div[6]/div[2]/div[1]/div[1]/div[6]/div[1]/div[1]/b[2]/a[1]").extract_first())
            f.write(soup.get_text() + '|\n')
            # Lyric:
            soup = bs(response.xpath("//p[@id='divLyric']").extract_first())
            f.write(soup.get_text() + '|\n')
            # Related song:
            soup = bs(response.xpath("//ul[@id='recommendZone']").extract_first())
            links = soup.find_all('a')
            links = [link.get('href') for link in links if link.get('href') not in crawled]
            links = np.unique(np.array([link for link in links if 'bai-hat' in link]))

            with open('/home/nghia/Desktop/NCT/NCT/waitting.txt', 'a+') as fin:
                for link in links:
                    fin.write(link + '\n')    

        time.sleep(3)    
