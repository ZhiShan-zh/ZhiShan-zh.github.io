# 责任链模式

# 1 责任链模式概述

## 1.1 定义

为请求创建了一个接受者对象的链。

## 1.2 优点

1. 请求的发送者和接受者解耦。
1. 可以控制执行顺序。
1. 复合开闭原则和单一职责原则。

## 1.3 应用场景

一个请求的处理需要多个对象当中的一个或几个协作处理。

## 1.4 源码应用

- `javax.servlet.Filter`
- `javax.servlet.FilterChain`

# 2 入门案例

```java
package com.zh.chainofresponsibility;

public class ChainOfResponsibilityTest {
	public static void main(String[] args) {
		Request request = new Request.RequestBuilder().frequentOk(true).loggedOn(true).build();
		RequestFrequentHandler handler = new RequestFrequentHandler(new LoggingHandler(null));
		if(handler.process(request)) {
			System.out.println("正常处理业务");
		}else {
			System.out.println("访问异常");
		}
	}
}

class Request{
	private boolean loggedOn;
	private boolean frequentOk;
	private boolean isPermits;
	private boolean containsSensitiveWords;
	private String requestBody;
	public Request(boolean loggedOn, boolean frequentOk, boolean isPermits, boolean containsSensitiveWords) {
		super();
		this.loggedOn = loggedOn;
		this.frequentOk = frequentOk;
		this.isPermits = isPermits;
		this.containsSensitiveWords = containsSensitiveWords;
	}
	static class RequestBuilder{
		private boolean loggedOn;
		private boolean frequentOk;
		private boolean isPermits;
		private boolean containsSensitiveWords;
		private String requestBody;
		RequestBuilder loggedOn(boolean loggedOn) {
			this.loggedOn = loggedOn;
			return this;
		}
		RequestBuilder frequentOk(boolean frequentOk) {
			this.frequentOk = frequentOk;
			return this;
		}
		RequestBuilder isPermits(boolean isPermits) {
			this.isPermits = isPermits;
			return this;
		}
		RequestBuilder containsSensitiveWords(boolean containsSensitiveWords) {
			this.containsSensitiveWords = containsSensitiveWords;
			return this;
		}
		public Request build() {
			Request request = new Request(loggedOn, frequentOk, isPermits, containsSensitiveWords);
			return request;
		}
	}
	
	public boolean isLoggedOn() {
		return loggedOn;
	}
	
	public boolean isFrequentOk() {
		return frequentOk;
	}
	
	public boolean isPermits() {
		return isPermits;
	}
	
	public boolean isContainsSensitiveWords() {
		return containsSensitiveWords;
	}
}

abstract class Handler{
	Handler next;
	public Handler(Handler next) {
		this.next = next;
	}
	public Handler getNext() {
		return next;
	}
	public void setNext(Handler next) {
		this.next = next;
	}
	abstract boolean process(Request request);
}

class RequestFrequentHandler extends Handler{

	public RequestFrequentHandler(Handler next) {
		super(next);
	}

	@Override
	boolean process(Request request) {
		System.out.println("访问频率控制");
		if(request.isFrequentOk()) {
			Handler next = getNext();
			if(null == next) {
				return true;
			}
			if(!next.process(request)) {
				return false;
			}else {
				return true;
			}
		}
		return false;
	}
}

class LoggingHandler extends Handler{

	public LoggingHandler(Handler next) {
		super(next);
	}

	@Override
	boolean process(Request request) {
		System.out.println("登录验证");
		if(request.isLoggedOn()) {
			Handler next = getNext();
			if(null == next) {
				return true;
			}
			if(!next.process(request)) {
				return false;
			}else {
				return true;
			}
		}
		return false;
	}
	
}
```
