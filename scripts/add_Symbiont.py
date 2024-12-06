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

def main():
    # 删除所有现有的 Symbiont 记录
    deleted_count = Symbiont.objects.all().delete()[0]
    print(f"已删除 {deleted_count} 条现有的 Symbiont 记录")

    added_count = 0
    error_count = 0

    # 定义字段映射关系（中文列名到英文字段名的映射）
    field_mapping = {
        '序号': 'id',
        '记录类型': 'record_type',
        '分类目': 'host_order',
        '分类科': 'host_family',
        '分类亚科': 'host_subfamily',
        '昆虫名称': 'host_species',
        '共生体分类门': 'symbiont_phylum',
        '共生体分类目': 'symbiont_order',
        '共生体分类属': 'symbiont_genus',
        '共生体分类级别': 'symbiont_rank',
        '共生体分类阶元': 'symbiont_taxon',
        '共生体名称': 'symbiont_name',
        '种类': 'classification',
        '功能': 'function',
        '功能标签': 'function_tag',
        '共生体序列数据': 'related_accession',
        '参考文献': 'reference',
        'doi号': 'doi',
        '期刊': 'journal',
        '出版年份': 'year',
        '备注': 'note'
    }

    try:
        with open('./data/symbionts241205.tab', 'r', encoding='UTF-8') as file:
            # 读取并验证表头
            headers = file.readline().strip().split('\t')
            english_headers = file.readline().strip().split('\t')  # 读取英文表头行

            for line_number, line in enumerate(file, start=3):
                try:
                    # 分割数据行
                    values = line.strip().split('\t')
                    if len(values) < len(headers):
                        print(f"警告：第 {line_number} 行数据不完整")
                        error_count += 1
                        continue

                    # 创建数据字典
                    symbiont_data = {}
                    for i, value in enumerate(values):
                        if i < len(headers):  # 确保不超出表头长度
                            field_name = field_mapping.get(headers[i])
                            if field_name:
                                # 特殊处理年份字段
                                if field_name == 'year':
                                    try:
                                        symbiont_data[field_name] = int(value) if value and value != 'None' else None
                                    except ValueError:
                                        symbiont_data[field_name] = None
                                else:
                                    symbiont_data[field_name] = value if value and value != 'None' else "NA"

                    # 创建新的 Symbiont 对象
                    new_symbiont = Symbiont(**symbiont_data)
                    new_symbiont.save()
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
        print(f"成功添加 {added_count} 条新的 Symbiont 记录")
        if error_count > 0:
            print(f"警告：处理过程中遇到 {error_count} 个错误")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
    print('Symbiont 数据导入完成！')
