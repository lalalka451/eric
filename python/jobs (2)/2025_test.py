import requests

url = "https://hk.jobsdb.com/job/82866958?type=standard&ref=search-standalone&origin=cardTitle"

# Headers for GET request
headers = {
    "Host": "hk.jobsdb.com",
    "Cookie": "sol_id=64da19d7-6716-44d0-b8aa-70b110fe4d02; JobseekerSessionId=97260934-230d-4da7-88d4-f91cfeda0e04; JobseekerVisitorId=97260934-230d-4da7-88d4-f91cfeda0e04; _fbp=fb.1.1741511124180.588908320802386667; ajs_anonymous_id=adbccd83c9c1bea78a225b95d22f6f6b; _gcl_au=1.1.530001795.1741511124; _hjSessionUser_337118=eyJpZCI6ImI5MWFhM2QyLTQ1NTUtNTQyOS1iMzBiLTk1MzVkODg2Zjc2YiIsImNyZWF0ZWQiOjE3NDE1MTExMjQ3NTQsImV4aXN0aW5nIjp0cnVlfQ==; _cfuvid=c6rrNdPh1veLtpNAcoQTr.4rO0VHq369gLYqkLhS8DU-1742578841257-0.0.1.1-604800000; cf_clearance=Blsc79ICrSACe42VYkWYKIcnkYbhxOguS5TsRxuf56o-1742578849-1.2.1.1-nSb5t1R4Ybbe3wxM.kyibFyx9Bqvqn5CzOZe16O4ZFXGba5gVduG2phI20Chl4odU_0J651J2FrZ7_WeXO4gchEjiXWL0hdfFHy.X.XNkE9Sdz42g5zU_vE3v.jSUkGyt4QXKQgkJb7EDXaSbe13ls2lz6EnR3y4h1t10PVHbcG.xT7gEt6G0ptEgchkVoOs9rkRRvkLjgcHd59szS.YmbpohZwoISMEKJ2wipy02vBjMFt8YOshLKQ23kNmtOcSZTZFg1JyJ5UXl1j6bThuqV6wWartGYFGMw8ARPwdl0FK70HnwLH5lqSwiJiQPVk49UudTdl.nUsFAzLbmc.6jOinjHTzCTPXWSvAPTl7MNApxXq_5yh6f4AmJhL0VHHU; da_searchTerm=undefined; _tea_utm_cache_586864={%22utm_source%22:%22google%22%2C%22utm_medium%22:%22cpc%22%2C%22utm_campaign%22:%22hk-c-ao-[c]_dbhk_google_all_sem_brand_brand_en_exact_ao%22}; _clck=z3cgsh%7C2%7Cfuf%7C0%7C1906; cf_clearance=pnPY2GDM2qAGOTnAi67F3J6Ac14dYZwlx_aoKq8gNbU-1742615131-1.2.1.1-Nq5ApI98CANPrNuJIppBw5k_cntuzWdZC7azHhoKHnlPTNgFZy2_l_WPn8cvtDqbQWfCwCwAP2Q5utPadIiIENOkpGxgI_JEM..kmUe_Fgzlf.3z7u7g9B_xhgnEWOX_66v7IafVCTvBy509jf9_d69tFn_zCuwKDHcetnA7FoSGEOFhx6HGkBjplO85uHgzLODD.5Iyq9QyUzoZBKcgkBOJJmEHblf7GUrob.d8XALG3q9.7HZwvEshvc0Wl3ah4PmrYlHm6dJDgLCJxHCLhy8Q9JrRrOxigj5BATIv.LvfpM4llQR9.uT7vO1cE5iajxsuEYisYGKJMNJ67ujxRYKmSHW1XD32Wx73iTlWLrw6rY8J3M.QFxRL87Fu59OTmXrhiYzTeG5l7_U5sFy6A5ylxSW9qpZcXDG0rEE20p4; da_cdt=visid_01957a26e407001a720b34840db70506f004406700978-sesid_1742615134604-hbvid_64da19d7_6716_44d0_b8aa_70b110fe4d02-tempAcqSessionId_1742615134583-tempAcqVisitorId_64da19d7671644d0b8aa70b110fe4d02; da_sa_candi_sid=1742615134604; _hjSession_337118=eyJpZCI6ImY2ZDEwZmI3LTZkODYtNDRkZS1hNGI2LWNmZWE1ZmQxMjAwNyIsImMiOjE3NDI2MTUxMzc1MjksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _gcl_gs=2.1.k1$i1742616849$u21133218; _gcl_aw=GCL.1742616855.CjwKCAjwnPS-BhBxEiwAZjMF0n3VMK9L1fSvN72GrCK-F0-FRDmH-ECbyCt6rY74hYWpeofYtsFzRRoCyQwQAvD_BwE; _hjHasCachedUserAttributes=true; __cf_bm=7rAQxawSaJfabZVpjkxKRBTG3D0zW_I_SybLRhcl7g8-1742618469-1.0.1.1-lx5lpnw4HbBHAP76tn0pvXEPFpO8Y7Half5gGWhuGxUNmls3Qb78wyKkQWbj.UZba6gYmnfbu7aMniBHsJDYCiD7b1YaFoKS9pfLP0c35qs; main=V%7C2~P%7Cjobsearch~K%7Cfrontend~OSF%7Cquick&set=1742618470513/V%7C2~P%7Cjobsearch~K%7C123~OSF%7Cquick&set=1742617292593/V%7C2~P%7Cjobsearch~K%7Cweb3~WH%7CScience%20Park%20Tai%20Po%20District~OSF%7Cquick&set=1742612786732; utag_main=v_id:01957a26e407001a720b34840db70506f004406700978$_sn:4$_se:27%3Bexp-session$_ss:0%3Bexp-session$_st:1742620845184%3Bexp-session$ses_id:1742615134604%3Bexp-session$_pn:11%3Bexp-session$_prevpage:job%20details%3Bexp-1742622647037; hubble_temp_acq_session=id%3A1742615134583_end%3A1742620847044_sent%3A46; _uetsid=a1ced1c0067711f0a9e453dc7fd172fc; _uetvid=a1cebe40067711f094fc5ffe6f0b7efe; _clsk=dltccc%7C1742619048367%7C6%7C0%7Cn.clarity.ms%2Fcollect; _dd_s=rum=0&expire=1742619991447&logs=0",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Full-Version": "\"134.0.6998.118\"",
    "Sec-Ch-Ua-Arch": "\"x86\"",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Ch-Ua-Platform-Version": "\"10.0.0\"",
    "Sec-Ch-Ua-Model": "\"\"",
    "Sec-Ch-Ua-Bitness": "\"64\"",
    "Sec-Ch-Ua-Full-Version-List": "\"Chromium\";v=\"134.0.6998.118\", \"Not:A-Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"134.0.6998.118\"",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://hk.jobsdb.com/frontend-jobs?jobId=82866958&type=standard",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Priority": "u=0, i"
}

# Make GET request
response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Content Length: {len(response.text)} bytes")