from bs4 import BeautifulSoup
import requests
import csv

baseUrl = 'https://www.philatlas.com';
urlRegions = baseUrl+'/regions.html';

web = requests.get(urlRegions, timeout=5);

regionTable = BeautifulSoup(web.content, 'html.parser').select('#lguTable')[0]

regionTableRows = regionTable.findAll('tbody')[0].findAll('tr')

regions = [];


def processRegion(region, regionIndex):
    regionWeb = requests.get(region['url'], timeout=5);
    provincesTable = BeautifulSoup(regionWeb.content, 'html.parser').select('#lguTable')[0];

    provincesTableRows = provincesTable.findAll('tbody')[0].findAll('tr');
    for provincesTableRow in provincesTableRows:
        element = provincesTableRow.findAll('a')[0];
        regions[regionIndex]['provinces'].append(element.text)


for row in regionTableRows:
    element = row.findAll('a')[0];

    regionUrl = baseUrl + '/' + element['href'];
    regionName = element.text;

    regions.append({'url': regionUrl, 'name': regionName, 'provinces': []})

for regionIndex, region in enumerate(regions):
    processRegion(region, regionIndex);

fields = ['Level 1', 'Type', 'Level 2', 'Type']
rows = [];

for region in regions:
    for provinceIndex, province in enumerate(region['provinces']):
        if provinceIndex == 0:
            rows.append([region['name'], 'Region', province, 'Province' ])
        else:
            rows.append(['', '', province, 'Province'])

with open('/root/app/csv/philippine.csv', 'w+') as csvFile:
    csvWriter = csv.writer(csvFile);
    csvWriter.writerow(fields);
    csvWriter.writerows(rows);
