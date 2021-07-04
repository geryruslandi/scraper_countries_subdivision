from bs4 import BeautifulSoup
import requests
import csv

url = 'https://www.citypopulation.de/en/malaysia/admin/'
webPage = requests.get(url, timeout=5)
table = BeautifulSoup(webPage.content, 'html.parser').select('#tl')[0]

tableBodies = table.findAll('tbody')

states = []

for tableBody in tableBodies:
    tableRows = tableBody.findAll('tr')
    for tableRow in tableRows:
        tableItems = tableRow.findAll('td')
        rowsClasses = tableRow.attrs.get('class') or []

        if 'rname' in rowsClasses:
            states.append({'name': tableItems[0].text, 'type': tableItems[1].text, 'subdivision': []})
        else:
            states[len(states) - 1]['subdivision'].append({'name': tableItems[0].text, 'type': tableItems[1].text})

fields = ['Level 1', 'Type', 'Level 2', 'Type']
rows = [];

for state in states:
    for index, subdivision in enumerate(state['subdivision']):
        if index == 0:
            rows.append([state['name'], state['type'], subdivision['name'], subdivision['type'] ])
        else:
            rows.append(['', '', subdivision['name'], subdivision['type']])

with open('/root/app/csv/malaysia.csv', 'w+') as csvFile:
    csvWriter = csv.writer(csvFile);
    csvWriter.writerow(fields);
    csvWriter.writerows(rows);
