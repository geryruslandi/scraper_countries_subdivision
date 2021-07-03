from bs4 import BeautifulSoup
import requests
import csv

url = 'https://www.citypopulation.de/en/thailand/admin/'
webPage = requests.get(url, timeout=5)
table = BeautifulSoup(webPage.content, 'html.parser').select('#tl')[0]

tableBodies = table.findAll('tbody')

provinces = []

for tableBody in tableBodies:
    tableRows = tableBody.findAll('tr')
    for tableRow in tableRows:
        tableItems = tableRow.findAll('td')
        if tableItems[1].text == 'Province':
            provinces.append({'name': tableItems[0].text, 'regions': []})
        else:
            provinces[len(provinces) - 1]['regions'].append(tableItems[0].text)


fields = ['Level 1', 'Type', 'Level 2', 'Type']
rows = [];

for province in provinces:
    for index, region in enumerate(province['regions']):
        if index == 0:
            rows.append([province['name'], 'Province', region, 'Region' ])
        else:
            rows.append(['', '', region, 'Region'])

with open('/root/app/csv/thailand.csv', 'w+') as csvFile:
    csvWriter = csv.writer(csvFile);
    csvWriter.writerow(fields);
    csvWriter.writerows(rows);
