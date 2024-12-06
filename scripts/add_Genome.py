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

from genome.models import Genome
from django.db import IntegrityError

def get_unique_fields(genome_data):
    # 定义用于判断唯一性的字段组合
    return (
        genome_data['genome_id'],
    )

def safe_value(value):
    return None if value in ('None', '', 'NA') else value

def safe_float(value):
    try:
        return float(value) if value not in ('None', '', 'NA') else None
    except ValueError:
        return None

def safe_int(value):
    try:
        return int(value) if value not in ('None', '', 'NA') else None
    except ValueError:
        return None

def main():
    # 删除所有现有的 Genome 记录
    deleted_count = Genome.objects.all().delete()[0]
    print(f"已删除 {deleted_count} 条现有的 Genome 记录")

    added_count = 0
    skipped_count = 0
    error_count = 0

    expected_fields = [
        'genome_id', 'metagenome_id', 'host', 'source', 'function', 'literature_name',
        'reference', 'checkm_marker_lineage', 'checkm_genomes', 'checkm_markers',
        'completeness', 'contamination', 'strain_heterogeneity', 'quality_score',
        'gtdb_classification', 'gtdb_phylum', 'closest_genome_reference',
        'closest_genome_reference_radius', 'closest_genome_ani',
        'closest_placement_reference', 'classification_method', 'note'
    ]

    try:
        with open('data/test_genomes.tab', 'r', encoding='UTF-8') as file:
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
                    genome_data = {
                        'genome_id': safe_value(split_table[0]),
                        'metagenome_id': safe_value(split_table[1]),
                        'host': safe_value(split_table[2]),
                        'source': safe_value(split_table[3]),
                        'function': safe_value(split_table[4]),
                        'literature_name': safe_value(split_table[5]),
                        'reference': safe_value(split_table[6]),
                        'checkm_marker_lineage': safe_value(split_table[7]),
                        'checkm_genomes': safe_int(split_table[8]),
                        'checkm_markers': safe_int(split_table[9]),
                        'completeness': safe_float(split_table[10]),
                        'contamination': safe_float(split_table[11]),
                        'strain_heterogeneity': safe_float(split_table[12]),
                        'quality_score': safe_float(split_table[13]),
                        'gtdb_classification': safe_value(split_table[14]),
                        'gtdb_phylum': safe_value(split_table[15]),
                        'closest_genome_reference': safe_value(split_table[16]),
                        'closest_genome_reference_radius': safe_float(split_table[17]),
                        'closest_genome_ani': safe_float(split_table[18]),
                        'closest_placement_reference': safe_value(split_table[19]),
                        'classification_method': safe_value(split_table[20]),
                        'note': safe_value(split_table[21]) if len(split_table) > 21 else None
                    }

                    # 检查是否已存在相同的记录
                    unique_fields = get_unique_fields(genome_data)
                    if Genome.objects.filter(**dict(zip(expected_fields[:len(unique_fields)], unique_fields))).exists():
                        skipped_count += 1
                        continue

                    # 创建新的 Genome 对象
                    new_genome = Genome(**genome_data)
                    new_genome.save()
                    added_count += 1

                except Exception as e:
                    print(f"错误：处理第 {line_number} 行时出现问题:")
                    print(f"  错误类型: {type(e).__name__}")
                    print(f"  错误信息: {str(e)}")
                    if hasattr(e, 'params'):
                        print(f"  缺失或有问题的字段: {', '.join(e.params)}")
                    error_count += 1

        print(f"成功添加 {added_count} 条新的 Genome 记录")
        print(f"跳过 {skipped_count} 条重复的记录")
        if error_count > 0:
            print(f"警告：处理过程中遇到 {error_count} 个错误")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
    print('Genome 模型导入完成！')
