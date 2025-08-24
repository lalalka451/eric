import requests
import json
import urllib.parse

import schedule

from baseHandler import BaseHandler
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Define multiple configurations
CONFIGURATIONS = [
    {
        'channel_id': 2484441083,
        'db_name': 'twitter_chinese',
        'session': 'twitter_chinese_session',
        'twitter_users': [
            'lsloops',
            "vista8",
            "xinwendiaocha",
            "gunsnrosesgirl3",
            "0xTib3rius",
            "forrestzh_",
            "bad_texter",
            "historyinmemes",
            "ollama",
            "Hikarumao",
            "bountywriteups",
            "hoshusokuhou",
            "91rumor",
            "whyyoutouzhele",
            "lidangzzz",
            "itsPaulAi",
            "TDS_95514874",
            "Mr_BlackMirror",
            "zaobaosg",
            "huajuanshiwo",
            "PlatinumEquinox",
            "XssPayloads",
            "waylybaye",
            "Basefount",
            "geekbb",
            "paranormal_2ch",
            "Tesla_Optimus",
            "bz678345",
            "ijKh5fThXH5lbDP",
            "xu96175836",
            "SandyLyons59766",
            "DiverX_VR",
            "wangzhian8848",
            "maruokun15",
            "shino7878shino",
            "Owatterushashin",
            "yuyudayo0924",
            "ooeli_eth",
            "crazyclipsonly",
            "lambdaprog",
            "crowkaka_no996",
            "jessyshen",
            "masami777777",
            "Biantaibear01",
            "natanielruizg",
            "NeverteIImeodd",
            "RIhFlv0lS1_YIqZ",
            "jajia",
            "tesuta001",
            "xiao_yi5645",
            "momo36497",
            "positivesideofx",
            "Birchlabs",
            "CarlZha",
            "KdWq5",
            "ayeejuju",
            "cubiq",
            "m_aqap",
            "xiaojingcanxue",
            "punimaru_luna",
            "NiKiTa_32156",
            "creepydotorg",
            "MOSSADil",
            "docchi13",
            "p_ma_ru",
            "samansajpn",
            "fladdict",
            "fekdaoui",
            "wuyuesanren",
            "yee_seol",
            "Sindigaisaac",
            "Jerrain22",
            "crackcobain__",
            "MatsumotoH873",
            "libsoftiktok",
            "patrickbetdavid",
            "QueenMAGAUltra",
            "_johnnymaga",
            "ClayTravis",
            "MTGrepp",
            "momo_ffmomo",
            "HienNguyen65277",
            "DFSGDFH27269175",
            "wanwanshouji2",
            "bushizhizhang1",
            "prolin123456",
            "sunfeng_China",
            "xiopngg61420599",
            "TinaTan01495509",
            "shitpost_2077",
            "yomogi_168",
            "HannaBarberaCap",
            "Fishing_Lovers2",
            "yyo23511",
            "linboweibu17",
            "TXMemeTheif",
            "YangZhao182",


            "FreiheitYu",
            "nateleex",
            "yuxiyou",
            "xushiwei",
            "skywind3000",
            "vikingmute",
            "waylybaye",
            "dotey",
            "manateelazycat",
            "middlefeng",
            "DLKFZWilliam",
            "javayhu",
            "nextify2024",
            "xiongchun007",
            "yihong0618",
            "yihui_indie",
            "goocarlos",
            "ruanyf",
            "appinn",
            "turingou",
            "Linmiv",
            "chenbimo",
            "feltanimalworld",
            "mrbear1024",
            "xiaopeng163",
            "AgileQuery",
            "tison1096",
            "RyanMfer",
            "zhugezifang",
            "haoel",
            "huihoo",
            "knowledgefxg",
            "hixiaoji",
            "bnu_chenshuo",
            "gefei55",
            "wshuyi",
            "felixding",
            "huangzworks",
            "zhufengme",
            "marchliu",
            "glow1n",
            "li_wujie",
            "yosei8964",
            "seclink",
            "kuizuo",
            "harryworld",
            "CoooolXyh",
            "DIGITALYCHEE",
            "davidchen2024",
            "taro_dict",
            "ihower",
            "ethanhuang13",
            "PeterTW777",
            "hwwaanng",
            "MapleShadow",
            "lexrus",
            "arui_kisi",
            "Bitturing",
            "ccbikai",
            "weijunext",
            "pingchn",
            "leafwind",
            "fetalkpodcast",
            "hhmy27",
            "indigo11",
            "decohack",
            "geekplux",
            "henices",
            "lyc_zh",
            "JourneymanChina",
            "huangyun_122",
            "vista8",
            "lewangdev",
            "thinkingjimmy",
            "shengxj1",
            "meathill1",
            "ailiangzi",
            "dingyi",
            "hal__lee",
            "shao__meng",
            "CZXNew",
            "henuwangkai",
            "YosefBlockchain",
            "cesihai1",
            "qloog",
            "johnny____11",
            "nishuang",
            "DashHuang",
            "robbinfan",
            "turingbook",
            "mujiang",
            "csdncto",
            "zhuangbiaowei",
            "buaaxhm",
            "nmdfzf404",
            "AndyRoamer",
            "wsygc",
            "monk_robot",
            "daniu1719",
            "remixdesigner",
            "imtigerchew",
            "ikennylin",
            "balconychy",
            "catmangox",
            "oran_ge",
            "river_leaves",
            "HiTw93",
            "trojantale",
            "9yearfish",
            "leoxoocanada",
            "i5ting",
            "blankwebdev",
            "boo_hz",
            "tonyzhu1984",
            "hongming731",
            "benshandebiao",
            "tinyfool",
            "whiteboardxcom",
            "CurtisChengC",
            "cui_xiaorui",
            "hsin747",
            "StarKnight",
            "easychen",
            "AndrewBBoo",
            "dev_afei",
            "pekingmuge",
            "ginhoor",
            "oulvhai",
            "Tumeng05",
            "anqirocks",
            "austinit",
            "hzlzh",
            "cellinlab",
            "richriverspirit",
            "sailfishcc1",
            "hi_an_orange",
            "fengbuyou",
            "ilovek8s",
            "evanlong_zh",
            "xinbaocode",
            "Amztion",
            "hagerhu",
            "liseami1",
            "container202",
            "oschina",
            "junyu",
            "DigitalNomadLC",
            "_kaichen",
            "taoshenga19",
            "shamzaaz1",
            "spacewander_lzx",
            "CarsonYangk8s",
            "Piglei",
            "ThonsChang",
            "435hz",
            "MooenyChu",
            "chenboos5",
            "greylihui",
            "foxshuo",
            "Ninsbay",
            "sekay2016",
            "layla8964",
            "kenshinji",
            "michaelwong666",
            "jessieinorge",
            "CaminoTexas",
            "no13bus",
            "USAHS1",
            "neverrainmyself",
            "tuturetom",
            "jyrnan",
            "NodYoung",
            "cellier_",
            "Aviva",
            "Gorden_Sun",
            "7733Bianca",
            "horsezhanbin",
            "iamluokai",
            "youtubedubbing",
            "Yangyixxxx",
            "op7418",
            "OwenYoungZh",
            "imxiaohu",
            "kasong2048",
            "arvin17x",
            "likefeiwu",
            "houjoe1",
            "readyfor2025",
            "choicky",
            "linroid",
            "real_kai42",
            "cholf5",
            "siantgirl",
            "lvxinxin",
            "__oQuery",
            "_justineo",
            "chaosflutt28952",
            "AnwFM",
            "JohnnyBi577370",
            "yan5xu",
            "VKoooooon",
            "belliedmonkey",
            "Huanghanzhilian",
            "pupilcc",
            "wangeguo",
            "frank_8848",
            "1024_zip",
            "zolplay",
            "nanshanjukr",
            "haohailong",
            "le0zh0u",
            "jinjinledaofm",
            "x_canoe",
            "sspai_com",
            "coolXiao",
            "jike_collection",
            "liruifengv",
            "whileGreatHair",
            "FinoGeng",
            "CMGS1988",
            "zuozizhen",
            "fuxiaohei",
            "randyloop",
            "Lakr233",
            "alswl",
            "HzaoHzao",
            "geekbb",
            "JinsFavorites",
            "leeoxiang",
            "nexmoe",
            "SaitoWu",
            "HongyuanCao",
            "huangjinbo",
            "CeoSpaceY",
            "9hills",
            "mundane799699",
            "luobogooooo",
            "OpenQiang",
            "qilong87",
            "ftium4",
            "CNBorn",
            "gametofuofl",
            "sh_awai",
            "strrlthedev",
            "freesisx",
            "baoshu88",
            "santiagoyoungus",
            "raycat2021",
            "mike_d1213",
            "liuren",
            "onenewbite",
            "thecalicastle",
            "Himalaya_bear1",
            "jason5ng32",
            "Beichen",
            "ifanr",
            "erchenlu1",
            "realliaohaibo",
            "oIUnIfxxuuNRpIA",
            "Yintinusa",
            "FinanceYF5",
            "0xluffy_eth",
            "HeySophiaHong",
            "Trillion5205189",
            "CoderJeffLee",
            "minizz1949",
            "juransir",
            "gidot",
            "lemon_hx",
            "imsingee",
            "HotmailfromSH",
            "WildCat_zh",
            "beihuo",
            "haveafreeheart",
            "wong2_x",
            "fkysly",
            "plusyip",
            "alanblogsooo",
            "nianyi_778",
            "ovst36099",
            "_KleinHe_",
            "lumaoyangmao",
            "ShouChen_",
            "wwek",
            "edwardzsky2017",
            "fxxkol",
            "ruiyanghim",
            "waiwen3",
            "gasikaramada",
            "marvin102465536",
            "tianlan",
            "wulujia",
            "quentin_hsu",
            "lgywrite",
            "FlashSnail",
            "nuannuan_share",
            "sitinme",
            "boy94288021",
            "liuyi0922",
            "kevinzhow",
            "DIYgod",
            "zoeyzhou1103",
            "caizhenghai",
            "DinChao",
            "KidyLee",
            "YunYouJun",
            "jesselaunz",
            "xds2000",
            "baiwusanyu",
            "laobaishare",
            "wanerfu",
            "Caijingtianxia",
            "iskyzh",
            "zty0826",
            "gong_cn",
            "zhongerxin",
            "Li_miao_wen",
            "ouranswers_",
            "yfractal",
            "Jiaxi_Cui",
            "iWillDev",
            "JJH_Chi",
            "leiyatsaan",
            "Raymond_Hou_",
            "eryidebiji",
            "Gruff1561002",
            "lvloomystery",
            "noobnooc",
            "lcayu",
            "xieisabug",
            "jrenc2002",
            "GoJun315",
            "suaihk",
            "_wissx",
            "lincolnstark5",
            "kiwiflysky",
            "KumaTea0",
            "__RedForest",
            "ivyliner",
            "oldj",
            "Hawstein",
            "joyqi",
            "_sluke_",
            "sunshineg",
            "pythonhunter__",
            "adaaaamwen",
            "tufucheung",
            "iamcheyan",
            "rickywang233",
            "shmily7",
            "EZFIX_",
            "dream_qiang",
            "wanghao8080",
            "jameszz343698",
            "patrici00662047",
            "bestlacklock",
            "FeigelC35583",
            "fyfyfm",
            "silosrc",
            "expatlevi",
            "modaotool",
            "recatm",
            "abskoop",
            "shuziyimin",
            "sunbelife"

            "vista8",
            "dotey",
            "op7418",
            "xicilion",
            "WaytoAGI",
            "hanqing_me",
            "jesselaunz",
            "lewangx",
            "JefferyTatsuya",
            "FinanceYF5",
            "thinkingjimmy",
            "oran_ge",
            "99aico",
            "XDash",
            "GlocalTerapy",
            "fuxiangPro",
            "Gorden_Sun",
            "indigo11",
            "NazareAmarga",
            "alvxaro",
            "euovitinn",
            "HugoGloss",
            "lacerda",
            "rafauccman",
            "maisa",
            "ciclopin",
            "luscas",
            "QuebrandoOTabu",
            "NetflixBrasil",
            "davidhazony",
            "YosephHaddad",
            "netanyahu",
            "Israel",
            "TheMossadIL",
            "RozRothstein",
            "IDF",
            "AviMayer",
            "HillelNeuer",
            "Ostrov_A",
            "MOSSADil",
            "fuadkawther",
            "melhamy",
            "m3takl",
            "Shuounislamiya",
            "hureyaksa",
            "s_alharbi2020",
            "oamaz7",
            "drassagheer",
            "saiedibnnasser",
            "Ahmadmuaffaq",
            "NasserAwadQ",
            "RFI_Cn",
            "x666psy",
            "GYEDI15",
            "wshr4310",
            "dyingpepper",
            "99Chuliuxiang",
            "JoanChe92404610",
            "power_up___",
            "HuYongHuYong",
            "msw5278",
            "riz2266",
            "greeeeenbabe_",
            "EllieLocal",
            "staysexystacy",
            "412cute_sun_sun",
            "mattymatty41214",
            "kittycornisme",
            "carpe_diem_po",
            "jcc012197519",
            "mattymatty417",
            "xiuyanxiuyan123",
            "rattanar11",
            "ming12345_ming",
            "ozzyozz35139092",
            "jeffery8910",
            "The_JamesJordan",
            "CapitalOfficial",
            "imacelebrity",
            "JamesArthur23",
            "bbceastenders",
            "thismorning",
            "romankemp",
            "JoshDevineDrums",
            "ollymurs",
            "itvcorrie",
            "TheXFactor",
            "thvphoto",
            "KTH_Facts",
            "vantecentric",
            "VGlobalUnion",
            "kthprettyhands",
            "Taehyungimpact",
            "healwithtae",
            "taeguide",
            "1230ZONE",
            "DailylofV",
            "loopskthv",
            "I_Am_Winter",
            "Kayjnr10",
            "kwadwosheldon",
            "sportingking365",
            "sarkodie",
            "thenanaaba",
            "tv3_ghana",
            "gyaigyimii",
            "AsieduMends",
            "the_marcoli_boy",
            "_Rexxxx1",
            "lalisahourIy",
            "LaliceUpdates",
            "nftbadger",
            "fubarhumor",
            "bellacatsu",
            "FunnymanPage",
            "klip_ent",
            "TheFigen_",
            "allymelons",
            "Enezator",
            "SEMichigan_Wx",
            "SetsetseDan",
            "AndrewElswickWX",
            "Mudim49",
            "TwistedJWx",
            "mcguiredaniel15",
            "weathermannick1",
            "Snn36551819",
            "SFMG_",
            "ks_weather_guy",
            "Sansan37431979",
            "GNZBoi",
            "wxManSmith22",
            "XHistoriek",
            "AntoineMommertz",
            "wheelieweather",
            "NatalieTaylorWx",
            "BenCohenTC",
            "tornadokie",
            "ErikPucek",
            "Henrik47970015",
            "Stormycat771",
            "christianthode3",
            "heyitsdj42",
            "ThomasO73237185",
            "DanDaManBeamish",
            "NdabaFactual",
            "tkanarsky",
            "BBCSouthNews",
            "RealBostonMedia",
            "boston25",
            "maureencaught",
            "BostonDotCom",
            "7News",
            "BwtrPolice",
            "OnlyInBOS",
            "PDChinese",
            "XiaozhPhD04",
            "zhang_heqing",
            "KELMAND1",
            "Fabianduduosaka",
            "CNS1952",
            "zaobaosg",
            "LM62710",
            "Vxujianing",
            "USA_Silly",
            "XinhuaChinese",
            "usembassydhaka",
            "cnni",
            "yiyansheng",
            "washingtonpost",
            "CNN",
            "WeiyuanOttawa",
            "TIME",
            "TinaDITH",
            "ABC",
            "CBSNews",
            "nytimes",
            "lisakashinsky",
            "BostonSatire",
            "maura_healey",
            "wutrain",
            "JonathanCohn",
            "AEON_netsuper",
            "sakuma_seika",
            "hisense_japan",
            "maxellJP",
            "Blueofficial_jp",
            "Sony_Xperia_au",
            "dynamjp",
            "edion_PR",
            "schickjapan",
            "BaIkolik",
            "gsarayruhu1905",
            "fotottarena",
            "KramponSport",
            "_samiyenhaber",
            "nexustransfer",
            "AliNaciKucuk",
            "ertansuzgun",
            "asistanaliz",
            "TransferWeb1",
            "SportsDigitale",
            "mummyengeng",
            "igibzguz",
            "Lora00l",
            "PpEL04_",
            "cngnlumd",
            "Plasalidtidkho_",
            "vanny_helsing",
            "PpanEngfa",
            "littleprince_21",
            "PhenixEnglot",
            "s0ba4k0",
            "manumansur2",
            "ThanaminV",
            "souza_edits",
            "hikingskiing",
            "DivesTech",
            "Teslarati",
            "DirtyTesLa",
            "woodhaus2",
            "DriveTeslaca",
            "TeslaCharging",
            "teslaownersSV",
            "teardowntitan",
            "Gfilche",
            "p_ferragu",
            "alex_avoigt",
            "MartinViecha",
            "TSLAFanMtl",
            "EmmetPeppers",
            "ray4tesla",
            "TeslaPodcast",
            "TeslaBoomerMama",
            "JoeTegtmeyer",
            "JCDoubleTaxed",
            "DemsAbroadTax",
            "USAccidental",
            "AbroadRebecca",
            "GOPIsrael",
            "wisecroneknows",
            "Amy_From_Sydney",
            "NicklesLee",
            "ExpatriationLaw",
            "suzanneherman1",
            "FATCAed",
            "LHHispanic",
            "zaynmalik",
            "HLDMedia",
            "wasia_project",
            "Ioverspring",
            "patwalterstv",
            "reticentdnp",
            "dailyjlocke",
            "jasondebolt",
            "GerberKawasaki",
            "WholeMarsBlog",
            "TroyTeslike",
            "ICannot_Enough",
            "Teslaconomics",
            "farzyness",
            "stevenmarkryan",
            "heydave7",
            "SawyerMerritt",
            "garyblack00",
            "Inc",
            "adage",
            "Tiffani_Bova",
            "Digiday",
            "FastCoDesign",
            "LBBOnline",
            "MarketingProfs",
            "Adweek",
            "mitsmr",
            "Campaignmag",
            "FastCompany",
            "gauravkheterpal",
            "amit_sfdc",
            "SalesforceAdmns",
            "salesforce",
            "swbjoyce",
            "charlieisaacs",
            "trailhead",
            "kavindrapatel",
            "rlvanessagrant",
            "parkerharris",
            "Benioff",
            "HsiangYu_Liu",
            "BlueBellsForest",
            "GingerDuan",
            "Be_Free_0526",
            "Hello_world_G",
            "MichaelKovrig",
            "CHRDnet",
            "YesterdayBigcat",
            "elonmusk",
            "patrici00662047",
            "Marionette_Sa",
            "realDonaldTrump",
            "elonmusk",
            "jakobsonradical",
            "investorMM",
            "LuvLetter_moe",
            "thinking_panda",
            "paranormal_2ch",
            "whyyoutouzhele",
            "SuuKn3",
            "zfcsoftware",
            "ju_kfc",
            "sarperavci",
            "drayqin",
            "Sindigaisaac",
            "exfil0",
            "harshleenchawl2",
            "DownloadVideo_",
            "nico_jeannen",
            "imwsl90",
            "tinyfool",
            "dotey",
            "DataChaz",
            "rin_k_ba61nka",
            "PLAawesome",
            "AI_dailyPic",
            "Yamkaz",
            "toyxyz3",
            "solarjunes",
            "TASUKU2023",
            "auditore_k",
            "bearbig",
            "lvwzhen",
            "pricarat",
            "honoka82362654",
            "tsuyopon0730",
            "proselector123",
            "TheGuruYouKnow",
            "FaradayFuture",
            "JulianKlymochko",
            "rei54847197",
            "tomatosp55",
            "LuoshengPeng",
            "Sora_No27",
            "WolfpackReports",
            "miniminimusic",
            "JoeBiden",
            "tesuta001",
            "cissan_9984",
            "AmericanAir",
            "NIOGlobal",
            "investorMM",
            "thinking_panda",
            "elonmusk",
            "sohbunshu",
            "elonmusk",
            "sohbunshu",
            "liyaosha",
            "crypt0grapherr",
            "roaneatan",
            "tkzwgrs",
            "madaomoshiroi",
            "CarlZha",
            "AMAZlNGNATURE",
            "twinewss",
            "paranormal_2ch",
            "JamesLucasIT",
            "Marionette_Sa",
            "Cydiar404",
            "luca_____1114",
            "bboczeng",
            "roriyatu",
            "Duomaomao9966",
            "HUANGDDXZ",
            "theCaptury",
            "rohanpaul_ai",
            "caizhenghai",
            "Crypto_hedyEth",
            "whyyoutouzhele",
            "jakobsonradical",
            "whyyoutouzhele",
            "nbykos",
            "thinking_panda",
            "BornAKang",
            "JZhen72937",
            "MOSSADil",
            "investorMM",
            "mrbear1024",
            "NeverteIImeodd",
            "street99fight2",
            "8co28",
            "fight444justice",
            "Todai_Renai",
            "yxxx206181",
            "paranormal_2ch",
            "crowkaka_no996",
            "jakobsonradical",
            "c0r1eone",
            "Japan_Emb_inCN",
            "Stv_Lynn",
            "7h3h4ckv157",
            "investorMM",
            "Shanice_Nici",
            "JOSTAR_PRODUCER",
            "wuren_Ltd",
            "hsn8086",
            "thinking_panda",
            "biantaidb",
            "zaobaosg",
            "torontobigface",
            "syen_white",
            "paranormal_2ch",
            "dontbesilent12",
            "shadouyoua",
            "jinwanxin",
            "tungnd_13",
            "fengjingduhao5",
            "unixzii",
            "elonmusk",
            "jakobsonradical",
            "investorMM",
            "Marionette_Sa",
            "thinking_panda",
            "HubaVision",
            "ooeli_eth",
            "Tesla_Optimus",
            "harimokawaii",
            "BingxunYao",
            "elonmusk",
            "Cldeop",
            "butz_yung",
            "nbykos",
            "__Inty__",
            "elonmusk",
            "xiaojingcanxue",
            "DiverX_VR",
            "Marionette_Sa",
            "Aichijiandanxyz",
            "laozhangisme",
            "nbykos",
            "bountywriteups",
            "happy_modeling",
            "hatadanna",
            "Basefount",
            "kirawontmiss",
            "tyomateee",
            "Jackywine",
            "ooeli_eth",
            "zhangmanman555",
            "bountywriteups",
            "raycat2021",
            "jinx_aiart",
            "zhonghuifufu",
            "largepotatol",
            "elonmusk",
            "investorMM",
            "thinking_panda",
            "paranormal_2ch",
            "JZhen72937",
            "jefflijun",
            "Hammer_EU_9527",
            "novasarc01",
            "elonmusk",
            "investorMM",
            "thinking_panda",
            "linhai203",
            "rounak131106",
            "realDonaldTrump",
            "Yangyixxxx",
            "oyatsu009",
            "bearbig",
            "houshayueguang",
            "zhangmanman555",
            "LiveOverflow",
            "Jerry00107966",
            "ntwdzkn",
            "yuashwe",
            "balagrivine_",
            "OreoBiscui74046",
            "teachaerli",
            "DemNikoArt",
            "hisa__N_",
            "liyaosha",
            "h5LPyKL7TP6jjop",
            "TruthMedia123",
            "elonmusk",
            "investorMM",
            "thinking_panda",
            "Ehco1996",
            "nmatt0",
            "myfxtrader",
            "knowledgefxg",
            "street99fight2",
            "survey_bot_1",
            "tinyfool",
            "supahvee1234",
            "muscle_penguin_",
            "8co28",
            "Kenntnis22",
            "torontobigface",
            "0427SMtieshou",
            "jye1968",
            "__Inty__",
            "Krit_Sec",
            "BertJanCyber",
            "Goryodynasty",
            "imwsl90",
            "mrbear1024",
            "xqliu",
            "lutinggelvshi89",
            "KN0X55",
            "thinking_panda",
            "investorMM",
            "elonmusk",
            "LUOXIANGZY",
            "yuaanlin",
            "aigclink",
            "Yali1028",


        ]
    },
    # {
    #     'channel_id': 2238825797,
    #     'db_name': 'twitter_love_girl',
    #     'session': 'twitter_love_girl_session',
    #     'twitter_users': [
    #         'Arkikir',
    #         'cpdd34d',
    #         'OLgirl_Akina_sc',
    #         '666xiaoliu',
    #         'nidonenko',
    #         'Arkikir',
    #         'Tainted_M',
    #         'Asai_chan_',
    #         'mizukinoxxxx',
    #         'Kana_Momonogi',
    #         'yua_mikami',
    #         'Kana_Momonogi',
    #         'kanaMomonogiR18',
    #         'rukaKANAE',
    #         'kizaki_jessica',
    #         'mila_azul',
    #         'LenaandersonFA',
    #         'TheLenaAnderson',
    #         'xuanzijutwotu',
    #         'NanaModeltt',
    #         'xiaozhiNana',
    #         '0511dyst',
    #         'naiqiu000',
    #         'naiqiu666',
    #         'Luoye3639210483',
    #         'pjms_miku_EN',
    #         'global_miku',
    #         'pjms_miku',
    #         'scrt_miku',
    #         'MilaAzulChan',
    #         'UNI_Chen999',
    #         'sby_200',
    #         '9_jfm',
    #         'MidAprilz',
    #         'KanaSaotome_',
    #         'kechunyaoll',
    #         'BNDBJKXF',
    #         'Songchuanbb',
    #         'mocck0216',
    #         'Mook717171',
    #         'PDBDSAMA',
    #         'EatHoneyPudding',
    #         'Mostion1ess',
    #         'kovoii_',
    #         'galaxyrita_',
    #         'uu_TvT',
    #         'maimaifukui',
    #         'kepaobb',
    #         '77buaoye',
    #         'Lris49638712',
    #         'Lisachan05',
    #         'fukada0318',
    #         'xiskoisstyssyl',
    #         'RenyuNami',
    #         'xiaotao6666',
    #         'OLrin_00',
    #         'ai_imnida0525',
    #         'sama31598328',
    #         'liuguangyinji',
    #         'xizi1840',
    #         'Adaydream617',
    #         'nnian_',
    #         'guoqimixianmeow',
    #         'AidanFarme32187',
    #         'YourMiracle_18',
    #         'alicekemone',
    #         'cute_mmira',
    #         'Inari_global',
    #         'mizuginomizuki',
    #         'rei_scrt02',
    #         'omakeno_nana',
    #         'hoshino_miyu721',
    #         'OoChiyuUoO',
    #         'hazirai_ami',
    #         'rankodazo',
    #         'mikutan_nurse',
    #         'ranko_ya',
    #         'Shizukunotamari',
    #         'misaki_melon',
    #         'saki_p_p_e',
    #         'inari_sc',
    #         'hina_ogland',
    #         'misaki_dayo88',
    #         'kuru_milkxx',
    #         'rihop_ch7',
    #         'airi_rinrin_x',
    #         'rin_sub_00',
    #         'siorisandesuyo',
    #         'darichu_ru',
    #         'mi0ura',
    #         'mi0uraR18',
    #         'panpianoatelier',
    #         'na_na_m1218',
    #         'yeyedasai',
    #         'azhu1997_',
    #         'shimiso108',
    #         'appe_45Ch',
    #         'mikoto_no_oto',
    #         'AcostaLaur30608',
    #         'hina_nyaa_',
    #         'miyu22958',
    #         'ura_miyu2626',
    #         'yururina_',
    #         'nagomi_rooom',
    #         'nagomi_ura_heya',
    #         'miu_nemutai',
    #         'misaki_kana88',
    #         'kuru_milkx',
    #         'kishi_aino',
    #         '_nagihikaru',
    #         'Saika_Kawakita',
    #         'm_nanami_m',
    #         'chee828',
    #         'rei_kamiki',
    #         'reikamiki_sub',
    #         'shiorionesan',
    #         'kunkunkun181',
    #         '_jiujiujiujiu',
    #         'fourlovesss_',
    #         'mutou_ayaka',
    #         'Lu_bbL',
    #         'kunkunkun188',
    #         'frid_klai',
    #         'Limokkii',
    #         'justkillllme',
    #         'xiaogualu',
    #         'mutoayaka12',
    #         'Naimei0727',
    #         'naimei0023',
    #         'FFan688'
    #     ]
    # },
    # {
    #     'channel_id': 2339485461,
    #     'db_name': 'twitter_fun',
    #     'session': 'twitter_fun_session',
    #     'twitter_users': [
    #         'hsn8086',
    #         'UnzipHelper',
    #     ]
    # },
    # Add more configurations as needed
]


# Remove the global variables as they are now part of configurations
# channel_id = 2238825797
# db_name = 'twitter_chinese'
x_guest_token = str(12345678)


def get_x_guest_token():
    # Set up Chrome options (optional: for headless mode)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Specify the path to chromedriver
    service = Service('/usr/lib/chromium-browser/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the specified URL
        driver.get("https://x.com/patrici00662047")

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)

        # Get all cookies
        cookies = driver.get_cookies()
        print(cookies)
        print(cookies[0]['value'])
        guest_token = cookies[0]['value']

        if guest_token:
            print(f"X-Guest-Token: {guest_token}")
            return guest_token
        else:
            print("X-Guest-Token not found in cookies")
            return None
    finally:
        driver.quit()


def refresh_guest_token():
    global x_guest_token
    x_guest_token = get_x_guest_token()


def parse_twitter_user_timeline(user_tweets):
    tweets_with_media = []

    # Navigate to the instructions containing tweet entries
    instructions = user_tweets.get('data', {}).get('user', {}).get('result', {}) \
        .get('timeline_v2', {}).get('timeline', {}).get('instructions', [])

    for instruction in instructions:
        if instruction.get('type') == 'TimelineAddEntries':
            entries = instruction.get('entries', [])
            for entry in entries:
                content = entry.get('content', {})
                item_content = content.get('itemContent', {})

                if item_content.get('itemType') == 'TimelineTweet':
                    tweet = item_content.get('tweet_results', {}).get('result', {})
                    legacy = tweet.get('legacy', {})
                    tweet_id = legacy.get('id_str')
                    text = legacy.get('full_text', '')

                    # Initialize media URLs list
                    media_urls = []

                    # Check for extended_entities and media
                    extended_entities = legacy.get('extended_entities', {})
                    media = extended_entities.get('media', [])

                    for m in media:
                        media_type = m.get('type')
                        if media_type == 'photo':
                            media_url = m.get('media_url_https')
                            if media_url:
                                media_urls.append(media_url)
                        elif media_type in ['video', 'animated_gif']:
                            variants = m.get('video_info', {}).get('variants', [])
                            # Select the MP4 variant with the highest bitrate
                            mp4_variants = [v for v in variants if v.get('content_type') == 'video/mp4']
                            if mp4_variants:
                                # Sort by bitrate descending and select the highest
                                mp4_variants.sort(key=lambda x: x.get('bitrate', 0), reverse=True)
                                media_url = mp4_variants[0].get('url')
                                if media_url:
                                    media_urls.append(media_url)

                    if media_urls:
                        tweets_with_media.append({
                            'tweet_id': tweet_id,
                            'text': text,
                            'media_urls': media_urls
                        })

    return tweets_with_media


def extract_tweet(tweet_data):
    """Extract tweet from tweet_data"""
    tweet = {}
    try:
        tweet['tweet_id'] = tweet_data.get('rest_id')
        tweet['text'] = tweet_data.get('legacy', {}).get('full_text')
        tweet['created_at'] = tweet_data.get('legacy', {}).get('created_at')
        user = tweet_data.get('core', {}).get('user_results', {}).get('result', {})

        tweet['user_id'] = user.get('rest_id')
        tweet['username'] = user.get('legacy', {}).get('screen_name')
        tweet['name'] = user.get('legacy', {}).get('name')

        extended_entities = tweet_data.get('legacy', {}).get('extended_entities', {})
        media = extended_entities.get('media', [])

        tweet['images'] = [item.get('media_url_https') for item in media if item.get('type') == 'photo']
        tweet['videos'] = []
        tweet['video_thumb'] = None  # Initialize video_thumb to None

        for item in media:
            if item.get('type') == 'video':
                variants = item.get('video_info', {}).get('variants', [])
                best_variant = max(variants, key=lambda x: x.get('bitrate', 0), default={})
                tweet['videos'].append(best_variant.get('url'))
                tweet['video_thumb'] = item.get('media_url_https')

        return tweet

    except (KeyError, AttributeError) as e:
        print("Error extracting data:", e)
        return None  # Return None if extraction fails


import random
import string
import time


def generate_random_cookie():
    # Helper function to generate random alphanumeric string
    def random_string(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # Generate random timestamp (within a reasonable range)
    timestamp = int(time.time() * 1000000) + random.randint(-1000000, 1000000)

    # Generate random 19-digit number for gt
    gt = ''.join(random.choices(string.digits, k=19))

    # Generate random base64-encoded string for personalization_id
    personalization_id = random_string(22)

    cookie = f"night_mode=2; kdt={random_string(30)}; dnt=1; att=1-{random_string(30)}; " \
             f"guest_id=v1%3A{timestamp}; guest_id_marketing=v1%3A{timestamp}; " \
             f"guest_id_ads=v1%3A{timestamp}; gt={gt}; " \
             f'personalization_id="v1_{personalization_id}=="'

    return cookie


def fetch_user_tweets(user_id, count=20):
    global x_guest_token
    url = "https://api.x.com/graphql/Tg82Ez_kxVaJf7OPbUdbCg/UserTweets"

    variables = {
        "userId": user_id,
        "count": count,
        "includePromotedContent": True,
        "withQuickPromoteEligibilityTweetFields": True,
        "withVoice": True,
        "withV2Timeline": True
    }

    features = {
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "communities_web_enable_tweet_community_results_fetch": True,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "articles_preview_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "creator_subscriptions_quote_tweet_preview_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_enhance_cards_enabled": False
    }

    field_toggles = {
        "withArticlePlainText": False
    }

    params = {
        "variables": json.dumps(variables),
        "features": json.dumps(features),
        "fieldToggles": json.dumps(field_toggles)
    }

    headers = {
        "Host": "api.x.com",
        "Cookie": generate_random_cookie(),
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "X-Guest-Token": x_guest_token,
        "X-Twitter-Client-Language": "en",
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Twitter-Active-User": "yes",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://x.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://x.com/",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6,ko;q=0.5",
        "Priority": "u=1, i"
    }

    response = requests.get(url, params=params, headers=headers)

    return response


def get_user_media(user_id, count=20):
    response = fetch_user_tweets(user_id)

    # print(response)
    # print(response.text)
    if response.status_code == 200:
        try:
            tweets = parse_twitter_user_timeline(response.json())
            print(tweets)
        except:
            print(response)
            print(response.text)
            return None
        return tweets
    else:
        return None


def format_tweet_caption(tweet):
    """Formats tweet text and adds tweet URL."""
    tweet_url = f"https://x.com/123/status/{tweet['tweet_id']}"
    caption = f"{tweet['text']}\n`{tweet_url}`"
    return caption


class TwitterUserHandler(BaseHandler):
    """
    Handler for fetching and processing Twitter user media.
    """

    def __init__(self, channel_id: int, db_name: str, telegram_session: str, user_id: str, count: int = 20):
        """
        Initializes the TwitterUserHandler with necessary parameters.

        Args:
            channel_id (int): The Telegram channel ID.
            db_name (str): The name of the database.
            user_id (str): The Twitter user ID to fetch media for.
            count (int, optional): Number of tweets to fetch. Defaults to 20.
        """
        super().__init__(channel_id, db_name, telegram_session)
        self.user_id = user_id
        self.count = count

    def fetch_and_send_media(self):
        """
        Fetches media from the specified Twitter user and sends it to Telegram.
        """
        tweets_data = None
        for i in range(3):
            try:
                tweets_data = get_user_media(self.user_id, self.count)
                break
            except KeyError:
                print(f'Error: tweets_data. Skipping...')
                refresh_guest_token()
                continue
        if not tweets_data:
            print("No tweets data fetched.")
            return
        for tweet in tweets_data:
            print(tweet)
            tweet_id = tweet.get('tweet_id')
            media_urls = tweet.get('media_urls', [])

            if not media_urls:
                print(f"No media found in tweet {tweet_id}. Skipping.")
                continue

            # Use the format_tweet_caption function to create the caption
            caption = format_tweet_caption(tweet)
            for media_url in media_urls:
                if self.db_handle.url_exists(tweet_id, media_url):
                    print(f"Media {media_url} already exists in tweet {tweet_id}. Skipping.")
                    continue
                if media_url.endswith(('.jpg', '.png', '.gif')):
                    success = self.send_photo_to_telegram(media_url, caption)
                    if success:
                        self.db_handle.insert_url(tweet_id, media_url)
                        print(f"Photo from tweet {tweet_id} sent successfully.")
                    else:
                        print(f"Failed to send photo from tweet {tweet_id}.")
                elif media_url.endswith('.mp4'):
                    success = self.send_video_to_telegram(media_url, caption)
                    if success:
                        self.db_handle.insert_url(tweet_id, media_url)
                        print(f"Video from tweet {tweet_id} sent successfully.")
                    else:
                        print(f"Failed to send video from tweet {tweet_id}.")
                else:
                    print(f"Unsupported media type for URL: {media_url}")

    def run(self):
        """
        Executes the media fetching and sending process.
        """
        self.fetch_and_send_media()
        self.disconnect_telegram()


import requests


def fetch_profile_spotlights(screen_name):
    global x_guest_token
    url = "https://api.x.com/graphql/BQ6xjFU6Mgm-WhEP3OiT9w/UserByScreenName"

    params = {
        "variables": f'{{"screen_name":"{screen_name}"}}',
        "features": '{"hidden_profile_subscriptions_enabled":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
        "fieldToggles": '{"withAuxiliaryUserLabels":false}'
    }

    headers = {
        "Host": "api.x.com",
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "X-Guest-Token": x_guest_token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
    }

    response = requests.get(url, params=params, headers=headers)
    return response.json()


if __name__ == "__main__":
    load_dotenv()


    def main():
        for config in CONFIGURATIONS:
            channel_id = config['channel_id']
            db_name = config['db_name']
            session = config['session']
            twitter_users = config['twitter_users']

            twitter_users = list(set(twitter_users))

            for twitter_user in twitter_users:
                for i in range(3):
                    try:
                        result = fetch_profile_spotlights(twitter_user)
                        rest_id = result['data']['user']['result']['rest_id']
                        print(f'User: {twitter_user}, rest_id: {rest_id}')
                        break
                    except KeyError:
                        print(f'Error: Unable to fetch rest_id for user {twitter_user}. Skipping...')
                        refresh_guest_token()
                        continue
                else:
                    print(f"Failed to fetch rest_id for user {twitter_user} after retries.")
                    continue  # Skip to the next user if all retries fail

                USER_ID = rest_id
                handler = TwitterUserHandler(
                    channel_id=channel_id,
                    db_name=db_name,
                    telegram_session=session,
                    user_id=USER_ID
                )
                handler.run()


    while True:
        main()
