import requests
import re
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import json


HOST = "https://spb.hh.ru"
url = f"{HOST}/search/vacancy?text=python&area=1&area=2"

def get_headers():
    return Headers(browser="firefox", os="win").generate()

def get_text(url):
    return requests.get(url, headers=get_headers()).text

def vacancy_parser(url):
    html = get_text(url)
    soup = BeautifulSoup(html, features="html5lib")
    vacancies = soup.findAll('div', class_='serp-item')
    data = []
    for vacancy in vacancies:
        dict_vac = {}
        dict_vac['link'] = vacancy.find('a', class_='serp-item__title').get('href')
        if vacancy.find('span', class_='bloko-header-section-3') is None:
            dict_vac['salary'] = ('не указано')
        else:
            dict_vac['salary'] = ((vacancy.find("span", class_="bloko-header-section-3").text).replace('\u202f', ''))
        dict_vac['company'] = (vacancy.find('div', class_='vacancy-serp-item__meta-info-company').text)
        dict_vac['location'] = (vacancy.find(attrs={"data-qa": "vacancy-serp__vacancy-address"}).text)    
        data.append(dict_vac)
    return data
    

def vac_sorter(url):
    final_list = vacancy_parser(url) 
    # pprint(start_list)   
    for vac in final_list:
        link = vac['link']
        html = get_text(link)
        soup = BeautifulSoup(html, features="html5lib")  
        info = soup.find(attrs={"class": ["vacancy-branded-user-content", "vacancy-description"]}).text     
        pattern1 = re.search(r'[Dd]jango', info)
        pattern2 = re.search(r'[Ff]lask', info)
        if pattern1 or pattern2:
            pass
        else:
            final_list.remove(vac)
    save_json(final_list)
    return final_list


def save_json(list):
    with open('web_parser.json', 'w', encoding='UTF-8') as f:
        json.dump(list, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    vac_sorter(url)
    

