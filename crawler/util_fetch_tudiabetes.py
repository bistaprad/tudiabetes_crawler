__author__ = "pradeepbista"

import requests
import pprint
import time


###############################
## get all discussions topics
def dump_dicussion_toics(db, COLL_DISCUSSION_TOPICS):
    coll = db[COLL_DISCUSSION_TOPICS]

    page = 1  # starts from 1
    while True:

        # time.sleep(1)

        discussion_url = "http://www.tudiabetes.org/forum/latest.json?no_definitions=true&order=default&page=" + str(
                page) + "&per_page=30"

        ##get the list of topics from the json response
        json_discussion = requests.get(discussion_url).json()
        topics = json_discussion["topic_list"]["topics"]

        if (len(topics) == 0):
            break
        else:
            page += 1
            print "page: %d topics: %d" % (page, len(topics))
            # dump the discussion in mongodb
            for t in topics:
                res = coll.insert_one(t)
                print "id inserted: " + str(t["id"]) + "--" + str(res)


######################
# dump_dicussion_toics()
## get a complete discussion

def dump_discussion(ids, db, COLL_DISCUSSION):
    coll = db[COLL_DISCUSSION]
    for id in ids:
        discussion_id = id[0]
        slug = id[1]
        discussion_url = "http://www.tudiabetes.org/forum/t/" + slug + "/" + str(discussion_id) + ".json"

        ##get the list of topics from the json response
        json_discussion = requests.get(discussion_url).json()
        # pprint.pprint(json_discussion)

        ##find all replies to this discussion
        ## ???????

        ## save to mongodb
        res = coll.insert_one(json_discussion)
        print "discussion inserted: " + str(id) + "--" + slug + "--" + str(res)


## to remove
# slug = "i-started-on-afrezza-last-night"
# discussion_id = str(23316)
# discuss = [slug, discussion_id]
# dump_discussion(discuss)


####################
## get list of users
def dump_list_users(db, COLL_USERS):
    coll = db[COLL_USERS]

    epoch = int(round(time.time() * 1000))
    page = 1  # starts from 1
    while True:

        # time.sleep(1)
        users_url = "http://www.tudiabetes.org/forum/directory_items.json?order=likes_received&page=" + str(
                page) + "&period=all&_=" + str(epoch)
        users_url = "http://www.tudiabetes.org/forum/directory_items.json?order=likes_received&page=" + str(
                page) + "&period=all&_=" + str(epoch)

        json_users = requests.get(users_url).json()
        users = json_users["directory_items"]

        if (len(users) == 0):
            break
        else:
            page += 1
            print "page: %d users: %d" % (page, len(users))
            ## save all users to mongodb
            for u in users:
                coll.insert_one(u)
                # print u["user"]["username"]
                print "user inserted: " + u["user"]["username"]


###################
## get user summary
def dump_user_summary(usernames, db, COLL_USER_SUMMARY):
    collection = db[COLL_USER_SUMMARY]

    for username in usernames:
        user_url = "http://www.tudiabetes.org/forum/users/" + username + "/summary.json"

        json_user = requests.get(user_url).json()
        user = json_user

        ## dump to mongodb
        collection.insert_one(user)
        print "user inserted: " + username


# dump_user_summary("terry4")



###################
## get user replies

def dump_user_replies(usernames, db, COLL_USER_REPLY):
    collection = db[COLL_USER_REPLY]
    for username in usernames:
        epoch = int(round(time.time() * 1000))
        offset = 0  # starts from 0
        while True:
            reply_url = "http://www.tudiabetes.org/forum/user_actions.json?offset=" + str(
                    offset) + "&username=" + username + "&filter=5&_=" + str(epoch)

            json_reply = requests.get(reply_url).json()
            reply = json_reply["user_actions"]

            if (len(reply) == 0):
                break
            else:
                offset += 30
                for r in reply:
                    ### save to mongodb
                    collection.insert_one(r)
                    print "user reply inserted: " + username

                    # dump_user_replies("larryest2")
