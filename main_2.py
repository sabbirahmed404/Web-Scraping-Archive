from bs4 import BeautifulSoup
import requests
import time

print('Put some skill that youre not familiar with')
unfamiliar_skills = input('>')
print(f'Filtering Out {unfamiliar_skills}')

def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
    for job in jobs:
        published_date = job.find('span', class_='sim-posted').text
        if 'few' in published_date:
            company_name = job.find('h3',class_='joblist-comp-name').text.replace(' ','')
            skills = job.find('span', class_='srp-skills').text.replace(' ', '')
            more_info = job.header.h2.a['href']
            if unfamiliar_skills not in skills:
                print(f"Company Name: {company_name.strip()}")
                print(f"Required Skills: {skills.strip()}")
                print(f"Posted Date: {published_date.strip()}")
                print(f"More Info : {more_info}")
                print('')
                

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 30
        print(f'Waiting {time_wait} seconds...')
        time.sleep(time_wait)
        