import logging
import requests
from bs4 import BeautifulSoup
import json
import sys
import state_scraper

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


def fetch_top_list(url, tag, attrs=None):
    """
    use a link to fetch a list of image links
    :param link:
    :param attrs:
    :return:
    """
    state_page = requests.get(url)
    soup = BeautifulSoup(state_page.content, 'html.parser')
    return soup.find_all(tag, attrs=attrs)


def scrape_california():
    sts = state_scraper.StateScraper()
    cali_data = sts.fetch_state_data('california')
    house_photos = fetch_top_list(cali_data)
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

    house_soup = BeautifulSoup(house_page.content, 'html.parser')
    house_photos = house_soup.find_all('img', attrs={'style': 'width:60px;'})
    house_purl = 'http://leg.wa.gov/House/Representatives/PublishingImages/'
    for hp in house_photos:
        try:
            himg = requests.get("{}{}.jpg".format(house_purl, hp['alt']))
            open('data/washington/house/{}.jpg'.format(hp['alt']), 'wb').write(himg.content)
        except:
            pass

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


def scrape_oregon():
    logger.debug('oregon')


def scrape_florida():
    logger.debug('florida')


def scrape_colorado():
    logger.debug('colorado')


def scrape_iowa():
    logger.debug('iowa')


def scrape_illinois():
    logger.debug('illinois')


def scrape_michigan():
    logger.debug('michigan')


def scrape_wisconsin():
    logger.debug('wisconsin')


def scrape_georgia():
    logger.debug('georgia')


if __name__ == '__main__':
    try:
        state = sys.argv[1]
    except Exception as e:
        logger.warning(e)

    if state == 'california':
        scrape_california()
    elif state == 'washington':
        scrape_washington()
    elif state == 'oregon':
        scrape_oregon()
    elif state == 'florida':
        scrape_florida()
    elif state == 'colorado':
        scrape_colorado()
    elif state == 'iowa':
        scrape_iowa()
    elif state == 'illinois':
        scrape_illinois()
    elif state == 'michigan':
        scrape_michigan()
    elif state == 'wisconsin':
        scrape_wisconsin()
    elif state == 'georgia':
        scrape_georgia()
    else:
        logger.info('Sorry, that state is not yet supported.')
