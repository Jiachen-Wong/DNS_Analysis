# spider for https://root-servers.org/archives/
import requests
import time
import os

# import datetime
from lxml import etree

# 数据源起自2015/03/02 至今
# The data source starts from 2015/03/02, and continues to the present.

# 在2022/05/12及之前 仅提供yml格式文件
# Only YML format files were provided on or before 2022/05/12

# 在2022/05/13及之后 同时提供yaml和json格式文件
# Both YAML & JSON format files were provided on or after 2022/05/13
from datetime import datetime, timedelta
import yaml


def root_server_org_spider(input_date_str=None):
    # 定义目标日期
    target_date = datetime.strptime("2022/05/13", "%Y/%m/%d")

    if input_date_str is None:
        # 缺省则默认获取前一天的信息
        input_date = datetime.now() - timedelta(days=1)
        input_date_str = input_date.strftime("%Y/%m/%d")
    else:
        # 解析输入日期字符串
        input_date = datetime.strptime(input_date_str, "%Y/%m/%d")
    # 比较日期
    if input_date < target_date:
        file_type = "yml"
    elif input_date >= target_date:
        file_type = "yaml"

    for root in 'abcdefghijklm':
    # for root in "a":
        # 构建保存文件的完整路径
        save_path = (
            "root/meta_data_spider/"
            + input_date_str.replace("/", "_")
            + "/"
            + root
            + "-root."
            + file_type
        )

        if os.path.exists(save_path):
            print(f"文件已存在：{save_path}")
            continue

        folder_path = os.path.dirname(save_path)

        # 如果文件夹不存在，则创建
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        url = (
            "https://root-servers.org/archives/"
            + input_date_str
            + "/"
            + root
            + "-root."
            + file_type
        )
        # print(url)
        response = requests.get(url)
        if response.status_code == 200:
            # 解析YAML文件
            yaml_data = yaml.safe_load(response.text)

            # 写入YAML文件到本地
            with open(save_path, "w", encoding="utf-8") as file:
                yaml.dump(yaml_data, file, default_flow_style=False, allow_unicode=True)
        else:
            print(f"url访问失败：{url}")


print(root_server_org_spider())
