from bs4 import BeautifulSoup
import requests

URL_PAGE = "https://gist.github.com/paulmillr/2657075"


def get_soup_from_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    return soup


def get_user_list(url):
    res = []
    soup = get_soup_from_url(url)
    table = soup.find('tbody')
    t_row = table.find_all('tr')
    for row in t_row:
        rank = row.find('th').text
        id = row.find('a').text
        link = row.find('a').attrs['href']
        name = row.find('td').text
        # print("rank: %s" % rank)
        # print("id: " + str(id))
        # print("link: " + str(link))
        # print("name: " + str(name))
        # print([rank, id, name])
        res.append([rank, id, name])
    return res

def get_request(url, headers):
    res = requests.get(url, headers=headers)
    return res.json()

def mean(lst):
    return sum(lst) / len(lst)

def get_repos_star(user_list):
    for user in user_list:
        url_repo = "https://api.github.com/users/" + user[1] + "/repos"
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Authorization': 'token f37830758283ea6a2f2d62d608e7cafedb56dc6b',
            'Content-Type': 'application/json',
            'method': 'GET',
            'Accept': 'application/json'
        }

        repos = get_request(url_repo, headers)
        star_list = []
        for repo in repos:
            star_list.append(repo['stargazers_count'])
        star_mean = mean(star_list)
        user.append(star_mean)
        # print(user)
    return user_list

def result_handle(repos_star_list):
    results = sorted(repos_star_list, key=lambda k: k[3], reverse=True)
    for i, r in enumerate(results):
        print("%s %s %s %s %.2f" % (i, r[0], r[1], r[2], r[3]))

if __name__ == "__main__":
    user_list = get_user_list(URL_PAGE)
    # print(user_list)
    repos_star_list = get_repos_star(user_list)

