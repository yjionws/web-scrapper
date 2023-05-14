from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs

keyword = input("What do you want to search for?")

indeed = extract_indeed_jobs(keyword)
wwr = extract_wwr_jobs(keyword)
jobs = indeed + wwr

file = open(f"{keyword}.csv", "w", encoding="utf-8")
file.write("Position, Company, Location, URL\n")  ## 새 행은 새 줄로 구분하기 위함

for job in jobs:
    file.write(
        f"{job['position']},{job['company']},{job['location']},{job['link']}\n"
        )                                         ## 쌍따옴표 안에는 쌍따옴표를 또 쓸 수 없음. 

file.close()





