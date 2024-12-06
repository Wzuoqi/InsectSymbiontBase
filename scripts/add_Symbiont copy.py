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

from symbiont.models import Symbiont
from django.db import IntegrityError

def get_unique_fields(symbiont_data):
    # 定义用于判断唯一性的字段组合
    return (
        symbiont_data['record_type'],
        symbiont_data['symbiont_name'],
        symbiont_data['host_species']
    )

def main():
    # 删除所有现有的 Symbiont 记录
    deleted_count = Symbiont.objects.all().delete()[0]
    print(f"已删除 {deleted_count} 条现有的 Symbiont 记录")

    added_count = 0
    skipped_count = 0
    error_count = 0

    expected_fields = [
        'ID', 'record_type', 'host_order', 'host_family', 'host_subfamily', 'host_species',
        'symbiont_phylum', 'symbiont_order', 'symbiont_genus', 'symbiont_rank',
        'symbiont_taxon', 'symbiont_name', 'classification', 'localization',
        'function', 'transmission_mode', 'related_accession', 'reference', 'doi', 'note'
    ]

    try:
        with open('data/symbionts241015.tab', 'r', encoding='UTF-8') as file:
            next(file)  # 跳过标题行
            for line_number, line in enumerate(file, start=2):
                split_table = line.strip().split('\t')

                # 数据验证
                if len(split_table) < len(expected_fields):
                    missing_fields = expected_fields[len(split_table):]
                    print(f"警告：第 {line_number} 行数据不完整，缺少以下字段：{', '.join(missing_fields)}")
                    error_count += 1
                    continue

                try:
                    # 读取每列的内容，忽略第一列（ID）
                    symbiont_data = {
                        'record_type': split_table[1],
                        'host_order': split_table[2],
                        'host_family': split_table[3],
                        'host_subfamily': split_table[4],
                        'host_species': split_table[5],
                        'symbiont_phylum': split_table[6],
                        'symbiont_order': split_table[7],
                        'symbiont_genus': split_table[8],
                        'symbiont_rank': split_table[9],
                        'symbiont_taxon': split_table[10],
                        'symbiont_name': split_table[11],
                        'classification': split_table[12],
                        'localization': split_table[13],
                        'function': split_table[14],
                        'transmission_mode': split_table[15],
                        'related_accession': split_table[16],
                        'reference': split_table[17],
                        'doi': split_table[18],
                        'note': split_table[19] if len(split_table) > 19 else "NA"
                    }

                    # 创建新的 Symbiont 对象
                    new_symbiont = Symbiont(**symbiont_data)
                    new_symbiont.save()
                    added_count += 1

                except Exception as e:
                    print(f"错误：处理第 {line_number} 行时出现问题:")
                    print(f"  错误类型: {type(e).__name__}")
                    print(f"  错误信息: {str(e)}")
                    if hasattr(e, 'params'):
                        print(f"  缺失或有问题的字段: {', '.join(e.params)}")
                    error_count += 1

        print(f"成功添加 {added_count} 条新的 Symbiont 记录")
        if error_count > 0:
            print(f"警告：处理过程中遇到 {error_count} 个错误")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
    print('Symbiont 模型导入完成！')
