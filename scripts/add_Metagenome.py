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

from metagenome.models import Metagenome

def main():
    metagenome_list = []

    try:
        with open('data/test_metagenomes.tab', 'r', encoding='UTF-8') as file:
            next(file)  # 跳过标题行
            for line in file:
                split_table = line.strip().split('\t')

                # 数据验证
                if len(split_table) < 18:  # 更新为新的最小列数（不包括isolation列）
                    continue  # 跳过不完整的行

                # 从文件中读取每一列的内容
                run = split_table[1]
                assay_type = split_table[2]
                biosample = split_table[3]
                bytes = int(split_table[4]) if split_table[4].isdigit() else None
                center_name = split_table[5]
                instrument = split_table[6]
                library_layout = split_table[7]
                library_selection = split_table[8]
                platform = split_table[9]
                bioproject = split_table[10]
                geo_loc_name_country = split_table[11]
                geo_loc_name_country_continent = split_table[12]
                collection_date = split_table[13] if split_table[13] not in ['not applicable', '', 'missing'] else "NA"
                geo_loc_name = split_table[14]
                biosample_model = split_table[15]
                lat_lon = split_table[16] if split_table[16] not in ['not applicable', ''] else None
                host = split_table[17]
                isolation = split_table[18] if len(split_table) > 18 and split_table[18] not in ['not applicable', '', 'missing'] else "NA"

                # 创建 Metagenome 对象
                tmp_metagenome = Metagenome(
                    run=run,
                    assay_type=assay_type,
                    biosample=biosample,
                    bytes=bytes,
                    center_name=center_name,
                    instrument=instrument,
                    library_layout=library_layout,
                    library_selection=library_selection,
                    platform=platform,
                    bioproject=bioproject,
                    geo_loc_name_country=geo_loc_name_country,
                    geo_loc_name_country_continent=geo_loc_name_country_continent,
                    collection_date=collection_date,
                    geo_loc_name=geo_loc_name,
                    biosample_model=biosample_model,
                    lat_lon=lat_lon,
                    host=host,
                    isolation=isolation
                )

                # 将对象添加到列表中
                metagenome_list.append(tmp_metagenome)

        # 批量插入数据库
        Metagenome.objects.bulk_create(metagenome_list)
        print(f"成功添加 {len(metagenome_list)} 条 Metagenome 记录")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
    print('Metagenome model import Done!')
