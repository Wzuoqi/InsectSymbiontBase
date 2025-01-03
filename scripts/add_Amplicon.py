import django
import os
import sys

# 获取脚本所在的目录
script_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(script_path, '..'))
sys.path.append(project_path)

# 设置 Django 环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InsectSymbiontDB.settings")
django.setup()

from amplicon.models import Amplicon
from django.db import IntegrityError

def main():
    # 删除所有现有的 Amplicon 记录
    deleted_count = Amplicon.objects.all().delete()[0]
    print(f"已删除 {deleted_count} 条现有的 Amplicon 记录")

    added_count = 0
    error_count = 0

    # 定义字段映射关系
    field_mapping = {
        'Run': 'run',
        'Assay Type': 'assay_type',
        'BioSample': 'biosample',
        'Bytes': 'bytes',
        'Center Name': 'center_name',
        'Instrument': 'instrument',
        'LibraryLayout': 'library_layout',
        'AvgSpotLen': 'avg_spot_len',
        'Bases': 'bases',
        'BioProject': 'bioproject',
        'Classification': 'classification',
        'geo_loc_name_country': 'geo_loc_name_country',
        'geo_loc_name_country_continent': 'geo_loc_name_country_continent',
        'Collection_Date': 'collection_date',
        'geo_loc_name': 'geo_loc_name',
        'HOST': 'host',
        'Host Order': 'host_order',
        'Host Family': 'host_family',
        'lat_lon': 'lat_lon',
        'env_broad_scale': 'env_broad_scale',
        'env_local_scale': 'env_local_scale',
        'env_medium': 'env_medium',
        'host_sex': 'host_sex',
        'Description': 'description',
        'DOI': 'doi'
    }

    try:
        with open('./data/amplicons250103.tab', 'r', encoding='UTF-8') as file:
            # 读取表头
            headers = file.readline().strip().split('\t')
            print(f"检测到 {len(headers)} 列")

            for line_number, line in enumerate(file, start=2):
                try:
                    # 分割数据行
                    values = line.strip().split('\t')
                    if len(values) < len(headers):
                        print(f"警告：第 {line_number} 行数据不完整")
                        values.extend([''] * (len(headers) - len(values)))

                    # 创建数据字典
                    amplicon_data = {}
                    for i, value in enumerate(values):
                        if i < len(headers):
                            field_name = field_mapping.get(headers[i])
                            if field_name:
                                # 处理数值型字段
                                if field_name in ['bytes', 'bases']:
                                    try:
                                        amplicon_data[field_name] = int(value) if value and value != 'None' else None
                                    except ValueError:
                                        amplicon_data[field_name] = None
                                else:
                                    # 处理字符串字段
                                    amplicon_data[field_name] = value if value and value not in ['None', 'NA', ''] else None

                    # 创建新的 Amplicon 对象
                    new_amplicon = Amplicon(**amplicon_data)
                    new_amplicon.save()
                    added_count += 1

                    # 每1000条记录打印一次进度
                    if added_count % 1000 == 0:
                        print(f"已处理 {added_count} 条记录...")

                except Exception as e:
                    print(f"错误：处理第 {line_number} 行时出现问题:")
                    print(f"  错误类型: {type(e).__name__}")
                    print(f"  错误信息: {str(e)}")
                    print(f"  问题数据: {values}")
                    error_count += 1
                    if error_count >= 10:  # 如果错误太多，终止导入
                        print("错误次数过多，终止导入")
                        break

        print(f"\n数据导入完成:")
        print(f"成功添加 {added_count} 条新的 Amplicon 记录")
        if error_count > 0:
            print(f"警告：处理过程中遇到 {error_count} 个错误")

    except Exception as e:
        print(f"发生严重错误: {e}")
        import traceback
        print(f"详细错误信息:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
    print('Amplicon 数据导入完成！')
