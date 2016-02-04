__author__ = "pradeepbista"

from pymongo import MongoClient
import sys

import util_fetch_tudiabetes as ft
import util_fetch_mongo as fm

## create mongo URI, you may have to change this
MONGODB_URI = 'mongodb://localhost:27017/'

# list of discussion topics is stored in this collection
# for example, http://www.tudiabetes.org/forum/
COLL_DISCUSSION_TOPICS = "discussion_topics"

# complete conversation is stored in this collection
# for example, http://www.tudiabetes.org/forum/t/outraged-and-concerned/48773
COLL_DISCUSSION = "discussions"

# all the user list is stored in this collection
# for example, http://www.tudiabetes.org/forum/users
COLL_USERS = "users"

# summary of a specific user is stored in this collection
# for example, http://www.tudiabetes.org/forum/users/terry4/summary
COLL_USER_SUMMARY = "user_summary"

# list of replies by a user is stored in this collection
# for example, http://www.tudiabetes.org/forum/users/terry4/activity/replies
COLL_USER_REPLY = "user_reply"

# this collection saves specific user/discussion if it has been downloaded.
# In case of interruption during the download this status helps to avoid the downloaded data again.
# {collection_name = "discussions", id:"57213"}
COLL_SAVE_STATUS = "status"

def main(args):
    client = MongoClient(MONGODB_URI)
    db = client.tudiabetes

    #***********************************
    # dump discussip topics and user list
    ft.dump_dicussion_toics(db, COLL_DISCUSSION_TOPICS) # dump discussion topics from the forum
    print "*"*15 + "DISCUSSION LIST SAVED" + "*"*15
    ft.dump_list_users(db, COLL_USERS) # dump all the users list
    print "*"*15 + "USER LIST SAVED" + "*"*15

    #***********************************
    # retrive discussion topic list from mongodb and dump complete discussion
    topic_ids = fm.get_topic_ids(db, COLL_DISCUSSION_TOPICS)  # retrieve list of topic ids and slug from mongo
    ft.dump_discussion(topic_ids, db, COLL_DISCUSSION, COLL_SAVE_STATUS)  # dump all the discussion from forum
    print "*"*15 + "DISCUSSIONS SAVED" + "*"*15

    # retrieve user list from mongodb and dump user information: summary and replies
    users = fm.get_users(db, COLL_USERS)  # retrieve list of usernames
    ft.dump_user_summary(users, db, COLL_USER_SUMMARY, COLL_SAVE_STATUS)  # dump user summary for all users
    print "*"*15 + "USER SUMMARY SAVED" + "*"*15
    ft.dump_user_replies(users, db, COLL_USER_REPLY, COLL_SAVE_STATUS)  # dump user replies for all users
    print "*"*15 + "DISCUSSION REPLLIES SAVED" + "*"*15

if __name__ == '__main__':
    main(sys.argv[1:])