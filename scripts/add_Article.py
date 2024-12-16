import django
import os
import sys
import csv
from datetime import datetime

# 获取脚本所在的目录
script_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(script_path, '..'))
sys.path.append(project_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InsectSymbiontDB.settings")
django.setup()

def clean_data(value):
    """清理数据中的特殊字符和格式"""
    if isinstance(value, str):
        value = value.strip('"').strip()
        value = value.replace('\n', ' ').replace('\r', ' ')
        value = ' '.join(value.split())
    return value if value and value != 'None' else "NA"

def clear_existing_data():
    """删除数据库中已存在的所有文章数据"""
    from article.models import Article
    try:
        existing_count = Article.objects.count()
        Article.objects.all().delete()
        print(f"Successfully deleted {existing_count} existing articles")
        return True
    except Exception as e:
        print(f"Error clearing existing data: {str(e)}")
        return False

def main():
    from article.models import Article

    # 首先清除现有数据
    if not clear_existing_data():
        print("Failed to clear existing data. Aborting import.")
        return

    article_list = []
    error_records = []

    print("Starting to read and process new data...")

    try:
        # 打开TSV文件
        with open('scripts/data/articles241216.tab', 'r', encoding='UTF-8') as file:
            # 读取第一行获取列名
            header = file.readline().strip().split('\t')

            # 计算总行数
            total_rows = sum(1 for line in file)
            file.seek(0)  # 重置文件指针
            next(file)    # 跳过标题行

            # 逐行处理数据
            for row_num, line in enumerate(file, start=1):
                try:
                    # 分割行数据
                    fields = line.strip().split('\t')
                    if len(fields) != len(header):
                        raise ValueError(f"Column count mismatch. Expected {len(header)}, got {len(fields)}")

                    # 创建数据字典
                    row_data = dict(zip(header, fields))

                    # 准备文章数据
                    article_data = {
                        'id': int(row_data['ID']),
                        'title': clean_data(row_data['Title']),
                        'authors': clean_data(row_data['Authors']),
                        'doi': clean_data(row_data['doi']),
                        'journal': clean_data(row_data['Journal']),
                        'publish_time': int(row_data['Publish Time']),
                        'species': clean_data(row_data['Species']),
                        'symbiont': clean_data(row_data['Symbiont'])
                    }

                    # 创建 Article 对象
                    article = Article(**article_data)
                    article_list.append(article)

                    # 显示进度
                    if row_num % 100 == 0:
                        print(f"Processed {row_num}/{total_rows} records...")

                except Exception as e:
                    error_records.append({
                        'row': row_num,
                        'data': line.strip(),
                        'error': str(e)
                    })
                    print(f"Error in row {row_num}: {str(e)}")
                    continue

        # 批量创建记录
        if article_list:
            Article.objects.bulk_create(article_list, batch_size=100)
            print(f"Successfully imported {len(article_list)} articles")

        # 如果有错误记录，保存到文件
        if error_records:
            error_file_path = 'scripts/data/import_errors.log'
            with open(error_file_path, 'w', encoding='UTF-8') as error_file:
                for record in error_records:
                    error_file.write(f"Row {record['row']}:\n")
                    error_file.write(f"Data: {record['data']}\n")
                    error_file.write(f"Error: {record['error']}\n")
                    error_file.write("-" * 50 + "\n")
            print(f"Found {len(error_records)} errors. Check {error_file_path} for details")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print("Starting data import process...")
    main()
    print('Article model import completed!')