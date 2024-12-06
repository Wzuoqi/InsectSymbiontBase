import requests
import xml.etree.ElementTree as ET
import sys

def get_taxonomy_info(species_name, cache={}):
    # 如果物种名为None或NA则直接返回
    if species_name is None or species_name.strip().lower() == "na":
        return f"No taxonomy information found for {species_name}"

    # 使用缓存避免重复请求
    if species_name in cache:
        return cache[species_name]

    try:
        # 通过物种名搜索 NCBI Taxonomy 数据库
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&term={species_name}[Scientific Name]&retmode=xml"
        search_response = requests.get(search_url)
        search_response.raise_for_status()
        search_tree = ET.fromstring(search_response.content)

        error_list = search_tree.find("ErrorList")
        if error_list is not None:
            return f"No taxonomy information found for {species_name}"

        tax_id = search_tree.find("IdList/Id")
        if tax_id is None:
            return f"No taxonomy information found for {species_name}"
        tax_id = tax_id.text

        # 通过 Taxonomy ID 获取分类信息
        fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id={tax_id}&retmode=xml"
        fetch_response = requests.get(fetch_url)
        fetch_response.raise_for_status()
        fetch_tree = ET.fromstring(fetch_response.content)

        # 解析分类信息
        taxonomy_info = {
            "organism": species_name,
            "phylum": "",
            "class": "",
            "subclass": "",
            "infraclass": "",
            "cohort": "",
            "superorder": "",
            "order": "",
            "suborder": "",
            "infraorder": "",
            "parvorder": "",
            "superfamily": "",
            "family": "",
            "subfamily": "",
            "tribe": "",
            "subtribe": "",
            "genus": ""
        }

        for taxon in fetch_tree.iter("Taxon"):
            rank = taxon.find("Rank").text.lower()
            name = taxon.find("ScientificName").text
            if rank in taxonomy_info:
                taxonomy_info[rank] = name

        # 将结果保存到缓存中
        cache[species_name] = taxonomy_info
        return taxonomy_info

    except requests.exceptions.RequestException as e:
        return f"Network error occurred: {str(e)}"
    except ET.ParseError as e:
        return f"XML parsing error occurred: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


# 从命令行参数读取物种名文件路径
species_file = sys.argv[1]

# 从文件中读取物种名
with open(species_file, 'r') as file:
    species_list = [line.strip() for line in file]

# 处理每个物种并打印结果
for species_name in species_list:
    taxonomy_info = get_taxonomy_info(species_name)
    if isinstance(taxonomy_info, dict):
        output = "\t".join(taxonomy_info.get(rank, "") for rank in taxonomy_info)
        print(output)
    else:
        print(taxonomy_info)
