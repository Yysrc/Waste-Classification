import jieba
import wordcloud
import imageio
from matplotlib import colors

# 装载停用词
f = open("stopword.txt", encoding='UTF8')
fl = f.readlines()
stoplist = []
for line in fl:
    stoplist.append(line.strip('\n'))
f.close()

# 统计词频的字典
wordfreq = dict()

with open('comment.txt', encoding='utf-8') as f:
    t = f.read()

# 切分、停用词过滤、统计词频
for w in list(jieba.cut(t, cut_all=False)):
    if len(w) > 1 and w not in stoplist:
        if w not in wordfreq:
            wordfreq[w] = 1
        else:
            wordfreq[w] = wordfreq[w] + 1

# 词云图形状
mask = imageio.imread('shape.png')

color_list = ['#436E67']
colormap = colors.ListedColormap(color_list)

# 绘制词云图
w = wordcloud.WordCloud(
    width=2000, 
    height=1400,
    font_path="msyh.ttc",
    colormap=colormap,
    mask=mask,
    max_words=130,
    background_color='white')

# 将词组变量txt导入词云对象w中并保存
w.generate_from_frequencies(wordfreq)
w.to_file('analyse.png')
