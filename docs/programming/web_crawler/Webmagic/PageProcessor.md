# 实现PageProcessor

# 1 PageProcessor代码示例

```java
package com.zh.webmagicmaven.simplespider;

import com.zh.webmagicmaven.simplespider.downloader.HttpClientDownloader;

import us.codecraft.webmagic.Page;
import us.codecraft.webmagic.Site;
import us.codecraft.webmagic.Spider;
import us.codecraft.webmagic.processor.PageProcessor;

/**
 * 抓取Github信息
 * 
 * @author zh
 *
 */
public class GithubRepoPageProcessor implements PageProcessor {

	// 部分一：抓取网站的相关配置，包括编码、抓取间隔、重试次数等
	private Site site = Site.me().setRetryTimes(3).setSleepTime(1000);

	@Override
	// process是定制爬虫逻辑的核心接口，在这里编写抽取逻辑
	public void process(Page page) {
		// 部分二：定义如何抽取页面信息，并保存下来
		page.putField("author", page.getUrl().regex("https://github\\.com/(\\w+)/.*").toString());
		page.putField("name", page.getHtml().xpath("//h1[@class='entry-title public']/strong/a/text()").toString());
		if (page.getResultItems().get("name") == null) {
			// skip this page
			page.setSkip(true);
		}
		page.putField("readme", page.getHtml().xpath("//div[@id='readme']/tidyText()"));

		// 部分三：从页面发现后续的url地址来抓取
		page.addTargetRequests(page.getHtml().links().regex("(https://github\\.com/[\\w\\-]+/[\\w\\-]+)").all());
	}

	@Override
	public Site getSite() {
		return site;
	}

	public static void main(String[] args) {
		// Spider是爬虫启动的入口。在启动爬虫之前，我们需要使用一个PageProcessor创建一个Spider对象
		Spider.create(new GithubRepoPageProcessor())
				// 从"https://github.com/code4craft"开始抓
				.addUrl("https://github.com/code4craft")
				// 解决Https下无法抓取只支持TLS1.2的站点，修改默认的HttpClientDownloader
				.setDownloader(new HttpClientDownloader())
				// 开启5个线程抓取
				.thread(5)
				// 启动爬虫
				.run();
	}
}
```

# 2 爬虫的入口Spider

Spider是爬虫启动的入口。在启动爬虫之前，我们需要使用一个PageProcessor创建一个Spider对象。

## 2.1 Spider的配置

| 方法                                                       | 说明                                             | 示例                                                         |
| ---------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| `public static Spider create(PageProcessor pageProcessor)` | 创建Spider                                       | `Spider.create(new GithubRepoPageProcessor())`               |
| `public Spider addUrl(String... urls)`                     | 添加URL                                          | `spider.addUrl("http://webmagic.io/docs/")`                  |
| `public Spider thread(int threadNum)`                      | 开启n个线程                                      | `spider.thread(5)`                                           |
| `public void run()`                                        | 启动，会阻塞当前线程执行                         | `spider.run()`                                               |
| `public void start()`<br/>`public void runAsync()`         | 异步启动，当前线程继续执行                       | `spider.start()`                                             |
| `public void stop()`                                       | 停止爬虫                                         | `spider.stop()`                                              |
| `public Spider addPipeline(Pipeline pipeline)`             | 添加一个Pipeline，一个Spider可以有多个Pipeline   | `spider .addPipeline(new ConsolePipeline())`                 |
| `public Spider setScheduler(Scheduler scheduler)`          | 设置Scheduler，一个Spider只能有个一个Scheduler   | `spider.setScheduler(new RedisScheduler())`                  |
| `public Spider setDownloader(Downloader downloader)`       | 设置Downloader，一个Spider只能有个一个Downloader | `spider.setDownloader( new SeleniumDownloader())`            |
| `public <T> T get(String url)`                             | 同步调用，并直接取得结果                         | `ResultItems result = spider.get("http://webmagic.io/docs/")` |
| `public <T> List<T> getAll(Collection<String> urls)`       | 同步调用，并直接取得一堆结果                     | `List results = spider.getAll("http://webmagic.io/docs/", "http://webmagic.io/xxx")` |

## 2.2 怎么在Spring Boot中使用WebMagic

### 2.2.1 定时任务方式

可以根据Spring Boot的定时任务规则书写任务，在任务中启动Spider。

### 2.2.2 调用方式

可以书写一个接口，如RestFul接口，在接口中启动Spider。

# 3 爬虫的设置Site

Site用于定义站点本身的一些配置信息，例如编码、HTTP头、超时时间、重试策略等、代理等，都可以通过设置Site对象来进行配置。

| 方法                                           | 说明                                      | 示例                                             |
| ---------------------------------------------- | ----------------------------------------- | ------------------------------------------------ |
| `Site setCharset(String charset)`              | 设置编码                                  | `site.setCharset("utf-8")`                       |
| `Site setUserAgent(String userAgent)`          | 设置UserAgent                             | `site.setUserAgent("Spider")`                    |
| `Site setTimeOut(int timeOut)`                 | 设置超时时间， 单位是毫秒                 | `site.setTimeOut(3000)`                          |
| `Site setRetryTimes(int retryTimes)`           | 设置重试次数                              | `site.setRetryTimes(3)`                          |
| `Site setCycleRetryTimes(int cycleRetryTimes)` | 设置循环重试次数                          | `site.setCycleRetryTimes(3)`                     |
| `Site addCookie(String name, String value)`    | 添加一条Cookie                            | `site.addCookie("dotcomt_user","code4craft")`    |
| `Site setDomain(String domain)`                | 设置域名，需设置域名后，addCookie才可生效 | `site.setDomain("github.com")`                   |
| `Site addHeader(String key, String value)`     | 添加一条Header                            | `site.addHeader("Referer","https://github.com")` |

# 4 页面对象Page

Page代表了从Downloader下载到的一个页面——可能是HTML，也可能是JSON或者其他文本格式的内容。Page是WebMagic抽取过程的核心对象，它提供一些方法可供抽取、结果保存等。

## 4.1 页面的抽取

对于下载到的Html页面，你如何从中抽取到你想要的信息？WebMagic里主要使用了三种抽取技术：XPath、正则表达式和CSS选择器。另外，对于JSON格式的内容，可使用JsonPath进行解析。

### 4.1.1 XPath

XPath本来是用于XML中获取元素的一种查询语言，但是用于Html也是比较方便的。例如：

```java
page.getHtml().xpath("//h1[@class='entry-title public']/strong/a/text()")
```

这段代码使用了XPath，它的意思是“查找所有class属性为'entry-title public'的h1元素，并找到他的strong子节点的a子节点，并提取a节点的文本信息”。

### 4.1.2 CSS选择器

CSS选择器是与XPath类似的语言。如果大家做过前端开发，肯定知道`$('h1.entry-title')`这种写法的含义。客观的说，它比XPath写起来要简单一些，但是如果写复杂一点的抽取规则，就相对要麻烦一点。

### 4.1.3 正则表达式

正则表达式则是一种通用的文本抽取语言。

```java
page.addTargetRequests(page.getHtml().links().regex("(https://github\\.com/\\w+/\\w+)").all());
```

这段代码就用到了正则表达式，它表示匹配所有"https://github.com/code4craft/webmagic"这样的链接。

### 4.1.4 JsonPath

JsonPath是于XPath很类似的一个语言，它用于从Json中快速定位一条内容。WebMagic中使用的JsonPath格式可以参考这里：https://code.google.com/p/json-path/

## 4.2 链接的发现

一个站点的页面是很多的，一开始我们不可能全部列举出来，于是如何发现后续的链接，是一个爬虫不可缺少的一部分。

```java
page.addTargetRequests(page.getHtml().links().regex("(https://github\\.com/\\w+/\\w+)").all());
```

这段代码的分为两部分：

- `page.getHtml().links().regex("(https://github\\.com/\\w+/\\w+)").all()`用于获取所有满足`https://github\.com/\w+/\w+`这个正则表达式的链接；
- `page.addTargetRequests()`则将这些链接加入到待抓取的队列中去。
    - `void addTargetRequests(List<String> requests)`：传入一个URL列表。
    - `void addTargetRequests(List<String> requests, long priority)`：传入一个URL列表，对每个URL创建一个Request实例，并设置此Request实例为指定的优先级priority。
        - priority：值越大处理的越早。
    - `void addTargetRequest(String requestString)`：传入一个URL连接。
    - `void addTargetRequest(Request request)`：传入一个request对象。

### 4.2.1 Request

```java
package us.codecraft.webmagic;

import us.codecraft.webmagic.model.HttpRequestBody;
import us.codecraft.webmagic.utils.Experimental;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

/**
 * Object contains url to crawl.<br>
 * It contains some additional information.<br>
 *
 * @author code4crafter@gmail.com <br>
 * @since 0.1.0
 */
public class Request implements Serializable {

    private static final long serialVersionUID = 2062192774891352043L;

    public static final String CYCLE_TRIED_TIMES = "_cycle_tried_times";

    private String url;

    private String method;//请求方法，POST GET等，使用us.codecraft.webmagic.utils.HttpConstant中的静态内部类Method中的静态属性来做参数即可

    private HttpRequestBody requestBody;//请求体

    /**
     * Store additional information in extras.
     */
    private Map<String, Object> extras;//存放额外的信息

    /**
     * cookies for current url, if not set use Site's cookies
     */
    private Map<String, String> cookies = new HashMap<String, String>();

    private Map<String, String> headers = new HashMap<String, String>();

    /**
     * Priority of the request.<br>
     * The bigger will be processed earlier. <br>
     * @see us.codecraft.webmagic.scheduler.PriorityScheduler
     */
    private long priority;//优先级，优先级数字越大，越早被处理

    /**
     * When it is set to TRUE, the downloader will not try to parse response body to text.
     *
     */
    private boolean binaryContent = false;

    private String charset;//编码

    public Request() {
    }

    public Request(String url) {
        this.url = url;
    }

    public long getPriority() {
        return priority;
    }

    /**
     * Set the priority of request for sorting.<br>
     * Need a scheduler supporting priority.<br>
     * @see us.codecraft.webmagic.scheduler.PriorityScheduler
     *
     * @param priority priority
     * @return this
     */
    @Experimental
    public Request setPriority(long priority) {
        this.priority = priority;
        return this;
    }

    public Object getExtra(String key) {
        if (extras == null) {
            return null;
        }
        return extras.get(key);
    }

    public Request putExtra(String key, Object value) {
        if (extras == null) {
            extras = new HashMap<String, Object>();
        }
        extras.put(key, value);
        return this;
    }

    public String getUrl() {
        return url;
    }

    public Map<String, Object> getExtras() {
        return extras;
    }

    public Request setExtras(Map<String, Object> extras) {
        this.extras = extras;
        return this;
    }

    public Request setUrl(String url) {
        this.url = url;
        return this;
    }

    /**
     * The http method of the request. Get for default.
     * @return httpMethod
     * @see us.codecraft.webmagic.utils.HttpConstant.Method
     * @since 0.5.0
     */
    public String getMethod() {
        return method;
    }

    public Request setMethod(String method) {
        this.method = method;
        return this;
    }

    @Override
    public int hashCode() {
        int result = url != null ? url.hashCode() : 0;
        result = 31 * result + (method != null ? method.hashCode() : 0);
        return result;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Request request = (Request) o;

        if (url != null ? !url.equals(request.url) : request.url != null) return false;
        return method != null ? method.equals(request.method) : request.method == null;
    }

    public Request addCookie(String name, String value) {
        cookies.put(name, value);
        return this;
    }

    public Request addHeader(String name, String value) {
        headers.put(name, value);
        return this;
    }

    public Map<String, String> getCookies() {
        return cookies;
    }

    public Map<String, String> getHeaders() {
        return headers;
    }

    public HttpRequestBody getRequestBody() {
        return requestBody;
    }

    public void setRequestBody(HttpRequestBody requestBody) {
        this.requestBody = requestBody;
    }

    public boolean isBinaryContent() {
        return binaryContent;
    }

    public Request setBinaryContent(boolean binaryContent) {
        this.binaryContent = binaryContent;
        return this;
    }

    public String getCharset() {
        return charset;
    }

    public Request setCharset(String charset) {
        this.charset = charset;
        return this;
    }

    @Override
    public String toString() {
        return "Request{" +
                "url='" + url + '\'' +
                ", method='" + method + '\'' +
                ", extras=" + extras +
                ", priority=" + priority +
                ", headers=" + headers +
                ", cookies="+ cookies+
                '}';
    }
}
```



## 4.3 使用Selectable抽取元素和获取结果

`Selectable`相关的抽取元素链式API是WebMagic的一个核心功能。使用Selectable接口，你可以直接完成页面元素的链式抽取，也无需去关心抽取的细节。

在刚才的例子中可以看到，`page.getHtml()`返回的是一个`Html`对象，它实现了`Selectable`接口。这个接口包含一些重要的方法，我将它分为两类：抽取部分和获取结果部分。

### 4.3.1 抽取部分API

| 方法                                                   | 说明                             | 示例                                  |
| ------------------------------------------------------ | -------------------------------- | ------------------------------------- |
| `Selectable xpath(String xpath)`                       | 使用XPath选择                    | `html.xpath("//div[@class='title']")` |
| `Selectable $(String selector)`                        | 使用Css选择器选择                | `html.$("div.title")`                 |
| `Selectable $(String selector, String attrName)`       | 使用Css选择器选择                | `html.$("div.title","text")`          |
| `Selectable css(String selector)`                      | 功能同`$()`，使用Css选择器选择   | `html.css("div.title")`               |
| `Selectable css(String selector, String attrName)`     | 功能同`$()`，使用Css选择器选择   | `html.css("div.title","text")`        |
| `Selectable links()`                                   | 选择所有链接                     | `html.links()`                        |
| `Selectable regex(String regex)`                       | 使用正则表达式抽取               | `html.regex("\(.\*?)\")`              |
| `Selectable regex(String regex, int group)`            | 使用正则表达式抽取，并指定捕获组 | `html.regex("\(.\*?)\",1)`            |
| `Selectable replace(String regex, String replacement)` | 替换内容                         | `html.replace("\","")`                |

注：这部分抽取API返回的都是一个`Selectable`接口，意思是说，抽取是支持链式调用的。

### 4.3.2 获取结果的API

当链式调用结束时，我们一般都想要拿到一个字符串类型的结果。这时候就需要用到获取结果的API了。我们知道，一条抽取规则，无论是XPath、CSS选择器或者正则表达式，总有可能抽取到多条元素。WebMagic对这些进行了统一，你可以通过不同的API获取到一个或者多个元素。

| 方法                 | 说明                                  | 示例                                   |
| -------------------- | ------------------------------------- | -------------------------------------- |
| `String get()`       | 返回一条String类型的结果              | `String link= html.links().get()`      |
| `String toString()`  | 功能同get()，返回一条String类型的结果 | `String link= html.links().toString()` |
| `List<String> all()` | 返回所有抽取结果                      | `List links= html.links().all()`       |
| `boolean match()`    | 是否有匹配结果                        | `if (html.links().match()){ xxx; }`    |

例如，我们知道页面只会有一条结果，那么可以使用`selectable.get()`或者`selectable.toString()`拿到这条结果。

这里`selectable.toString()`采用了`toString()`这个接口，是为了在输出以及和一些框架结合的时候，更加方便。因为一般情况下，我们都只需要选择一个元素！

`selectable.all()`则会获取到所有元素。

