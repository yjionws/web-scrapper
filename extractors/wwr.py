from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    response = get(f"{base_url}{keyword}")

    if response.status_code != 200:          # 200이면 페이지 접근 정상
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, 'html.parser') # html 불러와서 멋진수프로 파이썬 변환
        jobs = soup.find_all('section', class_='jobs')    # class만 쓰면 파이썬 언어와 겹쳐서 언더바 처리
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                link = anchor['href']
                company, kind, region = anchor.find_all('span', class_='company')
                title = anchor.find('span', class_='title')
                job_data = {
                    'link': f"https://weworkremotely.com/{link}",
                    'company': company.string.replace(","," "),
                    'location': region.string.replace(","," "),
                    'position': title.string.replace(","," ")
                 }
                results.append(job_data)
        return results
    


