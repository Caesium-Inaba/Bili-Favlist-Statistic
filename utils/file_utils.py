"""
utils.file_utils ，是关于文件的实用工具
"""

import os, json

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