# -*- coding: utf-8 -*-

from mn3spider.db import SqliteDB
import codecs
import csv
import time
import sqlite3
import numpy as np

db2 = sqlite3.connect('17.db')
db2.isolation_level = None #autocommit
cur = db2.cursor()
authors = cur.execute("SELECT * FROM AuthorList").fetchall()

def process(string):
    return string.strip().replace(" ", "")

def process2(authorid):
    string = authors[authorid][1]
    return string.strip().replace(" ", "")

db = SqliteDB()

#topics = db.getTopicsFromForum(17)
posts = db.getPostsFromForum(17)

num_posts = len(posts)

#### QUOTE ANALYSIS
# get all quotes
#num_quote = 0
#for post in posts:
#	if "quote" in post[5]:
#		num_quote = num_quote +1
#c = csv.writer(open('graphquotesGNOJ'+str(int(time.time()))+'.csv','wb'))

# get all quotes w references
#num_quote2 = 0
#for post in posts:
#    if u'alt="Oglej si sporočilo"' in post[5]:
#        start = post[5].find(u'alt="Oglej si sporočilo"></a>')+len(u'alt="Oglej si sporočilo"></a>')
#        author = post[5][start:]
#        stop = author.find(', ob')
#        author = author[:stop]
#        c.writerow([process(post[3]).encode('ascii', 'ignore'),process(author).encode('ascii', 'ignore')])


#print (num_posts, num_quote, num_quote2)


#### THREAD PARTECIPATION ANALYSIS
#c = csv.writer(open('graphpartecGNOJ'+str(int(time.time()))+'.csv','wb'))
#db2 = sqlite3.connect('17.db')
#db2.isolation_level = None #autocommit
#cur = db2.cursor()
# first: associate each user and each thread with a number, and add posts (links) between them
#for p in posts:
#    topic = cur.execute("SELECT id FROM TopicList WHERE topic=?",[p[0]]).fetchall()
#    if len(topic) < 1:
#	print "TOPIC INSERTED "+str(p[0])
#        cur.execute("INSERT INTO TopicList (topic) VALUES (?)",[p[0]])
#        topic = cur.lastrowid
#    else:
#        topic = topic[0][0]
#
#    author = cur.execute("SELECT id FROM AuthorList WHERE author=?",[p[3]]).fetchall()
#    if len(author) < 1:
#        print "AUTHOR INSERTED "+p[3]
#        cur.execute("INSERT INTO AuthorList (author) VALUES (?)",[p[3]])
#        author = cur.lastrowid
#    else:
#        author = author[0][0]
#    print (topic,author)
#    cur.execute("INSERT INTO PostList (topicid, authorid) VALUES (?,?)",[topic,author])

# second: make projections onto the user 
posts = cur.execute("SELECT * FROM PostList ORDER BY topicid ASC, authorid ASC").fetchall()
#make matrix
adjacency = np.zeros((len(posts),3),dtype=np.int32)
st = 0
for p in posts:
    if st == 0:
        adjacency[st][0] = p[1]-1
        adjacency[st][1] = p[0]-1
        adjacency[st][2] += 1
        st+=1
    if p[0] == adjacency[st-1][1]+1 and p[1] == adjacency[st-1][0]+1:
        adjacency[st-1][2] += 1
        continue
    adjacency[st][0] = p[1]-1
    adjacency[st][1] = p[0]-1
    adjacency[st][2] += 1
    st+=1

adjacency = adjacency[:st]
adjacency.view('i4,i4,i4').sort(order=['f0','f1'], axis=0)
print "FINISHED ADJACENCY"
#print "--------------------------------"
#print st
#st2 = 0
#while True:
#    print adjacency[st2]
#    st2 +=1
#    if st2 == st-1: break

#make projections
f = open('author-thread-list','w')
b = np.zeros(608,dtype=np.int32)
st1 = 0
st2 = 0
for row in adjacency:
    f.write(str(row)+"\n")
    if not row[0] == st1:
        raz = row[0] - st1-2
        while(raz > 0):
            b[st1+raz] = st2
            raz = raz -1
        b[st1] = st2
        st1 = row[0]
    st2 += 1
b[st1] = st2
f.close()

c = csv.writer(open('graphpartecGNOJ'+str(int(time.time()))+'.csv','wb'))
print "BEGIN PROJECTIONS"
for i in range(608):
    if i == 0: begi = 0
    else: begi = b[i-1]
    rangei = b[i]-begi-1
    print (i,rangei)
    if rangei < 0: continue
    for j in range(608):
        if i == j: continue
        if j == 0: begj = 0
        else: begj = b[j-1]
        rangej = b[j]-begj-1
        if rangej < 0: continue
        #print (j,rangej)
	i1 = 0
        i2 = 0
        value = 0
        #make intersect
        while True:
            if i1 > rangei or i2 > rangej: break
            thread1 = adjacency[begi + i1][1]
            thread2 = adjacency[begj + i2][1]
            if thread1 == thread2:
                #print "HIT: "+str(thread1)
                value += adjacency[begi+i1][2]
                i1 +=1
                i2 +=1
            elif thread1 > thread2:
                i2 +=1
            else: i1 +=1
        
        if value > 0:
            #print "WRITING: "+str((i,j,value))
            for v in range(value): c.writerow([process2(i).encode('ascii', 'ignore'),process2(j).encode('ascii', 'ignore')])

    # get all authors of posts in a topic in a list    
    # generate edges w weight 1 for all possible pairs of author (unidirectional)
    # PROBLEM: TOO SLOW db.getPostsFromTopic()

# TODO: recommendation system, similar topics, itd. - projection onto topic side

