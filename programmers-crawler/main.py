from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from extractors.programmers import extract_programmers_jobs
import numpy
import pandas as pd

"""
#we work remotely > wwr.csv
keyword = "python"

wwr = extract_wwr_jobs(keyword)

#Create file
file_name_for_wwr = "wwr"
file = open(f"{keyword}.csv", "w", encoding="utf-8")
file.write("position, company, kind, region, url\n")

for job in wwr:
    file.write(f"{job['position']},{job['company']},{job['kind']},{job['kind']},{job['region']},{job['url']}\n")
    
file.close()
"""

#programmers > programmers.csv
page_num = 1
programmers = extract_programmers_jobs(page_num) # list

"""
file_name_for_programmers = "programmers"
with open(f"{file_name_for_programmers}_{page_num}.csv", "w", encoding='utf-8') as file:
    #header 작성하기
    #file.write("name, response_speed, company_link, company_name, position, end_date, job_type, experience, salary, location, tech_stacks\n")

    for job in programmers:
        file.write(f"{job['site_name']}, {job['url']}, {job['collection_date']}, {job['start_date']}, {job['end_date']}, {job['company_name']}, {job['location']}, {job['recruit_field']}, {job['recruit_type']}, {job['recruit_classification']}, {job['personnel']}, {job['salary']}, {job['position']}, {job['task']}, {job['qualification']}, {job['prefer']}, {job['welfare']}, {job['description']}, {job['stacks']}\n")
"""
#list -> DataFrame
df = pd.DataFrame.from_dict(programmers)
df.to_csv(f"programmers_{page_num}.csv", sep=',', header=False)

#DataFrame -> json
df_json = df.to_json(f"programmers_{page_num}.json")
