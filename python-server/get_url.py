import requests
import urllib
import os
from bs4 import BeautifulSoup


def getImageUrl(path):
    url = "https://www.noelshack.com/api.php"

    fn = os.path.basename(path)

    payload = {
        "fichier" : open(path, "rb")
    }

    r = requests.post(url, files=payload)
    with urllib.request.urlopen(r.text) as url:
        s = url.read()
    soup = BeautifulSoup(s, "html.parser")
    all_tag_a = soup.find_all("img", limit=1)
    for links in all_tag_a:
        myLink = links.get('src')
#        print(myLink)
        return myLink
