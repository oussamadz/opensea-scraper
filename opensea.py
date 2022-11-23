#!/usr/bin/python3

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import xlsxwriter
collections = names = owners = favs = avgs = covers = audios = descs = props = abouts = details = []


def propProcess(prop):
    items = prop.find_elements_by_class_name('item--property')
    text = ""
    for it in items:
        type_ = it.find_element_by_class_name('Property--type').text
        value_ = it.find_element_by_class_name('Property--value').text
        rarity_ = it.find_element_by_class_name(
            'Property--rarity').text.replace(' have this trait', '')
        text += f"{type_}:{value_}:{rarity_},"
    return text


def detailProcess(detail):
    items = detail.find_elements_by_tag_name('div')
    text = ""
    for div in items:
        title = div.text.split('\n')[0]
        if 'Address' in title:
            value = div.find_element_by_tag_name("a").get_attribute('href')
        else:
            value = div.find_element_by_tag_name("span").text
        text += f"{title}:{value},"
    return text


br = webdriver.Firefox()
br.get("https://opensea.io/assets?search[categories][0]=music")
container = br.find_element_by_class_name("AssetsSearchView--assets")
items = container.find_elements_by_tag_name("article")
links = []
for it in items:
    links.append(it.find_element_by_tag_name('a').get_attribute('href'))

print(f"{len(links)} item loaded\n processing ...")
for link in links:
    br.get(link)
    WebDriverWait(br, 60).until(
        EC.presence_of_element_located((By.TAG_NAME, 'audio')))
    collections.append(br.find_element_by_class_name(
        "CollectionLink--link").text)
    names.append(br.find_element_by_class_name('item--title').text)
    owners.append(br.find_element_by_class_name(
        "AccountLink--ellipsis-overflow").text)
    favs.append(br.find_element_by_class_name(
        'Textreact__Text-sc-1w94ul3-0').text.replace('favorites', ''))
    try:
        avgs.append(br.find_element_by_class_name(
            'PriceHistoryStats--value').text)
    except:
        avgs.append('N\A')
    covers.append(br.find_element_by_class_name(
        'Image--image').get_attribute('src'))
    audios.append(br.find_element_by_tag_name('audio').get_attribute('src'))
    descs.append(br.find_element_by_class_name("item--description-text").text)
    br.find_element_by_id('Header react-aria-3').click()
    props.append(propProcess(
        br.find_element_by_class_name('item--properties')))
    abouts.append(br.find_element_by_class_name('item--about-container').text)
    print(br.find_element_by_class_name('item--about-container').text)
    br.find_element_by_id('Header react-aria-11').click()
    details.append(detailProcess(br.find_element_by_id("react-aria-24")))
df = pd.DataFrame({'collections': collections, 'names': names, 'owners': owners, 'favs': favs, 'avgs': avgs,
                  'covers': covers, 'audios': audios, 'descs': descs, 'props': props, 'abouts': abouts, 'details': details})
writer = pd.ExcelWriter('audionft.xlsx', engine="xlsxwriter")
df.to_excel(writer, sheet_name="Sheet1")
