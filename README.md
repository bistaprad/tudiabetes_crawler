

# tudiabetes_crawler
Web crawler for "http://www.tudiabetes.org/forum/". 

This crawler is written in python and the data is stored in MongoDB database.
Inspite of inspecting the HTML file, this program utilizes the json response from the disucssion forum.


Before you run this script please install the following in your system.
* [Python](https://www.python.org/downloads/)
 *  [MongoDB](https://docs.mongodb.org/manual/installation/)


#### How to run this script?
After downloading this repo, go to command line.
```
pradeepbista$ cd ./tudiabetes_crawler/crawler/
pradeepbista$ python dump_discussion_forum.py
```