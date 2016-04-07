import requests as req
import re
ftpURL = "http://mirror.yandex.ru/mirrors/ftp.flightgear.org/flightgear/Scenery-v2.12/"

r = req.get(ftpURL)
pattern = re.compile(r'\w\d{3}\w\d{2}.tgz')
pfound = list(set(pattern.findall(r.text)))
pfound.sort()
# print(pfound)
fp = open("url.txt", 'w')
for item in pfound:
    fp.write(ftpURL + item + '\n')

# fp.write(r.text)
fp.close()