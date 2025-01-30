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

from gene.models import Gene
from django.db import IntegrityError

def main():
    # 删除所有现有的 Gene 记录
    deleted_count = Gene.objects.all().delete()[0]
    print(f"已删除 {deleted_count} 条现有的 Gene 记录")

    added_count = 0
    error_count = 0

    try:
        with open('./data/gene250131.tab', 'r') as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    # 分割数据行
                    values = line.strip().split('\t')
                    if len(values) < 18:  # 确保至少有基本字段 (新增host字段后至少18个)
                        print(f"警告：第 {line_number} 行数据不完整")
                        error_count += 1
                        continue

                    # 创建Gene对象的数据字典
                    gene_data = {
                        'host': values[0] if values[0] else 'None',  # 新增host字段
                        'source_id': values[1] if len(values) > 1 and values[1] else '',
                        'gene_id': values[2] if len(values) > 2 and values[2] else '',
                        'nr_id': values[3] if len(values) > 3 and values[3] else '',
                        'identity': float(values[4]) if len(values) > 4 and values[4] else 0.0,
                        'alignment_length': int(values[5]) if len(values) > 5 and values[5] else 0,
                        'mismatches': int(values[6]) if len(values) > 6 and values[6] else 0,
                        'gap_openings': int(values[7]) if len(values) > 7 and values[7] else 0,
                        'query_start': int(values[8]) if len(values) > 8 and values[8] else 0,
                        'query_end': int(values[9]) if len(values) > 9 and values[9] else 0,
                        'subject_start': int(values[10]) if len(values) > 10 and values[10] else 0,
                        'subject_end': int(values[11]) if len(values) > 11 and values[11] else 0,
                        'evalue': float(values[12]) if len(values) > 12 and values[12] else 0.0,
                        'bit_score': float(values[13]) if len(values) > 13 and values[13] else 0.0,
                        'sequence': values[14] if len(values) > 14 and values[14] else '',
                        'gene_length': int(values[15]) if len(values) > 15 and values[15] else 0,
                        'nr_annotation': values[16] if len(values) > 16 and values[16] else '',
                        'nr_species': values[17] if len(values) > 17 and values[17] else '',

                        # 以下字段索引都加1了，因为前面新增了host字段
                        'seed_ortholog': values[18] if len(values) > 18 and values[18] else '',
                        'eggnog_evalue': float(values[19]) if len(values) > 19 and values[19] else 0.0,
                        'eggnog_score': float(values[20]) if len(values) > 20 and values[20] else 0.0,
                        'eggnog_ogs': values[21] if len(values) > 21 and values[21] else '',
                        'max_annot_lvl': values[22] if len(values) > 22 and values[22] else '',
                        'cog_category': values[23] if len(values) > 23 and values[23] else '',
                        'description': values[24] if len(values) > 24 and values[24] else '',
                        'preferred_name': values[25] if len(values) > 25 and values[25] else '',
                        'go_terms': values[26] if len(values) > 26 and values[26] else '',
                        'ec_number': values[27] if len(values) > 27 and values[27] else '',
                        'kegg_ko': values[28] if len(values) > 28 and values[28] else '',
                        'kegg_pathway': values[29] if len(values) > 29 and values[29] else '',
                        'kegg_module': values[30] if len(values) > 30 and values[30] else '',
                        'kegg_reaction': values[31] if len(values) > 31 and values[31] else '',
                        'kegg_rclass': values[32] if len(values) > 32 and values[32] else '',
                        'brite': values[33] if len(values) > 33 and values[33] else '',
                        'kegg_tc': values[34] if len(values) > 34 and values[34] else '',
                        'cazy': values[35] if len(values) > 35 and values[35] else '',
                        'bigg_reaction': values[36] if len(values) > 36 and values[36] else '',
                        'pfams': values[37] if len(values) > 37 and values[37] else ''
                    }

                    # 创建新的 Gene 对象
                    new_gene = Gene(**gene_data)
                    new_gene.save()
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
        print(f"成功添加 {added_count} 条新的 Gene 记录")
        if error_count > 0:
            print(f"警告：处理过程中遇到 {error_count} 个错误")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
    print('Gene 数据导入完成！')
