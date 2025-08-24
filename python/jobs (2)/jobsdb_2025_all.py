import time

import requests
import re
import json
import pymysql

from jobsdb_constrant import get_jobsdb_headers, get_session_id, get_jobsdb_headers_with_session

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
            CREATE TABLE IF NOT EXISTS  HelpYourself.jobsdb2024all (
                    job_id  VARCHAR(255) PRIMARY KEY,
                    job_title TEXT,
                    job_url TEXT,
                    company TEXT,
                    job_function TEXT,
                    job_type TEXT,
                    industry TEXT,
                    career_level TEXT,
                    years_of_experience TEXT,
                    qualification TEXT,
                    benefits TEXT,
                    description TEXT,
                    postDate TEXT,
                    location TEXT,
                    question TEXT,
                    search_type TEXT
                );
                ''')

# Define the URL for the request


query = "frontend"


def fetch_data(url):
    """Fetches data from the given URL and returns the response content."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


url = "https://imperialb.in/r/ywkbzmxe"
data = fetch_data(url)
import random

http_proxies = ["127.0.0.1:" + port for port in data.split("\n") if port]  # Filter out empty strings


def get_random_proxy():
    # """Returns a dictionary with a random proxy from http_proxies or a default proxy if the list is empty."""
    # if http_proxies:
    #     proxy = random.choice(http_proxies)
    #     return {'http': proxy}
    # else:
    # return {'http': '127.0.0.1:10809'}  # Default proxy if http_proxies is empty
    proxy_host = "107.173.3.55"
    proxy_port = "51422"
    proxy_url = f"http://{proxy_host}:{proxy_port}"
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    return proxies

def find_job_id():
    """Fetches job IDs from the API using the query as keywords parameter."""
    page = 1
    max_pages = 100  # Safety limit
    max_retries = 9999  # Number of retries for database connection errors

    while page <= max_pages:
        try:
            # Construct the API URL with proper parameters
            url = f'https://hk.jobsdb.com/api/jobsearch/v5/search?siteKey=HK-Main&page={page}&pageSize=100'
            # print(f"Fetching page {page} for query '{query}'")
            print(url)

            # Make the request
            response = requests.get(url, headers=get_jobsdb_headers(), proxies=get_random_proxy())

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                response_data = response.json()

                # Extract jobs from the data array
                jobs = response_data.get('data', [])

                # If no jobs in this page, we've reached the end - move to next query
                if not jobs:
                    print(f"No more jobs found for '{query}'. Moving to next query.")
                    break
                print('finded jobs', len(jobs))
                # Process each job
                for job in jobs:
                    job_id = job.get('id')
                    job_title = job.get('title', "")
                    company_name = job.get("companyName")
                    if not company_name:
                        advertiser = job.get("advertiser", {})
                        company_name = advertiser.get("description", "")
                    print(job_id, job_title, company_name)

                    # Handle MySQL connection errors with retries
                    retry_count = 0
                    while retry_count < max_retries:
                        try:
                            if job_id and not check_job_exists(job_id):
                                print(f"Processing Job ID: {job_id}")
                                find_job_detail(job_id)
                                # time.sleep(1)
                            break  # Exit retry loop if successful
                        except pymysql.Error as db_error:
                            retry_count += 1
                            error_code = db_error.args[0]
                            # Handle lost connection error
                            if error_code == 2013:  # Lost connection to MySQL server
                                print(f"MySQL connection lost. Retrying ({retry_count}/{max_retries})...")
                                # Reconnect to the database
                                try:
                                    global conn
                                    conn = pymysql.connect(
                                        host='192.168.1.14',
                                        user='username',
                                        passwd='password',
                                        port=3306,
                                        connect_timeout=60
                                    )
                                    time.sleep(5)  # Wait before retrying
                                except Exception as reconnect_error:
                                    print(f"Failed to reconnect: {reconnect_error}")
                            else:
                                print(f"Database error: {db_error}")
                                if retry_count == max_retries:
                                    print(f"Max retries reached for job {job_id}. Skipping.")

                # Move to next page
                page += 1

            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                print(f"Response text: {response.text}")
                break

        except Exception as e:
            print(f"Error retrieving data: {e}")
            # If it's a database connection error, try to reconnect
            if isinstance(e, pymysql.Error) and e.args[0] == 2013:
                try:
                    print("Attempting to reconnect to the database...")
                    conn = pymysql.connect(
                        host='192.168.1.14',
                        user='username',
                        passwd='password',
                        port=3306,
                        connect_timeout=60
                    )
                    print("Reconnected successfully. Continuing...")
                    continue  # Try the current page again
                except Exception as reconnect_error:
                    print(f"Failed to reconnect: {reconnect_error}")
            break

    print(f"Finished processing query: '{query}'")


from datetime import datetime


def clean_string(s):
    return s.replace("'", "''") if s else ''


def convert_date_format(date_time_str):
    # Parse the ISO 8601 date-time string
    dt = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')

    # Format the date into 'YYYY-MM-DD' format
    return dt.strftime('%Y-%m-%d')


def check_job_exists(job_id):
    try:
        with conn.cursor() as cursor:
            # Query to check if job_id exists
            sql = "SELECT COUNT(*) FROM HelpYourself.jobsdb2024all WHERE job_id = %s"
            cursor.execute(sql, (job_id,))

            # Fetch the result
            result = cursor.fetchone()

            # Check if job_id exists
            if result[0] > 0:
                # print(f"Job ID: {job_id} already exists in the database.")
                return True
            else:
                # print(f"Job ID: {job_id} does not exist in the database.")
                return False

    except pymysql.MySQLError as e:
        print(f"Error checking job existence: {e}")
        return False


def find_job_detail(id):
    session_id = get_session_id()
    json_data = {
        'operationName': 'jobDetails',
        'variables': {
            "countryCode": "HK",
            "jobDetailsViewedCorrelationId": session_id,
            "jobId": id,
            "languageCode": "en",
            "locale": "en-HK",
            "sessionId": session_id,
            "timezone": "Etc/GMT-8",
            "zone": "asia-1"
        },
        'query': "query jobDetails($jobId: ID!, $jobDetailsViewedCorrelationId: String!, $sessionId: String!, $zone: Zone!, $locale: Locale!, $languageCode: LanguageCodeIso!, $countryCode: CountryCodeIso2!, $timezone: Timezone!) {\n  jobDetails(\n    id: $jobId\n    tracking: {channel: \"WEB\", jobDetailsViewedCorrelationId: $jobDetailsViewedCorrelationId, sessionId: $sessionId}\n  ) {\n    job {\n      sourceZone\n      tracking {\n        adProductType\n        classificationInfo {\n          classificationId\n          classification\n          subClassificationId\n          subClassification\n          __typename\n        }\n        hasRoleRequirements\n        isPrivateAdvertiser\n        locationInfo {\n          area\n          location\n          locationIds\n          __typename\n        }\n        workTypeIds\n        postedTime\n        __typename\n      }\n      id\n      title\n      phoneNumber\n      isExpired\n      expiresAt {\n        dateTimeUtc\n        __typename\n      }\n      isLinkOut\n      contactMatches {\n        type\n        value\n        __typename\n      }\n      isVerified\n      abstract\n      content(platform: WEB)\n      status\n      listedAt {\n        label(context: JOB_POSTED, length: SHORT, timezone: $timezone, locale: $locale)\n        dateTimeUtc\n        __typename\n      }\n      salary {\n        currencyLabel(zone: $zone)\n        label\n        __typename\n      }\n      shareLink(platform: WEB, zone: $zone, locale: $locale)\n      workTypes {\n        label(locale: $locale)\n        __typename\n      }\n      advertiser {\n        id\n        name(locale: $locale)\n        __typename\n      }\n      location {\n        label(locale: $locale, type: LONG)\n        __typename\n      }\n      classifications {\n        label(languageCode: $languageCode)\n        __typename\n      }\n      products {\n        branding {\n          id\n          cover {\n            url\n            __typename\n          }\n          thumbnailCover: cover(isThumbnail: true) {\n            url\n            __typename\n          }\n          logo {\n            url\n            __typename\n          }\n          __typename\n        }\n        bullets\n        questionnaire {\n          questions\n          __typename\n        }\n        video {\n          url\n          position\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    companyProfile(zone: $zone) {\n      id\n      name\n      companyNameSlug\n      shouldDisplayReviews\n      branding {\n        logo\n        __typename\n      }\n      overview {\n        description {\n          paragraphs\n          __typename\n        }\n        industry\n        size {\n          description\n          __typename\n        }\n        website {\n          url\n          __typename\n        }\n        __typename\n      }\n      reviewsSummary {\n        overallRating {\n          numberOfReviews {\n            value\n            __typename\n          }\n          value\n          __typename\n        }\n        __typename\n      }\n      perksAndBenefits {\n        title\n        __typename\n      }\n      __typename\n    }\n    companySearchUrl(zone: $zone, languageCode: $languageCode)\n    learningInsights(platform: WEB, zone: $zone, locale: $locale) {\n      analytics\n      content\n      __typename\n    }\n    companyTags {\n      key(languageCode: $languageCode)\n      value\n      __typename\n    }\n    restrictedApplication(countryCode: $countryCode) {\n      label(locale: $locale)\n      __typename\n    }\n    sourcr {\n      image\n      imageMobile\n      link\n      __typename\n    }\n    gfjInfo {\n      location {\n        countryCode\n        country(locale: $locale)\n        suburb(locale: $locale)\n        region(locale: $locale)\n        state(locale: $locale)\n        postcode\n        __typename\n      }\n      workTypes {\n        label\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

    base_url = 'https://hk.jobsdb.com/graphql'

    data = {}
    for attempt in range(5):
        headers = get_jobsdb_headers_with_session(session_id)
        response = requests.post(base_url, headers=headers, json=json_data, proxies=get_random_proxy())

        try:
            response_json = response.json()
            data = response_json
            # print(data)
            # print(get_random_proxy())
            if 'error' in data and 'message' in data['error'] and 'too many requests' in data['error']['message']:
                print(f'Too many requests. Attempt {attempt + 1} of 5')
                if attempt == 4:  # Last attempt
                    print('Max retries reached. Exiting.')
                    data = {}
                continue  # Try again
            else:
                break
            # If we get here, we have a valid response
            # return data

        except requests.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON response. Attempt {attempt + 1} of 5")
            if attempt == 4:  # Last attempt
                print("Max retries reached. Exiting.")
                data = {}

    if data == {}:
        return
    # # If we get here, all attempts failed
    # print("All attempts failed. Exiting.")
    # exit()
    # try:
    # Extract fields safely
    job_id = data['data']['jobDetails']['job']['id']
    job_title = data['data']['jobDetails']['job']['title']
    job_url = data['data']['jobDetails']['job']['shareLink']
    company = data['data']['jobDetails']['job']['advertiser']['name']
    job_function = data['data']['jobDetails']['job']['classifications'][0]['label'].split(' (')[0]
    job_type = data['data']['jobDetails']['job']['workTypes']['label']
    industry = data['data']['jobDetails']['job']['classifications'][0]['label'].split(' (')[1].replace(')', '')
    career_level = None  # Assuming this field can be NULL
    years_of_experience = ''
    qualification = ''
    benefits = ''
    description = data['data']['jobDetails']['job']['content']
    postDate = convert_date_format(data['data']['jobDetails']['job']['listedAt']['dateTimeUtc'])
    location = data['data']['jobDetails']['job']['location']['label']
    search_type = query  # Replace 'query' with the actual value if available

    # Safely extract the questions
    questions_text = ''
    if 'questionnaire' in data['data']['jobDetails']['job']:
        questions = data['data']['jobDetails']['job']['questionnaire']['questions']
        questions_text = '; '.join(questions)

    # Create the SQL query with placeholders
    sql = """
        INSERT IGNORE INTO HelpYourself.jobsdb2024all (
            job_id,
            job_title,
            job_url,
            company,
            job_function,
            job_type,
            industry,
            career_level,
            years_of_experience,
            qualification,
            benefits,
            description,
            postDate,
            location,
            question,
            search_type
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
    """

    # Example usage
    with conn.cursor() as crsr:
        crsr.execute(sql, (
            job_id,
            job_title,
            job_url,
            company,
            job_function,
            job_type,
            industry,
            career_level,
            years_of_experience,
            qualification,
            benefits,
            description,
            postDate,
            location,
            questions_text,
            search_type
        ))
        conn.commit()

        # Function to fetch job details using GraphQL
        def fetch_job_details(job_id):
            url = "https://hk.jobsdb.com/graphql"

            payload = {
                "operationName": "GetAppliedJobDetail",
                "variables": {
                    "jobId": job_id,
                    "locale": "en-HK"
                },
                "query": """
                query GetAppliedJobDetail($jobId: ID!, $locale: Locale!) {
                    viewer {
                        id
                        appliedJob(jobId: $jobId) {
                            id
                            documents {
                                resume {
                                    attachmentMetadata {
                                        fileName
                                        __typename
                                    }
                                    __typename
                                }
                                coverLetter {
                                    attachmentMetadata {
                                        fileName
                                        __typename
                                    }
                                    __typename
                                }
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                    jobDetails(id: $jobId) {
                        insights {
                            ... on ApplicantCount {
                                __typename
                                count
                                message(locale: $locale)
                            }
                            ... on ApplicantsWithResumePercentage {
                                __typename
                                percentage
                                message(locale: $locale)
                            }
                            ... on ApplicantsWithCoverLetterPercentage {
                                __typename
                                percentage
                                message(locale: $locale)
                            }
                            __typename
                        }
                        __typename
                    }
                }
                """
            }

            response = requests.post(url, headers=headers, json=payload, proxies=get_random_proxy())

            if response.status_code == 200:
                try:
                    data = response.json()
                    # handle this {"errors":[{"message":"An error occurred","path":["viewer"],"extensions":{"code":"UNAUTHENTICATED"}}],"data":{"viewer":null,"jobDetails":{"insights":[{"__typename":"ApplicantCount","count":9,"message":"Less than 10 candidates have applied for this role"},{"__typename":"ApplicantsWithResumePercentage","percentage":100,"message":"100% of candidates attached a resumé"}],"__typename":"JobDetails"}}}
                    # check typename instead
                    data = data["data"]["jobDetails"]["insights"]
                    typeName = [
                        "ApplicantCount",
                        "ApplicantsWithResumePercentage",
                        "ApplicantsWithCoverLetterPercentage"
                    ]
                    applicant_count = ''
                    resume_percentage = ''
                    cover_letter_percentage = ''

                    for i in data:
                        if i["__typename"] == "ApplicantCount":
                            applicant_count = i["count"]
                        elif i["__typename"] == "ApplicantsWithResumePercentage":
                            resume_percentage = i["percentage"]
                        elif i["__typename"] == "ApplicantsWithCoverLetterPercentage":
                            cover_letter_percentage = i["percentage"]

                    return {
                        "applicant_count": applicant_count,
                        "resume_percentage": resume_percentage,
                        "cover_letter_percentage": cover_letter_percentage
                    }
                except Exception as e:
                    print(f"Error fetching job details: {e}")
                    print(job_id)
                    print(response.text)
                    return None
            else:
                print(f"Request failed with status code: {response.status_code}")
                return None

        job_details = fetch_job_details(job_id)
        if job_details:
            print(f"Job ID: {job_id}")
            if job_details['applicant_count'] != '':
                print(f"Applicant Count: {job_details['applicant_count']}")
                crsr.execute("UPDATE jobsdb2024all SET ApplicantCount = %s WHERE job_id = %s",
                             (job_details['applicant_count'], job_id))
                conn.commit()
            if job_details['resume_percentage'] != '':
                print(f"Resume Percentage: {job_details['resume_percentage']}")
                crsr.execute("UPDATE jobsdb2024all SET ApplicantsWithResumePercentage = %s WHERE job_id = %s",
                             (job_details['resume_percentage'], job_id))
                conn.commit()
            if job_details['cover_letter_percentage'] != '':
                print(f"Cover Letter Percentage: {job_details['cover_letter_percentage']}")
                crsr.execute("UPDATE jobsdb2024all SET ApplicantsWithCoverLetterPercentage = %s WHERE job_id = %s",
                             (job_details['cover_letter_percentage'], job_id))
                conn.commit()
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

        # job_details = fetch_job_details(job_id)
        # if job_details:
        #     print(f"Job ID: {job_id}")
        #     if job_details['applicant_count'] != '':
        #         print(f"Applicant Count: {job_details['applicant_count']}")
        #         crsr.execute("UPDATE jobsdb2024all SET ApplicantCount = %s WHERE job_id = %s",
        #                      (job_details['applicant_count'], job_id))
        #         conn.commit()
        #     if job_details['resume_percentage'] != '':
        #         print(f"Resume Percentage: {job_details['resume_percentage']}")
        #         crsr.execute("UPDATE jobsdb2024all SET ApplicantsWithResumePercentage = %s WHERE job_id = %s",
        #                      (job_details['resume_percentage'], job_id))
        #         conn.commit()
        #     if job_details['cover_letter_percentage'] != '':
        #         print(f"Cover Letter Percentage: {job_details['cover_letter_percentage']}")
        #         crsr.execute("UPDATE jobsdb2024all SET ApplicantsWithCoverLetterPercentage = %s WHERE job_id = %s",
        #                      (job_details['cover_letter_percentage'], job_id))
        #         conn.commit()

    # job_details = fetch_job_details(job_id)
    # if job_details:
    #     print(f"Job ID: {job_id}",job_title,job_details['applicant_count'],job_details['resume_percentage'],job_details['cover_letter_percentage'])
    #     with conn.cursor() as crsr:
    #
    #         # ApplicantCount, ApplicantsWithResumePercentage, ApplicantsWithCoverLetterPercentage update by job_id
    #         crsr.execute(
    #             "UPDATE jobsdb2024all SET ApplicantCount = %s, ApplicantsWithResumePercentage = %s, ApplicantsWithCoverLetterPercentage = %s WHERE job_id = %s",
    #             (job_details['applicant_count'], job_details['resume_percentage'],
    #              job_details['cover_letter_percentage'], job_id))
    #         conn.commit()
    # except Exception as e:
    #     print(e.with_traceback())


# keys = [
#     # 'oscp'
#     'frontend',
#     'backend',
#     'fullstack',
#     'programmer',
#     'software enginner',
#     'java',
#     'react',
#     'c#',
#     'python',
#     'network',
#     'Software Developer',
#     'rust'
#     # ,
#     # 'unity',
#     # 'unreal',
#     # 'blender',
#     # 'maya',
# ]
# # print(sql)
# # find_job_detail("82866958")
# for query1 in keys:
#     query = query1
#     query = query.replace('#', '%23')
find_job_id()