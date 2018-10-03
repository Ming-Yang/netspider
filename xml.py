from lxml import etree

# 定义一个函数，给他一个html，返回xml结构
def getxpath(html):
    return etree.HTML(html)

# 下面是我们实战的第一个html
fd = open('temp.txt',mode='r')
sample1 = fd.read();

# 获取xml结构
s1 = getxpath(sample1)

sample2 = """
<html>
  <body>
    <ul>
      <li>Quote 1</li>
      <li>Quote 2 with <a href="...">link</a></li>
      <li>Quote 3 with <a href="...">another link</a></li>
      <li><h2>Quote 4 title</h2> ...</li>
    </ul>
  </body>
</html>
"""
s2 = getxpath(sample2)


# 获取标题(两种方法都可以)
#有同学在评论区指出我这边相对路径和绝对路径有问题，我搜索了下
#发现定义如下图
tds = s1.xpath('//tr[4]/td[2]/table/tr/td')
for td in tds:
	# print(td.a.title)
	print(td.text)

# detail = title.xpath('./parent/text()')
# print(title)
# print(detail)
# print(s1.xpath('//tr[2]/td[2]/table/tr/td/a/@title'))
# print(s1.xpath('//tr[2]/td[2]/table/tr/td/text()'))