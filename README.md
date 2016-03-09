


# tudiabetes_crawler
Web crawler for "http://www.tudiabetes.org/forum/".

This crawler is written in python and the data is stored in MongoDB database.
Inspite of inspecting the HTML file, this program utilizes the json response from the disucssion forum.


Before you run this script please install the following in your system.
* [Python](https://www.python.org/downloads/)
* [MongoDB](https://docs.mongodb.org/manual/installation/)


#### How to run this script?
After downloading this repo, go to command line.
```
pradeepbista$ cd ./tudiabetes_crawler/crawler/
pradeepbista$ python dump_discussion_forum.py discussion_topic_list
```

Use arguments below in sequential order once it gets completed.

1) To save the discussion topic list : discussion_topic_list
2) To save the user list: user_list
3) To save the discussions with replies : discussions
4) To save the individual user summary: user_sumary
5) To save the user replies: user_replies