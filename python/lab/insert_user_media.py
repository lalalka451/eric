from all_twitter_user import all_twitter_users1, all_twitter_users2, all_twitter_new_user
from rss_send import db_handler


# 1 all
# 2 all2
# 3 new
db_handle2 = db_handler('twitter_user_name', 'media')
# all_twitter_users = all_twitter_users2
all_twitter_users = all_twitter_new_user
for user in all_twitter_users:
    if not db_handle2.thread_id_exists(user):
    #     db_handle2.insert_url(user,'')
        db_handle2.insert_url3(user,'',3)
    db_handle2.set_url(user)
    print(user)