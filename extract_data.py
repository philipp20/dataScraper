import requests
from bs4 import BeautifulSoup
import pandas as pd

# Open the local HTML file
with open("HiringCafe.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find all job containers
job_divs = soup.find_all("div", class_="relative xl:z-10")

# Text to be displayed for unavailable data
data_unavailable_text = "<Data Unavailable>"

data = []
for div in job_divs:
    title_div = div.find("div", class_="mt-1 mr-10")
    title_span = title_div.find("span")
    location_div = div.find("div", class_="mt-1 flex items-center space-x-1 rounded text-xs px-1 font-medium border bg-gray-50 w-fit text-gray-700")
    location_span = location_div.find("span", class_="line-clamp-2")
    other_details_div = div.find("div", class_="flex flex-wrap gap-1.5 mt-2 w-full")
    more_details_div = div.find("div", class_="flex flex-col mt-4 mb-2 space-y-2.5 text-sm w-full")
    company_span = more_details_div.find("span", class_="line-clamp-3 font-light")
    qualifications_div = div.find("div", class_="flex space-x-1 w-full")
    qualifications_span = qualifications_div.find("span", class_="line-clamp-5 font-light")
    tools_div = div.find("div", class_="flex space-x-1")

    if title_span:
        title = title_span.get_text(strip=True) if title_span else data_unavailable_text
        location = location_span.get_text(strip=True) if location_span else data_unavailable_text
        company = company_span.get_text(strip=True) if company_span else data_unavailable_text
        qualifications = qualifications_span.get_text(strip=True) if qualifications_span else data_unavailable_text
        tools = tools_div.get_text(strip=True) if tools_div else data_unavailable_text
        salary = ""
        work_setup = ""
        job_type = ""

        if other_details_div:
            others_spans = other_details_div.find_all("span")
            others_count = len(others_spans)

            # some listings don't have the salary data
            if others_count > 2:
                salary = others_spans[0].get_text(strip=True) if others_spans[0] else data_unavailable_text
                work_setup = others_spans[1].get_text(strip=True) if others_spans[1] else data_unavailable_text
                job_type = others_spans[2].get_text(strip=True) if others_spans[2] else data_unavailable_text
            else:
                salary = data_unavailable_text
                work_setup = others_spans[0].get_text(strip=True) if others_spans[0] else data_unavailable_text
                job_type = others_spans[1].get_text(strip=True) if others_spans[1] else data_unavailable_text

        data.append({"Job Title": title, "Salary": salary, "Location": location, "Work Setup": work_setup,
                     "Job Type": job_type, "Company Name": company, "Qualifications": qualifications, "Tools": tools})

# Convert to DataFrame
df = pd.DataFrame(data)

# Display and save results
print(df)
df.to_csv("hiringcafe_job_listings.csv", index=False, encoding="utf-8")
print("✅ Saved to hiringcafe_job_listings.csv")
