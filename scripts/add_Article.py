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

def main():
    from article.models import Article  # 这里需要确认 'article' 是您的 Django app 名称
    article_list = []

    # 打开制表符分隔的文件
    with open('data/test_articles.tab', 'r', encoding='UTF-8') as file:
        for line in file:
            split_table = line.strip().split('\t')
            article_id = int(split_table[0])  # 假设 id 是整数类型
            title = split_table[1]
            authors = split_table[2]
            publish_time = int(split_table[3])  # 假设 publish_time 是整数类型
            journal = split_table[4]
            doi = split_table[5]
            wos = split_table[6]
            accession_numbers = split_table[7]
            species = split_table[8]

            # 创建 Article 对象
            tmp_article = Article(
                id=article_id,
                title=title,
                authors=authors,
                publish_time=publish_time,
                journal=journal,
                doi=doi,
                wos=wos,
                accession_numbers=accession_numbers,
                species=species
            )

            # 将对象添加到列表中
            article_list.append(tmp_article)

    # 批量插入数据库
    Article.objects.bulk_create(article_list)

if __name__ == "__main__":
    main()
    print('Article model import Done!')