from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from time import sleep
import csv
import re
import pandas as pd
import os

infoTagList = ['제목', '기관명', '채용분야', '고용형태', '학력정보', '채용구분', '근무지', '채용인원', '공고기간', '우대조건', '응시자격']
infoValueList = []

year = datetime.today().year
month = datetime.today().month
day = datetime.today().day

# from_date = str(year - 1) + '.' + str(month) + '.' + str(day)
from_date = '2018.01.01'
to_date = str(year) + '.' + str(month) + '.' + str(day)

driver = webdriver.Chrome()
url = 'https://job.alio.go.kr/recruit.do?pageNo=1&idx=&s_date=' + from_date + '&e_date=' + to_date + '&detail_code=R600020&org_type=&org_name=&title=&order=REG_DATE'
driver.get(url)

driver.implicitly_wait(2)

# 페이지 개수 찾기
pageClass = driver.find_element(By.XPATH, '//*[@id="frm"]/div[6]')
pageTags = pageClass.find_elements(By.TAG_NAME, "a")
onclickText = pageTags[len(pageTags) - 1].get_attribute("onclick")
pageCount = int(re.sub(r'[^0-9]', '', onclickText))
# pageCount = 1

# 페이지 개수 만큼 반복
for page in range (1, pageCount+1):
    # 해당 페이지로 이동
    pageUrl = 'https://job.alio.go.kr/recruit.do?pageNo=' + str(page) + '&idx=&s_date=' + from_date + '&e_date=' + to_date + '&detail_code=R600020&org_type=&org_name=&title=&order=REG_DATE'
    driver.get(pageUrl)

    # 매 페이지마다 공고 링크를 기억해두고 순차대로 접근
    postTable = driver.find_element(By.XPATH, '//*[@id="frm"]/table')
    tbody = postTable.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    linkList = []

    for index, value in enumerate(rows):
        # 링크 찾기
        td = value.find_element(By.CLASS_NAME, "left")
        aTag = td.find_element(By.TAG_NAME, "a")
        href = aTag.get_attribute("href")

        linkList.append(href)

    for link in linkList:
        dict = {}

        for element in infoTagList:
            dict[element] = []


        # 링크 접속
        driver.get(link)

        # 정보 찾기
        infoTable = driver.find_element(By.XPATH, '//*[@id="txt"]/table')
        infoTbody = infoTable.find_element(By.TAG_NAME, "tbody")
        infoRows = infoTbody.find_elements(By.TAG_NAME, "tr")
        for index, value in enumerate(infoRows):
            try:
                infoTag = value.find_element(By.TAG_NAME, "th")
                if infoTag:
                    infoTagText = value.find_element(By.TAG_NAME, "th").get_attribute('innerText')

                    # infoTag가 허용하는 값인 경우
                    if infoTagText in infoTagList:
                        # dict[infoTagText] = value.find_element(By.TAG_NAME, "td").get_attribute('innerText')
                        dict[infoTagText].append(value.find_element(By.TAG_NAME, "td").get_attribute('innerText'))
                        # print(infoTagText, dict[infoTagText][len(dict[infoTagText])-1])

            except NoSuchElementException:
                continue

        print('printing... ' + str(page))

        

        # dataframe으로 변환
        data = {
            "sitename" : dict["제목"],
            "url" : str(link),
            "collectiondate" : "",
            "startdate" : "",
            "enddate" : "",
            "companyname" : dict["기관명"],
            "location" : dict["근무지"],
            "recruitfield" : dict["채용분야"],
            "recruittype" : dict["고용형태"],
            "recruitclassification" : dict["채용구분"],
            "personnel" : dict["채용인원"],
            "salary" : "",
            "position" : "",
            "task" : "",
            "qualifications" : dict["응시자격"],
            "prefer" : dict["우대조건"],
            "welfare" : "",
            "description" : "",
            "stacks" : ""
        }

        df = pd.DataFrame(data)
        js = df.to_json(force_ascii=False)
        print(js)

        # csv로 추출
        if not os.path.exists('output.csv'):
            df.to_csv('output.csv', index=False, mode='w', encoding='utf-8-sig')
        else:
            df.to_csv('output.csv', index=False, mode='a', encoding='utf-8-sig', header=False)