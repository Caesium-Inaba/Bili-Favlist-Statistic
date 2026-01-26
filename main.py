import fetch_favlist
from utils.bili_utils import *
from random import *
from collections import Counter
from bilibili_api.exceptions import ResponseCodeException


# uid -> fids
favlistapi = fetch_favlist.main()

# fid -> bids

favlist = []
i = 0
while True:
    try:
        fid = favlistapi["list"][i]["id"]
        favlist.append(fid)
        i += 1
    except IndexError:
        break




# bid -> tags


print("Favlist is as follows:")
print(json.dumps(favlist, indent=4))
fid = int(input("Which fav do you want to analyze? Please type the fid: "))

bvids = fid2bvids(fid, output=True)

tags = []

for vid in bvids:
    try:
        tagsapi = bvid2tags(vid)
    except ResponseCodeException: # 有的稿件下架了
        continue
    # 比如收藏夹 2347842475 中是有下架的稿件的
    for tagapi in tagsapi:
        tags.append(tagapi['tag_name'])
    # print(bvid2tags(vid))
    time.sleep(uniform(0.5, 1.2))

print("tags is as follows:")
print(tags, end="\n\n")

tagscounter = Counter(tags)

print("tagscounter is as follows:")
print(tagscounter, end="\n\n")