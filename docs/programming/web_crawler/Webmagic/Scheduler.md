# 使用和定制Scheduler

# 1 概述

Scheduler是WebMagic中进行URL管理的组件。

一般来说，Scheduler包括两个作用：

1. 对待抓取的URL队列进行管理。
2. 对已抓取的URL进行去重。

在0.5.1版本里，WebMagic对Scheduler的内部实现进行了重构，去重部分被单独抽象成了一个接口：`DuplicateRemover`，从而可以为同一个Scheduler选择不同的去重方式，以适应不同的需要。

# 2 WebMagic内置的Scheduler

## 2.1 简述

| 类                        | 说明                                                         | 备注                                                         |
| ------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| DuplicateRemovedScheduler | 抽象基类，提供一些模板方法                                   | 继承它可以实现自己的功能                                     |
| QueueScheduler            | 使用内存队列保存待抓取URL                                    |                                                              |
| PriorityScheduler         | 使用带有优先级的内存队列保存待抓取URL                        | 耗费内存较QueueScheduler更大，但是当设置了request.priority之后，只能使用PriorityScheduler才可使优先级生效 |
| FileCacheQueueScheduler   | 使用文件保存抓取URL，可以在关闭程序并下次启动时，从之前抓取到的URL继续抓取 | 需指定路径，会建立.urls.txt和.cursor.txt两个文件             |
| RedisScheduler            | 使用Redis保存抓取队列，可进行多台机器同时合作抓取            | 需要安装并启动redis                                          |

## 2.2 简单使用

**内存队列QueueScheduler**：

```java
spider.setScheduler(new QueueScheduler())；
```

**文件队列FileCacheQueueScheduler**：

使用文件保存抓取URL，可以在关闭程序并下次启动时，从之前抓取到的URL继续抓取。

```java
spider.setScheduler(new FileCacheQueueScheduler("E:\\scheduler"))//设置文件队列
```

运行后文件夹`E:\scheduler`会产生两个文件`xxx.urls.txt`和`xxx.cursor.txt`，这里的xxx是爬取网站的域名。

**Redis队列RedisScheduler**：

使用Redis保存抓取队列，可进行多台机器同时合作抓取，运行之前需要先运行redis服务端。

```java
spider.setScheduler(new RedisScheduler("127.0.0.1"))//设置Redis队列
```

# 3 自定义Scheduler

## 3.1 定制文件队列：实现本地存储Request中的extras字典信息

在使用文件队列FileCacheQueueScheduler的时候发现一个问题：重启爬虫的时候，需要从本地文件中重新读取URL连接并封装成Request实例，但是新封装的Request实例是不包含里边的extras信息。

为了解决了这个问题，便修改了一下`us.codecraft.webmagic.scheduler.FileCacheQueueScheduler`使其在`.urls.txt`文件中存储url的时候另外存储request实例中的extras信息，两者使用`|`分割，在重启爬虫后重新粉状request实例的时候，把extras的信息也重新封装进去。

`.urls.txt`文件内容示例：

```
http://news.people.com.cn/210801/211150/index.js?_=1592708021443|null
http://sports.people.com.cn/n1/2020/0621/c22147-31754259.html|{"date":"2020-06-21 10:46:17","imgCount":"0","id":"31754259","title":"意甲综合：都灵平帕尔马&nbsp;维罗纳胜卡利亚里","nodeId":"14820","url":"http://sports.people.com.cn/n1/2020/0621/c22147-31754259.html"}
http://sports.people.com.cn/n1/2020/0621/c22148-31754258.html|{"date":"2020-06-21 10:45:46","imgCount":"0","id":"31754258","title":"英超综合：阿森纳连败又损兵&nbsp;莱斯特绝杀不成遭逼平","nodeId":"22176","url":"http://sports.people.com.cn/n1/2020/0621/c22148-31754258.html"}
http://sports.people.com.cn/n1/2020/0621/c22142-31754257.html|{"date":"2020-06-21 10:45:16","imgCount":"0","id":"31754257","title":"德甲综合：莱万一传两射破纪录&nbsp;多特获胜夺亚军","nodeId":"22176","url":"http://sports.people.com.cn/n1/2020/0621/c22142-31754257.html"}
```

实现代码：

```java
package com.lifeng.quantitativetrading.crawler.scheduler;

import java.io.BufferedReader;
import java.io.Closeable;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.Executors;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.commons.io.IOUtils;
import org.apache.commons.lang3.math.NumberUtils;
import org.springframework.util.StringUtils;

import us.codecraft.webmagic.Request;
import us.codecraft.webmagic.Task;
import us.codecraft.webmagic.scheduler.DuplicateRemovedScheduler;
import us.codecraft.webmagic.scheduler.MonitorableScheduler;
import us.codecraft.webmagic.scheduler.component.DuplicateRemover;
import us.codecraft.webmagic.selector.Json;

/**
 * 基于us.codecraft.webmagic.scheduler.FileCacheQueueScheduler修改，使本地文件中存储Request.getExras()的信息
 * @author zh
 *
 */
public class FileCacheQueueSchedulerWithExtras extends DuplicateRemovedScheduler
		implements MonitorableScheduler, Closeable {

	private String filePath = System.getProperty("java.io.tmpdir");

	private String fileUrlAllName = ".urls.txt";

	private Task task;

	private String fileCursor = ".cursor.txt";

	private PrintWriter fileUrlWriter;

	private PrintWriter fileCursorWriter;

	private AtomicInteger cursor = new AtomicInteger();

	private AtomicBoolean inited = new AtomicBoolean(false);

	private BlockingQueue<Request> queue;

	private Set<String> urls;

	private ScheduledExecutorService flushThreadPool;

	public FileCacheQueueSchedulerWithExtras(String filePath) {
		if (!filePath.endsWith("/") && !filePath.endsWith("\\")) {
			filePath += "/";
		}
		this.filePath = filePath;
		initDuplicateRemover();
	}

	private void flush() {
		fileUrlWriter.flush();
		fileCursorWriter.flush();
	}

	private void init(Task task) {
		this.task = task;
		File file = new File(filePath);
		if (!file.exists()) {
			file.mkdirs();
		}
		readFile();
		initWriter();
		initFlushThread();
		inited.set(true);
		logger.info("init cache scheduler success");
	}

	private void initDuplicateRemover() {
		setDuplicateRemover(new DuplicateRemover() {
			@Override
			public boolean isDuplicate(Request request, Task task) {
				if (!inited.get()) {
					init(task);
				}
				return !urls.add(request.getUrl());
			}

			@Override
			public void resetDuplicateCheck(Task task) {
				urls.clear();
			}

			@Override
			public int getTotalRequestsCount(Task task) {
				return urls.size();
			}
		});
	}

	private void initFlushThread() {
		flushThreadPool = Executors.newScheduledThreadPool(1);
		flushThreadPool.scheduleAtFixedRate(new Runnable() {
			@Override
			public void run() {
				flush();
			}
		}, 10, 10, TimeUnit.SECONDS);
	}

	private void initWriter() {
		try {
			fileUrlWriter = new PrintWriter(new FileWriter(getFileName(fileUrlAllName), true));
			fileCursorWriter = new PrintWriter(new FileWriter(getFileName(fileCursor), false));
		} catch (IOException e) {
			throw new RuntimeException("init cache scheduler error", e);
		}
	}

	private void readFile() {
		try {
			queue = new LinkedBlockingQueue<Request>();
			urls = new LinkedHashSet<String>();
			readCursorFile();
			readUrlFile();
			// initDuplicateRemover();
		} catch (FileNotFoundException e) {
			// init
			logger.info("init cache file " + getFileName(fileUrlAllName));
		} catch (IOException e) {
			logger.error("init file error", e);
		}
	}

	private void readUrlFile() throws IOException {
		String line;
		BufferedReader fileUrlReader = null;
		try {
			fileUrlReader = new BufferedReader(new FileReader(getFileName(fileUrlAllName)));
			int lineReaded = 0;
			while ((line = fileUrlReader.readLine()) != null) {
				String[] strings = StringUtils.split(line, "|");
				urls.add(strings[0].trim());
				lineReaded++;
				if (lineReaded > cursor.get()) {
					Request request = new Request(strings[0]);
					if (null != strings && strings[1] != "null") {
						Json json = new Json(strings[1]);
						request.setExtras(json.toObject(Map.class));
					}
					queue.add(request);
				}
			}
		} finally {
			if (fileUrlReader != null) {
				IOUtils.closeQuietly(fileUrlReader);
			}
		}
	}

	private void readCursorFile() throws IOException {
		BufferedReader fileCursorReader = null;
		try {
			fileCursorReader = new BufferedReader(new FileReader(getFileName(fileCursor)));
			String line;
			// read the last number
			while ((line = fileCursorReader.readLine()) != null) {
				cursor = new AtomicInteger(NumberUtils.toInt(line));
			}
		} finally {
			if (fileCursorReader != null) {
				IOUtils.closeQuietly(fileCursorReader);
			}
		}
	}

	public void close() throws IOException {
		flushThreadPool.shutdown();
		fileUrlWriter.close();
		fileCursorWriter.close();
	}

	private String getFileName(String filename) {
		return filePath + task.getUUID() + filename;
	}

	@Override
	protected void pushWhenNoDuplicate(Request request, Task task) {
		if (!inited.get()) {
			init(task);
		}
		queue.add(request);
		fileUrlWriter.println(request.getUrl() + "|" + request.getExtras());
	}

	@Override
	public synchronized Request poll(Task task) {
		if (!inited.get()) {
			init(task);
		}
		fileCursorWriter.println(cursor.incrementAndGet());
		return queue.poll();
	}

	@Override
	public int getLeftRequestsCount(Task task) {
		return queue.size();
	}

	@Override
	public int getTotalRequestsCount(Task task) {
		return getDuplicateRemover().getTotalRequestsCount(task);
	}
}
```

