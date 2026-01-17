from bilibili_api import video, sync, favorite_list
import json
from collections import Counter # 给 tags 计数
import time # sleep
import os



def uid2favlist(uid: int) -> dict:
    """
    输入 uid 抓取其收藏夹列表
    """
    favlist = sync(favorite_list.get_video_favorite_list(uid=int(uid)))
    return favlist

def bvid2tags(bvid: str) -> list[dict]:
    """
    输入 bvid 展示其 tags
    """
    v = video.Video(bvid=bvid) # v 是 Video 类的一个实例，video 是 module，Video 是类
    tags = sync(v.get_tags())
    # print(json.dumps(tags, ensure_ascii=False, indent=4)) # dumps() -> str
    return tags

def savejson(data:str | dict | list, name: str, dir: str = "") -> str:  
    """
    自带文件命名冲突自动解决机制的保存函数

    Args:
        data (str | dict | list): 数据

        name (str): json 的文件名。不带后缀

        dir (str, optional): 放在哪个文件夹下。没有就是放在同级文件夹中

    Returns:
        str: 保存到的 path
    """   
    if not name:
        raise ValueError("文件名不能为空")

    i = 0
    while True:
        if i == 0:
            filename = f"{name}.json" if dir == "" else f"{dir}\\{name}.json" # filename 是最终的 path
        else:
            filename = f"{name}({i}).json" if dir == "" else f"{dir}\\{name}({i}).json"

        if os.path.exists(filename): # 如果 filename 存在
            i += 1
        else:
            os.makedirs(dir, exist_ok=True)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            break
    
    return filename # 把最终的 path return 出来

# # 对以上函数的测试：
# data = []
# name = "fuck"
# savejson(data,name,dir="fuck")


def main():

    # input uid
    print("=" * 60)
    uid = int(input("Please enter uid, e.g.: 525323175.\nuid: "))
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
