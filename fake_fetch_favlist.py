import json
from typing import List, Dict
from bilibili_api import user, sync


def fetch_public_favorites(uid: int) -> List[Dict]:
    """
    获取指定 uid 的公开收藏夹列表

    Args:
        uid (int): B站用户 UID

    Returns:
        List[Dict]: 收藏夹信息列表
    """
    u = user.User(uid=uid)

    # bilibili-api 是 async 的，这里用 sync 包一层
    fav_data = sync(u.get_favorites())

    # fav_data 是 dict，真正的列表在 list 字段里
    favorites = fav_data.get("list", [])

    return favorites


def save_favorites_to_json(uid: int, favorites: List[Dict]) -> None:
    """
    将收藏夹数据保存为 json 文件
    """
    filename = f"uid_{uid}_favorites.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            favorites,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"已保存 {len(favorites)} 个公开收藏夹 → {filename}")


def main():
    uid = int(input("请输入 B 站 UID：").strip())

    favorites = fetch_public_favorites(uid)
    save_favorites_to_json(uid, favorites)


if __name__ == "__main__":
    main()
