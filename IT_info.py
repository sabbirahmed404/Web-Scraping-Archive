import requests
from bs4 import BeautifulSoup
import pandas as pd
# Function to fetch and parse a single page
def fetch_jobs_from_page(page_number):
    base_url = 'https://jobs.bdjobs.com/jobsearch.asp'
    params = {
        'txtsearch': '',
        'fcat': 8,
        'qOT': 0,
        'iCat': 0,
        'Country': 0,
        'qPosted': 0,
        'qDeadline': 0,
        'Newspaper': 0,
        'qJobNature': 0,
        'qJobLevel': 0,
        'qExp': 0,
        'qAge': 0,
        'hidOrder': "''",
        'pg': page_number,
        'rpp': 100,
        'hidJobSearch': 'JobSearch',
        'MPostings': '',
        'ver': '',
        'strFlid_fvalue': '',
        'strFilterName': '',
        'hClickLog': 1,
        'hPopUpVal': 1,
        'rc1': 1,
        'userfiltername1': '',
        'userfiltername': '',
        'hUserfiltername': 0
    }
    response = requests.get(base_url, params=params)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    return soup

# Initialize the dictionary to store job details
job_details = {
    "Title": [],
    "Company Name": [],
    "Promotion Text": [],
    "Location": [],
    "Experience Required": []
}

# Number of pages to scrape
num_pages = 4

# Loop through each page and extract job details
for page in range(1, num_pages + 1):
    soup = fetch_jobs_from_page(page)
    
    # Find all job postings with the specified classes
    job_postings = soup.find_all('div', class_=['norm-jobs-wrapper', 'sout-jobs-wrapper'])
    
    # Debug: Print the number of job postings found on the current page
    print(f"Page {page}: Found {len(job_postings)} job postings")
    
    for job in job_postings:
        # Extract the job title
        title = job.find('div', class_='job-title-text')
        job_details["Title"].append(title.get_text(strip=True) if title else 'N/A')
        
        # Extract the company name
        company_name = job.find('div', class_='comp-name-text')
        job_details["Company Name"].append(company_name.get_text(strip=True) if company_name else 'N/A')
        
        # Extract the promotion text (if available)
        promo_text = job.find('div', class_='promo-text')
        job_details["Promotion Text"].append(promo_text.get_text(strip=True) if promo_text else 'N/A')
        
        # Extract the location
        location = job.find('div', class_='locon-text-d')
        job_details["Location"].append(location.get_text(strip=True) if location else 'N/A')
        
        # Extract the experience required
        exp_required = job.find('div', class_='exp-text-d')
        job_details["Experience Required"].append(exp_required.get_text(strip=True) if exp_required else 'N/A')
    
    # Debug: Print the number of titles collected so far
    print(f"Page {page}: Collected {len(job_details['Title'])} job titles so far")

# Convert the dictionary to a pandas DataFrame
job_df = pd.DataFrame(job_details)

# Display the DataFrame
print(job_df)
