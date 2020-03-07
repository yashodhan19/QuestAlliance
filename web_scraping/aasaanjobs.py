import logging
import os
import re
from time import strptime

from kirmi import Kirmi

website_baseurl = 'https://www.aasaanjobs.com'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

kirmi = Kirmi(caching=True, cache_path="./bulletin_cache.sqlite3")

cc_jobs = kirmi.get_soup('https://www.aasaanjobs.com/s/customer-care-jobs/')


job_urls = cc_jobs.find_all('div', attrs={'data-job-url': re.compile("\/job\/.*")})

jobs =[]
job_details= dict()
# job container
for j in job_urls:
    job_url = j['data-job-url']
    job_page = kirmi.get_soup(website_baseurl + job_url)

    # Salary
    job_details['salary_min'] = job_page.find_all('span', attrs={'itemprop': 'minValue'})[0].text
    job_details['salary_max'] = job_page.find_all('span', attrs={'itemprop': 'maxValue'})[0].text

    # Experience
    job_exp = job_page.find('img', attrs={'src': re.compile("https.*icon\-briefcase.*")})
    job_details['experience'] = job_exp.parent.parent.parent.find_all('div')[-1].find('p').text

    location = job_page.find('img', attrs={'src': re.compile("https.*icon\-pin.*")})
    job_details['location'] = location.parent.parent.parent.find_all('div')[1].find('p').text

    # ---------------------

    # Additional Details

    sections = job_page.find('div', attrs={'id': 'job-details'})

    for s in sections:
        col = s.find_all('div')[0]
        print(col.find('div', attrs={'class': 'row'}))

    print(sections)
    import pdb
    pdb.set_trace()


