__author__ = "pradeepbista"

from pymongo import MongoClient
import sys

import util_fetch_tudiabetes as ft
import util_fetch_mongo as fm

MONGODB_URI = 'mongodb://localhost:27017/'
COLL_DISCUSSION_TOPICS = "discussion_topics"
COLL_DISCUSSION = "discussions"
COLL_USERS = "users"
COLL_USER_SUMMARY = "user_summary"
COLL_USER_REPLY = "user_reply"


def main(args):
    client = MongoClient(MONGODB_URI)
    db = client.tudiabetes

    # dump discussion topics from the forum
    ft.dump_dicussion_toics(db, COLL_DISCUSSION_TOPICS)

    # retrieve list of topic ids and slug from mongo
    topic_ids = fm.get_topic_ids(db, COLL_DISCUSSION_TOPICS)

    # dump all the discussion from forum
    ft.dump_discussion(topic_ids, db, COLL_DISCUSSION)

    # dump all the users list
    ft.dump_list_users(db, COLL_USERS)

    # retrieve list of usernames
    users = fm.get_users(db, COLL_USERS)

    # dump user summary for all users
    ft.dump_user_summary(users, db, COLL_USER_SUMMARY)

    # dump user replies for all users
    ft.dump_user_summary(users, db, COLL_USER_REPLY)


if __name__ == '__main__':
    main(sys.argv[1:])
