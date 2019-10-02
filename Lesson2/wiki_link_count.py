from bs4 import BeautifulSoup
import requests
import re


def f(word):
    if word.title() == "Philosophy":
        return 0

    session_api = requests.Session()

    url_api = "https://en.wikipedia.org/w/api.php"

    params_api = {
        "action": "parse",
        "page": word,
        "format": "json"
    }

    response = session_api.get(url=url_api, params=params_api)
    data = response.json()
    html = data['parse']['text']['*']
    soup = BeautifulSoup(html, features="html.parser")
    # paragraph = soup.find('p', class_='')
    # paragraph_no_para = re.sub(u"\\(.*?\\)", "", str(paragraph))
    # paragraph_no_para = str(paragraph)
    # paragraph_no_para = BeautifulSoup(paragraph_no_para, features="html.parser")
    # link = paragraph_no_para.select("p > a")[0]
    # link = soup.select("p.mw-body-content>a")[0]
    p_list = soup.find_all('p', class_='')
    for p in p_list:

        links = p.find_all('a', class_='')
        if len(links):
            if judge_link(links):
                break
    link = links[0]
    print(link)
    print(link.attrs['href'])
    print(link.attrs['href'].split("/")[-1])
    return f(link.attrs['href'].split("/")[-1]) + 1

def judge_link(link):
    if link[0].attrs['href'].startswith('/wiki/Help'):
        return False
    return True

input = "science"
# input = "Astronomical_body"

print(f(input))
