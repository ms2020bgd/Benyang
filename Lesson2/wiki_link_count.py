from bs4 import BeautifulSoup
import requests
import re


def f(word):
    if word.title() == "Philosophy":
        return 0
    print(word)
    page = 'https://en.wikipedia.org/wiki/' + word.title()

    content = requests.get(page).text

    soup = BeautifulSoup(content)
    paragraph = soup.find('p', class_='')
    paragraph_no_para = re.sub(u"\\(.*?\\)", "", str(paragraph))
    paragraph_no_para = BeautifulSoup(paragraph_no_para)
    # link = paragraph_no_para.find('p', class_='').find('a')
    link = paragraph_no_para.select("p > a")[0]
    print(link)
    print(link.attrs['href'].split("/")[-1])
    return f(link.attrs['href'].split("/")[-1]) + 1


input = "word"

print(f(input))
