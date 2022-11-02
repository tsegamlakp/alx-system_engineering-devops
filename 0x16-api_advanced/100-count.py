#!/usr/bin/python3
"""
Get title of top ten hot posts
"""
import requests


def count_words(subreddit, word_list=[], after="", res={}):
    """ Recursively get data """
    url = "https://www.reddit.com/r/{}/hot.json?limit=100&after={}".format(
        subreddit, after)
    headers = {"User-Agent": "Getacher-Top-Ten"}
    try:
        resp = requests.get(url, headers=headers, allow_redirects=False)
        if resp.status_code != 200:
            return
        after = resp.json().get("data").get("after")
        ch = resp.json().get("data").get("children")
        keys = [k.lower() for k in word_list]
        for item in ch:
            title = item.get("data").get("title").lower().split(" ")
            for k in keys:
                if res.get(k, None):
                    res[k] += title.count(k)
                else:
                    res[k] = title.count(k)
        if not after:
            res = dict(sorted(res.items(), key=lambda x: (-x[1], x[0])))
            for key, value in res.items():
                if value:
                    print("{}: {}".format(key, value))
            return
    except Exception:
        return
    return count_words(subreddit, keys, after, res)
