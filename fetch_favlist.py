"""
通过 uid 给你弄 favlist 的 json 出来
"""



from bilibili_api import video, sync, favorite_list
import json
from collections import Counter # 给 tags 计数

from utils.file_utils import savejson # 输出 json 的函数被打包出来，也被放进 utils 了
from utils.bili_utils import uid2favlist # 


def main():
    """互动调用关于 favlist 的 API，并返回调用 API 的结果（关于 favlist）"""

    # input uid
    print("=" * 60)
    uid = int(input("Please enter uid, e.g.: 525323175\nuid: "))
    print("Fetching...")
    favlist = uid2favlist(uid)

    # 保存 favlist
    final_path = savejson(favlist, name=f"favlist_of_uid_{uid}", dir="output\\favlists")

    print(f"Done. All the data have been stored in to {final_path}.")
    r = input("Do you want to read it in CMD? (Y/N. Default to Y):")
    if r not in {"N"}:
        print("-" * 60)
        print(json.dumps(favlist, ensure_ascii=False, indent=4))
    print("=" * 60)

    return favlist


if __name__ == "__main__":
    main()

# 看看vids长什么样

# fav = favlist["list"][0]
# fid = fav["id"]
# page = 1
# vids = sync(favorite_list.get_video_favorite_list_content(media_id=fid, page=page))
# print(json.dumps(vids, ensure_ascii=False, indent=4)) # dumps() -> str



# tagslist = [] # taglist 中存入 tag



# 连锁循环，一步到位，但似乎不行，太难调试。应该先把所有数据弄下来，先爬再分析

# dict(favlist) -> str(bvid)
# for fav in favlist["list"]: # 此人的各个收藏夹
#     fid = fav["id"] # int # 各个收藏夹的 fid
#     page = 1 # 从第一页开始
#     while True: # 该收藏夹下各页
#         pagepart = sync(favorite_list.get_video_favorite_list_content(media_id=fid, page=page))
#         vids = pagepart.get("medias", [])

#         if not vids: # 该页没东西就 break
#             break
        
#         for vid in vids:
#             bvid = vid["bvid"]
            
            
#             tags = bvid2tags(bvid)
#             for tag in tags:
#                 tagslist.append(tag["tag_name"])

#         print(f"Done: page {page}")
#         page += 1
        
#         time.sleep(0.5)


# print(f"tagslist 是\n{tagslist}")




# # tagslist 中元素的计数
# tagscount = Counter(tagslist) # Counter 类是专门用来计数的 dict
# print(f"tagscount 是\n{tagscount}")



# Video.get_info() 之后 json.dumps() 出来
# vdata = video.Video(bvid="BV1jZhEzLEDC")
# info = sync(vdata.get_info())
# print(json.dumps(info, ensure_ascii=False, indent=4)) # dumps() -> str
