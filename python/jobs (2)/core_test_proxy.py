import uuid

import requests

def fetch_data(url):
  """Fetches data from the given URL and returns the response content."""
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.text
  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from {url}: {e}")
    return None


session_id = str(uuid.uuid4())

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    'X-Seek-Ec-Sessionid': session_id,
}

def test_proxy(proxy):
    try:
        json_data = {
            'operationName': 'jobDetails',
            'variables': {
                "countryCode": "HK",
                "jobDetailsViewedCorrelationId": session_id,
                "jobId": '78865175',
                "languageCode": "en",
                "locale": "en-HK",
                "sessionId": session_id,
                "timezone": "Etc/GMT-8",
                "zone": "asia-1"
            },
            'query': "query jobDetails($jobId: ID!, $jobDetailsViewedCorrelationId: String!, $sessionId: String!, $zone: Zone!, $locale: Locale!, $languageCode: LanguageCodeIso!, $countryCode: CountryCodeIso2!, $timezone: Timezone!) {\n  jobDetails(\n    id: $jobId\n    tracking: {channel: \"WEB\", jobDetailsViewedCorrelationId: $jobDetailsViewedCorrelationId, sessionId: $sessionId}\n  ) {\n    job {\n      sourceZone\n      tracking {\n        adProductType\n        classificationInfo {\n          classificationId\n          classification\n          subClassificationId\n          subClassification\n          __typename\n        }\n        hasRoleRequirements\n        isPrivateAdvertiser\n        locationInfo {\n          area\n          location\n          locationIds\n          __typename\n        }\n        workTypeIds\n        postedTime\n        __typename\n      }\n      id\n      title\n      phoneNumber\n      isExpired\n      expiresAt {\n        dateTimeUtc\n        __typename\n      }\n      isLinkOut\n      contactMatches {\n        type\n        value\n        __typename\n      }\n      isVerified\n      abstract\n      content(platform: WEB)\n      status\n      listedAt {\n        label(context: JOB_POSTED, length: SHORT, timezone: $timezone, locale: $locale)\n        dateTimeUtc\n        __typename\n      }\n      salary {\n        currencyLabel(zone: $zone)\n        label\n        __typename\n      }\n      shareLink(platform: WEB, zone: $zone, locale: $locale)\n      workTypes {\n        label(locale: $locale)\n        __typename\n      }\n      advertiser {\n        id\n        name(locale: $locale)\n        __typename\n      }\n      location {\n        label(locale: $locale, type: LONG)\n        __typename\n      }\n      classifications {\n        label(languageCode: $languageCode)\n        __typename\n      }\n      products {\n        branding {\n          id\n          cover {\n            url\n            __typename\n          }\n          thumbnailCover: cover(isThumbnail: true) {\n            url\n            __typename\n          }\n          logo {\n            url\n            __typename\n          }\n          __typename\n        }\n        bullets\n        questionnaire {\n          questions\n          __typename\n        }\n        video {\n          url\n          position\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    companyProfile(zone: $zone) {\n      id\n      name\n      companyNameSlug\n      shouldDisplayReviews\n      branding {\n        logo\n        __typename\n      }\n      overview {\n        description {\n          paragraphs\n          __typename\n        }\n        industry\n        size {\n          description\n          __typename\n        }\n        website {\n          url\n          __typename\n        }\n        __typename\n      }\n      reviewsSummary {\n        overallRating {\n          numberOfReviews {\n            value\n            __typename\n          }\n          value\n          __typename\n        }\n        __typename\n      }\n      perksAndBenefits {\n        title\n        __typename\n      }\n      __typename\n    }\n    companySearchUrl(zone: $zone, languageCode: $languageCode)\n    learningInsights(platform: WEB, zone: $zone, locale: $locale) {\n      analytics\n      content\n      __typename\n    }\n    companyTags {\n      key(languageCode: $languageCode)\n      value\n      __typename\n    }\n    restrictedApplication(countryCode: $countryCode) {\n      label(locale: $locale)\n      __typename\n    }\n    sourcr {\n      image\n      imageMobile\n      link\n      __typename\n    }\n    gfjInfo {\n      location {\n        countryCode\n        country(locale: $locale)\n        suburb(locale: $locale)\n        region(locale: $locale)\n        state(locale: $locale)\n        postcode\n        __typename\n      }\n      workTypes {\n        label\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }

        base_url = 'https://hk.jobsdb.com/graphql'
        proxies = {
        # 'http': '127.0.0.1:6666'
        # 'http': '127.0.0.1:10809'
        'http': f'127.0.0.1:{proxy}'
        # 'http': random.choice(http_proxies) if http_proxies else '127.0.0.1:10809'
    }
        print(proxies)
        response = requests.post(base_url, headers=headers, json=json_data, proxies=proxies)
        # response = requests.post(base_url, headers=headers, json=json_data)

        print(f"Status code: {response.status_code}")
        print(f"Status code: {response.text}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error testing proxy {proxy}: {e}")
        return False

def main():
  url = "https://imperialb.in/r/ywkbzmxe"
  data = fetch_data(url)
  http_proxies = data.split("\n")
  # http_proxies = ["127.0.0.1:" + port for port in http_proxies]
  # test_proxy('127.0.0.1:10809')
  for proxy in http_proxies:
    if test_proxy(proxy):
      print(f"Proxy {proxy} is working")
    else:
      print(f"Proxy {proxy} is not working")
    break


if __name__ == "__main__":
  main()
