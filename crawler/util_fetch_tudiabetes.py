__author__ = "pradeepbista"

import requests
import pprint
import time
import util_fetch_mongo as fm


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
## get a complete discussion

def dump_discussion(ids, db, COLL_DISCUSSION, COLL_SAVE_STATUS):
    coll = db[COLL_DISCUSSION]
    coll_status = db[COLL_SAVE_STATUS]

    # find the list discussion id which have not been saved in mongodb
    unsaved_ids = []
    for id in ids:
        if not fm.check_if_saved(db, COLL_SAVE_STATUS, COLL_DISCUSSION, id[0]):
            unsaved_ids.append(id)

    count = 0
    for id in unsaved_ids:

        discussion_id = id[0]
        slug = id[1]

        ##find all replies to this discussion
        page = 1
        discussion_complete = {}
        first = True
        while True:
            discussion_url = "http://www.tudiabetes.org/forum/t/" + slug + "/" + str(
                discussion_id) + ".json?page=" + str(page)

            # if this url doesnt return a json response stop the json request, by breaking this while loop
            try:
                json_discussion = requests.get(discussion_url).json()
                # pprint.pprint(json_discussion)
            except ValueError:
                break
            else:
                page += 1
                if (first):
                    discussion_complete = json_discussion
                    first = False
                else:
                    for p in json_discussion["post_stream"]["posts"]:
                        discussion_complete["post_stream"]["posts"].append(p)
                        # print "post_count:" + str(index) +" >> post_id: " + str(p["id"]) + " >> "+ p["cooked"]

        ## save to mongodb
        res = coll.insert_one(discussion_complete)

        # save this id in "save" collection
        coll_status.insert_one({"collection":COLL_DISCUSSION, "id":id[0]})

        try:
            discussion_complete["post_stream"]["posts"]
        except KeyError:
            replies = 0
        else:
            replies = str(len(discussion_complete["post_stream"]["posts"]))

        print "inserted discussion: count = %s replies = %s [id, slug] = %s):" % (str(count), replies, str(id))
        count += 1


# slug = "word-association-game"
# discussion_id = str(1311)

# slug = "are-we-close-to-a-cure-scientists-think-so"
# discussion_id = str(50840)


## to remove
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
def dump_user_summary(usernames, db, COLL_USER_SUMMARY, COLL_SAVE_STATUS):
    collection = db[COLL_USER_SUMMARY]
    coll_status = db[COLL_SAVE_STATUS]

    # find the list discussion usernames which have not been saved in mongodb
    unsaved_usernames = []
    for username in usernames:
        if not fm.check_if_saved(db, COLL_SAVE_STATUS, COLL_USER_SUMMARY, username):
            unsaved_usernames.append(username)

    # print len(unsaved_usernames)
    for username in unsaved_usernames:
        user_url = "http://www.tudiabetes.org/forum/users/" + username + "/summary.json"

        json_user = requests.get(user_url).json()
        user = json_user

        ## dump to mongodb
        collection.insert_one(user)

        # save this id in "save" collection
        coll_status.insert_one({"collection":COLL_USER_SUMMARY, "id":username})
        print "user summary inserted: " + username


# dump_user_summary("terry4")



###################
## get user replies

def dump_user_replies(usernames, db, COLL_USER_REPLY, COLL_SAVE_STATUS):
    collection = db[COLL_USER_REPLY]
    coll_status = db[COLL_SAVE_STATUS]

    # find the list discussion usernames which have not been saved in mongodb
    unsaved_usernames = []
    for username in usernames:
        if not fm.check_if_saved(db, COLL_SAVE_STATUS, COLL_USER_REPLY, username):
            unsaved_usernames.append(username)

    print len(unsaved_usernames)

    for username in usernames:
        epoch = int(round(time.time() * 1000))
        offset = 0  # starts from 0
        replies_complete = []
        first = True
        while True:
            reply_url = "http://www.tudiabetes.org/forum/user_actions.json?offset=" + str(
                    offset) + "&username=" + username + "&filter=5&_=" + str(epoch)

            json_reply = requests.get(reply_url).json()
            reply = json_reply["user_actions"]

            if (len(reply) == 0):
                break
            else:
                if(first):
                    replies_complete = reply
                    first = False
                else:
                    offset += 30
                    for r in reply:
                        ### save to mongodb
                        replies_complete.append(r)

        reply_dict = {"username": username, "reply": replies_complete}
        #dump the list of relies to the mongodb
        collection.insert(reply_dict)

        # save this id in "save" collection
        coll_status.insert_one({"collection":COLL_USER_REPLY, "id":username})
        print "user reply inserted: " + username
