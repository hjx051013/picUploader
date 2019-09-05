
# 批量迁移markdown文档到云存储中

之前一直为撰写md文档的图片问题感到苦恼，要么存在本地但是文档想要整体迁移到网上就很麻烦，要么就得往文档中插入插入图片就得传到云端费时费力。于是感觉到写一个python脚本一劳永逸地解决这个问题的必要性。

1. 需求

   - 通过类似于`python srcipt md_file/directory `的命令整体将指定md文档或者指定文件夹下的所有md文档中的图片整体从其他网址或本地相对/绝对路径迁移到指定的云存储中
   - 通过默认或者指定配置文件来支持多种类型的云存储
   - 支持图片压缩
   - 目前支持七牛云和又拍云云存储

2. 整体的代码流程

   ![切换md图片流程图.png](批量迁移markdown文件图片到云存储中.assets/36031ec2c22a531e1496be21ee69974a.png)

3. 预备环境

   - python3

   - 依赖库, `pip install -r requirements.txt`安装所有依赖库

     ```markdown
     qiniu
     certifi==2019.6.16
     chardet==3.0.4
     decorator==4.4.0
     idna==2.8
     requests==2.22.0
     six==1.12.0
     tinify==1.5.1
     upyun==2.5.2
     urllib3==1.25.3
     validators==0.14.0
     ```

   - 如果实在类unix系统中，可在家目录下新建`.md.mdPicTransfer.cfg`文件，用于配置云存储。格式如下：

     - 三个配置大项。`common`,`upai`,`qiniu`分别对应基础配置，又拍云配置，七牛云配置
     - upai下面是又拍云上传文件所需要的基本配置
     - qiniu下面是七牛云上传文件所需要的基本配置

     ```markdown
     [common]
     option=upai/qiniu
     tinypngkey=xxx
     [upai]
     servicename=xxx
     operatorname=xxx
     password=xxx
     domain=xxx
     [qiniu]
     accesskey=xxx
     secretkey=xxx
     bucketname=xxx
     domain=xxx
     ```

     

   - 获得代码

     1. 将下面源码所列的四个文件放在一个文件夹中，按照提示运行程序迁移指定md文档或指定文件夹的所有md文档中的图片到云存储中。
     2. 从[此仓库]()克隆代码下来到本地，`pip install -r requirements.txt`安装所有依赖库，按照提示运行程序。

   
   - 运行程序
   ```shell
    # file为指定md文档路径，相对绝对均可；configfile为配置文件路径，如果没有则为默认家目录下.mdPicTransfer.cfg
    # zip表示使用tinyPNG压缩图片，此时需要配置tinypngkey；cache表示缓存文图片到sqlite3数据库中，需要安装sqlite3;
    # back表示在转换前备份原md文档；help打印帮助信息
    python %s file [-c|--config configfile] [-z|--zip] [--cache] [-b|--back]
    python %s -R|--Recursive directory [-c|--config configfile] [-z|--zip] [-b|--back]
    python %s -h|--help
   ```
5. 演示效果

   运行该程序，将得到文件与备份文件用`git diff origin cur`,比较有如下结果：

   ```text
   diff --git "a/Java\345\271\266\345\217\221.md" "b/Java\345\271\266\345\217\221.md.bak"
   index 2ba4604..5db5bf0 100644
   --- "a/Java\345\271\266\345\217\221.md"
   +++ "b/Java\345\271\266\345\217\221.md.bak"
   @@ -2,7 +2,7 @@
    
    ### 一、线程状态转换
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image1.png" width="600px"> </div><br>
   +<div align="center"> <img src="pics/adfb427d-3b21-40d7-a142-757f4ed73079.png" width="600px"> </div><br>
    
    #### 新建（New）
    
   @@ -675,7 +675,7 @@ java.util.concurrent（J.U.C）大大提高了并发性能，AQS 被认为是 J.
    
    维护了一个计数器 cnt，每次调用 countDown() 方法会让计数器的值减 1，减到 0 的时候，那些因为调用 await() 方法而在等待的线程就会被唤醒。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image2.png" width="300px"> </div><br>
   +<div align="center"> <img src="pics/ba078291-791e-4378-b6d1-ece76c2f0b14.png" width="300px"> </div><br>
    ...
   ```
    


   