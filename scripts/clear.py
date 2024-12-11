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

from django.db import connection

def main():
    try:
        with connection.cursor() as cursor:
            # 清空 gene_gene 表
            cursor.execute('TRUNCATE TABLE gene_gene CASCADE;')
            print("Gene 表数据已清空")
    except Exception as e:
        print(f"清空数据时出错: {e}")

if __name__ == "__main__":
    main()