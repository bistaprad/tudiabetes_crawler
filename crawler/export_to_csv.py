__author__ = "pradeepbista"

from pymongo import MongoClient
import sys

import util_fetch_mongo as fm
import pprint as pp
import util_export_to_csv as ex

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

# user description stored in this collection
# for example, http://www.tudiabetes.org/forum/users/rgcainmd/activity
COLL_USER_DESCRIPTION = "user_description"

# this collection saves specific user/discussion if it has been downloaded.
# In case of interruption during the download this status helps to avoid the downloaded data again.
# {collection_name = "discussions", id:"57213"}
COLL_SAVE_STATUS = "status"

def main(args):

    client = MongoClient(MONGODB_URI)
    db = client.tudiabetes

    if args[0] == "discussions":
        # export discussions to csv
        ex.discussions(db, COLL_DISCUSSION, COLL_SAVE_STATUS)


    # elif args[0] == "user_list":
        # ft.dump_list_users(db, COLL_USERS, COLL_SAVE_STATUS) # dump all the users list
        # print "*"*15 + "USER LIST SAVED" + "*"*15

    else:
        print "Invalid argument !!! \n"
        print "Use arguments as below in sequential order"
        print "1) To export discussions in csv format : discussions"
        print "2) To save the user list: user_list"

if __name__ == '__main__':
    main(sys.argv[1:])