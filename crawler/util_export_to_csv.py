import sys

### export discussions to csv file
def discussions(db, COLL_DISCUSSION):
    cursor = db[COLL_DISCUSSION].find()

    header_disucssion = "like_count,highest_post_number,id,user_id,title,last_posted_at,participant_count,views,reply_count,links,sum_of_clicks,replies"
    header_replies = ",post_number,quote_count,updated_at,moderator,reads,reply_count,id,avg_time,cooked,topic_id,username,user_created_at,user_id,incoming_link_count,reply_to_post_number"
    header = header_disucssion + header_replies + "\n"

    f = open("discussions.csv", "w")
    f.write(header)

    for d in cursor:

        like_count = -1
        highest_post_number = -1
        discuss_id = -1
        user_id = -1
        title = ""
        last_posted_at = -1
        participant_count = -1
        views = -1
        reply_count = -1
        links = -1
        sum_of_clicks = -1
        replies = -1

        try:
            d['like_count']
        except KeyError:
            continue
        else:
            like_count = d['like_count']

        try:
            d['highest_post_number']
        except KeyError:
            continue
        else:
            highest_post_number = d['highest_post_number']

        try:
            d['id']
        except KeyError:
            continue
        else:
            discuss_id = d['id']

        try:
            d['user_id']
        except KeyError:
            continue
        else:
            user_id = d['user_id']

        try:
            d['title']
        except KeyError:
            continue
        else:
            title = d['title'].replace(",", "").encode('ascii', 'ignore')

        try:
            d['last_posted_at']
        except KeyError:
            continue
        else:
            last_posted_at = d['last_posted_at']

        try:
            d['participant_count']
        except KeyError:
            continue
        else:
            participant_count = d['participant_count']

        try:
            d['views']
        except KeyError:
            continue
        else:
            views = d['views']

        try:
            d['reply_count']
        except KeyError:
            continue
        else:
            reply_count = d['reply_count']

        try:
            d["details"]["links"]
        except KeyError:
            continue
        else:
            l_dict = d["details"]["links"]
            links = len(l_dict)
            for l in l_dict:
                sum_of_clicks = sum_of_clicks + l["clicks"]

        try:
            d["post_stream"]["posts"]
        except KeyError:
            continue
        else:
            replies = len(d["post_stream"]["posts"]) - 1

        line_discuss = [like_count,highest_post_number,discuss_id,user_id,title,last_posted_at,participant_count,views,reply_count,links,sum_of_clicks,replies]
        line_discuss_str = [str(i) for i in line_discuss]
        line_discuss_str = ",".join(line_discuss_str)

        for p in d["post_stream"]["posts"]:

            post_number = -1
            quote_count = -1
            updated_at = ""
            moderator = ""
            reads = -1
            reply_count = -1
            id = -1
            avg_time = -1
            cooked = ""
            topic_id = -1
            username = ""
            user_created_at = ""
            user_id = -1
            incoming_link_count = -1
            reply_to_post_number = -1

            post_number = p["post_number"]
            quote_count = p["quote_count"]
            updated_at = p["updated_at"]
            moderator = p["moderator"]
            reads = p["reads"]
            reply_count = p["reply_count"]
            id = p["id"]
            avg_time = p["avg_time"]
            cooked = p["cooked"].replace(",", "").encode('ascii', 'ignore')
            topic_id = p["topic_id"]
            username = p["username"]
            user_created_at = p["user_created_at"]
            user_id = p["user_id"]
            incoming_link_count = p["incoming_link_count"]
            reply_to_post_number = p["reply_to_post_number"]

            line_post = [post_number, quote_count, updated_at, moderator, reads, reply_count, id, avg_time, cooked, topic_id, username, user_created_at, user_id, incoming_link_count, reply_to_post_number]

            # print line_discuss
            # print len(line_post)

            line_post = [str(i) for i in line_post]
            line_post = ",".join(line_post).replace("\n", "")

            final_line = line_discuss_str+","+line_post+"\n"

            final_line  = final_line.encode('ascii', 'ignore')
            f.write(final_line)

        print "ID : " + str(discuss_id) + " saved"

    f.close()