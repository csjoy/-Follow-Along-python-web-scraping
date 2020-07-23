import requests
from bs4 import BeautifulSoup
import pprint

source_url = 'https://news.ycombinator.com/'


def sort_stories_by_votes(hacker_news):
    return sorted(hacker_news, key=lambda k: k['votes'], reverse=True)


def create_custom_hacker_news(source_url):
    url = source_url
    hacker_news = list()

    while True:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        links = soup.select('.storylink')
        subtext = soup.select('.subtext')
        more = soup.select('.morelink')

        if len(more):
            next_page = more[0].get('href', None)
        else:
            next_page = None

        for index, item in enumerate(links):
            title = item.getText()
            href = item.get('href', None)
            vote = subtext[index].select('.score')
            if len(vote):
                points = int(vote[0].getText().replace(' points', ''))
                if points > 99:
                    hacker_news.append(
                        {'title': title, 'link': href, 'votes': points})

        if next_page is None:
            break
        else:
            url = source_url + next_page
            print('.')

    return sort_stories_by_votes(hacker_news)


output_result = create_custom_hacker_news(source_url)
pprint.pprint(output_result)
# print(len(output_result))
