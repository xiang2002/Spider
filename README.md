# Spider:
    Python-Spider:使用scrapy框架，requests,Beautifulsoup等实现


# GAN_data 目录：

* GAN_data  
    - items.py  
    ```类似于python字典,实际上就是继承了python的字典类，用于承载从网页响应的文件中抓取出来的数据，传输给PipeLine，交由PipeLine进行处理```
    + middlewares.py  
    ```scrapy的工作流程中有两个中间件,分别是spider中间件,一个是Downloader中间件。在请求与响应之间进行处理```