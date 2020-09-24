[toc]



## 宝贝回家网页爬虫

### 爬虫的思路

最方便进行爬取的页面是这里[https://www.baobeihuijia.com/so.aspx](https://www.baobeihuijia.com/so.aspx)，只需要进行一些筛选就可以得到全部的信息，因此下面的代码也是从这个网站开始的。

### 0. 宝贝回家 页面爬虫

由于网站是用aspx写的，我学艺不精，不知道怎么用requests爬取，因此使用了selenium模拟点击的方式进行了爬取，也就是模拟点击`下一页`，然后保存下页面进行分析。

以下为爬取时的示例图

![image-20200924180825131](C:\Users\UncleDong\AppData\Roaming\Typora\typora-user-images\image-20200924180825131.png)

以下为爬取的到的页面

![image-20200924181056729](C:\Users\UncleDong\AppData\Roaming\Typora\typora-user-images\image-20200924181056729.png)



### 1. 解析爬下来的所有页面

仔细观察可以看到页面最左边的一列是ID，这也每个人的唯一标识，并且可以通过这个网页访问到详细信息https://www.baobeihuijia.com/view.aspx?id=446331，只要替换到后面的ID就可以了。因此这里就是用`BeautifulSoup`来对页面进行解析，提取出所有的ID信息。不得不说`Beautiful`真好用...这是我[总结](https://blog.csdn.net/weixin_42763696/article/details/108712503)的使用方法。

解析的最终结果是将ID保存在一个大列表中，然后存储到了pickle文件中，如下图所示。

![image-20200924181521636](C:\Users\UncleDong\AppData\Roaming\Typora\typora-user-images\image-20200924181521636.png)

![image-20200924181659709](C:\Users\UncleDong\AppData\Roaming\Typora\typora-user-images\image-20200924181659709.png)



### 2.  python+命令行获取所有数据

获取ID后就是按照1中提到的url一个个访问了，由于这些url中的信息格式非常工整，因此只要把它们全部存入字典就好了。鉴于要爬上万条数据，使用`requests`模块会非常的慢，因此需要使用到`async`异步操作。作为对比，我使用了100条数据进行`顺序爬取`和`异步爬取`，其消耗时间的对比如下。

![image-20200924184318471](C:\Users\UncleDong\AppData\Roaming\Typora\typora-user-images\image-20200924184318471.png)

<center>顺序爬取</center>



![image-20200924184355515](C:\Users\UncleDong\AppData\Roaming\Typora\typora-user-images\image-20200924184355515.png)

<center>异步爬取</center>

#### get_all_information_async_py

该文件为异步爬取的py文件，需要使用命令行来运行它，参数列表是`起始下标 终止下标 信息类型`，如下图所示，意思就是爬取0~100条数据

![image-20200924185126692](C:\Users\UncleDong\AppData\Roaming\Typora\typora-user-images\image-20200924185126692.png)



为什么要设置这个区间范围呢？直接4w多条一起爬不就完事儿了吗？实际上那么多一起爬的话会造成一个问题，就是`链接无法得到响应`。现在没有找到很好的解释，我的理解是由于异步线程会同时发送很多，并且不会等待之前的回复，因此发送太多的请求也意味着之前的大部分链接都在处于等待响应的状态。这样就会导致爆出`链接无法得到响应`的问题。我的解决方法是在`python+命令行获取所有数据`中写了个命令行脚本，批量爬取url。经测试，1000次的时候较为稳定，几乎总是能够在十秒左右得到回复，因此我就这样每次爬1000条，一共爬4.6w条。最终的速度也可以接受，花了10分钟左右，总比用request爬一晚上快多了。



### 3.   最终整合所有数据到CSV

所有url的信息已经被存入到字典中了，这个时候就用`pandas`库将他们保存起来就好了。要注意的是不能用`,`作为分隔符，因为信息中也会出现逗号，这样会让信息直接打散。最终的结果如下所示

![image-20200924185536667](C:\Users\UncleDong\AppData\Roaming\Typora\typora-user-images\image-20200924185536667.png)