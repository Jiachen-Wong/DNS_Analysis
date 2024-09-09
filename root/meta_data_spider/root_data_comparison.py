# spider for https://root-servers.org/archives/
import requests
import time
import os
from datetime import datetime, timedelta
import yaml
from lxml import etree

# 数据源起自2015/03/02 至今
# The data source starts from 2015/03/02, and continues to the present.

# 在2020/09/15当天文件缺失，此前同一IP下不同镜像称为Instances，Instances下进一步细分为Sites；此后同一IP下不同镜像称为Sites，Sites下进一步细分改为Instances
# The archives lack the data of 2020/09/15.
# Before this day different mirrors of same IP is called 'Instances', and there can be serveral sites owned by only one instance.
# After this day different mirrors of same IP is called 'Sites', and there can be serveral instances owned by only one site.

# 在2022/05/12及之前 仅提供yml格式文件
# Only YML format files were provided on or before 2022/05/12

# 在2022/05/13及之后 同时提供yaml和json格式文件
# Both YAML & JSON format files were provided on or after 2022/05/13


start_date = datetime.strptime("2024/02/19", "%Y/%m/%d")
latest_date = {}

for root in "abcdefghijklm":
    latest_date[root] = start_date
for root in "abcdefghijklm":
    latest_date[root] = start_date
# print(latest_data)
input_date = start_date


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

    for root in "abcdefghijklm":
        time.sleep(0.5)
        # for root in "a":
        # 构建保存文件的完整路径
        save_path = (
            "root/meta_data_spider/"
            + input_date_str.replace("/", "_")
            + "/"
            + root
            + "-root."
            + "yml"
        )

        if os.path.exists(save_path):
            print(f"文件已存在：{save_path}")
            continue

        

        url = (
            "https://root-servers.org/archives/"
            + input_date_str
            + "/"
            + root
            + "-root."
            + file_type
        )
        # print(url)
        success = False

        for _ in range(5):
            try:
                response = requests.get(url)
            except:
                continue
            if response.status_code == 200:
                success = True
                break

        if success:
            # 解析YAML文件
            yaml_data = yaml.safe_load(response.text)
            # print(yaml_data)
            latest_date_str = latest_date[root].strftime("%Y/%m/%d")

            with open(
                "root/meta_data_spider/"
                + latest_date_str.replace("/", "_")
                + "/"
                + root
                + "-root."
                + "yml",
                "r",
                encoding="utf-8",
            ) as file:
                latest_data = yaml.load(file, Loader=yaml.FullLoader)
            if yaml_data != latest_data:
                folder_path = os.path.dirname(save_path)
                latest_date[root]=input_date
                # 如果文件夹不存在，则创建
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                # 写入YAML文件到本地
                with open(save_path, "w", encoding="utf-8") as file:
                    yaml.dump(
                        yaml_data, file, default_flow_style=False, allow_unicode=True
                    )
        else:
            with open("log.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"url访问失败：{url}\n")


# print(root_server_org_spider("2015/03/02"))

finish_date = datetime.strptime("2024/09/03", "%Y/%m/%d")
while input_date < finish_date:
# while input_date < datetime.now:
    input_date = input_date + timedelta(days=1)
    input_date_str = input_date.strftime("%Y/%m/%d")

    root_server_org_spider(input_date_str)
    print(input_date)
