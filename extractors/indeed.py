from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_page_count(keyword):
  browser = webdriver.Chrome()                                ## 셀레미늄으로 브라우저 요청
  base_url = "https://kr.indeed.com/jobs?q="
  browser.get(f"{base_url}{keyword}")
  soup = BeautifulSoup(browser.page_source, "html.parser")    ## 페이지 코드 불러오기
  navigation = soup.find("nav", {"aria-label":"pagination"})  ## 페이지 넘버 리스트 녀석 찾기
  if navigation == None:                                      ## 없으면 1로 처리
     return 1
  pages = navigation.find_all("div", recursive=False)         ## 있으면 div 태그로 구성된 페이지수 세기
  count = len(pages)
  if count >= 5:
     return 5
  else:
     return count


def extract_indeed_jobs(keyword):
  pages = get_page_count(keyword) # 위 코드에서 구한 페이지수 얻기
  print("found", pages, "pages")
  results = []                    # 최종 job 데이터를 담을 리스트 생성
  for page in range(pages):       # 0~n개의 페이지를 모두 조회하도록 for 루프 함수 처리
   browser = webdriver.Chrome()
   base_url = "https://kr.indeed.com/jobs"
   final_url = f"{base_url}?q={keyword}&start={page*10}"  # 페이지 고유 번호 확인하여 삽입
   print("Requesting", final_url)
   browser.get(final_url)

   soup = BeautifulSoup(browser.page_source, "html.parser")  # job 정보 쓸어담기 시작
   job_list = soup.find("ul", class_="jobsearch-ResultsList")
   jobs = job_list.find_all('li', recursive=False)           # 최상단에 있는 li만 뽑기
   for job in jobs:
         zone = job.find("div", class_="mosaic-zone")
         if zone ==None:                                     # 직무정보 아닌 건 제외
            anchor = job.select_one("h2 a")
            title = anchor['aria-label']
            link = anchor['href']
            company = job.find("span", class_="companyName")
            location = job.find("div", class_="companyLocation")
            job_data = {
               'link': f"https://kr.indeed.com{link}",
               'company': company.string.replace(","," "),
               'location': location.string.replace(","," "),
               'position': title.replace(","," ")                               
            }
            results.append(job_data)                          # job 정보 어팬드 해주기
  return results                                              # 리턴으로 데이터 반환해주고 종료

