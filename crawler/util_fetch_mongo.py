__author__ = "pradeepbista"


# extract the list of topic id and slug
def get_topic_ids(db, discussion_topics):
    cursor = db[discussion_topics].find()

    lis = []
    for t in cursor:
        lis.append([t["id"], str(t["slug"])])
        # print t["id"], t["slug"]

    return lis


# extract the list users
def get_users(db, COLL_USERS):
    cursor = db[COLL_USERS].find()
    lis = []

    for t in cursor:
        lis.append(t["user"]["username"])
    return lis
