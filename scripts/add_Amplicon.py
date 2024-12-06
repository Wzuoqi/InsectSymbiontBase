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

from amplicon.models import Amplicon

def main():
    amplicon_list = []

    try:
        with open('data/test_amplicons.tab', 'r', encoding='UTF-8') as file:
            next(file)  # 跳过标题行
            for line in file:
                split_table = line.strip().split('\t')

                # 数据验证
                if len(split_table) < 21:  # Amplicon 数据有 21 列
                    continue  # 跳过不完整的行

                # 从文件中读取每一列的内容
                run = split_table[1]
                assay_type = split_table[2]
                biosample = split_table[3]
                bytes = int(split_table[4]) if split_table[4].isdigit() else None
                center_name = split_table[5]
                instrument = split_table[6]
                library_layout = split_table[7]
                bioproject = split_table[10]
                classification = split_table[11]
                geo_loc_name_country = split_table[12]
                geo_loc_name_country_continent = split_table[13]
                collection_date = split_table[14] if split_table[14] not in ['not applicable', '', 'missing'] else "NA"
                geo_loc_name = split_table[15]
                host = split_table[16]
                lat_lon = split_table[17] if split_table[17] not in ['not applicable', '', 'missing'] else None
                env_broad_scale = split_table[18] if split_table[18] not in ['not applicable', '', 'missing'] else "NA"
                env_local_scale = split_table[19] if split_table[19] not in ['not applicable', '', 'missing'] else "NA"
                env_medium = split_table[20] if split_table[20] not in ['not applicable', '', 'missing'] else "NA"
                host_sex = split_table[21] if len(split_table) > 21 and split_table[21] not in ['not applicable', '', 'missing'] else "NA"

                # 创建 Amplicon 对象
                tmp_amplicon = Amplicon(
                    run=run,
                    assay_type=assay_type,
                    biosample=biosample,
                    bytes=bytes,
                    center_name=center_name,
                    instrument=instrument,
                    library_layout=library_layout,
                    bioproject=bioproject,
                    classification=classification,
                    geo_loc_name_country=geo_loc_name_country,
                    geo_loc_name_country_continent=geo_loc_name_country_continent,
                    collection_date=collection_date,
                    geo_loc_name=geo_loc_name,
                    host=host,
                    lat_lon=lat_lon,
                    env_broad_scale=env_broad_scale,
                    env_local_scale=env_local_scale,
                    env_medium=env_medium,
                    host_sex=host_sex
                )

                # 将对象添加到列表中
                amplicon_list.append(tmp_amplicon)

        # 批量插入数据库
        Amplicon.objects.bulk_create(amplicon_list)
        print(f"成功添加 {len(amplicon_list)} 条 Amplicon 记录")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
    print('Amplicon model import Done!')
