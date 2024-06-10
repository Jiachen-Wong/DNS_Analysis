import yaml
import os

def compare_yaml_dicts(dict1, dict2, path=""):
    added = {}
    removed = {}

    for key in dict1:
        if key not in dict2:
            removed[path + key] = dict1[key]
        elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            sub_added, sub_removed = compare_yaml_dicts(dict1[key], dict2[key], path + key + "/")
            if sub_added:
                added[key] = sub_added
            if sub_removed:
                removed[key] = sub_removed
        elif dict1[key] != dict2[key]:
            removed[path + key] = dict1[key]
            added[path + key] = dict2[key]

    for key in dict2:
        if key not in dict1:
            added[path + key] = dict2[key]

    return added, removed

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def save_yaml(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

def compare_and_save_yaml(file1, file2, output_file):
    yaml1 = load_yaml(file1)
    yaml2 = load_yaml(file2)

    added, removed = compare_yaml_dicts(yaml1, yaml2)

    result = {
        'added': added,
        'removed': removed
    }

    save_yaml(result, output_file)
    print(f"比较结果已保存到：{output_file}")

# 示例使用
yaml_file1 = 'root/meta_data_spider/2024_06_07/a-root.yaml'  # 替换为第一个YAML文件的路径
yaml_file2 = 'root/meta_data_spider/2015_03_02/a-root.yml'  # 替换为第二个YAML文件的路径
output_file = 'difference.yaml'  # 输出结果保存的路径

compare_and_save_yaml(yaml_file1, yaml_file2, output_file)
