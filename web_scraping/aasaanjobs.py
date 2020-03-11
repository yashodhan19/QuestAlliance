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

    '''
    Below is the hierarchy / structure (this structure is below the "Apply CV" button)

    - #job-details
        - .row
            - .col-xs-12
                - .col-xs-12
                    - .row
                        - 

    '''
    sections = job_page.find('div', attrs={'id': 'job-details'})

    for s in sections:
        divs = s.find_all('div')
        print(divs.find('div', attrs={'class': 'row'}))
        
        import pdb
        pdb.set_trace()

        # divs[0] = salary, experience, location etc.

        
        # Additional Details
        '''
        divs[1]
            -> div.col-xs-12
                -> div.col-xs-12/col.md-12...
                    -> div.row
                        -> 2nd div (value)
                            -> p.text()
        '''


        
        # Job Requirements
        '''
        divs[2]
            -> div.col-xs-12
                -> div.col-xs-12/col.md-12...
                    -> div.row
                        -> 2nd div (under the title div)
                            -> loop through every div.row
                                -> 2nd div (value)
                                    -> directly find `<p>`.text()
        '''


        # Job Description
        '''
        divs[3]
            -> div.col-xs-12
                -> div.col-xs-12/col.md-12...
                    -> div.row
                        -> 2nd div (under the title div)
                            -> directly find `<p>`.text()
        '''

