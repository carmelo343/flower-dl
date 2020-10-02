from bs4 import BeautifulSoup
import requests
import os

def main():
    download_imgs()

def get_page_urls():
    source = requests.get('https://www.atozflowers.com/flower/').text
    soup = BeautifulSoup(source, 'lxml')

    aTags = soup.select('h4 a')
    page_urls = []
    for a in aTags:
        page_urls.append(a['href'])
    soup.decompose()
    return page_urls

def download_imgs():
    page_urls = get_page_urls()
    download_count = 0
    for page_url in page_urls:
        source = requests.get(page_url).text
        soup = BeautifulSoup(source, 'lxml')

        flower_name = soup.find('h1').contents[0]
        if flower_name.endswith(' '):
            flower_name = flower_name[:-1]

        aTags = soup.find_all('a', {'data-fancybox': 'gallery'})
        for i, a in enumerate(aTags):
            file_name = f"{flower_name}-{i+1}.jpg"
            img_url = a['href']
            img_request = requests.get(img_url)

            if not os.path.exists('./img'):
                os.mkdir('./img')
            with open(f'./img/{file_name}', 'wb') as file:
                file.write(img_request.content)

            download_count += 1
            print(f"#{download_count} - Downloading {img_url}")
            
        soup.decompose()
    print(f"{download_count} images downloaded")

if __name__ == "__main__":
    main()
