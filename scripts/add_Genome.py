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

def main():
    # 删除所有现有的 Genome 记录
    deleted_count = Genome.objects.all().delete()[0]
    print(f"已删除 {deleted_count} 条现有的 Genome 记录")

    added_count = 0
    error_count = 0

    # 定义字段映射关系
    field_mapping = {
        'Genome ID': 'genome_id',
        'Source ID': 'source_id',
        'Source': 'source',
        'Host': 'host',
        'Function': 'function',
        'Reference Name': 'reference_name',  # 添加 Reference Name 字段
        'Reference Accession': 'reference_accession',
        'Reference Phylum': 'reference_phylum',
        'Reference Order': 'reference_order',
        'Reference Genus': 'reference_genus',
        'CheckM Marker lineage': 'checkm_marker_lineage',
        'CheckM genomes': 'checkm_genomes',
        'CheckM markers': 'checkm_markers',
        'Completeness': 'completeness',
        'Contamination': 'contamination',
        'Strain heterogeneity': 'strain_heterogeneity',
        'QS': 'quality_score',
        'gtdb classification': 'gtdb_classification',
        'gtdb Phylum': 'gtdb_phylum',
        'closest_genome_reference': 'closest_genome_reference',
        'closest_genome_reference_radius': 'closest_genome_reference_radius',
        'closest_genome_ani': 'closest_genome_ani',
        'closest_placement_reference': 'closest_placement_reference',
        'classification_method': 'classification_method',
        'note': 'note'
    }

    try:
        with open('./data/genomes250109.tab', 'r', encoding='UTF-8') as file:
            # 读取并验证表头
            headers = file.readline().strip().split('\t')

            for line_number, line in enumerate(file, start=2):
                try:
                    # 分割数据行
                    values = line.strip().split('\t')
                    if len(values) < len(headers):
                        print(f"警告：第 {line_number} 行数据不完整")
                        error_count += 1
                        continue

                    # 创建数据字典
                    genome_data = {}
                    for i, value in enumerate(values):
                        if i < len(headers):  # 确保不超出表头长度
                            field_name = field_mapping.get(headers[i])
                            if field_name:
                                # 特殊处理数值字段
                                if field_name in ['checkm_genomes', 'checkm_markers']:
                                    genome_data[field_name] = int(value) if value and value != 'None' else None
                                elif field_name in ['completeness', 'contamination', 'strain_heterogeneity', 'quality_score', 'closest_genome_reference_radius', 'closest_genome_ani']:
                                    genome_data[field_name] = float(value) if value and value != 'None' else None
                                else:
                                    # 处理空值和None值
                                    genome_data[field_name] = value if value and value != 'None' else "NA"

                    # 创建新的 Genome 对象
                    new_genome = Genome(**genome_data)
                    new_genome.save()
                    added_count += 1

                    # 每1000条记录打印一次进度
                    if added_count % 1000 == 0:
                        print(f"已处理 {added_count} 条记录...")

                except Exception as e:
                    print(f"错误：处理第 {line_number} 行时出现问题:")
                    print(f"  错误类型: {type(e).__name__}")
                    print(f"  错误信息: {str(e)}")
                    error_count += 1

        print(f"\n数据导入完成:")
        print(f"成功添加 {added_count} 条新的 Genome 记录")
        if error_count > 0:
            print(f"警告：处理过程中遇到 {error_count} 个错误")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
    print('Genome 数据导入完成！')