base_header = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
}

# #     # @dsfasf938337
# #     # hrthrts@outlook.com
# {
#     "auth_token": "5a23ebf645c8af8d98bf129f464fe792c1389122",
#     "ct0": "5f1f04d0f98d0606eac53b17bbc4fdff8639c3f807a78277be69e7ba37a986af49a592f42011ffb5ff46099a8e92c855d4c34774cca5595f8ad696a7a77e7c7bca5eb154eb744f68b5538facee7c0ebe",
# },

other_headers = [
    # # @tatafa112157
    # {
    #     "auth_token": "984d40ba28798a4008ee6972f543cf49d4be88e8",
    #     "ct0": "d1ea7ac110c79812a538957cc4c6bfec0435672a2cf1caa2fd2a37ab9fcae02fb62a79e6e70266ce81761ad7ac7e13ba699308f906b2597388f4f87ae0fd88473b937519f9ed005bd519ad5936823c97",
    # },
    # # @HerekSilbe96611
    # {
    #     "auth_token": "34cb6f16c9e36fd2b78a188ea3097d01be1d050a",
    #     "ct0": "497ab9a3deee698d1af8ce0309fa134c1945801027b2c9c9295a30e94288e0809a08fc522e5b960670f8fadd524bc463b4166aab8730c6152976b93df5aae4f8000d2f62a2c82d8d8304cb524e4d4b8d",
    # },
    # # eric21516693724
    # # tatafa2234@gmail.com
    # {
    #     "auth_token": "984d40ba28798a4008ee6972f543cf49d4be88e8",
    #     "ct0": "d1ea7ac110c79812a538957cc4c6bfec0435672a2cf1caa2fd2a37ab9fcae02fb62a79e6e70266ce81761ad7ac7e13ba699308f906b2597388f4f87ae0fd88473b937519f9ed005bd519ad5936823c97",
    # },
    # # ffsaf261920
    # # rqwrwqrwq2@outlook.com
    # {
    #     "auth_token": "34cb6f16c9e36fd2b78a188ea3097d01be1d050a",
    #     "ct0": "497ab9a3deee698d1af8ce0309fa134c1945801027b2c9c9295a30e94288e0809a08fc522e5b960670f8fadd524bc463b4166aab8730c6152976b93df5aae4f8000d2f62a2c82d8d8304cb524e4d4b8d",
    # },
    # # ffsaf261920
    # # rqwrwqrwq2@outlook.com
    # {
    #     "auth_token": "eb03c1e5aa93b597f2ab9a7fb75f3616db014ed4",
    #     "ct0": "0a19aa7d34a436b9630fc46b6a385cf40efb512bdb614d537b888be5682d4264cba73454d4b62ff5dad579f8f217387d5c1dd08ded473407d70ae3deeb3881cfaed883ce93c3920c1a0871cc9353e740",
    # },
    # # @deswfqw89664
    # # rwqtawrw@outlook.com
    # {
    #     "auth_token": "7e18cb8ae700dc0df540ab9ba260ecb2a383a2e6",
    #     "ct0": "dfb99836a337aae471bc23adf12acc58ccda050d7fe33603bfdd113d5bfafe303a137e9c24fa4c4976cd8c8a69815ef6e1fdcd8e2b238870a2e91440829381875fd5960debbbb92b06885239ba864132",
    # },
    # # @rdudu268799
    # # fueqq23fdas@outlook.com
    # {
    #     "auth_token": "fb66a309ab5245a255ac8e90d4a4efaffd41e021",
    #     "ct0": "3a8b403d6b2193522bfc7f5bc99d1db65f8151d5d666b42dab1dade3ce887785e6d63cdb6520277dff9c9ecb9b82b45269a0cd17a0375c09123d42b9799129ad56763758533a0ad9a5f90566c72d45fe",
    # },
    # #@dsafww190922
    # #a.2392243459@gmail.com
    # {
    #     "auth_token": "75427f2fbccb734e1589437c242aa0c6acc2c71c",
    #     "ct0": "8ab292f94e6a1b59441b03dbf092d5c78ad0def7a06590c48968ed9b0f36b506bd16953ec3a1b5e82f5ecf8a9e8605b69a30500900f386684da1bf45f28a65ce90db8a3918b1f6d7f47c9d85544d1b0a",
    # },
    #
    # # @qegrwhrwhr95890
    # # a2.392243459@gmail.com
    # {
    #     "auth_token": "c957290c4930a3ae828f3d1ffa9269a481da955e",
    #     "ct0": "37fc9f40ed0a806469ef0def68811554912fe9e6c900b3c281fd09809eefdcf3fcd8cb0d8263fbf417641ddb348c8406555ac74b2e2bbcd4180889bf6f18955e8d12b67a15f97e5f014924c6139c54af",
    # },
    {
    "auth_token": "93d9683795c082fea341afef6424b63e5f84d369",
"ct0": "9e7191a35c4b224016a75eee23ef8890e6cac949290036fef9756b0b8906e4e4f7f6ea0beaf22510295f60c17f348d2cd0957dbb49fa49ba73ed02db399e63f08822397a99e34537a813a8cf914e82b5",
    }
]

import requests
import random

def fetch_profile_spotlights(screen_name):
    url = "https://x.com/i/api/graphql/-0XdHI-mrHWBQd8-oLo1aA/ProfileSpotlightsQuery"
    params = {
        "variables": f'{{"screen_name":"{screen_name}"}}'
    }

    print(len(other_headers))
    for i, header_set in enumerate(other_headers):
        try:
            headers = base_header.copy()
            headers.update({
                "Cookie": f"auth_token={header_set['auth_token']}; ct0={header_set['ct0']}",
                "X-Csrf-Token": header_set['ct0'],
                "Referer": f"https://x.com/{screen_name}/",
            })

            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            if response.status_code == 200:
                print(f"Success with header set {i + 1}")
        except requests.RequestException as e:
            print(f"Header set {i + 1} failed: {str(e)}")
    
    return None

# Test the function
a = fetch_profile_spotlights('BBmianmian')
