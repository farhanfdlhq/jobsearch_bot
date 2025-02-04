import requests
from bs4 import BeautifulSoup

def scrape_glints():
    url = "https://glints.com/id/lowongan-kerja"  # URL halaman Glints
    response = requests.get(url)
    
    if response.status_code != 200:
        return ["⚠️ Tidak bisa mengambil data dari Glints."]
    
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []
    
    # Contoh mengambil data job list
    for job in soup.find_all("div", class_="JobCard_classname__placeholder-class", limit=10):  # Sesuaikan class
        title = job.find("h3").text.strip() if job.find("h3") else "No Title"
        link = job.find("a", href=True)["href"] if job.find("a", href=True) else "#"
        jobs.append(f"{title}\n🔗 {link}")
    
    return jobs if jobs else ["Tidak ada lowongan terbaru."]
