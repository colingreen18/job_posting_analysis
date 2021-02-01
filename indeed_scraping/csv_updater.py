import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def main():
    """
    Entrypoint into program.
    """
    searches = ['data intern', 'data analyst', 'data science', 'machine learning', 'data student', 'junior analyst']
    range = 14
    radius = 100
    urls = create_urls('toronto', searches, range=range, province='BC', radius=radius)
    soups = get_pages(urls)
    job_titles = extract_job_title_from_result(soups)
    companies = extract_company_from_result(soups)
    locations = extract_location_from_result(soups)
    old_df = pd.read_csv('job_postings.csv')
    href = extract_job_href_from_result(soups)
    descriptions = []
    full_pages = get_pages(href)
    descriptions = get_job_description(full_pages)
    df = check_for_duplicates(job_titles, companies, locations, href, old_df, descriptions)
    save_results(df)


def create_urls(location, searches, radius=100, province='ON', range=14):
    """create a list of urls for multiple searches"""
    print('creating urls')
    urls_list = []
    for search in searches:
        search = search.split(" ")
        search = '+'.join(search)
        url = 'https://ca.indeed.com/jobs?q=' + search
        url = url + '&l=' + location + '%2C+' + province
        url = url + '&radius=' + str(radius) + '&sort=date'
        url = url + '&fromage=' + str(range) + '&filter=0'
        for i in [0, 10, 20, 30]:
            url = url + '&start=' + str(i)
            urls_list.append(url)
    return urls_list


def get_pages(urls):
    """get the page data for each search"""
    print('getting pages')
    pages = []
    for url in urls:
        pages.append(requests.get(url))
        time.sleep(2)
        if len(pages) % 5 == 0:
            print(f'{len(pages)} pages found')
    soups = [BeautifulSoup(page.text, 'html.parser') for page in pages]
    return soups


def extract_job_title_from_result(soups):
    print('getting job titles')
    jobs = []
    for soup in soups:
        for div in soup.find_all(name='div', attrs={'class': 'row'}):
            for a in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
                jobs.append(a['title'])
    return(jobs)


def extract_company_from_result(soups):
    print('getting company names')
    companies = []
    for soup in soups:
        for div in soup.find_all(name='div', attrs={'class': 'row'}):
            company = div.find_all(name='span', attrs={'class': 'company'})
            if len(company) > 0:
                for b in company:
                    companies.append(b.text.strip())
                else:
                    sec_try = div.find_all(name='span', attrs={'class': 'result-link-source'})
                    for span in sec_try:
                        companies.append(span.text.strip())
    return(companies)


def extract_location_from_result(soups):
    print('getting locations')
    locations = []
    for soup in soups:
        spans = soup.findAll('span', attrs={'class': 'location'})
        for span in spans:
            locations.append(span.text)
    return(locations)


def extract_job_href_from_result(soups):
    print('getting job urls')
    href = []
    for soup in soups:
        for div in soup.find_all(name='div', attrs={'class': 'row'}):
            for a in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
                href.append('https://ca.indeed.com' + str(a['href']))
    return(href)


def get_job_description(full_pages):
    print('getting job descriptions')
    descriptions = []
    for page in full_pages:
        desc = []
        for div in page.find_all(attrs={'class': 'jobsearch-jobDescriptionText'}):
            desc.append(div.contents)
            time.sleep(2)
        descriptions.append(desc)
    return descriptions


def check_for_duplicates(job_titles, companies, locations, href, old_df, descriptions):
    print('removing duplicates')
    columns = ["job_title", "company", "location", "href", 'description', 'apply']
    apply = ['NaN']*len(job_titles)
    df = pd.DataFrame(list(zip(job_titles, companies, locations, href, descriptions, apply)), columns=columns)
    jobs = len(df['job_title'])
    print(f'{jobs} total jobs found')
    df = pd.concat([old_df, df])
    df = df.drop_duplicates(subset=['job_title', 'company'], keep='first')
    jobs = len(df['job_title']) - len(old_df['job_title'])
    print(f'{jobs} new jobs found')
    return df


def save_results(df):
    print('saving results')
    path = 'C:\\Users\\green\Documents\\GitHub\\job_posting_analysis\\indeed_scraping\\'
    df.to_csv(path + "job_postings.csv", index=False)
    return

if __name__ == '__main__':
    main()
