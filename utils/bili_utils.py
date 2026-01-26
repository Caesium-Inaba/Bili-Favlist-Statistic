"""
给 bilibili_api 打了一层包
"""

from .file_utils import savejson
from bilibili_api import favorite_list, sync, video
import json
import time, random # 更像人的间隔请求


def uid2favlist(uid: int) -> dict:
    """
    输入 uid 抓取其收藏夹列表
    """
    favlist = sync(favorite_list.get_video_favorite_list(uid=int(uid)))
    return favlist



def fid2bvids(fid: int, output: bool = True) -> list[str]:
    """
    输入 fid，输出对应的 bvids 列表，而且可以把 API 返回的内容保存。

    Args:
        fid (int):

        output (bool): 做不做 output。正常是 True

    Returns:
        list[str]: bvids 列表
    """
    page = 1
    bvids = []
    while True: # 没内容了就 break
        data = sync(favorite_list.get_video_favorite_list_content(fid, page))
        if not data["medias"]: # data 作为对收藏夹的描述的字典，永远有东西。但 data["medias"] 这个 list 并不
            break
        for vid in data["medias"]: # vid 是一个字典
            bvids.append(vid["bvid"])
        page += 1
        time.sleep(random.uniform(0.5, 1.2))

    # 保存为 json
    if output:
        savejson(data=bvids, name=f"bvidlist_of_fav_{fid}_of_uid_{data["info"]["mid"]}_{data['info']["upper"]["name"]}"\
                 , dir="output\\bvids")
        
    # print(bvids)
    return bvids

# # 测试
# fid2bvids(3368327975)
        


#     # 先爬个一页看看效果
#     data = sync(favorite_list.get_video_favorite_list_content(fid, page))
#     print(json.dumps(data, ensure_ascii=False, indent=4))


    


def bvid2tags(bvid: str) -> list[dict]:
    """
    输入 bvid 展示其 tags
    """
    v = video.Video(bvid=bvid) # v 是 Video 类的一个实例，video 是 module，Video 是类
    tags = sync(v.get_tags())
    # print(json.dumps(tags, ensure_ascii=False, indent=4)) # dumps() -> str
    return tags


