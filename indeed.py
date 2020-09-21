import requests
from bs4 import BeautifulSoup
from pagination import get_last_page

LIMIT = 50
URL_INDEED = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}&radius=25"

def extract_jobs(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find("span", {"class": "location"}).string
    job_id = html["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        "link": f"https://kr.indeed.com/viewjob?jk={job_id}"
    }


def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL_INDEED}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        job = extract_jobs(result)
        jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page(URL_INDEED)
  jobs = extract_indeed_jobs(last_page)
  return jobs