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

def clean_value(value):
    """清理和标准化数据值"""
    if value in ['not applicable', '', 'missing', 'uncalculated', 'None']:
        return "NA"
    return value.strip()

def main():
    try:
        # 删除所有现有的 Metagenome 记录
        deleted_count = Metagenome.objects.all().delete()[0]
        print(f"已删除 {deleted_count} 条现有的 Metagenome 记录")

        metagenome_list = []
        skipped = 0
        added = 0

        with open('data/metagenomes250103.tab', 'r', encoding='UTF-8') as file:
            # 跳过标题行
            next(file)

            for line_number, line in enumerate(file, start=2):
                split_table = line.strip().split('\t')

                # 数据验证 - 确保至少有基本必需的列
                if len(split_table) < 15:
                    print(f"警告：第 {line_number} 行数据不完整")
                    skipped += 1
                    continue

                # 从文件中读取每一列的内容
                try:
                    # 创建 Metagenome 对象
                    tmp_metagenome = Metagenome(
                        run=split_table[1],  # SRR ID在第2列
                        assay_type=clean_value(split_table[2]),  # WGS/RNA-Seq等
                        biosample=clean_value(split_table[3]),  # SAMN ID
                        bytes=int(split_table[4]) if split_table[4].isdigit() else None,
                        center_name=clean_value(split_table[5]),
                        instrument=clean_value(split_table[6]),
                        library_layout=clean_value(split_table[7]),
                        library_selection=clean_value(split_table[8]),
                        platform=clean_value(split_table[9]),
                        bioproject=clean_value(split_table[10]),
                        geo_loc_name_country=clean_value(split_table[11]),
                        geo_loc_name_country_continent=clean_value(split_table[12]),
                        collection_date=clean_value(split_table[13]),
                        geo_loc_name=clean_value(split_table[14]),
                        biosample_model=clean_value(split_table[15]),
                        lat_lon=split_table[16] if len(split_table) > 16 and split_table[16] not in ['not applicable', '', 'missing'] else None,
                        host=clean_value(split_table[17]) if len(split_table) > 17 else "NA",
                        host_order=clean_value(split_table[18]) if len(split_table) > 18 else "NA",
                        host_family=clean_value(split_table[19]) if len(split_table) > 19 else "NA",
                        isolation=clean_value(split_table[20]) if len(split_table) > 20 else "NA",
                        description=clean_value(split_table[21]) if len(split_table) > 21 else "None",
                        doi=clean_value(split_table[22]) if len(split_table) > 22 else "None"
                    )
                    metagenome_list.append(tmp_metagenome)
                    added += 1

                    # 每1000条记录打印一次进度
                    if added % 1000 == 0:
                        print(f"已处理 {added} 条记录...")

                except Exception as e:
                    print(f"错误：处理第 {line_number} 行时出现问题:")
                    print(f"  错误类型: {type(e).__name__}")
                    print(f"  错误信息: {str(e)}")
                    skipped += 1
                    continue

        # 批量插入数据库
        if metagenome_list:
            Metagenome.objects.bulk_create(metagenome_list)
            print(f"\n数据导入完成:")
            print(f"成功添加 {added} 条新的 Metagenome 记录")
        else:
            print("警告: 没有有效的数据被添加")

        if skipped > 0:
            print(f"警告：处理过程中遇到 {skipped} 个错误")

    except FileNotFoundError:
        print("错误: 找不到数据文件 'data/metagenomes250103.tab'")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
    print('Metagenome 数据导入完成！')
