import re

urls = [
    "https://p9-sign.douyinpic.com/tos-cn-i-p14lwwcsbr/31089e309cdb4cc0ad8df282410ca3ee~tplv-p14lwwcsbr-7.image?x-expires=1728208800&x-signature=n2HvuhY%2BklCLd9VJq7ioW7tMxRo%3D&from=2064092626&se=false&sc=image&biz_tag=aweme_comment&l=20241006124732B8581C1AFEC72F39C0C1",
    "https://p26-sign.douyinpic.com/tos-cn-i-p14lwwcsbr/31089e309cdb4cc0ad8df282410ca3ee~tplv-p14lwwcsbr-7.image?x-expires=1728208800&x-signature=RettODoBGzxuKWvavvgnMt1Gu%2Bc%3D&from=2064092626&se=false&sc=image&biz_tag=aweme_comment&l=20241006124732B8581C1AFEC72F39C0C1",
    "https://p3-sign.douyinpic.com/tos-cn-i-p14lwwcsbr/31089e309cdb4cc0ad8df282410ca3ee~tplv-p14lwwcsbr-7.jpeg?x-expires=1728208800&x-signature=G05%2BOuGembI8O9zimOafAQctVq8%3D&from=2064092626&se=false&sc=image&biz_tag=aweme_comment&l=20241006124732B8581C1AFEC72F39C0C1",
    "https://p3-sign.douyinpic.com/tos-cn-i-p14lwwcsbr/31089e309cdb4cc0ad8df282410ca3ee~tplv-p14lwwcsbr-7.image?x-expires=1728208800&x-signature=GdSqPvhDi67g%2BSbdhG%2FxRVglhUk%3D&from=2064092626&se=false&sc=image&biz_tag=aweme_comment&l=20241006124732B8581C1AFEC72F39C0C1"
]

pattern = r"https://.*?sign\.douyinpic\.com/.*?/(.*?)(?=[~?])"

for url in urls:
    match = re.search(pattern, url)
    if match:
        print(match.group(1))
else:
    print("No match found")
