import requests
from bs4 import BeautifulSoup
import csv

languages = {"Hin"}

def check_lang(language):
    if language in languages.keys:
        return True
    else:
        return False

def scrape(language):
    '''
    '''
    
    if not check_lang(language):
        print()
        return
    
    lang_short = languages[language]
    website_url = requests.get(f'https://lrc.la.utexas.edu/lex/languages/{lang_short}').text

    soup = BeautifulSoup(website_url,'html.parser')

    my_table = soup.find_all('table', {'class':'reflexTable'})
    headers = ['Reflex', 'Etyma']

    rows = []

    # Find all `tr` tags
    data_rows = soup.find_all('tr')

    for row in data_rows:
        value = row.find_all('td')
        beautified_value = [ele.text.strip() for ele in value]
        # Remove data arrays that are empty
    #     if len(beautified_value) == 0:
    #         continue
        rows.append(beautified_value)

    # TODO change file name in open to an input filename using the language name being scraped
    with open('got_pie.csv', 'w', newline="") as output:
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)

lang = "Hin"
scrape(lang)
print("done!")