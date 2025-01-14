import pandas as pd
import plotly.express as px

def preprocess_and_plot(tsv_file):
    # 读取TSV文件
    df = pd.read_csv(tsv_file, sep='\t')

    # 处理经纬度数据：提取纬度和经度
    def parse_lat_lon(lat_lon_str):
        try:
            parts = lat_lon_str.split()
            lat = float(parts[0])
            if 'S' in parts:
                lat = -lat
            lon = float(parts[2])
            if 'W' in parts:
                lon = -lon
            return lat, lon
        except (ValueError, IndexError) as e:
            print(f"Error parsing lat_lon: {lat_lon_str}. Error: {e}")
            return None, None

    df[['lat', 'lon']] = df['lat_lon'].apply(parse_lat_lon).apply(pd.Series)

    # 删除无法解析的行
    df = df.dropna(subset=['lat', 'lon'])

    # 按地点和Host合并数据，并计算相同Host的出现次数
    grouped_df = df.groupby(['geo_loc_name', 'lat', 'lon', 'Host'], as_index=False).size()
    grouped_df['Host'] = grouped_df.apply(lambda row: f"{row['Host']} * {row['size']}" if row['size'] > 1 else row['Host'], axis=1)

    # 按地点合并所有Host信息
    final_df = grouped_df.groupby(['geo_loc_name', 'lat', 'lon'], as_index=False).agg({
        'Host': lambda x: '<br>'.join(x)
    })

    # 计算每个点的大小（根据Host数量）
    final_df['size'] = final_df['Host'].apply(lambda x: min(len(x.split('<br>')) * 1.5, 15))

    # 使用Plotly创建Buddle Map
    fig = px.scatter_geo(final_df,
                         lat='lat',
                         lon='lon',
                         size='size',  # 根据合并后的Host数量调整点的大小
                         hover_name='geo_loc_name',  # 显示位置名称
                         hover_data={'Host': True, 'size': False},  # 显示所有Host
                         title="Sampling Locations of Metagenomes and Amplicons associated with Insect Symbionts",
                         projection="natural earth")

    # 更新图表布局，调整颜色和透明度
    fig.update_traces(marker=dict(color='rgba(0, 64, 150, 0.7)'),  # 调整颜色数据点，透明度为0.7
                      selector=dict(mode='markers'))

    # 更新悬浮标签样式
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",  # 悬浮框背景色
            bordercolor="black",  # 边框颜色
            font_size=16,     # 字体大小
            font_family="Arial",  # 字体类型
            font_color='rgba(0, 0, 0, 0.8)'  # 深色字体
        ),
        showlegend=False  # 隐藏图例
    )

    # 设置hovermode为closest，确保指向箭头出现
    fig.update_layout(
        hovermode='closest'
    )

    # 将图表保存为HTML文件
    output_html = 'aggregated_sampling_locations_map.html'
    fig.write_html(output_html, auto_open=False)

    print(f"Map has been saved to {output_html}")

# 示例用法：
tsv_file = 'test.tsv'  # 替换为你的TSV文件路径
preprocess_and_plot(tsv_file)
