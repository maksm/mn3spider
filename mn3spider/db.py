#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3

class SqliteDB:
    def __init__(self):
        self.db = "mn3.db"
        self.connection = sqlite3.connect(self.db)
        self.connection.isolation_level = None #autocommit
        self.cursor = self.connection.cursor()
        
    def insertForum(self):
        forums =[["3", u"Revija Joker"], ["64", u"Mn3njalnik"], 
                 ["4", u"Igrovje za PC"], ["45", u"Brezmejni onkraj"], ["46", u"Starinarnica"], ["51", u"Zmajev šupak"], 
                 ["5", u"Železnina"], ["42", u"Frizeraj v Las Vegasu"], ["52", u"Čiparna"],["54", u"Camera obscura"],  
                 ["8", u"Konzolec"], ["60", u"Zdej"], ["59", u"Retro friki"], ["21", u"Drkamož"], 
                 ["6", u"Programje in ok(n)ovje"], ["18", u"Šoferje"], ["19", u"DV kotič"], ["20", u"Neznančev čošak"], ["35", u"Karantena"], ["57", u"7edem"],
                 ["7", u"Netki"], ["41", u"Mobidik"], 
                 ["9", u"Slikosuk"], ["24", u"Japanka"], ["55", u"Nizke"], 
                 ["10", u"Cigu migu"], ["11", u"Črkožer"], ["38", u"Namiznik"], 
                 ["13", u"Telovadba"], ["22", u"Formulce"], ["23", u"Metnoge"], ["58", u"Gimnazija"],
                 ["12", u"Straniščni humor"], ["14", u"Bela tehnika"],["48", u"Forum"], ["50", u"Trola"],["56", u"Frotirka"], 
                 ["15", u"Vseučilišče"],["16", u"Paritveni brlog"],["25", u"Brum bruuum"],["26", u"Rokodelstvo"],
                 ["27", u"Mojstri kode"],["28", u"Knjižnica"]]
        for forum in forums:
            self.cursor.execute("INSERT INTO ForumList (forumid, title) VALUES (?,?)", [forum[0], forum[1]])
        
    def insertTopic(self, forumid,  topicid,  title,  author,  date):
        self.cursor.execute("INSERT INTO TopicList (forumid, topicid, title, author, date) VALUES (?,?,?,?,?)", [forumid, topicid, title, author, date])
        
    def insertPost(self, topicid,  postid,  postnum,  author,  date,  content):
        self.cursor.execute("INSERT INTO PostList (topicid,  postid,  postnum,  author,  date,  content) VALUES (?,?,?,?,?,?)", [ topicid,  postid,  postnum,  author,  date,  content])
        
    def getForums(self):
        return self.cursor.execute("SELECT forumid FROM ForumList").fetchall()

    def getTopics(self):
	return self.cursor.execute("SELECT topicid FROM TopicList").fetchall()

    def getTopicsFromForum(self, forumid):
	return self.cursor.execute("SELECT topicid FROM TopicList WHERE forumid=?",[forumid]).fetchall()

    def getPosts(self):
        return self.cursor.execute("SELECT * FROM PostList").fetchall()

    def getPostsFromTopic(self, topicid):
        return self.cursor.execute("SELECT * FROM PostList WHERE topicid=?",[topicid]).fetchall()

    def delete(self):
        pass
    
    def create(self):
        self.clear()
        forumlist = '''CREATE TABLE ForumList
        (forumid INTEGER PRIMARY KEY, title TEXT, numtopic INTEGER, numpost INTEGER)'''

        topiclist = '''CREATE TABLE TopicList
        (forumid INTEGER REFERENCES ForumList(forumid),
        topicid INTEGER PRIMARY KEY, title TEXT, author TEXT, date TEXT, 
        replies INT, views INT)'''

        postlist = '''CREATE TABLE PostList 
        (topicid INTEGER REFERENCES TopicList(topicid),
        postid INTEGER PRIMARY KEY, postnum INTEGER, author TEXT, date TEXT, content TEXT)'''
        
        self.cursor.execute(forumlist)
        self.cursor.execute(topiclist)
        self.cursor.execute(postlist)
        self.connection.commit()
        self.insertForum()
        self.connection.commit()
        
    def clear(self):
        forumlist = "DROP TABLE IF EXISTS ForumList"
        topiclist = "DROP TABLE IF EXISTS TopicList"
        postlist = "DROP TABLE IF EXISTS PostList"
        self.cursor.execute(forumlist)
        self.cursor.execute(topiclist)
        self.cursor.execute(postlist)
        self.connection.commit()
