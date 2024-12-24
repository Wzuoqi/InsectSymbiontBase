from django.contrib import admin
from .models import Host

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    # 列表页显示的字段
    list_display = ('species', 'order', 'family', 'subfamily', 'genus', 'common_name')

    # 可以搜索的字段
    search_fields = ('species', 'order', 'family', 'genus', 'common_name')

    # 可以筛选的字段
    list_filter = ('order', 'family', 'subfamily')

    # 排序方式
    ordering = ('species',)

    # 详情页字段分组
    fieldsets = (
        ('基本信息', {
            'fields': ('species', 'common_name', 'description')
        }),
        ('分类信息', {
            'fields': ('order', 'family', 'subfamily', 'genus')
        }),
    )

    # 每页显示的记录数
    list_per_page = 50

    # 允许在列表页直接编辑的字段
    list_editable = ('common_name',)

    # 在列表页显示详细信息的字段
    list_display_links = ('species',)
