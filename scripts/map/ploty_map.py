import plotly.express as px
import pandas as pd
import plotly.io as pio

# 创建数据
data = {
    'geo_loc_name': ['Belgium:Londerzeel', 'USA: Idaho', 'China: Zhejiang', 'India: Tamil Nadu','Belgium:Londerzeel'],
    'Host': ['Musca domestica', 'Bactericera cockerelli', 'Drosophila melanogaster', 'Guava','Bombyx mori'],
    'lat': [50.991972, 42.58611, 30.3, 11.0069,50.991972],
    'lon': [4.282715, -114.30119, 120.2, 76.9309,4.282715]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 使用Plotly创建Buddle Map
fig = px.scatter_geo(df,
                     lat='lat',
                     lon='lon',
                     text='geo_loc_name',
                     hover_name='Host',
                     title="Sampling Locations for Two Data Types",
                     projection="natural earth")

# 将图表保存为HTML文件
pio.write_html(fig, file='sampling_locations_map.html', auto_open=False)

# 如果你想直接在Python环境中打开图表，可以使用以下命令
# fig.show()
