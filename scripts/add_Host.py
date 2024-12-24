import django
import os
import sys

# 获取脚本所在的目录
script_path = os.path.dirname(os.path.abspath(__file__))

# 获取 Django 项目根目录的路径
project_path = os.path.abspath(os.path.join(script_path, '..'))

# 将项目路径添加到 Python 路径中
sys.path.append(project_path)

# 设置 DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InsectSymbiontDB.settings")

# 导入 Django 设置
django.setup()

from host.models import Host
from django.db import IntegrityError

def main():
    # 删除所有现有的 Host 记录
    deleted_count = Host.objects.all().delete()[0]
    print(f"已删除 {deleted_count} 条现有的 Host 记录")

    added_count = 0
    error_count = 0

    try:
        with open('./data/hosts241224.tab', 'r', encoding='UTF-8') as file:
            # 跳过标题行
            header = file.readline().strip()

            for line_number, line in enumerate(file, start=2):
                try:
                    # 分割数据行
                    values = line.strip().split('\t')
                    if len(values) != 5 or not line.strip():  # 跳过空行和格式不正确的行
                        continue

                    # 解析数据
                    species, order, family, subfamily, genus = values

                    # 处理 'None' 值
                    subfamily = None if subfamily.lower() == 'none' else subfamily

                    # 创建 Host 记录
                    host_data = {
                        'species': species,
                        'order': order,
                        'family': family,
                        'subfamily': subfamily,
                        'genus': genus,
                        'common_name': '',  # 设置默认空字符串
                        'description': ''   # 设置默认空字符串
                    }

                    # 创建新的 Host 对象
                    new_host = Host(**host_data)
                    new_host.save()
                    added_count += 1

                    # 每100条记录打印一次进度
                    if added_count % 100 == 0:
                        print(f"已处理 {added_count} 条记录...")

                except Exception as e:
                    print(f"错误：处理第 {line_number} 行时出现问题:")
                    print(f"  错误类型: {type(e).__name__}")
                    print(f"  错误信息: {str(e)}")
                    error_count += 1

        print(f"\n数据导入完成:")
        print(f"成功添加 {added_count} 条新的 Host 记录")
        if error_count > 0:
            print(f"警告：处理过程中遇到 {error_count} 个错误")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
    print('Host 数据导入完成！')
