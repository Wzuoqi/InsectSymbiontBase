"""
URL configuration for InsectSymbiontDB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="homepage"),
    path("home/", views.home, name="home"),
    path("test/", views.test, name="test"),
    path("network/", views.network, name="network"),
    path("resources/", views.resources, name="resources"),
    path("contact/", views.contact, name="contact"),

    #symbiont
    path('symbionts/',include(('symbiont.urls', 'symbiont'), namespace='symbiont')),

    #metagenome
    path('metagenomes/',include(('metagenome.urls', 'metagenome'), namespace='metagenome')),

    #amplicon
    path('amplicons/',include(('amplicon.urls', 'amplicon'), namespace='amplicon')),

    # article
    path('articles/',include(('article.urls', 'article'), namespace='article')),

    # genome
    path('genomes/',include(('genome.urls', 'genome'), namespace='genome')),

    # gene
    path('genes/',include(('gene.urls', 'gene'), namespace='gene')),

    # host
    path('hosts/', include('host.urls')),

    # tools
    path("blast/", views.blast, name="blast"),
    path("blast_search/", views.blast_search, name="blast_search"),

    path("batch_search/", views.batch_search, name="batch_search"),



    path("map/", views.map, name="map"),

    path('feedback/', include('feedback.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 添加媒体文件服务
