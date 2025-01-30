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
        with open('./data/gene250130.tab', 'r') as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    # 分割数据行
                    values = line.strip().split('\t')
                    if len(values) < 17:  # 确保至少有基本字段
                        print(f"警告：第 {line_number} 行数据不完整")
                        error_count += 1
                        continue

                    # 创建数据字典，严格按照表格顺序和models字段顺序
                    gene_data = {
                        'source_id': values[0],
                        'gene_id': values[1],
                        'nr_id': values[2],
                        'identity': float(values[3]) if values[3] else 0.0,
                        'alignment_length': int(values[4]) if values[4] else 0,
                        'mismatches': int(values[5]) if values[5] else 0,
                        'gap_openings': int(values[6]) if values[6] else 0,
                        'query_start': int(values[7]) if values[7] else 0,
                        'query_end': int(values[8]) if values[8] else 0,
                        'subject_start': int(values[9]) if values[9] else 0,
                        'subject_end': int(values[10]) if values[10] else 0,
                        'evalue': float(values[11]) if values[11] else 0.0,
                        'bit_score': float(values[12]) if values[12] else 0.0,
                        'sequence': values[13],
                        'gene_length': int(values[14]) if values[14] else 0,
                        'nr_annotation': values[15] if values[15] else '',
                        'nr_species': values[16] if values[16] else ''
                    }

                    # 处理eggNOG注释部分（如果存在）
                    if len(values) > 17:
                        gene_data.update({
                            'seed_ortholog': values[17] if len(values) > 17 and values[17] else '',
                            'eggnog_evalue': float(values[18]) if len(values) > 18 and values[18] else 0.0,
                            'eggnog_score': float(values[19]) if len(values) > 19 and values[19] else 0.0,
                            'eggnog_ogs': values[20] if len(values) > 20 and values[20] else '',
                            'max_annot_lvl': values[21] if len(values) > 21 and values[21] else '',
                            'cog_category': values[22] if len(values) > 22 and values[22] else '',
                            'description': values[23] if len(values) > 23 and values[23] else '',
                            'preferred_name': values[24] if len(values) > 24 and values[24] else '',
                            'go_terms': values[25] if len(values) > 25 and values[25] else '',
                            'ec_number': values[26] if len(values) > 26 and values[26] else '',
                            'kegg_ko': values[27] if len(values) > 27 and values[27] else '',
                            'kegg_pathway': values[28] if len(values) > 28 and values[28] else '',
                            'kegg_module': values[29] if len(values) > 29 and values[29] else '',
                            'kegg_reaction': values[30] if len(values) > 30 and values[30] else '',
                            'kegg_rclass': values[31] if len(values) > 31 and values[31] else '',
                            'brite': values[32] if len(values) > 32 and values[32] else '',
                            'kegg_tc': values[33] if len(values) > 33 and values[33] else '',
                            'cazy': values[34] if len(values) > 34 and values[34] else '',
                            'bigg_reaction': values[35] if len(values) > 35 and values[35] else '',
                            'pfams': values[36] if len(values) > 36 and values[36] else ''
                        })

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
