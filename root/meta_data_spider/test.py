import yaml
from pprint import pprint
import requests

def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

dict1=load_yaml('root/meta_data_spider/2015_03_02/a-root.yml')
pprint(dict1['Instances'])


# url = (
#     "https://root-servers.org/archives/"
#     + input_date_str
#     + "/"
#     + root
#     + "-root."
#     + file_type
# )
# # print(url)
# response = requests.get(url)
# if response.status_code == 200:
#     # 解析YAML文件
#     yaml_data = yaml.safe_load(response.text)