#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# B站收藏夹视频标题爬取工具
# 使用 bilibili-api-python 库

import time
import sys
from bilibili_api import sync, favorite_list

def extract_ids_from_url(url):
    """
    从B站收藏夹URL中提取用户ID(uid)和收藏夹ID(fid)
    使用字符串分割法
    
    参数:
        url: 完整的收藏夹URL，例如:
            https://space.bilibili.com/525323175/favlist?fid=3312428975&ftype=create
    
    返回:
        tuple: (uid, fid)
    
    异常:
        如果URL格式不正确，会抛出ValueError
    """
    try:
        # 提取用户ID (uid) - space.bilibili.com/ 后的第一个数字部分
        # 例如从 https://space.bilibili.com/525323175/favlist?... 中提取 525323175
        uid_part = url.split('space.bilibili.com/')[1]
        uid = uid_part.split('/')[0]
        
        # 提取收藏夹ID (fid) - fid= 后的值
        # 例如从 ...?fid=3312428975&ftype=create 中提取 3312428975
        fid_part = url.split('fid=')[1]
        fid = fid_part.split('&')[0] if '&' in fid_part else fid_part
        
        # 简单验证：提取的ID应该是纯数字
        if not uid.isdigit() or not fid.isdigit():
            raise ValueError("提取的ID不是纯数字，请检查URL格式")
            
        return uid, fid
        
    except (IndexError, ValueError) as e:
        raise ValueError(f"URL解析失败: {e}。请确保URL格式正确，例如：https://space.bilibili.com/525323175/favlist?fid=3312428975&ftype=create")

def main():
    """主函数"""
    print("=" * 60)
    print("B站收藏夹视频标题爬取工具")
    print("=" * 60)
    
    # 1. 获取用户输入的收藏夹URL
    print("\n请输入B站收藏夹的完整URL（公开收藏夹）：")
    print("示例：https://space.bilibili.com/525323175/favlist?fid=3312428975&ftype=create")
    print("-" * 60)
    
    url = input("请输入URL: ").strip()
    
    # 2. 从URL中提取用户ID和收藏夹ID
    try:
        uid, fid = extract_ids_from_url(url)
        print(f"✓ 解析成功: 用户ID={uid}, 收藏夹ID={fid}")
    except ValueError as e:
        print(f"✗ 错误: {e}")
        print("程序退出，请检查URL格式后重试。")
        sys.exit(1)
    
    # 3. 准备保存结果的文件
    output_file = rf"output\b站收藏夹_{uid}_{fid}_视频标题.txt"
    
    try:
        # 4. 开始爬取收藏夹内容
        print("\n" + "=" * 60)
        print(f"开始爬取收藏夹内容，结果将保存到: {output_file}")
        print("=" * 60 + "\n")
        
        video_count = 0
        page_num = 1
        
        # 打开文件准备写入
        with open(output_file, 'w', encoding='utf-8') as file:
            # 写入文件头部信息
            file.write(f"B站收藏夹视频标题爬取结果\n")
            file.write(f"用户ID: {uid}\n")
            file.write(f"收藏夹ID: {fid}\n")
            file.write(f"源URL: {url}\n")
            file.write(f"爬取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 80 + "\n\n")
            
            # 循环爬取每一页，直到没有更多数据
            while True:
                try:
                    print(f"正在获取第 {page_num} 页数据...")
                    
                    # 使用sync调用bilibili-api-python的收藏夹内容获取函数
                    # 这里使用了同步调用方式，避免异步编程的复杂性
                    data = sync(favorite_list.get_video_favorite_list_content(
                        media_id=int(fid),  # 收藏夹ID，转为整数
                        page=page_num       # 页码
                    ))
                    
                    # 获取当前页的视频列表
                    videos = data.get('medias', [])
                    
                    # 如果没有视频数据，说明已经爬取完毕
                    if not videos:
                        print(f"第 {page_num} 页没有数据，爬取结束。")
                        break
                    
                    # 处理当前页的每个视频
                    for i, video in enumerate(videos, 1):
                        # 提取视频标题
                        title = video.get('title', '无标题')
                        
                        # 打印到屏幕
                        print(f"  {video_count + i}. {title}")
                        
                        # 写入文件
                        file.write(f"{video_count + i}. {title}\n")
                    
                    # 更新总视频计数
                    video_count += len(videos)
                    
                    # 检查是否还有更多页
                    # 有些收藏夹的返回数据中会包含总页数信息
                    has_more = data.get('has_more', 1)  # 默认为1，表示可能还有更多
                    
                    if has_more == 0:
                        print(f"已到达最后一页，爬取结束。")
                        break
                    
                    # 翻到下一页
                    page_num += 1
                    
                    # 重要：请求间隔，避免给B站服务器造成压力
                    # 建议保持至少1秒的间隔，更友好的可以设置为2-3秒
                    print(f"等待1秒后继续下一页...\n")
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"获取第 {page_num} 页时出错: {e}")
                    print("爬取中断，已保存现有数据。")
                    break
        
        # 5. 爬取完成，显示统计信息
        print("\n" + "=" * 60)
        print(f"爬取完成！")
        print(f"总共爬取 {video_count} 个视频")
        print(f"结果已保存到: {output_file}")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n用户中断操作，程序退出。")
        sys.exit(0)
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 检查是否安装了必要的库
    try:
        from bilibili_api import sync, favorite_list
    except ImportError:
        print("错误：未找到 bilibili-api-python 库")
        print("请先运行以下命令安装：")
        print("pip install bilibili-api-python")
        sys.exit(1)
    
    main()
