# Future模式

# 1 概述
Future模式有点类似于商品订单。比如在网购时，当看中某一见商品时，就可以提交订单，当订单处理完成后，在家里等待商品送货上门即可。或者说更形象的我们发送Ajax请求的时候，页面是异步地进行后台处理，用户无须一直等待请求的结果，可以继续浏览或操作其它内容。
![image.png](https://zhishan-zh.github.io/media/1587547631719-cdf31aa6-f956-4ed8-a436-8c4a285d3b9a.png)

# 2 Future模式实现
## 2.1 FutureClient
```java
package com.bjsxt.height.design014;

public class FutureClient {
	public Data request(final String queryStr){
		//1 我想要一个代理对象（Data接口的实现类）先返回给发送请求的客户端，告诉他请求已经接收到，可以做其他的事情
		final FutureData futureData = new FutureData();
		//2 启动一个新的线程，去加载真实的数据，传递给这个代理对象
		new Thread(new Runnable() {
			@Override
			public void run() {
				//3 这个新的线程可以去慢慢的加载真实对象，然后传递给代理对象
				RealData realData = new RealData(queryStr);
				futureData.setRealData(realData);
			}
		}).start();		
		return futureData;
	}	
}
```
## 2.2 FutureData
```java
package com.bjsxt.height.design014;

public class FutureData implements Data{
	private RealData realData ;	
	private boolean isReady = false;
	
	public synchronized void setRealData(RealData realData) {
		//如果已经装载完毕了，就直接返回
		if(isReady){
			return;
		}
		//如果没装载，进行装载真实对象
		this.realData = realData;
		isReady = true;
		//进行通知
		notify();
	}
	
	@Override
	public synchronized String getRequest() {
		//如果没装载好 程序就一直处于阻塞状态
		while(!isReady){
			try {
				wait();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		//装载好直接获取数据即可
		return this.realData.getRequest();
	}
}
```
## 2.3 RealData
```java
package com.bjsxt.height.design014;

public class RealData implements Data{
	private String result ;
	
	public RealData (String queryStr){
		System.out.println("根据" + queryStr + "进行查询，这是一个很耗时的操作..");
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		System.out.println("操作完毕，获取结果");
		result = "查询结果";
	}
	
	@Override
	public String getRequest() {
		return result;
	}
}
```


## 2.4 Data
```java
package com.bjsxt.height.design014;

public interface Data {
	String getRequest();
}
```


## 2.5 使用测试


```java
package com.bjsxt.height.design014;

public class Main {
	public static void main(String[] args) throws InterruptedException {		
		FutureClient fc = new FutureClient();
		Data data = fc.request("请求参数");
		System.out.println("请求发送成功!");
		System.out.println("做其他的事情...");
		
		String result = data.getRequest();
		System.out.println(result);		
	}
}
```


# 3 JDK中的Future
## 3.1 Runnable&Callable
### 3.1.1 Runnable
```java
package java.lang;
@FunctionalInterface
public interface Runnable {
    public abstract void run();
}
```
由于run()方法返回值为void类型，所以在执行完任务之后无法返回任何结果。
### 3.1.2 Callable
这是一个泛型接口，call()函数返回的类型就是传递进来的V类型。
```java
package java.util.concurrent;
@FunctionalInterface
public interface Callable<V> {
    V call() throws Exception;
}
```


## 3.2 Future接口
### 3.2.1 接口声明
```java
public interface Future<V> {
    /*
    cancel方法用来取消任务，如果取消任务成功则返回true，如果取消任务失败则返回false。
    参数mayInterruptIfRunning表示是否允许取消正在执行却没有执行完毕的任务，
    如果设置true，则表示可以取消正在执行过程中的任务。
    1. 如果任务已经完成，则无论mayInterruptIfRunning为true还是false，此方法肯定返回false，
    	即如果取消已经完成的任务会返回false；
    2. 如果任务正在执行，若mayInterruptIfRunning设置为true，则返回true，
    	若mayInterruptIfRunning设置为false，则返回false；
    3. 如果任务还没有执行，则无论mayInterruptIfRunning为true还是false，肯定返回true。
    */
	boolean cancel(boolean mayInterruptIfRunning);
    //表示任务是否被取消成功，如果在任务正常完成前被取消成功，则返回 true。
    boolean isCancelled();
    //表示任务是否已经完成，若任务完成，则返回true；
    boolean isDone();
    //用来获取执行结果，这个方法会产生阻塞，会一直等到任务执行完毕才返回；
    V get() throws InterruptedException, ExecutionException;
    //用来获取执行结果，如果在指定时间内，还没获取到结果，就直接返回null。
    V get(long timeout, TimeUnit unit)
        throws InterruptedException, ExecutionException, TimeoutException;
}
```
### 3.2.1 使用案例
**Future + Callable**：
```java
package com.zh.java7;

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class FutureTest {
	public static void main(String[] args) {
		ExecutorService executor = Executors.newCachedThreadPool();
		Future<Integer> future = executor.submit(new Callable<Integer>() {
			@Override
			public Integer call() throws Exception {
				System.out.println("开始执行子线程，开始时间为:" + System.currentTimeMillis());
				Thread.sleep(3000);
				return 1;
			}
		});
        executor.shutdown();
		try {
			System.out.println("子线程执行结束，结果为：" + future.get() + "；结束时间为：" + System.currentTimeMillis());
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		}
	}
}
```


## 3.3 FutureTask
类FutureTask的声明：
```java
public class FutureTask<V> implements RunnableFuture<V>
```
接口RunnableFuture的声明：
```java
public interface RunnableFuture<V> extends Runnable, Future<V> {
    /**
     * Sets this Future to the result of its computation
     * unless it has been cancelled.
     */
    void run();
}
```
可以看到FutureTask类中有一个重写接口RunnableFuture的run方法，查看源码可以run方法调用的是私有属性Callable的call方法来实现业务逻辑的。
**FutureTask类有2个构造器**：

1. 传入一个Callable
```java
public FutureTask(Callable<V> callable) {
    if (callable == null)
        throw new NullPointerException();
    this.callable = callable;
    this.state = NEW;       // ensure visibility of callable
}
```

2. 传入一个Runnable和一个泛型的结果对象，在这个构造器中，使用Executors的工具方法callable，把Runnable转换成了一个Callable。
```java
public FutureTask(Runnable runnable, V result) {
    this.callable = Executors.callable(runnable, result);
    this.state = NEW;       // ensure visibility of callable
}
```
### 3.3.1 使用案例
**ExecutorService + FutureTask**：

```java
package com.zh.java7;

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.FutureTask;

public class FutureTest {
	public static void main(String[] args) {
		ExecutorService executor = Executors.newCachedThreadPool();
		FutureTask<Integer> futureTask = new FutureTask<Integer>(new Callable<Integer>() {

			@Override
			public Integer call() throws Exception {
				System.out.println("开始执行子线程，开始时间为:" + System.currentTimeMillis());
				Thread.sleep(3000);
				return 1;
			}
		});
		executor.submit(futureTask);
		executor.shutdown();
		try {
			System.out.println("子线程执行结束，结果为：" + futureTask.get() + "；结束时间为：" + System.currentTimeMillis());
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		}
	}
}
```
**Thread + FutureTask**：
```java
package com.zh.java7;

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;

public class FutureTest {
	public static void main(String[] args) {
		FutureTask<Integer> futureTask = new FutureTask<Integer>(new Callable<Integer>() {

			@Override
			public Integer call() throws Exception {
				System.out.println("开始执行子线程，开始时间为:" + System.currentTimeMillis());
				Thread.sleep(3000);
				return 1;
			}
		});
		Thread thread = new Thread(futureTask);
		thread.start();
		try {
			System.out.println("子线程执行结束，结果为：" + futureTask.get() + "；结束时间为：" + System.currentTimeMillis());
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		}
	}
}
```
## 3.4 ListenableFuture
**依赖**：

- `failureaccess-1.0.1.jar`
- `guava-29.0-jre.jar`
### 3.4.1 接口声明
Guava的ListenableFuture扩展了Future接口，是一个可以监听结果的Future。就是它可以监听异步执行的过程，执行完了，自动触发后续操作。
```java
package com.google.common.util.concurrent;

import com.google.errorprone.annotations.DoNotMock;
import java.util.concurrent.Executor;
import java.util.concurrent.Future;

@DoNotMock("Use the methods in Futures (like immediateFuture) or SettableFuture")
public abstract interface ListenableFuture<V> extends Future<V> {
	public abstract void addListener(Runnable paramRunnable, Executor paramExecutor);
}
```
### 3.4.2 通过ListenableFuture的addListener执行回调函数
```java
package com.zh.java7;

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;

import com.google.common.util.concurrent.ListenableFuture;
import com.google.common.util.concurrent.ListeningExecutorService;
import com.google.common.util.concurrent.MoreExecutors;

public class ListenableFutureTest {
	public static <T> void main(String[] args) {
		//MoreExecutors.listeningDecorator就是包装了一下ThreadPoolExecutor，目的是为了使用ListenableFuture
		ListeningExecutorService pool = MoreExecutors.listeningDecorator(Executors.newFixedThreadPool(5));

		final ListenableFuture<String> future2 = pool.submit(new Callable<String>() {

			@Override
			public String call() throws Exception {
				return "future2 任务";
			}
		});

		future2.addListener(new Runnable() {
			@Override
			public void run() {
				try {
					System.out.println("可以执行回调函数了，ListenableFuture执行结果=" + future2.get());
				} catch (InterruptedException e) {
					e.printStackTrace();
				} catch (ExecutionException e) {
					e.printStackTrace();
				}
			}
		}, pool);
	}
}

```
### 3.4.3 Futures使用addCallback添加FutureCallBack回调函数
```java
package com.zh.java7;

import java.util.concurrent.Callable;
import java.util.concurrent.Executors;

import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;
import com.google.common.util.concurrent.ListeningExecutorService;
import com.google.common.util.concurrent.MoreExecutors;

public class ListenableFutureTest {
	public static void main(String[] args) {
		// MoreExecutors.listeningDecorator就是包装了一下ThreadPoolExecutor，目的是为了使用ListenableFuture
		ListeningExecutorService pool = MoreExecutors.listeningDecorator(Executors.newFixedThreadPool(5));
		ListenableFuture<String> future = pool.submit(new Callable<String>() {

			@Override
			public String call() throws Exception {
				return "future 任务";
			}
		});
		// FutureCallBack接口可以对每个任务的成功或失败单独做出响应
		FutureCallback<String> futureCallback = new FutureCallback<String>() {
			@Override
			public void onSuccess(String result) {
				System.out.println("Futures.addCallback 能带返回值：" + result);
			}

			@Override
			public void onFailure(Throwable t) {
				System.out.println("出错,业务回滚或补偿");
			}
		};
		// 为任务绑定回调接口
		Futures.addCallback(future, futureCallback, pool);
	}
}
```
## 3.5 CompletableFuture
### 3.5.1 概述
CompletableFuture是JDK1.8新增的的类，提供了非常强大的Future的扩展功能。可以对多个异步处理进行编排，实现更复杂的异步处理。它能够将回调放到与任务不同的线程中执行，也能将回调作为继续执行的同步函数，在与任务相同的线程中执行。

其内部使用ForkJoinPool实现异步处理。

### 3.5.2 优点

- 异步任务结束时，会自动回调某个对象的方法；
- 异步任务出错时，会自动回调某个对象的方法；
- 线程设置好回调后，不再关心异步任务的执行。
### 3.5.3 基本用法

- `thenAccept()` ：处理正常结果；
- `exceptional()` ：处理异常结果。
```java
CompletableFuture<String> cf = CompletableFuture.supplyAsync(new Supplier<String>() {
    @Override
    public String get() {
        return "异步执行代码";
    }
});
cf.thenAccept(new Consumer<String>() {

    @Override
    public void accept(String str) {
        System.out.println("异步执行结果:" + str);
    }
});
cf.exceptionally(new Function<Throwable, String>() {

    @Override
    public String apply(Throwable t) {
        System.out.println("Error:" + t.getMessage());
        return "异步执行错误";
    }
});
cf.join();
```
### 3.5.3 入门案例
#### 3.5.3.1 DownloadUtil
```java
package com.zh.future;

import java.io.IOException;

import org.apache.http.HttpEntity;
import org.apache.http.ParseException;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;

public class DownloadUtil {
	public static String download(String url) {
		CloseableHttpClient httpClient = HttpClientBuilder.create().build();
		// 创建Get请求
		HttpGet httpGet = new HttpGet(url);
		// 响应模型
		CloseableHttpResponse response = null;
		try {
			// 由客户端执行(发送)Get请求
			response = httpClient.execute(httpGet);
			// 从响应模型中获取响应实体
			if(response.getStatusLine().getStatusCode()==200) {
				HttpEntity responseEntity = response.getEntity();
				if(null != responseEntity)
					return EntityUtils.toString(responseEntity);
			}
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (ParseException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				// 释放资源
				if (httpClient != null) {
					httpClient.close();
				}
				if (response != null) {
					response.close();
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return null;
	}
}
```
#### 3.5.3.2 CompletableFutureSample
```java
package com.zh.future;

import java.util.concurrent.CompletableFuture;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;

class StockSupplier implements Supplier<Float>{

	@Override
	public Float get() {
		String url = "http://hq.sinajs.cn/list=sh000001";
		System.out.println("GET:" + url);
		String result = DownloadUtil.download(url);
		String[] ss = result.split(",");
		return Float.parseFloat(ss[3]);
	}
}
public class CompletableFutureSample{
	public static void main(String[] args) {
		CompletableFuture<Float> getStockFuture = CompletableFuture.supplyAsync(new StockSupplier());
		getStockFuture.thenAccept(new Consumer<Float>() {

			@Override
			public void accept(Float price) {
				System.out.println("Current price:" + price);
			}
		});
		getStockFuture.exceptionally(new Function<Throwable, Float>() {

			@Override
			public Float apply(Throwable t) {
				System.out.println("Error:" + t.getMessage());
				return Float.NaN;
			}
		});
		getStockFuture.join();
	}
}
```
### 3.5.4 多个CompletableFuture串行执行

- thenApplyAsync方法：用于串行化另一个CompletableFuture
```java
CompletableFuture<String> cf1 = CompletableFuture.supplyAsync(new Supplier<String>() {
    @Override
    public String get() {
        return "异步执行代码1";
    }
});
CompletableFuture<Float> cf2 = cf1.thenApplyAsync(new Supplier<Float>() {
    @Override
    public Float get() {
        return 1.0f;
    }
});
cf2.thenAccept(new Consumer<Float>() {

    @Override
    public void accept(Float num) {
        System.out.println("异步执行2结果:" + num);
    }
});
```
示例：
```java
package com.zh.future;

import java.util.concurrent.CompletableFuture;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;

class Price{
	final String code;
	final float price;
	public Price(String code, float price) {
		this.code = code;
		this.price = price;
	}
}
class StockLookupSupplier implements Supplier<String>{
	String name;
	
	public StockLookupSupplier(String name) {
		this.name = name;
	}

	@Override
	public String get() {
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		return "sh000001";
	}
}
public class CompletableFutureSequenceSample {
	public static void main(String[] args) {
		String name = "上证指数";
		CompletableFuture<String> getStockCompletableFuture = CompletableFuture.supplyAsync(new StockLookupSupplier(name));
		CompletableFuture<Price> getStockPriceFuture = getStockCompletableFuture.thenApplyAsync(new Function<String, Price>() {

			@Override
			public Price apply(String code) {
				String url = "http://hq.sinajs.cn/list=" + code;
				System.out.println("GET:" + url);
				String result = DownloadUtil.download(url);
				String[] ss = result.split(",");
				return new Price(code, Float.parseFloat(ss[3]));
			}
		});
		getStockPriceFuture.thenAccept(new Consumer<Price>() {

			@Override
			public void accept(Price price) {
				System.out.println(price.code + ":" + price.price);
			}
		});
		getStockPriceFuture.join();
	}
}
```
### 3.5.5 多个CompletableFuture并行执行

- anyOf方法：用于并行执行两个CompletableFuture，任何一个异步任务返回结果后就调用`thenAccept`。
- allOf方法：用于并行执行两个CompletableFuture，全部异步任务返回结果后再去执行`thenAccept`。
```java
package com.zh.future;

import java.util.concurrent.CompletableFuture;
import java.util.function.Consumer;
import java.util.function.Supplier;

class StockPrice{
	final float price;
	final String from;
	public StockPrice(float price, String from) {
		this.price = price;
		this.from = from;
	}
	@Override
	public String toString() {
		return "StockPrice [price=" + price + ", from=" + from + "]";
	}
}
class StockFromSina implements Supplier<StockPrice>{

	@Override
	public StockPrice get() {
		String url = "http://hq.sinajs.cn/list=sh000001";
		String result = DownloadUtil.download(url);
		String[] ss = result.split(",");
		return new StockPrice(Float.parseFloat(ss[3]), "sina");
	}
}
class StockFromNetease implements Supplier<StockPrice>{

	@Override
	public StockPrice get() {
		String url = "http://api.money.126.net/data/feed/000001,money.api";
		String result = DownloadUtil.download(url);
		int priceIndex = result.indexOf("\"price\"");
		if(priceIndex > 0) {
			int start = result.indexOf(":", priceIndex);
			int end = result.indexOf(",", priceIndex);
			return new StockPrice(Float.parseFloat(result.substring(start, end)), "netease");
		}else {
			//此接口可能没有price，故以此测试调用效果
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			return new StockPrice(0.0f, "netease");
		}
	}
}
public class CompletableFutureAnyOfSample {
	public static void main(String[] args) {
		CompletableFuture<StockPrice> getStockFromSina = CompletableFuture.supplyAsync(new StockFromSina());
		CompletableFuture<StockPrice> getStockFromNetease = CompletableFuture.supplyAsync(new StockFromNetease());
		//CompletableFuture<Void> getStockkFuture = CompletableFuture.allOf(getStockFromSina, getStockFromNetease);
		CompletableFuture<Object> getStockkFuture = CompletableFuture.anyOf(getStockFromSina, getStockFromNetease);
		getStockkFuture.thenAccept(new Consumer<Object>() {
			@Override
			public void accept(Object result) {
				System.out.println("Result:" + result);
			}
		});
		getStockkFuture.join();	
	}
}
```
### 3.5.6 CompletableFuture的命名规则

- `xxx()` ：继续在已有的线程中执行；
- `xxxAsync()` ：用Executor的新线程执行。

### 3.5.7 异步编排CompletableFuture

#### 3.5.7.1 场景一：三个服务异步并发调用，然后对结果合并处理，不阻塞主线程

![image-20200520221915867](https://zhishan-zh.github.io/media/image-20200520221915867.png)

```java
public static void test1() throws Exception {
    MyService service = new MyService();
    CompletableFuture<String> future1 = service.getHttpData("http://www.jd.com");
    CompletableFuture<String> future2 = service.getHttpData("http://www.jd.com");
    CompletableFuture<String> future3 = service.getHttpData("http://www.jd.com");
    CompletableFuture.allOf(future1, future2, future3).thenApplyAsync((Void) -> {
        // 异步处理 future1, future2, future3结果
    }).exceptionally(e -> {
        // 处理异常
    });
}
```

上方直接通过thenApplyAsync异步处理future1~3的结果，不阻塞主线程，内部使用ForkJoinPool线程池实现。也可以通过饭后一个新的CompletableFuture来同步处理结果，即阻塞主线程。

```java
CompletableFuture<List> future4 = CompletableFuture.allOf(future1, future2, future3).thenApply((Void) -> {
        return Lists.newArrayList(future1.get(), future2.get(), future3.get());
    }).exceptionally(e -> {
        // 处理异常
    });
```

#### 3.5.7.2 场景二：两个服务并发调用，然后消费结果，不阻塞主线程

```java
public static void test1() throws Exception {
    MyService service = new MyService();
    CompletableFuture<String> future1 = service.getHttpData("http://www.jd.com");
    CompletableFuture<String> future2 = service.getHttpData("http://www.jd.com");
    CompletableFuture.thenAcceptBothAsync(future2, (future1Result, future2Result) -> {
        // 异步处理结果
    }).exceptionally(e -> {
        // 处理异常
    });
}
```

#### 3.5.7.3 场景三：服务1执行完成后，结果并发执行服务2和服务3，然后消费相关结果，不阻塞主线程

![image-20200520224333112](https://zhishan-zh.github.io/media/image-20200520224333112.png)

```java
public static void test1() throws Exception {
    MyService service = new MyService();
    CompletableFuture<String> future1 = service.getHttpData("http://www.jd.com");
    CompletableFuture<String> future2 = future1.thenApplyAsync((v) -> {
        return "result from service2";
    });
    CompletableFuture<String> future3 = service.getHttpData("http://www.jd.com");
    future2.a\thenCombineAsync(future3, (future2Result, future3Result) -> {
        // 处理业务
    }).exceptionally(e -> {
        // 处理异常
    });
}
```













