# 使用Pipeline保存结果

# 1 概述

我如果想把抓取的结果保存下来，要怎么做呢？WebMagic用于保存结果的组件叫做`Pipeline`。例如我们通过“控制台输出结果”这件事也是通过一个内置的Pipeline完成的，它叫做`ConsolePipeline`。那么，我现在想要把结果用Json的格式保存下来，怎么做呢？我只需要将Pipeline的实现换成"JsonFilePipeline"就可以了。

```java
public static void main(String[] args) {
    Spider.create(new GithubRepoPageProcessor())
            //从"https://github.com/code4craft"开始抓
            .addUrl("https://github.com/code4craft")
            .addPipeline(new JsonFilePipeline("D:\\webmagic\\"))
            //开启5个线程抓取
            .thread(5)
            //启动爬虫
            .run();
}
```

这样子下载下来的文件就会保存在D盘的webmagic目录中了。

通过定制Pipeline，我们还可以实现保存结果到文件、数据库等一系列功能。

# 2 Pipeline接口

Pipeline的接口定义如下：

```java
public interface Pipeline {
    // ResultItems保存了抽取结果，它是一个Map结构，
    // 在page.putField(key,value)中保存的数据，可以通过ResultItems.get(key)获取
    public void process(ResultItems resultItems, Task task);
}
```

可以看到，`Pipeline`其实就是将`PageProcessor`抽取的结果，继续进行了处理的，其实在Pipeline中完成的功能，你基本上也可以直接在PageProcessor实现，那么为什么会有Pipeline？有几个原因：

1. 为了模块分离。“页面抽取”和“后处理、持久化”是爬虫的两个阶段，将其分离开来，一个是代码结构比较清晰，另一个是以后也可能将其处理过程分开，分开在独立的线程以至于不同的机器执行。
2. Pipeline的功能比较固定，更容易做成通用组件。每个页面的抽取方式千变万化，但是后续处理方式则比较固定，例如保存到文件、保存到数据库这种操作，这些对所有页面都是通用的。WebMagic中就已经提供了控制台输出、保存到文件、保存为JSON格式的文件几种通用的Pipeline。

在WebMagic里，一个`Spider`可以有多个Pipeline，使用`Spider.addPipeline()`即可增加一个Pipeline。这些Pipeline都会得到处理，例如你可以使用`spider.addPipeline(new ConsolePipeline()).addPipeline(new FilePipeline())`实现输出结果到控制台，并且保存到文件的目标。

# 3 将结果输出到控制台

这里还是基于WebMagic的入门案例GithubRepoPageProcessor。其中某一段代码中，我们将结果进行了保存：

```java
public void process(Page page) {
    page.addTargetRequests(page.getHtml().links().regex("(https://github\\.com/\\w+/\\w+)").all());
    page.addTargetRequests(page.getHtml().links().regex("(https://github\\.com/\\w+)").all());
    //保存结果author，这个结果会最终保存到ResultItems中
    page.putField("author", page.getUrl().regex("https://github\\.com/(\\w+)/.*").toString());
    page.putField("name", page.getHtml().xpath("//h1[@class='entry-title public']/strong/a/text()").toString());
    if (page.getResultItems().get("name")==null){
        //设置skip之后，这个页面的结果不会被Pipeline处理
        page.setSkip(true);
    }
    page.putField("readme", page.getHtml().xpath("//div[@id='readme']/tidyText()"));
}
```

现在我们想将结果保存到控制台，要怎么做呢？ConsolePipeline可以完成这个工作：

```java
public class ConsolePipeline implements Pipeline {

    @Override
    public void process(ResultItems resultItems, Task task) {
        System.out.println("get page: " + resultItems.getRequest().getUrl());
        //遍历所有结果，输出到控制台，上面例子中的"author"、"name"、"readme"都是一个key，其结果则是对应的value
        for (Map.Entry<String, Object> entry : resultItems.getAll().entrySet()) {
            System.out.println(entry.getKey() + ":\t" + entry.getValue());
        }
    }
}
```

然后在Spider中加入ConsolePipeline：

```java
public static void main(String[] args) {
    Spider.create(new GithubRepoPageProcessor())
        // 从"https://github.com/code4craft"开始抓
        .addUrl("https://github.com/code4craft")
        // 解决Https下无法抓取只支持TLS1.2的站点，修改默认的HttpClientDownloader
        .setDownloader(new HttpClientDownloader())
        .addPipeline(new ConsolePipeline())
        // 开启5个线程抓取
        .thread(5)
        // 启动爬虫
        .run();
}
```

# 4 WebMagic提供的Pipeline

WebMagic中已经提供了将结果输出到控制台、保存到文件和JSON格式保存的几个Pipeline：

| 类                        | 说明                             | 备注                             |
| ------------------------- | -------------------------------- | -------------------------------- |
| ConsolePipeline           | 输出结果到控制台                 | 抽取结果需要实现toString方法     |
| FilePipeline              | 保存结果到文件                   | 抽取结果需要实现toString方法     |
| JsonFilePipeline          | JSON格式保存结果到文件           |                                  |
| ConsolePageModelPipeline  | (注解模式)输出结果到控制台       |                                  |
| FilePageModelPipeline     | (注解模式)保存结果到文件         |                                  |
| JsonFilePageModelPipeline | (注解模式)JSON格式保存结果到文件 | 想要持久化的字段需要有getter方法 |

# 5 定制Pipeline

如果WebMagic提供的Pipeline不能满足我们的需要，我们可以定制自己的Pipeline：

## 5.1 创建类MyPipeline实现接口Pipeline

```java
package com.zh.webmagicmaven.simplespider.pipeline;

import us.codecraft.webmagic.ResultItems;
import us.codecraft.webmagic.Task;
import us.codecraft.webmagic.pipeline.Pipeline;

public class MyPipeline implements Pipeline{

	@Override
	public void process(ResultItems resultItems, Task task) {
		String title = resultItems.get("title");
		Object object = resultItems.get("obj");
		System.out.println("定制的title：" + title + "，和obj：" + object);
	}
}
```

在Spider中添加定制的Pipeline：

```java
public static void main(String[] args) {
    Spider.create(new GithubRepoPageProcessor())
        // 从"https://github.com/code4craft"开始抓
        .addUrl("https://github.com/code4craft")
        // 解决Https下无法抓取只支持TLS1.2的站点，修改默认的HttpClientDownloader
        .setDownloader(new HttpClientDownloader())
        .addPipeline(new ConsolePipeline())
        // 添加定制的Pipeline：MyPipeline
        .addPipeline(new MyPipeline())
        // 开启5个线程抓取
        .thread(5)
        // 启动爬虫
        .run();
}
```

