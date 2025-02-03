import requests
from bs4 import BeautifulSoup

def scrape_glints():
    url = "https://glints.com/id/opportunities/jobs/explore"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    # Sesuaikan selector sesuai struktur website Glints (bisa berubah!)
    for item in soup.select('div[data-test="job-card"]'):
        title = item.select_one('h3.job-title').text.strip()
        company = item.select_one('div.company-name').text.strip()
        location = item.select_one('div.location').text.strip()
        link = item.find('a')['href']
        jobs.append(f"🔹 {title}\n🏢 {company}\n📍 {location}\n🔗 https://glints.com{link}\n")
    
    return jobs[:5]  # Ambil 5 lowongan pertama