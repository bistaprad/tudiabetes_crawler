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


# retrieve the datus if an id in a collection has been saved
# for example, if a discussion (235631) has been dumped or not
def check_if_saved(db, COLL_SAVE_STATUS, col, id):
     return db[COLL_SAVE_STATUS].find({"collection":col, "id":id}).count() > 0

