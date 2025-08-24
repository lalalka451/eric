import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pymysql
import json


def fetch_linkedin_profiles():
    conn = pymysql.connect(
        host='192.168.1.14',
        user='username',
        passwd='password',
        port=3306
    )
    conn.autocommit = True
    crsr = conn.cursor()
    crsr.execute("CREATE DATABASE IF NOT EXISTS HelpYourself")
    crsr.execute("USE HelpYourself")
    crsr.execute('''
        CREATE TABLE IF NOT EXISTS linkedin_profile (
            user_name VARCHAR(255) PRIMARY KEY,
            jobs TEXT,
            education TEXT
        );
    ''')
    crsr.execute("SELECT * FROM linkedin_profile WHERE jobs LIKE '%MAD Mobile Application Development Ltd%'")
    results = crsr.fetchall()
    profiles = []

    for row in results:
        user_profile = {
            "user_name": row[0],
            "jobs": [],
            "education": row[2]
        }
        jobs_raw = re.findall(r'_\$_([\W\S\n]+?)_#_', row[1])
        for job in jobs_raw:
            formatted_job = parse_job_entry(job.strip())
            if formatted_job:
                user_profile["jobs"].append(formatted_job)
        profiles.append(user_profile)

    conn.close()
    return profiles


def parse_job_entry(job_text):
    """
    Parses a single job entry text and returns a structured dictionary.
    """
    try:
        # Split the job entry into sections based on multiple spaces
        sections = re.split(r'\s{2,}', job_text)
        title_company = sections[0].split('·')
        title = title_company[0].strip()
        company = title_company[1].strip() if len(title_company) > 1 else "N/A"

        duration = sections[1].strip() if len(sections) > 1 else "N/A"
        location = sections[2].strip() if len(sections) > 2 else "N/A"
        description = sections[3].strip() if len(sections) > 3 else "N/A"
        skills_section = sections[4].strip() if len(sections) > 4 else ""
        skills = [skill.strip() for skill in skills_section.replace('Skills:', '').split('·')] if skills_section else []

        job_dict = {
            "title": title,
            "company": company,
            "duration": duration,
            "location": location,
            "description": description,
            "skills": skills
        }
        return job_dict
    except Exception as e:
        print(f"Error parsing job entry: {e}")
        return None


def display_profiles(profiles):
    for profile in profiles:
        print(f"## {profile['user_name']}\n")
        for job in profile['jobs']:
            if str(job).__contains__('Mad Mobile Application Development Ltd'):
                print(f"### {job['title']} at {job['company']}")
                print(f"**Duration:** {job['duration']}")
                print(f"**Location:** {job['location']}\n")
                # print(f"**Description:**\n{job['description']}\n")
                # print(f"**Skills:** {', '.join(job['skills'])}\n")
                # print("---\n")
        # break
        # print("\n")


# def save_profiles_to_json(profiles, filename='profiles.json'):
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(profiles, f, ensure_ascii=False, indent=4)
#     print(f"Profiles saved to {filename}")

if __name__ == "__main__":
    profiles = fetch_linkedin_profiles()
    display_profiles(profiles)
    # save_profiles_to_json(profiles)



