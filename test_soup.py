import re
import requests
from bs4 import BeautifulSoup
import os


def find_styles(URL):
    a = requests.get(URL)
    a.raise_for_status()
    soup = BeautifulSoup(a.text, 'lxml')
    list_of_styles = [btn.text for btn in soup.find_all('button') if
                      btn.text not in [' Previous', ' Next', 'submit', 'see our new stores', 'sold out', '',
                                       'add to cart']]
    return list_of_styles


def get_image(url, style, class_attr):
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, 'lxml')

    if style is not None:
        images = soup.find_all('image')
        img_to_download = re.findall("href=[\"\'](.*?)[\"\']", str(images[style]))
    else:
        images = soup.findall('div', {'class': class_attr})
        img_to_download = [i.find('img')['src'] for i in images]

    print(img_to_download[0])
    return download_image(img_to_download[0])


def download_image(image_url, first_sep='/', sec_sep='?'):
    """
        Downloads a file given an URL and puts it in the folder `pathname`

        """

    local_filename = image_url.split(first_sep)[-1].split(sec_sep)[0] + '.jpg'

    complete_filename = os.path.join('C:/Users/colin/PycharmProjects/', 'squish_site/media/images', local_filename)

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})

    r = session.get(image_url, stream=True, verify=True)
    print(complete_filename)
    with open(complete_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)

    return local_filename  # returns name of file image is downloaded as
