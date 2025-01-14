import pandas as pd
import plotly.express as px

def preprocess_and_plot(file1, file2, label1, label2, color1, color2, symbol1, symbol2):
    def process_file(tsv_file, data_label, symbol):
        try:
            # 读取TSV文件
            df = pd.read_csv(tsv_file, sep='\t', encoding='utf-8')
        except Exception as e:
            print(f"Error reading file {tsv_file}: {e}")
            return pd.DataFrame()  # 返回空DataFrame

        if 'lat_lon' not in df.columns:
            print(f"Missing required column 'lat_lon' in {tsv_file}")
            return pd.DataFrame()

        # 处理经纬度数据：提取纬度和经度
        def parse_lat_lon(lat_lon_str):
            try:
                # 移除所有逗号
                lat_lon_str = lat_lon_str.replace(',', '')
                parts = lat_lon_str.split()

                # 如果第一个部分是 E/W，说明是反向格式
                if parts[0] in ['E', 'W']:
                    # 格式: E/W 经度 N/S 纬度
                    lon = float(parts[1])
                    if parts[0] == 'W':
                        lon = -lon

                    lat = float(parts[3])
                    if parts[2] == 'S':
                        lat = -lat
                else:
                    # 标准格式: 纬度 N/S 经度 E/W
                    lat = float(parts[0])
                    if parts[1] == 'S':
                        lat = -lat

                    lon = float(parts[2])
                    if parts[3] == 'W':
                        lon = -lon

                return lat, lon
            except (ValueError, IndexError) as e:
                print(f"Error parsing lat_lon: {lat_lon_str}. Error: {e}")
                return None, None

        df[['lat', 'lon']] = df['lat_lon'].apply(parse_lat_lon).apply(pd.Series)

        def validate_coordinates(lat, lon):
            """验证经纬度是否在合理范围内"""
            if lat is None or lon is None:
                return False
            if not (-90 <= lat <= 90):
                print(f"Invalid latitude: {lat}")
                return False
            if not (-180 <= lon <= 180):
                print(f"Invalid longitude: {lon}")
                return False
            return True

        df['valid_coords'] = df.apply(lambda row: validate_coordinates(row['lat'], row['lon']), axis=1)
        df = df[df['valid_coords']].drop('valid_coords', axis=1)

        def format_host_name(host, count):
            """格式化Host名称，将物种名设置为斜体"""
            non_italic_terms = {'None', 'not applicable', 'irrigation channels', 'Drainage ditches',
                               'paddy fields', 'large water containers', 'Sargassum'}

            if host in non_italic_terms:
                return f"{host} * {count}" if count > 1 else host
            else:
                return f"<i>{host}</i> * {count}" if count > 1 else f"<i>{host}</i>"

        # 按地点和Host合并数据，并计算相同Host的出现次数
        grouped_df = df.groupby(['geo_loc_name', 'lat', 'lon', 'Host'], as_index=False).size()
        grouped_df['Host'] = grouped_df.apply(
            lambda row: format_host_name(row['Host'], row['size']),
            axis=1
        )

        # 添加数据标签列和标记符号
        grouped_df['Data Label'] = data_label
        grouped_df['Symbol'] = symbol

        # 按地点合并所有Host信息
        final_df = grouped_df.groupby(['geo_loc_name', 'lat', 'lon', 'Data Label', 'Symbol'], as_index=False).agg({
            'Host': lambda x: '<br>'.join(x)
        })

        # 计算每个点的大小（根据Host数量）
        final_df['size'] = final_df['Host'].apply(lambda x: min(len(x.split('<br>')) * 1.5, 15))

        return final_df

    # 处理两个文件
    df1 = process_file(file1, label1, symbol1)
    df2 = process_file(file2, label2, symbol2)

    # 合并两个数据集
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # 使用Plotly创建Buddle Map
    fig = px.scatter_geo(combined_df,
                         lat='lat',
                         lon='lon',
                         size='size',
                         color='Data Label',  # 使用Data Label来区分颜色
                         symbol='Symbol',  # 使用Symbol来区分标记形状
                         hover_name='geo_loc_name',
                         hover_data={'Host': True, 'size': False},
                         title="Sampling Locations of Metagenomes and Amplicons associated with Insect Symbiont Worldwide",
                         projection="natural earth",
                         color_discrete_map={label1: color1, label2: color2})  # 自定义颜色映射

    # 更新图表布局，删除图例
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
            font_size=16,
            font_family="Arial",
            font_color='rgba(0, 0, 0, 0.8)'
        ),
        showlegend=False,  # 隐藏图例
        margin=dict(l=10, r=10, t=50, b=10),
        title_x=0.5,
        hovermode='closest'
    )

    # 将图表保存为HTML文件
    output_html = 'sample_map.html'
    fig.write_html(output_html, auto_open=False)

    print(f"Map has been saved to {output_html}")

def check_data_format(df, filename):
    """检查数据格式并打印统计信息"""
    print(f"\nChecking data in {filename}:")
    print(f"Total rows: {len(df)}")
    print(f"Unique lat_lon formats found:")
    for format_example in df['lat_lon'].unique()[:5]:
        print(f"  - {format_example}")
    print(f"Missing values:")
    print(df.isnull().sum())

# 示例用法：
file1 = 'amplicons.tsv'  # 替换为你的第一个TSV文件路径
file2 = 'metagenomes.tsv'  # 替换为你的第二个TSV文件路径
label1 = 'Amplicon'  # 第一个数据集的标签
label2 = 'Metagenome'  # 第二个数据集的标签

# 自定义颜色
color1 = 'rgba(0, 64, 150, 0.7)'  # Amplicon数据点颜色
color2 = 'rgba(184, 207, 143, 0.7)'  # Metagenome数据点颜色

# 自定义标记形状
symbol1 = 'circle'  # Amplicon数据点标记形状
symbol2 = 'circle'  # Metagenome数据点标记形状

preprocess_and_plot(file1, file2, label1, label2, color1, color2, symbol1, symbol2)
