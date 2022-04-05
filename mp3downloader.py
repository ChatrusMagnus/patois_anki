
import requests as req
import re

class Mp3Downloader():

    def getMp3(self,url):
        if url is not None:
            mp3 = req.get(url)
            filename=re.findall("[0-9]+.mp3",url)
            print(filename[0])
            with open(filename[0],'wb') as f:
                f.write(mp3.content)
