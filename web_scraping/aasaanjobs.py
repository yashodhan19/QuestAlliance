import logging
import os
import re
import math
from time import strptime
from bs4 import BeautifulSoup
from kirmi import Kirmi

website_baseurl = 'https://www.aasaanjobs.com'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

scraper = Kirmi(caching=True, cache_path="./aasan_cache.sqlite3")


def get_job_categories(xml_path=None):
    """
    :param xml_path: path to xml with the state and assembly constituency mappings
    :return:
    """
    with open(xml_path) as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    return soup.find_all('job')


def get_number_of_jobs(jobs):
    try:
        number_of_jobs = jobs.find_all("span", string=re.compile("Showing\s+\d+.*jobs"))
        number_of_jobs = re.search('Showing.*of\s+(\d{1,5})\s+jobs', number_of_jobs[0].text).group(1)
        number_of_pages = math.ceil(int(number_of_jobs) / 10)

        return int(number_of_jobs), number_of_pages
    except Exception:
        logger.error("Could not obtain number of pages or jobs")



def get_job_details(job_url):
    soup = scraper.get_soup(website_baseurl + job_url)

    sections = soup.find('div', attrs={'id': 'job-details'})

    job_details = dict()


    # Salary
    job_details['salary_min'] = soup.find_all('span', attrs={'itemprop': 'minValue'})[0].text
    job_details['salary_max'] = soup.find_all('span', attrs={'itemprop': 'maxValue'})[0].text

    # Experience
    job_exp = soup.find('img', attrs={'src': re.compile("https.*icon\-briefcase.*")})
    job_details['experience'] = job_exp.parent.parent.parent.find_all('div')[-1].find('p').text

    # Location
    location = soup.find('img', attrs={'src': re.compile("https.*icon\-pin.*")})
    job_details['location'] = location.parent.parent.parent.find_all('div')[1].find('p').text

    print(job_details)

<<<<<<< HEAD
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
=======
    sections = soup.find('div', attrs={'id': 'job-details'})
    print(sections)




def process_job_url(jobs, job_category, number_of_pages):
    # get job details

    job_urls = jobs.find_all('div', attrs={'data-job-url': re.compile("\/job\/.*")})

    for j in job_urls:
        job_url = j['data-job-url']
        get_job_details(job_url)

        if number_of_pages >= 2:
            for i in range(2, number_of_pages + 1):
                print(website_baseurl + job_category["url"] + "?page={}".format(i))

                jobs = scraper.get_soup(website_baseurl + job_category["url"] + "?page=" + str(i))
                job_urls = jobs.find_all('div', attrs={'data-job-url': re.compile("\/job\/.*")})

                for j in job_urls:
                    job_url = j['data-job-url']
                    get_job_details(job_url)







# jobs =[]
# job_details= dict()
# # job container
# for j in job_urls:
#     job_url = j['data-job-url']
#     job_page = kirmi.get_soup(website_baseurl + job_url)
#
#     # Salary
#     job_details['salary_min'] = job_page.find_all('span', attrs={'itemprop': 'minValue'})[0].text
#     job_details['salary_max'] = job_page.find_all('span', attrs={'itemprop': 'maxValue'})[0].text
#
#     # Experience
#     job_exp = job_page.find('img', attrs={'src': re.compile("https.*icon\-briefcase.*")})
#     job_details['experience'] = job_exp.parent.parent.parent.find_all('div')[-1].find('p').text
#
#     location = job_page.find('img', attrs={'src': re.compile("https.*icon\-pin.*")})
#     job_details['location'] = location.parent.parent.parent.find_all('div')[1].find('p').text
#
#     # ---------------------
#
#     # Additional Details
#
#     sections = job_page.find('div', attrs={'id': 'job-details'})
#
#     for s in sections:
#         col = s.find_all('div')[0]
#         print(col.find('div', attrs={'class': 'row'}))
#
#     print(sections)
#     import pdb
#     pdb.set_trace()
#
#
def run_process():
    job_categories = get_job_categories(
        xml_path='/Users/yashodhanjoglekar/QuestAlliance/web_scraping/job_categories.xml')

    for job_category in job_categories:
        jobs = scraper.get_soup(website_baseurl + job_category["url"])
        logger.debug("Getting job list for {}".format(job_category["category"]))

        # Identify the number of jobs and pages
        number_of_jobs, number_of_pages = get_number_of_jobs(jobs)

        process_job_url(jobs, job_category, number_of_pages)




            # job_page = scraper.get_soup(website_baseurl + job_url)



            # # Salary
            # job_details['salary_min'] = job_page.find_all('span', attrs={'itemprop': 'minValue'})[0].text
            # job_details['salary_max'] = job_page.find_all('span', attrs={'itemprop': 'maxValue'})[0].text
            #
            # # Experience
            # job_exp = job_page.find('img', attrs={'src': re.compile("https.*icon\-briefcase.*")})
            # job_details['experience'] = job_exp.parent.parent.parent.find_all('div')[-1].find('p').text
            #
            # location = job_page.find('img', attrs={'src': re.compile("https.*icon\-pin.*")})
            # job_details['location'] = location.parent.parent.parent.find_all('div')[1].find('p').text
            #
            # # ---------------------
            #
            # # Additional Details
            #
            # sections = job_page.find('div', attrs={'id': 'job-details'})
            #
            # for s in sections:
            #     col = s.find_all('div')[0]
            #     print(col.find('div', attrs={'class': 'row'}))
            #
            # print(sections)

#
#
#
#
if __name__ == "__main__":

    run_process()

>>>>>>> 0ae76dd225c208788854399c04273d352ac0e28a

