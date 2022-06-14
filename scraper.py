#!/usr/bin/python3

"""
Scraper bestand om alle infopunten te downloaden.
Let op: de volgorde is niet correct.
Dit moet handmatig omdat de GBG punten op de wandelroutes niet exact overheenkomen met de echte puntnamen.
"""


import os
import json
import string
import requests
import traceback
from collections import OrderedDict
from bs4 import BeautifulSoup as BS


URL = "https://www.beeldengedicht.nl/beeld-en-gedicht/"


def GetRouteLinks(bsdom:BS, naam:str):
    div = bsdom.find(text=naam).parent.parent.find(class_="u-blog").find_all("a", href=True)
    links = list(OrderedDict.fromkeys([str(a['href']) for a in div]))
    return links

def FetchPointData(link):
    dom = requests.get(link)
    if dom.ok == False:
        raise Exception(f"URL '{link}' had return code {dom.status_code}")

    bsdom = BS(dom.text, 'html.parser')

    titel = bsdom.find('h2')
    afbeelding = titel.parent.find('img')

    gedicht_titel = titel.parent.find('strong')
    gedicht = '\n\n'.join([a.text for a in titel.parent.find('div').find('div').find_all('p') if not '<strong>' in str(a)])

    info = titel.parent.find('pre')

    return {
        'titel': string.capwords(titel.text),
        'afbeelding': afbeelding['src'],
        'gedicht_titel': gedicht_titel.text if gedicht_titel != None else string.capwords(titel.text),
        'gedicht': gedicht,
        'info': '\n'.join(info.text.split('\n')[1:])
        
    }

def SavePoint(point, path, index=0):
    mypath = f'{path}/{index}${point["titel"]}'
    # print(f'   [i] Dit punt word opgeslagen naar "{mypath}"')
    os.mkdir(mypath)
    
    img = requests.get(point['afbeelding'])
    if img.ok == False:
        raise Exception(f"Kan afbeelding '{point['afbeelding']}' niet downloaden. return code: {img.status_code}")

    file_extension = img.headers['Content-Type'].split('/')[-1]

    with open(mypath+'/img.'+file_extension, 'wb') as f:
        f.write(img.content)
    
    # print(f'   [i] Afbeelding gedownload als img.{file_extension}')

    with open(mypath+'/data.json', 'w') as f:
        f.write(json.dumps(point))

    # print('   [i] Punt opgeslagen als data.json')

def DownloadPoints(links:list, path:str):
    print(f"De punten zullen opgeslagen worden in de folder '{path}'")
    if os.path.exists(path):
        if len(os.listdir(path)) > 0:
            raise Exception(f"De folder {path} bestaat al en is niet leeg! Verwijder deze bestanden: {[a for a in os.listdir(path)]}")
    else:
        os.mkdir(path)
        print("Folder aangemaakt.")


    print("Punten downloaden...")
    for i, link in enumerate(links):
        print(f' Item {i+1}/{len(links)}: "{link}"')
        try:
            # print('  Fetchen...')
            data = FetchPointData(link)
            print('   [i] Punt naam:',data['titel'])
            # print('  Downloaden...')
            SavePoint(data, path)
            # print('  Klaar.')

        except Exception as e:
            print(" [!!] Error: "+str(e))
            # traceback.print_exc()
            raise e
        
    

def main():
    print(f"{URL} fetchen...")
    dom = requests.get(URL)
    if dom.ok == False:
        raise Exception(f"URL '{URL}' had return code {dom.status_code}")
    print("OK\n")

    bsdom = BS(dom.text,'html.parser')
    routes = bsdom.find_all('h2') 
    print("Routes: ")
    print('\n'.join([f"   [{i}] {a.text}" for i,a in enumerate(routes)]))
    print()
    choice = input("Maak een keuze (nummer): ")
    
    links = GetRouteLinks(bsdom, routes[int(choice)].text)

    print()
    print(f"Deze route heeft {len(links)} infopunten")

    DownloadPoints(links, f'./wandelroutes/{routes[int(choice)].text}')

    print("Helemaal klaar.")

if __name__ == "__main__":
    main()