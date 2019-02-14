import logging
import requests
from bs4 import BeautifulSoup
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def scrape_state_sites():
    state_leg_list = "https://www.congress.gov/state-legislature-websites"
    state_page = requests.get(state_leg_list)
    soup = BeautifulSoup(state_page.content, 'html.parser')
    state_list = soup.find_all(attrs={'class': 'plain margin7 three-column-list'})
    links = []
    for state in state_list:
        links.extend(state.find_all('a', href=True))

    state_links = {}
    for link in links:
        state_links.update({link.text: link['href']})

    open('data/state_legislatures.json', 'w').write(json.dumps(state_links, indent=4))


def scrape_california():
    house_link = 'https://www.assembly.ca.gov/assemblymembers'
    senate_link = 'https://www.senate.ca.gov/senators'
    house_page = requests.get(house_link)
    senate_page = requests.get(senate_link)

    house_soup = BeautifulSoup(house_page.content, 'html.parser')
    house_photos = house_soup.find_all('img', attrs={'width': '120', 'height': '150'})
    for hp in house_photos:
        file_name = hp['src'].split('/')[-1]
        himg = requests.get(hp['src'])
        open('data/california/house/{}'.format(file_name), 'wb').write(himg.content)
        logger.debug(hp['src'])

    senate_soup = BeautifulSoup(senate_page.content, 'html.parser')
    senate_photos = senate_soup.find_all('img', attrs={'typeof': 'foaf:Image'})
    for sp in senate_photos:
        sfile_name = (sp['alt'].replace('Senator ', '')).replace(' ', '_')
        logger.debug(sp['src'])
        simg = requests.get(sp['src'])
        open('data/california/senate/{}.jpg'.format(sfile_name), 'wb').write(simg.content)


def scrape_washington():
    house_link = 'http://leg.wa.gov/House/Pages/MemberPortraits.aspx'
    senate_link = 'http://leg.wa.gov/Senate/Senators/Pages/SenatePhotoResources.aspx'
    house_page = requests.get(house_link)
    senate_page = requests.get(senate_link)

    # house_soup = BeautifulSoup(house_page.content, 'html.parser')
    # house_photos = house_soup.find_all('img', attrs={'style': 'width:60px;'})
    # house_purl = 'http://leg.wa.gov/House/Representatives/PublishingImages/'
    # for hp in house_photos:
    #     try:
    #         himg = requests.get("{}{}.jpg".format(house_purl, hp['alt']))
    #         open('data/washington/house/{}.jpg'.format(hp['alt']), 'wb').write(himg.content)
    #     except:
    #         pass

    senate_soup = BeautifulSoup(senate_page.content, 'html.parser')
    senate_photos = senate_soup.find_all('a')
    for sp in senate_photos:
        try:
            pol = sp['href'].split('/Senate/Senators/publishingimages/')
            if '.jpg' in pol[1]:
                simg = requests.get("http://leg.wa.gov{}".format(sp['href']))
                open('data/washington/senate/{}'.format(pol[1]), 'wb').write(simg.content)
            else:
                pass
        except Exception as e:
            logger.debug(e)
            pass

if __name__ == '__main__':
    # scrape_state_sites()
    # scrape_california()
    scrape_washington()
