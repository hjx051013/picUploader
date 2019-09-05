
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

   ```html
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
    
    ```java
    public class CountdownLatchExample {
   @@ -724,7 +724,7 @@ public CyclicBarrier(int parties) {
    }
    ```
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image3.png" width="300px"> </div><br>
   +<div align="center"> <img src="pics/f71af66b-0d54-4399-a44b-f47b58321984.png" width="300px"> </div><br>
    
    ```java
    public class CyclicBarrierExample {
   @@ -961,7 +961,7 @@ public class ForkJoinPool extends AbstractExecutorService
    
    ForkJoinPool 实现了工作窃取算法来提高 CPU 的利用率。每个线程都维护了一个双端队列，用来存储需要执行的任务。工作窃取算法允许空闲的线程从其它线程的双端队列中窃取一个任务来执行。窃取的任务必须是最晚的任务，避免和队列所属线程发生竞争。例如下图中，Thread2 从 Thread1 的队列中拿出最晚的 Task1 任务，Thread1 会拿出 Task2 来执行，这样就避免发生竞争。但是如果队列中只有一个任务时还是会发生竞争。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image4.png" width="300px"> </div><br>
   +<div align="center"> <img src="pics/e42f188f-f4a9-4e6f-88fc-45f4682072fb.png" width="300px"> </div><br>
    
    ### 九、线程不安全示例
    
   @@ -1016,19 +1016,19 @@ Java 内存模型试图屏蔽各种硬件和操作系统的内存访问差异，
    
    加入高速缓存带来了一个新的问题：缓存一致性。如果多个缓存共享同一块主内存区域，那么多个缓存的数据可能会不一致，需要一些协议来解决这个问题。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image5.png" width="600px"> </div><br>
   +<div align="center"> <img src="pics/942ca0d2-9d5c-45a4-89cb-5fd89b61913f.png" width="600px"> </div><br>
    
    所有的变量都存储在主内存中，每个线程还有自己的工作内存，工作内存存储在高速缓存或者寄存器中，保存了该线程使用的变量的主内存副本拷贝。
    
    线程只能直接操作工作内存中的变量，不同线程之间的变量值传递需要通过主内存来完成。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image6.png" width="600px"> </div><br>
   +<div align="center"> <img src="pics/15851555-5abc-497d-ad34-efed10f43a6b.png" width="600px"> </div><br>
    
    #### 内存间交互操作
    
    Java 内存模型定义了 8 个操作来完成主内存和工作内存的交互操作。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image7.png" width="450px"> </div><br>
   +<div align="center"> <img src="pics/8b7ebbad-9604-4375-84e3-f412099d170c.png" width="450px"> </div><br>
    
    - read：把一个变量的值从主内存传输到工作内存中
    - load：在 read 之后执行，把 read 得到的值放入工作内存的变量副本中
   @@ -1051,11 +1051,11 @@ Java 内存模型保证了 read、load、use、assign、store、write、lock 和
    
    下图演示了两个线程同时对 cnt 进行操作，load、assign、store 这一系列操作整体上看不具备原子性，那么在 T1 修改 cnt 并且还没有将修改后的值写入主内存，T2 依然可以读入旧值。可以看出，这两个线程虽然执行了两次自增运算，但是主内存中 cnt 的值最后为 1 而不是 2。因此对 int 类型读写操作满足原子性只是说明 load、assign、store 这些单个操作具备原子性。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image8.jpg" width="300px"> </div><br>
   +<div align="center"> <img src="pics/2797a609-68db-4d7b-8701-41ac9a34b14f.jpg" width="300px"> </div><br>
    
    AtomicInteger 能保证多个线程修改的原子性。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image9.jpg" width="300px"> </div><br>
   +<div align="center"> <img src="pics/dd563037-fcaa-4bd8-83b6-b39d93a12c77.jpg" width="300px"> </div><br>
    
    使用 AtomicInteger 重写之前线程不安全的代码之后得到以下线程安全实现：
    
   @@ -1163,7 +1163,7 @@ volatile 关键字通过添加内存屏障的方式来禁止指令重排，即
    
    在一个线程内，在程序前面的操作先行发生于后面的操作。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image10.png" width="180px"> </div><br>
   +<div align="center"> <img src="pics/874b3ff7-7c5c-4e7a-b8ab-a82a3e038d20.png" width="180px"> </div><br>
    
    ##### 2. 管程锁定规则
    
   @@ -1171,7 +1171,7 @@ volatile 关键字通过添加内存屏障的方式来禁止指令重排，即
    
    一个 unlock 操作先行发生于后面对同一个锁的 lock 操作。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image11.png" width="350px"> </div><br>
   +<div align="center"> <img src="pics/8996a537-7c4a-4ec8-a3b7-7ef1798eae26.png" width="350px"> </div><br>
    
    ##### 3. volatile 变量规则
    
   @@ -1179,7 +1179,7 @@ volatile 关键字通过添加内存屏障的方式来禁止指令重排，即
    
    对一个 volatile 变量的写操作先行发生于后面对这个变量的读操作。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image12.png" width="400px"> </div><br>
   +<div align="center"> <img src="pics/942f33c9-8ad9-4987-836f-007de4c21de0.png" width="400px"> </div><br>
    
    ##### 4. 线程启动规则
    
   @@ -1187,7 +1187,7 @@ volatile 关键字通过添加内存屏障的方式来禁止指令重排，即
    
    Thread 对象的 start() 方法调用先行发生于此线程的每一个动作。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image13.png" width="380px"> </div><br>
   +<div align="center"> <img src="pics/6270c216-7ec0-4db7-94de-0003bce37cd2.png" width="380px"> </div><br>
    
    ##### 5. 线程加入规则
    
   @@ -1195,7 +1195,7 @@ Thread 对象的 start() 方法调用先行发生于此线程的每一个动作
    
    Thread 对象的结束先行发生于 join() 方法返回。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image14.png" width="400px"> </div><br>
   +<div align="center"> <img src="pics/233f8d89-31d7-413f-9c02-042f19c46ba1.png" width="400px"> </div><br>
    
    ##### 6. 线程中断规则
    
   @@ -1413,7 +1413,7 @@ public class ThreadLocalExample1 {
    
    它所对应的底层结构图为：
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image15.png" width="500px"> </div><br>
   +<div align="center"> <img src="pics/6782674c-1bfe-4879-af39-e9d722a95d39.png" width="500px"> </div><br>
    
    每个 Thread 都有一个 ThreadLocal.ThreadLocalMap 对象。
    
   @@ -1516,17 +1516,17 @@ JDK 1.6 引入了偏向锁和轻量级锁，从而让锁拥有了四个状态：
    
    以下是 HotSpot 虚拟机对象头的内存布局，这些数据被称为 Mark Word。其中 tag bits 对应了五个状态，这些状态在右侧的 state 表格中给出。除了 marked for gc 状态，其它四个状态已经在前面介绍过了。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image16.png" width="500"/> </div><br>
   +<div align="center"> <img src="pics/bb6a49be-00f2-4f27-a0ce-4ed764bc605c.png" width="500"/> </div><br>
    
    下图左侧是一个线程的虚拟机栈，其中有一部分称为 Lock Record 的区域，这是在轻量级锁运行过程创建的，用于存放锁对象的 Mark Word。而右侧就是一个锁对象，包含了 Mark Word 和其它信息。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image17.png" width="500"/> </div><br>
   +<div align="center"> <img src="pics/051e436c-0e46-4c59-8f67-52d89d656182.png" width="500"/> </div><br>
    
    轻量级锁是相对于传统的重量级锁而言，它使用 CAS 操作来避免重量级锁使用互斥量的开销。对于绝大部分的锁，在整个同步周期内都是不存在竞争的，因此也就不需要都使用互斥量进行同步，可以先采用 CAS 操作进行同步，如果 CAS 失败了再改用互斥量进行同步。
    
    当尝试获取一个锁对象时，如果锁对象标记为 0 01，说明锁对象的锁未锁定（unlocked）状态。此时虚拟机在当前线程的虚拟机栈中创建 Lock Record，然后使用 CAS 操作将对象的 Mark Word 更新为 Lock Record 指针。如果 CAS 操作成功了，那么线程就获取了该对象上的锁，并且对象的 Mark Word 的锁标记变为 00，表示该对象处于轻量级锁状态。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image18.png" width="400"/> </div><br>
   +<div align="center"> <img src="pics/baaa681f-7c52-4198-a5ae-303b9386cf47.png" width="400"/> </div><br>
    
    如果 CAS 操作失败了，虚拟机首先会检查对象的 Mark Word 是否指向当前线程的虚拟机栈，如果是的话说明当前线程已经拥有了这个锁对象，那就可以直接进入同步块继续执行，否则说明这个锁对象已经被其他线程线程抢占了。如果有两条以上的线程争用同一个锁，那轻量级锁就不再有效，要膨胀为重量级锁。
    
   @@ -1538,7 +1538,7 @@ JDK 1.6 引入了偏向锁和轻量级锁，从而让锁拥有了四个状态：
    
    当有另外一个线程去尝试获取这个锁对象时，偏向状态就宣告结束，此时撤销偏向（Revoke Bias）后恢复到未锁定状态或者轻量级锁状态。
    
   -<div align="center"> <img src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image19.jpg" width="600"/> </div><br>
   +<div align="center"> <img src="pics/390c913b-5f31-444f-bbdb-2b88b688e7ce.jpg" width="600"/> </div><br>
    
    ### 十三、多线程开发良好的实践
    
   @@ -1578,4 +1578,4 @@ JDK 1.6 引入了偏向锁和轻量级锁，从而让锁拥有了四个状态：
    
    更多精彩内容将发布在微信公众号 CyC2018 上，你也可以在公众号后台和我交流学习和求职相关的问题。另外，公众号提供了该项目的 PDF 等离线阅读版本，后台回复 "下载" 即可领取。公众号也提供了一份技术面试复习大纲，不仅系统整理了面试知识点，而且标注了各个知识点的重要程度，从而帮你理清多而杂的面试知识点，后台回复 "大纲" 即可领取。我基本是按照这个大纲来进行复习的，对我拿到了 BAT 头条等 Offer 起到很大的帮助。你们完全可以和我一样根据大纲上列的知识点来进行复习，就不用看很多不重要的内容，也可以知道哪些内容很重要从而多安排一些复习时间。
    
   -<div align="center"><img width="480px" src="http://hjx-markdown-images.test.upcdn.net/20190906_--cache/image9.png"></img></div>
   \ No newline at end of file
   +<div align="center"><img width="480px" src="pics/公众号海报4.png"></img></div>
   \ No newline at end of file
   ```
    


   