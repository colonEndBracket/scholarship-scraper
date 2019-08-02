#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import csv
import os

'''
<table class = "scholarshiplistdirectory">
<ul id="ullist">
'''

base_url = 'https://www.scholarships.com'
directory_url = "https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory"

#Crawl the website
targets = [base_url]
seen_targets = set(targets)
scholarships = []

def findTargets(url): #Pulls url's from a page that may contain scholarships
    global targets
    global seen_targets
    page = requests.get(url)
    rawhtml = BeautifulSoup(page.text, "lxml")
    for ul in rawhtml.find_all('ul', id="ullist"): #ul contains li's
         for li in ul.find_all('li'): #li links to schol list
            try:
                a = li.find('a')
                link = base_url+a['href'] #https://base.url/given-by-href
                if link not in seen_targets:
                    seen_targets.add(link)
                    targets.append(link)
                    findTargets(link)
            except TypeError as e:
                     pass
    
    targets = [i for i in targets if i.startswith(directory_url)]



def scrapeSchol(url):
    page = requests.get(url)
    rawhtml = BeautifulSoup(page.text, "lxml")

    #Get list of Scholarship Titles (scholtitle)
    titles = []
    for ele in rawhtml.select('td.scholtitle'):
        titles.append(ele.text)
    #Get list of Scholarship Amounts (scholamt)
    amounts = []
    for ele in rawhtml.select('td.scholamt'):
        amounts.append(ele.text)
    #Get list of Scholarship Due Dates (scholdd)
    duedates = []
    for ele in rawhtml.select('td.scholdd'):
        duedates.append(ele.text)
    #Get list of Scholarship Links
    slinks = []
    for ele in rawhtml.select('td.scholtitle.a[href]'):
        slinks.append(ele.text)

    #Print list of scholarship information as long as information is consistent
    consistent = (len(titles) == len(amounts)) and (len(amounts)==len(duedates)) 
    quantity = len(titles)
    if( consistent ):
        with open('names.csv', 'w') as csvfile:
            fieldnames = ['title', 'amount', 'due date', 'link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(quantity):
                schol = "{} - {} - {}".format(titles[i],amounts[i],duedates[i])
                writer.writerow({'title': titles[i],'amount': amounts[i],'due date': duedates[i],'link': slinks[i]})
                seen_scholarships = set(scholarships)
                if schol not in seen_scholarships:
                    seen_scholarships.add(schol)
                    scholarships.append(schol)

    else:
        print("Error Encountered: Inconsistent quantity of scholarship titles, amounts, and due dates.")


findTargets(directory_url)
for url in targets:
    scrapeSchol(url)
'''
for scholarship in scholarships:
    print(scholarship)
'''
