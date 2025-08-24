import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pymysql



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
            CREATE TABLE IF NOT EXISTS  HelpYourself.linkedin_profile (
                    user_name  VARCHAR(255) PRIMARY KEY,
                    jobs TEXT,
                    education TEXT
                );
                ''')

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--proxy-server=127.0.0.1:10809')

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)



# Navigate to LinkedIn login page
driver.get('https://www.linkedin.com/')

# Add cookies
cookies = [
    {"name": "_gcl_au", "value": "1.1.1721707426.1727171750", "domain": ".linkedin.com"},
    {"name": "aam_uuid", "value": "07868016791971602070784486213911446024", "domain": ".linkedin.com"},
    {"name": "AMCV_14215E3D5995C57C0A495C55%40AdobeOrg", "value": "-637568504%7CMCIDTS%7C20028%7CMCMID%7C07308242556923865000732997340730814915%7CMCAAMLH-1730984241%7C3%7CMCAAMB-1730984241%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1730386641s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C-936160148", "domain": ".linkedin.com"},
    {"name": "AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg", "value": "1", "domain": ".linkedin.com"},
    {"name": "AnalyticsSyncHistory", "value": "AQJN8EhLaTX-xwAAAZJ1BX0pVi_U31av-ZbhFPtb9y3x_ZGIu74f1nfzf9DGdBmYaGChEFGsVaDjFhFs2mGzgQ", "domain": ".linkedin.com"},
    {"name": "bcookie", "value": "\"v=2&f90622b7-0467-43d8-881e-afb0c35d38d3\"", "domain": ".linkedin.com"},
    {"name": "bscookie", "value": "\"v=1&20240923091315177f2631-1386-42cb-866e-854131598e98AQGkJv09cJJ4A0g9l4eZVSDOhdM9JYQV\"", "domain": ".www.linkedin.com"},
    {"name": "li_at", "value": "AQEDATZUEIYCF5UMAAABksgnb78AAAGS7DPzv1YA0eftZL6D3d0u1rHWnqQMWqwlwxpiITC1cOv48pl91loV12TTuH6pSkpf6wdn_-FbpI9ho8xgd1zKwlQ9GK-EX3SxTFinoqJujwvIIRRsBnGWqPPM", "domain": ".www.linkedin.com"},
    {"name": "liap", "value": "true", "domain": ".linkedin.com"},
    {"name": "li_theme", "value": "light", "domain": ".www.linkedin.com"},
    {"name": "li_theme_set", "value": "app", "domain": ".www.linkedin.com"},
    {"name": "timezone", "value": "Asia/Shanghai", "domain": ".www.linkedin.com"},
]

for cookie in cookies:
    driver.add_cookie(cookie)

linkedin_profiles = '''
https://www.linkedin.com/in/pui-yu-kwok-050340180?trk=people-search-result https://www.linkedin.com/in/mangowong?trk=people-search-result https://www.linkedin.com/in/hazel-tong-uxuidesigner?trk=people-search-result https://www.linkedin.com/in/eching0519?trk=people-search-result https://www.linkedin.com/in/chau-wing-mok-540163320?trk=people-search-result https://www.linkedin.com/in/yipeng-wu-47aa20238?trk=people-search-result https://www.linkedin.com/in/shikhachaurasiya?trk=people-search-result https://www.linkedin.com/in/asliaktas?trk=people-search-result https://www.linkedin.com/in/aidan-pastel?trk=people-search-result https://www.linkedin.com/in/khotso-pakkies-8974b9196?trk=people-search-result https://www.linkedin.com/in/adebsalert?trk=people-search-result https://www.linkedin.com/in/gary-baughman-0930841?trk=people-search-result https://www.linkedin.com/in/buyelwa-gxido-72b957161?trk=people-search-result https://www.linkedin.com/in/josh-chepiri-329786127?trk=people-search-result https://www.linkedin.com/in/francois-grogor-50853168?trk=people-search-result https://www.linkedin.com/in/twasanta-seleti-bab88248?trk=people-search-result https://www.linkedin.com/in/derecklhw?trk=people-search-result https://www.linkedin.com/in/asandaj2387?trk=people-search-result https://www.linkedin.com/in/rowanwalkercampbell?trk=people-search-result https://www.linkedin.com/in/karolkonwerski?trk=people-search-result
'''
usernames = re.findall(r'https://www\.linkedin\.com/in/([^?]+)', linkedin_profiles)

for user_name in usernames:
    # Check if user already exists
    check_sql = "SELECT user_name FROM linkedin_profile WHERE user_name = %s"
    crsr.execute(check_sql, (user_name,))
    if crsr.fetchone():
        print(f"User {user_name} already exists, skipping...")
        continue


    # Navigate to the desired LinkedIn profile
    driver.get(f'https://www.linkedin.com/in/{user_name}/details/experience/')
    jobs_text = []

    time.sleep(2)

    experience_elements = driver.execute_script("""
        return Array.from(document.querySelectorAll('div > div > div > div > div:nth-child(2) > div > div > main > section > div:nth-child(2) > div > div:nth-child(1) > ul > li > div > div'))
            .map(element => element.textContent);
    """)


    # Print each experience
    for experience in experience_elements:
        print(experience)
        jobs_text.append('_$_'+experience+'_#_')



    # Navigate to education page
    driver.get(f'https://www.linkedin.com/in/{user_name}/details/education/')

    time.sleep(2)

    education_text = []
    education_elements_js = driver.execute_script("""
        return Array.from(document.querySelectorAll('div > div > div > div > div:nth-child(2) > div > div > main > section > div:nth-child(2) > div > div:nth-child(1) > ul > li > div > div'))
            .map(element => element.textContent);
    """)

    for education in education_elements_js:
        print(education)
        education_text.append('_$_'+education+'_#_')

    # Insert data into database
    try:
        sql = "INSERT INTO linkedin_profile (user_name, jobs, education) VALUES (%s, %s, %s)"
        values = (user_name, '\n'.join(jobs_text), '\n'.join(education_text))
        crsr.execute(sql, values)
        conn.commit()
        print(f"Successfully inserted data for {user_name}")
    except pymysql.Error as e:
        print(f"Error inserting data for {user_name}: {e}")

# Close database connection
conn.close()



# Close the browser
driver.quit()