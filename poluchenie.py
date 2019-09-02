import requests
import json
import csv
# -*- codng: utf8 -*-
import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())


def take_post():
    all_posts = []
    domain='menalis'
    version=5.101
    ofset = 0
    token = 'f278d496f278d496f278d496dcf2145754ff278f278d496af1bc2e2cb7cce7a192f2a23'

    #запрос записей
    while ofset< 15:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params = {
                                'access_token':token,
                                'v':version,
                                'domain':domain,
                                'count':15,
                                'ofset':ofset
                                }

                                )

        data = response.json()['response']['items']
        all_posts.extend(data)
        return all_posts

def filter(all_posts):
    length = len(all_posts)
    filter_posts = []
    try:
        for post in all_posts:
            filter_post= {'url':'','id':'','type':''}
            b = 0
            for k,v in post.items():
                if k == 'text':
                    filter_post[k] = v
                elif k == 'id':
                    filter_post[k] = v

                    with open('isp_id.json','a') as file:
                        id_app = str(v)
                        prog = json.dump(id_app,file)

                elif k == 'attachments':
                    for p in v:
                        for q,w in p.items():
                            if q == 'photo':
                                filter_post["type"]= q
                                for o,i in w.items():
                                    if o == 'sizes':
                                        for j in i:
                                            for u,y in j.items():
                                                if u == 'url':
                                                    filter_post[u]= y
                            if q == 'video':
                                filter_post["type"]= q
                                for o,i in w.items():
                                    if o == 'id':
                                        last_name = i
                                    elif o == 'owner_id':
                                        first_name = i
                                url = "https://vk.com/video"+str(first_name)+"_"+str(last_name)
                                filter_post["url"]=url
            filter_posts.append(filter_post)
            b += 1
        return filter_posts
    except UnicodeEncodeError :
        pass

def file_maker(filter_posts):
    FILE = 'posts.csv'
    columns = ["id", "text","url","type"]
    with open(FILE,'w',newline='',encoding="utf-8") as fl:
        posts = csv.DictWriter(fl,fieldnames = columns)
        posts.writeheader()
        for k in filter_posts:
            if k['url']!= '':
                posts.writerow(k)


all_posts = take_post()
filter_posts = filter(all_posts)
file_maker(filter_posts)
