from bs4 import BeautifulSoup
import requests
import csv

countries = [
    'indonesia',
    'vietnam',
    'malaysia',
    'thailand',
    'philippines'
];

def processCountry(country):
    url = 'https://www.citypopulation.de/en/'+country+'/admin/'
    webPage = requests.get(url, timeout=5)
    table = BeautifulSoup(webPage.content, 'html.parser').select('#tl')[0]
    tableBodies = table.findAll('tbody')
    tableBodies.pop(len(tableBodies) - 1)

    divisions = []

    for tableBody in tableBodies:
        tableRows = tableBody.findAll('tr')
        for tableRow in tableRows:
            tableItems = tableRow.findAll('td')
            rowsClasses = tableRow.attrs.get('class') or []

            if 'rname' in rowsClasses:
                divisions.append({'name': tableItems[0].text, 'type': tableItems[1].text, 'subdivision': []})
            else:
                divisions[len(divisions) - 1]['subdivision'].append({'name': tableItems[0].text, 'type': tableItems[1].text})

    fields = ['Level 1', 'Type', 'Level 2', 'Type']
    rows = [];

    for division in divisions:
        for index, subdivision in enumerate(division['subdivision']):
            if index == 0:
                rows.append([division['name'], division['type'], subdivision['name'], subdivision['type'] ])
            else:
                rows.append(['', '', subdivision['name'], subdivision['type']])

    with open('/root/app/csv/'+country+'.csv', 'w+') as csvFile:
        csvWriter = csv.writer(csvFile);
        csvWriter.writerow(fields);
        csvWriter.writerows(rows);


for country in countries:
    processCountry(country)
