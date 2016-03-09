__author__ = "pradeepbista"


# retrieve the list of topic id and slug
def get_topic_ids(db, discussion_topics):
    cursor = db[discussion_topics].find()

    lis = []
    for t in cursor:
        lis.append([t["id"], str(t["slug"])])
        # print t["id"], t["slug"]

    return lis


# retrieve the list users
def get_users(db, COLL_USERS):
    cursor = db[COLL_USERS].find()
    lis = []

    for t in cursor:
        lis.append(t["user"]["username"])
    return lis


# retrieve the satus of an id in a collection
# for example, if a complete discussion (235631) has been dumped
#              or if a user summary has been dumped
def check_if_saved(db, COLL_SAVE_STATUS, col, id):
    return db[COLL_SAVE_STATUS].find({"collection":col, "id":id}).count() > 0


## check if a user has been saved in a user_list
def check_user(db, COLL_USERS, userid):
     return db[COLL_USERS].find({"id":userid}).count() > 0


# for example, if a discussion topic (235631) has been saved in discussion topic list
def check_discussion(db, COLL_DISCUSSION_TOPICS, id):
     return db[COLL_DISCUSSION_TOPICS].find({"id":id}).count() > 0

