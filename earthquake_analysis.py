import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl  #用于修改 x 轴坐标


pl.rcParams['font.sans-serif'] = ['SimHei']  # 防中文显示成小方块


plt.style.use('ggplot')   #默认绘图风格很难看，替换为好看的 ggplot 风格
fig = plt.figure(figsize=(8,5))   #设置图片大小
colors1 = '#FF8000'  #设置图表 title、text 标注的颜色

columns = ['CATA_ID', 'Magnitude', 'Earthquake_Time', 'Latitude', 'Longitude', 'Depth', 'Earthquake_Location', 'Url']  #设置表头
df = pd.read_csv('最近一年世界地震情况.csv',encoding = "utf-8",header = None,names =columns)  #打开表格

df_score = df.sort_values('Magnitude',ascending = False)  #按得分降序排列
# df # 查看全部数据
# df.head()  # 默认前5行
# df.info()


## 分析近一年全球震级级别最高 top10
def analisis_level():
    loc = df_score.Earthquake_Location[:10]      #x 轴坐标
    m = df_score.Magnitude[:10]    #y 轴坐标  
    plt.bar(range(10),m,tick_label = loc)  #绘制条形图，用 range()能搞保持 x 轴正确顺序
    plt.ylim ((1,10))  #设置纵坐标轴范围
    plt.title('近一年全球震级级别最高 top10',color = colors1) #标题
    plt.xlabel('地震具体位置',color = colors1)      #x 轴标题
    plt.ylabel('震级级别',color = colors1)          #y 轴标题

    # 为每个条形图添加数值标签
    for x,y in enumerate(list(m)):
        plt.text(x,y+0.2,'%s' %round(y,1),ha = 'center')
    pl.xticks(rotation=290)   #x 轴名称太长发生重叠，旋转为纵向显示
    plt.tight_layout()    #自动控制空白边缘，以全部显示 x 轴名称

    plt.savefig('近一年全球震级级别最高 top10.png')   #保存图片
    #plt.show()
    
## analisis_level()


## 分析近一年全球每月发生地震次数排名
def analysis_times():
    # 从日期中提取月份
    df['Earthquake_Time'] = df['Earthquake_Time'].map(lambda x:x.split('-')[1])
    # print(df.info())
    # print(df.head())

    # 统计各月发生地震次数
    grouped_month = df.groupby('Earthquake_Time')
    grouped_month_amount = grouped_month.Earthquake_Time.count()
    top_month = grouped_month_amount.sort_values(ascending = False)
    # 绘图
    top_month.plot(kind = 'bar',color = '#58ACFA') 
    for x,y in enumerate(list(top_month.values)):
        plt.text(x,y+0.8,'%s' %round(y,1),ha = 'center',color = "red")
    pl.xticks(rotation=0)   #x 轴名称太长发生重叠，旋转为纵向显示
    plt.title('近一年全球每月发生地震次数排名',color = colors1)
    plt.xlabel('月份(年月)')
    plt.ylabel('地震次数(此次)')
    plt.tight_layout()
    plt.savefig('近一年全球每月发生地震次数排名.png')
    # plt.show()

## analysis_times()


## 分析近一年中全球各地地震地区分布占比情况
def analysis_sites():
    # 绘制饼图并保存 

    count = df['Earthquake_Location'].value_counts()

    plt.pie(count, labels = count.keys(),labeldistance=1.4,autopct='%2.1f%%') 

    plt.axis('equal') # 使饼图为正圆形 

    plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1)) 

    plt.savefig('地震地区分布占比图.png') 

    # plt.show()

## analysis_sites()


## 分析近一年地震级别级数分布占比情况
def analysis_level_scores():
    # 绘制饼图并保存 

    count = df['Magnitude'].value_counts()

    plt.pie(count, labels = count.keys(),labeldistance=1.4,autopct='%2.1f%%') 

    plt.axis('equal') # 使饼图为正圆形 

    plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1)) 

    plt.savefig('地震级别级数分布占比图.png') 

    # plt.show() 

## analysis_level_scores()


## 制作地震高频地区分布词云图
def make_wordcloud():
    import pandas as pd
    import matplotlib.dates as mdate
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    columns = ['CATA_ID', 'Magnitude', 'Earthquake_Time', 'Latitude', 'Longitude', 'Depth', 'Earthquake_Location', 'Url']  #设置表头
    df = pd.read_csv('最近一年世界地震情况.csv',encoding = "utf-8",header = None,names =columns)  #打开表格
    #df = df.groupby(by = 'Magnitude').count()
    #df = df['Earthquake_Location'].sort_values(ascending = False)
    #df.head()
    df = df.groupby(by = 'Earthquake_Location').count()
    df = df['Magnitude'].sort_values(ascending = False)
    #print(df[:10])

    font_path='simfang.ttf'  # 仿宋
    #background_Image='ditu.jpg'
    wordcloud = WordCloud(
        background_color = '#F3F3F3',
        font_path = font_path,
        #mask = background_Image,
        width = 1200,
        height = 800,
        margin = 2,
        max_font_size = 200,
        random_state = 42,
        scale = 2,
        colormap = 'viridis',  # 默认virdis
        )
    #wordcloud.generate_from_frequencies(df)
    # or
    wordcloud.fit_words(df)
    plt.imshow(wordcloud,interpolation = 'bilinear')
    plt.axis('off')
    plt.savefig('地震高频地区分布词云制作图.png')
    # plt.show()
    
## make_wordcloud()
     
