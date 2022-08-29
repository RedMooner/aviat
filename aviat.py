import requests
from bs4 import BeautifulSoup
import datetime
import urllib.request
import argparse
from tqdm import tqdm
import time

now = datetime.datetime.now()


def monthToNum(shortMonth):
    return {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря"
    }[shortMonth]


parser = argparse.ArgumentParser(
    description='replacement of aviation classes')
parser.add_argument(
    '--day',
    type=int,
    default=now.day + 1,
    help=f'provide an integer (default: next day)'
)


parser.add_argument(
    '--month',
    type=int,
    default=now.month,
    help=f'provide an integer (default: current month)'
)


def main():
    args = parser.parse_args()
    print("Поиск расписания на: " + str(args.day) +
          " " + str(monthToNum(args.month)))

    url = 'https://permaviat.ru/raspisanie-zamen/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='file_link')
    isConsists = False
    pbar = tqdm(total=len(items))
    for n, i in tqdm(enumerate(items, start=1)):
        itemName = i.find('div', class_='header').find('a').text.strip()
        if (str(itemName).__contains__(str(args.day)) and str(itemName).__contains__(monthToNum(args.month))):
            tqdm.write(f'Выложено расписание: {itemName}')
            link = i.find('div', class_='header').find('a').get("href")
            tqdm.write(f"{url}{link}")
            urllib.request.urlretrieve(
                f"https://permaviat.ru{link}", "temp.pdf")
            isConsists = True
        pbar.update(1)
    pbar.close()
    if (isConsists == False):
        print("Расписания еще нет!")
        
        
if __name__ == "__main__":
	main()