### **💾 Gene 索引恢复与 Elasticsearch 相关信息汇总**
为了方便后续**使用大模型修改 Django 项目**，以下是 `genes` 索引相关的重要信息，供大模型参考：

---

## **1️⃣ Elasticsearch 服务器信息**
- **Elasticsearch 版本**：`7.17.7`
- **运行端口**：`9201`
- **Elasticsearch 配置文件**：
  - **`elasticsearch.yml` 关键参数**：
    ```yaml
    cluster.name: my-django-cluster
    node.name: node-1
    path.data: /home/elasticsearch_data
    path.logs: /var/log/elasticsearch
    network.host: 0.0.0.0
    http.port: 9201
    discovery.type: single-node
    ```
  - **快照存储路径**：`/home/elasticsearch_data/snapshots`

---

## **2️⃣ 快照恢复信息**
- **快照仓库名称**：`my_backup`
- **快照名称**：`genes_snapshot`
- **快照存储路径**（云服务器）：
  ```bash
  /home/elasticsearch_data/snapshots
  ```
- **快照恢复操作**
  ```bash
  curl -X POST "localhost:9201/_snapshot/my_backup/genes_snapshot/_restore" \
       -H 'Content-Type: application/json' \
       -d '{
         "indices": "genes",
         "ignore_unavailable": true,
         "include_global_state": false
       }'
  ```
- **快照恢复进度检查**
  ```bash
  curl -X GET "localhost:9201/_cat/recovery?v"
  ```

---

## **3️⃣ Gene 索引状态**
- **索引名称**：`genes`
- **索引状态检查**
  ```bash
  curl -X GET "localhost:9201/_cat/indices?v"
  ```
  **期望结果（示例）**
  ```
  health status index uuid                   pri rep docs.count docs.deleted store.size pri.store.size
  green  open   genes  XqLqasQuTU2qoN1vFMRQOw  1   0   23041894   0            80.1gb      80.1gb
  ```

---

## **4️⃣ Gene 索引结构**
在 Django `models.py` 中定义的 `Gene` Model 结构：
```python
class Gene(models.Model):
    host = models.CharField(max_length=200, db_index=True, default='None')
    source_id = models.CharField(max_length=200, db_index=True)
    gene_id = models.CharField(max_length=200, db_index=True)
    nr_id = models.CharField(max_length=200, null=True, blank=True)

    identity = models.FloatField(null=True, blank=True, default=0.0)
    alignment_length = models.IntegerField(null=True, blank=True, default=0)
    mismatches = models.IntegerField(null=True, blank=True, default=0)
    gap_openings = models.IntegerField(null=True, blank=True, default=0)
    query_start = models.IntegerField(null=True, blank=True, default=0)
    query_end = models.IntegerField(null=True, blank=True, default=0)
    subject_start = models.IntegerField(null=True, blank=True, default=0)
    subject_end = models.IntegerField(null=True, blank=True, default=0)
    evalue = models.FloatField(null=True, blank=True, default=0.0)
    bit_score = models.FloatField(null=True, blank=True, default=0.0)
    sequence = models.TextField(default='')

    nr_annotation = models.TextField(null=True, blank=True, default='')
    nr_species = models.TextField(null=True, blank=True, default='')
    seed_ortholog = models.TextField(null=True, blank=True, default='')

    description = models.TextField(null=True, blank=True, default='')
    preferred_name = models.TextField(null=True, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

- **索引字段示例**
  ```json
  {
    "gene_id": "XYZ123",
    "nr_annotation": "Example annotation",
    "description": "Sample gene description",
    "identity": 95.6,
    "bit_score": 110.2
  }
  ```

---

## **5️⃣ Elasticsearch 索引查询**
- **文档总数检查**
  ```bash
  curl -X GET "localhost:9201/genes/_count?pretty"
  ```
  **示例返回**
  ```json
  {
    "count": 23041894,
    "_shards": {
      "total": 1,
      "successful": 1,
      "skipped": 0,
      "failed": 0
    }
  }
  ```

- **全文搜索（所有文档）**
  ```bash
  curl -X GET "localhost:9201/genes/_search?pretty" \
       -H 'Content-Type: application/json' \
       -d '{
         "query": {
           "match_all": {}
         },
         "size": 2
       }'
  ```
  **示例返回**
  ```json
  {
    "hits": {
      "total": 23041894,
      "hits": [
        {
          "_source": {
            "gene_id": "XYZ123",
            "nr_annotation": "Example annotation",
            "description": "Sample gene description"
          }
        },
        {
          "_source": {
            "gene_id": "ABC456",
            "nr_annotation": "Another annotation",
            "description": "Another gene description"
          }
        }
      ]
    }
  }
  ```

- **按 `gene_id` 精确匹配**
  ```bash
  curl -X GET "localhost:9201/genes/_search?pretty" \
       -H 'Content-Type: application/json' \
       -d '{
         "query": {
           "term": {
             "gene_id": "XYZ123"
           }
         }
       }'
  ```

- **按 `nr_annotation` 进行模糊搜索**
  ```bash
  curl -X GET "localhost:9201/genes/_search?pretty" \
       -H 'Content-Type: application/json' \
       -d '{
         "query": {
           "match": {
             "nr_annotation": "annotation"
           }
         }
       }'
  ```

---

## **6️⃣ Django 项目 Elasticsearch 相关配置**
在 `settings.py` 配置：
```python
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://localhost:9201',
        'timeout': 60,
    },
}
```
在 Django `views.py` 中进行搜索：
```python
from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9201"])

def search_gene_by_id(gene_id):
    query = {
        "query": {
            "term": {
                "gene_id": gene_id
            }
        }
    }
    result = es.search(index="genes", body=query)
    return result['hits']['hits']
```
Django `urls.py`：
```python
from django.urls import path
from .views import search_gene

urlpatterns = [
    path('search/<str:gene_id>/', search_gene),
]
```
Django `views.py`：
```python
from django.http import JsonResponse
from .elasticsearch_client import search_gene_by_id

def search_gene(request, gene_id):
    result = search_gene_by_id(gene_id)
    return JsonResponse(result, safe=False)
```

---

## **📌 总结**
**对大模型有帮助的信息**
1. **Elasticsearch 服务器信息**
   - 运行端口：`9201`
   - 快照存储路径：`/home/elasticsearch_data/snapshots`
   - 索引名：`genes`
2. **快照恢复操作**
   - 快照仓库 `my_backup`，快照名 `genes_snapshot`
   - 80.1GB 数据，`23041894` 条文档
3. **Django 项目**
   - 关键模型字段：`gene_id`, `nr_annotation`, `description`
   - Elasticsearch 查询示例

🚀 **这些信息可以帮助大模型理解 Elasticsearch 索引，并自动生成 Django 代码来实现 Gene 搜索功能！**