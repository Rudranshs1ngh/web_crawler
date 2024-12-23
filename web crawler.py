import requests
from bs4 import BeautifulSoup
import time
import random
import csv

HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
]


def get_soup(url):
    """
    Sends an HTTP GET request to url, returns a BeautifulSoup object.
    """
    headers = random.choice(HEADERS_LIST)

    # Increase sleep time to avoid rate limiting
    time.sleep(random.uniform(5, 10))

    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"Error: Received status code {
                  response.status_code} for {url}")
            return None
    except Exception as e:
        print(f"Error accessing {url}: {str(e)}")
        return None


def extract_profile_info(soup):
    """
    Extracts user Name, Job Title, Location, and About/Summary 
    from a public profile's BeautifulSoup object (if available).
    """
    profile_data = {}

    # The following selectors are purely illustrative.
    # Real LinkedIn public pages can have dynamic or hidden selectors.
    name_tag = soup.find("h1", {"class": "top-card-layout__title"})
    job_title_tag = soup.find("div", {"class": "top-card-layout__headline"})
    location_tag = soup.find("span", {"class": "top-card__subline-item"})
    summary_tag = soup.find("section", {"class": "summary"})

    profile_data["name"] = name_tag.get_text(strip=True) if name_tag else None
    profile_data["job_title"] = (
        job_title_tag.get_text(strip=True) if job_title_tag else None
    )
    profile_data["location"] = (
        location_tag.get_text(strip=True) if location_tag else None
    )
    profile_data["summary"] = (
        summary_tag.get_text(strip=True) if summary_tag else None
    )

    return profile_data


def extract_company_info(soup):
    """
    Extracts Company Name, Industry, Headquarters Location, 
    and Overview/About from a public company page's BeautifulSoup object (if available).
    """
    company_data = {}

    # Again, these selectors are illustrative; actual LinkedIn might differ.
    company_name_tag = soup.find(
        "h1", {"class": "org-top-card-summary__title"})
    industry_tag = soup.find(
        "div", {"class": "org-top-card-summary__industry"})
    headquarters_tag = soup.find(
        "div", {"class": "org-top-card-summary__headquarters"}
    )
    overview_tag = soup.find(
        "section", {"class": "org-about-company-module__description"})

    company_data["company_name"] = (
        company_name_tag.get_text(strip=True) if company_name_tag else None
    )
    company_data["industry"] = (
        industry_tag.get_text(strip=True) if industry_tag else None
    )
    company_data["headquarters"] = (
        headquarters_tag.get_text(strip=True) if headquarters_tag else None
    )
    company_data["overview"] = (
        overview_tag.get_text(strip=True) if overview_tag else None
    )

    return company_data


def crawl_linkedin_pages(urls, output_file="linkedin_data.csv"):
    """
    Given a list of LinkedIn public URLs, attempts to scrape profile or company data
    and writes it to a CSV. This is just a minimal example.
    """
    fieldnames = [
        "url",
        "type",
        "name",
        "job_title",
        "location",
        "summary",
        "company_name",
        "industry",
        "headquarters",
        "overview",
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for url in urls:
            soup = get_soup(url)
            if not soup:
                continue

            # Simplistic check to decide if it's a "profile" or "company" page
            if "linkedin.com/in/" in url:
                # likely a personal profile
                data = extract_profile_info(soup)
                data["type"] = "profile"
            else:
                # likely a company page
                data = extract_company_info(soup)
                data["type"] = "company"

            data["url"] = url
            writer.writerow(data)
            print(f"Scraped data for: {url}")


if name == "main":
    # Example usage
    sample_urls = [
        # Replace with valid LinkedIn public profile or company URLs (if permitted)
        "https://www.linkedin.com/in/gaurav-chitwaan-4a6579166/",
        "https://www.linkedin.com/company/ernstandyoung",
    ]
    crawl_linkedin_pages(sample_urls)