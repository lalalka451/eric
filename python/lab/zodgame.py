import requests
import time
from datetime import datetime, timedelta
import re

import schedule


def sign_in(cookie):
    # Get the current date in GMT+8 timezone
    current_date = datetime.now() + timedelta(hours=8)
    current_day = current_date.day

    # First request to get the formhash
    url = "https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign"

    headers = {
        "Host": "zodgame.xyz",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Google Chrome";v="103", "Chromium";v="103", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://zodgame.xyz/",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": cookie,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        formhash_match = re.search(r'name="formhash" value="(.+?)"', response.text)
        if formhash_match:
            formhash = formhash_match.group(1)
        else:
            print(response.text)
            print("Failed to find formhash")
            return

        # Second request to actually sign in
        sign_url = "https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1"

        sign_headers = headers.copy()
        sign_headers.update({
            "Cache-Control": "max-age=0",
            "Origin": "https://zodgame.xyz",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign",
            "Sec-Fetch-Dest": "iframe",
        })

        sign_data = f"formhash={formhash}&qdxq=kx"

        sign_response = requests.post(sign_url, headers=sign_headers, data=sign_data)

        if sign_response.status_code == 200:
            # Third request to check sign-in status and get points
            check_url = "https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign"
            check_response = requests.get(check_url, headers=headers)

            if "今天签到了吗？" not in check_response.text:
                log_all = re.search(r'您累计已签到: <b>(.+?)</b> 天', check_response.text)
                log_day = re.search(r'您本月已累计签到:<b>(.+?)</b> 天', check_response.text)
                log_value = re.search(r'您目前获得的总奖励为:酱油 <font color="#ff00cc"><b>(.+?)</b></font> 瓶', check_response.text)

                if log_all and log_day and log_value:
                    print(f"Sign-in successful. 您累计已签到: {log_all.group(1)} 天 , 您本月已累计签到: {log_day.group(1)} 天 , 您目前获得的总奖励为:酱油 {log_value.group(1)}")
                else:
                    print("Sign-in successful, but couldn't extract all information.")
            else:
                print("Sign-in failed or already signed in today.")
        else:
            print(f"Sign-in request failed with status code: {sign_response.status_code}")
    else:
        print(f"Initial request failed with status code: {response.status_code}")

    # Implement the ad viewing for points
    ad_url = "https://zodgame.xyz/plugin.php?id=jnbux"
    ad_response = requests.get(ad_url, headers=headers)

    if ad_response.status_code == 200:
        clickid = re.search(r'clickid=(.+?)&', ad_response.text)
        timeo = re.search(r'timeo=(.+?)&', ad_response.text)
        onlyhash = re.search(r'onlyhash=(.+?)&', ad_response.text)
        userid = re.search(r'userid=(.+?)",', ad_response.text)
        needtime = re.search(r'<td>(.+?) 秒</td>', ad_response.text)

        if "参与任务" in ad_response.text and clickid and timeo and onlyhash and userid and needtime:
            click_url = f"https://zodgame.xyz/plugin.php?id=jnbux:jnbux&do=click&clickid={clickid.group(1)}&timeo={timeo.group(1)}&onlyhash={onlyhash.group(1)}&formhash={formhash}&userid={userid.group(1)}"
            requests.get(click_url, headers=headers)

            time.sleep(int(needtime.group(1)))

            update_url = f"https://zodgame.xyz/plugin.php?id=jnbux:jnbux&do=update&clickid={clickid.group(1)}&timeo={timeo.group(1)}&onlyhash={onlyhash.group(1)}&formhash={formhash}&userid={userid.group(1)}"
            requests.get(update_url, headers=headers)

            check_url = f"https://zodgame.xyz/plugin.php?id=jnbux:jnbux&do=check&clickid={clickid.group(1)}&userid={userid.group(1)}&formhash={formhash}&page=0&infloat=yes&handlekey=check&inajax=1&ajaxtarget=fwin_content_check"
            check_response = requests.get(check_url, headers=headers)

            if "检查成功" in check_response.text:
                print("Ad viewing task completed successfully.")
            else:
                print("Ad viewing task failed.")
        else:
            print("Ad viewing task not available or couldn't extract necessary information.")
    else:
        print(f"Ad viewing request failed with status code: {ad_response.status_code}")

if __name__ == "__main__":
    accounts = [
        {
            "name": "lalalka",
            "cookie": "qhMq_2132_sid=BZ4bx9; qhMq_2132_noticeTitle=1; qhMq_2132_saltkey=K4LHwQZl; qhMq_2132_lastvisit=1728802703; qhMq_2132_sendmail=1; qhMq_2132_ulastactivity=eacbydnQ0CACzHmjk4mO8elYX50sNQbqKEbSxkOHMxvPjla68cTS; qhMq_2132_auth=defeljDCL5kNxpuzV8Wn10uvmmUP%2BDRX00z5%2B4ClH8fMwMUWuIfkUf%2BbAM1dF3%2BxAtCMwsqRgPH7ZiwCJQ%2FhmTZXATw; qhMq_2132_lastcheckfeed=858308%7C1728806317; qhMq_2132_checkfollow=1; qhMq_2132_lip=210.209.119.91%2C1728806300; qhMq_2132_myrepeat_rr=R0; qhMq_2132_lastact=1728806318%09misc.php%09seccode; qhMq_2132_seccodecSBZ4bx9=8016.0a15cc6f7f8cb761fc"
        },
        {
            "name": "tatafa",
            "cookie": "qhMq_2132_saltkey=Cc0CosNu; qhMq_2132_lastvisit=1728801752; qhMq_2132_sendmail=1; qhMq_2132_ulastactivity=d44cParaoyoIjRYjeCFdI%2FxNx2pTJPaeM8anYsvzIe%2FK0lJFFsAM; qhMq_2132_auth=d86aPbC7sIf0gLKKQcOVAp59uLy1%2Bql4Tmk9ZHODnr9EvZprbF%2B4irBjSmP55qwvxp9cQf10wbNCsO9voFjwuzfR6zw; qhMq_2132_lastcheckfeed=804292%7C1728805376; qhMq_2132_myrepeat_rr=R0; qhMq_2132_seccodecSmSS1Sl=7749.f977931d6ff512bca6; qhMq_2132_nofavfid=1; qhMq_2132_onlineusernum=532; qhMq_2132_noticeTitle=1; qhMq_2132_sid=k2qZ3e; qhMq_2132_lip=210.209.119.91%2C1728805376; qhMq_2132_lastact=1728805417%09plugin.php%09; qhMq_2132_creditnotice=0D6D0D0D0D0D0D0D0D804292; qhMq_2132_creditbase=0D34D0D0D1D0D0D0D0"
        },
        {
            "name": "babama",
            "cookie": "qhMq_2132_saltkey=EZEGl7SL; qhMq_2132_lastvisit=1728803884; qhMq_2132_sendmail=1; qhMq_2132_noticeTitle=1; qhMq_2132_seccodecSb7V1VV=8259.aae254529a03af1c90; qhMq_2132_sid=W00GPa; qhMq_2132_seccodecSAgPdW00GPa=8267.610d7d2716a0990213; qhMq_2132_ulastactivity=35f3eN0tliZyf23h9uYPRQqV4gwUx8w42HlCAi38WuhoGlc%2BIB%2Bt; qhMq_2132_auth=9feexKLnG8rnMzeCWedKog68wsBS9RCRHt0JXhOsAwO6m13RYDT6F%2BWod54ms8CZg4JvFPu%2BDJIBR0tUJHQMxIcVCm8; qhMq_2132_lastcheckfeed=868632%7C1728807560; qhMq_2132_checkfollow=1; qhMq_2132_lip=210.209.119.91%2C1728807545; qhMq_2132_myrepeat_rr=R0; qhMq_2132_checkpm=1; qhMq_2132_lastact=1728807567%09misc.php%09patch"
        },
        # Add more accounts here if needed
    ]

    def main():
        for account in accounts:
            print(f"Signing in with account: {account['name']}")
            sign_in(account['cookie'])
            print("\n")  # Add a newline for better separation between sign-ins


    main()
    schedule.every(24).hours.do(main)
    while True:
        schedule.run_pending()
