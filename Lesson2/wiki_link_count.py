from bs4 import BeautifulSoup
import requests

# can import func-timeout to set a timer to kill the function for timeout

# A set to include all the path to avoid dead loop
res = set()


def find_distance(word):
    """
    :param word: the word to find the distance with 'Philosophy'
    :return: the distance with 'Philosophy'
    """
    global res
    while word.title() != "Philosophy":
        word_new = get_word(word)
        print(word_new)
        if word_new == -1:
            return -1
        res.add(word_new)
        word = word_new
    return len(res)


def judge_link(link):
    """
    jugde the link (label 'a') is useful or not
    :param link: label 'a'
    :return: true or false
    """
    # simple case
    if 'href' not in link.attrs:
        return False
    if link.attrs['href'].startswith('/wiki/Help'):
        return False
    if link.attrs['href'].startswith('#cite'):
        return False
    if 'class' in link.attrs and 'mw-redirect' in link.attrs['class']:
        return False

    return True


def judge_word(word_new):
    """
    judge the word (get from label 'a') is useful or not
    :param word_new:
    :return: true or false
    """
    global res
    if word_new in res:
        return False
    if '%' in word_new:
        return False
    return True


def get_word(word):
    """
    use api to get new word
    :param word: current word
    :return: new word which is got from the current word's wiki
    """
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
    # simple case to choose link
    ps = soup.find_all("p", class_="")
    for p in ps:
        # print(p)
        links = p.find_all("a")
        for link in links:
            # print(link)
            if judge_link(link):
                word_new = link.attrs['href'].split("/")[-1]
                # print(word_new)
                if judge_word(word_new):
                    return word_new

    print("no new word is found")
    return -1


if __name__ == "__main__":
    # input = "earth"   # => 45
    # input = "word"    # => 37
    input = "number"    # => 34
    res = find_distance(input)
    if res == -1:
        print("The distance is not found")
    print("The distance of " + input + " is: " + str(res))
