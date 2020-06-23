# Java8新时间日期API

# 1 传统时间API的线程安全问题

## 1.1 问题表现

```java
package com.zh.time;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class SimpleDataFormatTest {
	public static void main(String[] args) throws InterruptedException, ExecutionException {
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyyMMdd");
		Callable<Date> task = new Callable<Date>() {
			@Override
			public Date call() throws Exception {
				return simpleDateFormat.parse("20161218");
			}
		};
		ExecutorService pool = Executors.newFixedThreadPool(10);
		List<Future<Date>> results = new ArrayList<Future<Date>>();
		for(int i=0; i < 10; i++) {
			results.add(pool.submit(task));
		}
		for(Future<Date> future:results)
			System.out.println(future.get());
        pool.shutdown();
	}
}
```

输出：

> Sat Dec 18 00:00:00 CST 2060Exception in thread "main" java.util.concurrent.ExecutionException: java.lang.NumberFormatException: For input string: ".2060"<br />
	at java.util.concurrent.FutureTask.report(FutureTask.java:122)<br />
at java.util.concurrent.FutureTask.get(FutureTask.java:192)<br />
at com.zh.time.SimpleDataFormatTest.main(SimpleDataFormatTest.java:28)<br />
Caused by: java.lang.NumberFormatException: For input string: ".2060"<br />
at java.lang.NumberFormatException.forInputString(NumberFormatException.java:65)<br />
at java.lang.Long.parseLong(Long.java:578)<br />
at java.lang.Long.parseLong(Long.java:631)<br />
at java.text.DigitList.getLong(DigitList.java:195)<br />
at java.text.DecimalFormat.parse(DecimalFormat.java:2084)<br />
at java.text.SimpleDateFormat.subParse(SimpleDateFormat.java:1867)<br />
at java.text.SimpleDateFormat.parse(SimpleDateFormat.java:1514)<br />
at java.text.DateFormat.parse(DateFormat.java:364)<br />
at com.zh.time.SimpleDataFormatTest$1.call(SimpleDataFormatTest.java:19)<br />
at com.zh.time.SimpleDataFormatTest$1.call(SimpleDataFormatTest.java:1)<br />
at java.util.concurrent.FutureTask.run(FutureTask.java:266)<br />
at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)<br />
at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)<br />
at java.lang.Thread.run(Thread.java:748)

> Fri Dec 18 00:00:00 CST 2015


## 1.2 使ThreadLocal优化

```java
package com.zh.time;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class DataFormatThreadLocal {
	private static final ThreadLocal<DateFormat> THREAD_LOCAL = new ThreadLocal<DateFormat>() {
		protected DateFormat initialValue() {
	        return new SimpleDateFormat("yyyyMMdd");
	    }
	};
	public static Date convert(String source) throws ParseException {
		return THREAD_LOCAL.get().parse(source);
	}
	public static void main(String[] args) throws InterruptedException, ExecutionException {
		Callable<Date> task = new Callable<Date>() {
			@Override
			public Date call() throws Exception {
				return DataFormatThreadLocal.convert("20161218");
			}
		};
		ExecutorService pool = Executors.newFixedThreadPool(10);
		List<Future<Date>> results = new ArrayList<Future<Date>>();
		for(int i=0; i < 10; i++) {
			results.add(pool.submit(task));
		}
		for(Future<Date> future:results)
			System.out.println(future.get());
		pool.shutdown();
	}
}
```

输出：

> Sun Dec 18 00:00:00 CST 2016<br />
Sun Dec 18 00:00:00 CST 2016<br />
Sun Dec 18 00:00:00 CST 2016<br />
Sun Dec 18 00:00:00 CST 2016<br />
Sun Dec 18 00:00:00 CST 2016<br />
Sun Dec 18 00:00:00 CST 2016<br />
Sun Dec 18 00:00:00 CST 2016<br />
Sun Dec 18 00:00:00 CST 2016<br />
Sun Dec 18 00:00:00 CST 2016<br />
Sun Dec 18 00:00:00 CST 2016


## 1.3 使用Java8 时间日期API优化

```java
package com.zh.time;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class Java8LocalDateTimeFormatterTest {
	public static void main(String[] args) throws InterruptedException, ExecutionException {
		//或者使用预定义格式：DateTimeFormatter.ISO_LOCAL_DATE
		DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyyMMdd");
		Callable<LocalDate> task = new Callable<LocalDate>() {
			@Override
			public LocalDate call() throws Exception {
				return LocalDate.parse("20161218", dateTimeFormatter);
			}
		};
		ExecutorService pool = Executors.newFixedThreadPool(10);
		List<Future<LocalDate>> results = new ArrayList<Future<LocalDate>>();
		for(int i=0; i < 10; i++) {
			results.add(pool.submit(task));
		}
		for(Future<LocalDate> future:results)
			System.out.println(future.get());
		pool.shutdown();
	}
}
```

输出：

> 2016-12-18<br />
2016-12-18<br />
2016-12-18<br />
2016-12-18<br />
2016-12-18<br />
2016-12-18<br />
2016-12-18<br />
2016-12-18<br />
2016-12-18<br />
2016-12-18


# 2 LocalDate、LocalTime、LocalDateTime

LocalDate、LocalTime、LocalDateTime类的实例是**不可变的对象**，分别标识使用ISO-8601（ISO-8601日历系统是国际标准化组织指定的现代公民的日期和时间表示法）日期系统的日期、时间、日期和时间。它们提供了简单的日期或时间，并不包括当前的时间信息。也不包括与时区相关的信息。

```java
package com.zh.time;

import java.time.LocalDateTime;
import org.junit.Test;

public class LocalDateTimeTest {
	@Test
	public void test1() {
		LocalDateTime localDateTime = LocalDateTime.now();
		System.out.println(localDateTime);//输出：2020-04-02T10:06:39.103
		
		System.out.println("----------------------");
		LocalDateTime localDateTime2 = LocalDateTime.of(2020, 8, 8, 8, 8, 8);
		System.out.println(localDateTime2);//输出：2020-08-08T08:08:08
		
		System.out.println("----------------------");
		//加年操作
		LocalDateTime localDateTime3 = localDateTime.plusYears(2);
		System.out.println(localDateTime3);//输出：2022-04-02T10:06:39.103
		
		System.out.println("----------------------");
		//减月操作
		LocalDateTime localDateTime4 = localDateTime.minusMonths(2);
		System.out.println(localDateTime4);//输出：2020-02-02T10:06:39.103
		
		System.out.println("----------------------");
		//获取
		System.out.println(localDateTime.getYear());//获取年 2020
		System.out.println(localDateTime.getMonth().getValue());//获取月 4
		System.out.println(localDateTime.getMonthValue());//获取月 4
	}
}
```

# 3 时间戳Instant

时间戳：以Unix元年（1970年1月1日00:00:00）到某个时间点的毫秒值

默认时区为UTC（世界协调时间）

```java
package com.zh.time;

import java.time.LocalDateTime;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;

import org.junit.Test;

public class LocalDateTimeTest {
	@Test
	public void test2() {
		Instant instant = Instant.now();//默认UTC时区
		System.out.println(instant);//输出：2020-04-02T02:14:24.800Z
		
		OffsetDateTime offsetDateTime = instant.atOffset(ZoneOffset.ofHours(8));//设置时区偏移量
		System.out.println(offsetDateTime);//输出：
		
		System.out.println(instant.toEpochMilli());//时间戳（毫秒级）
		System.out.println(instant.getEpochSecond());//时间戳（秒级）
		
		System.out.println(instant.ofEpochSecond(1));//相较于元年改变时间戳：增加1秒
	}
}
```

# 4 时间间隔Duration和日期间隔Period

```java
package com.zh.time;

import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.OffsetDateTime;
import java.time.Period;
import java.time.ZoneOffset;

import org.junit.Test;

public class LocalDateTimeTest {
	@Test
	public void test3() {
		Instant instant = Instant.now();
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		Instant instant2 = Instant.now();
		Duration duration = Duration.between(instant, instant2);
		System.out.println(duration);//输出：PT1.001S
		System.out.println(duration.getSeconds());//输出：1
		System.out.println(duration.toMillis());//输出：1001
		
		System.out.println("------------------");
		LocalTime time1 = LocalTime.now();
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		LocalTime time2 = LocalTime.now();
		System.out.println(Duration.between(time1, time2).toMillis());//输出：1001
	}
	
	@Test
	public void test4() {
		LocalDate localDate1 = LocalDate.of(2019, 3, 8);
		LocalDate localDate2 = LocalDate.now();
		Period period = Period.between(localDate1, localDate2);
		System.out.println(period);//输出：P1Y25D
		System.out.println(period.getYears());//输出：1
		System.out.println(period.getMonths());//输出：0
		System.out.println(period.getDays());//输出：25
		
	}
}
```

# 5 时间矫正器

- TemporalAdjuster：时间矫正器。有时我们可能需要获取例如：将日期调整到“下个周日”等操作。
- TemporalAdjuster**s**：该类通过静态方法提供了大量的常用TemporalAdjuster的实现。

```java
package com.zh.time;

import java.time.DayOfWeek;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.OffsetDateTime;
import java.time.Period;
import java.time.ZoneOffset;
import java.time.temporal.TemporalAdjusters;

import org.junit.Test;

public class LocalDateTimeTest {	
	@Test
	public void test5() {
		LocalDateTime localDateTime = LocalDateTime.now();
		System.out.println(localDateTime);//输出：2020-04-02T12:57:13.950
		LocalDateTime localDateTime2 = localDateTime.withDayOfMonth(10);//把日期设定为本月10号
		System.out.println(localDateTime2);//输出：2020-04-10T12:57:13.950
		LocalDateTime localDateTime3 = localDateTime.with(TemporalAdjusters.next(DayOfWeek.SUNDAY));//下一个周日
		System.out.println(localDateTime3);//输出：2020-04-05T12:57:13.950
		
		//自定义：下一个工作日
		LocalDateTime localDateTime5 = localDateTime.with((l) -> {
			LocalDateTime localDateTime4 = (LocalDateTime) l;
			DayOfWeek dayOfWeek = localDateTime4.getDayOfWeek();
			if(dayOfWeek.equals(DayOfWeek.FRIDAY))
				return localDateTime4.plusDays(3);
			else if (dayOfWeek.equals(DayOfWeek.SATURDAY))
				return localDateTime4.plusDays(2);
			else 
				return localDateTime4.plusDays(1);
		});
		System.out.println(localDateTime5);//输出：2020-04-03T12:57:13.950
	}
}
```

# 6 格式化时间/日期DateTimeFormatter

```java
package com.zh.time;

import java.time.DayOfWeek;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.OffsetDateTime;
import java.time.Period;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAdjusters;

import org.junit.Test;

public class LocalDateTimeTest {
	@Test
	public void test6() {
		DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ISO_DATE;
		LocalDateTime localDateTime = LocalDateTime.now();
		String format = localDateTime.format(dateTimeFormatter);
		System.out.println(format);//输出：2020-04-02
		
		System.out.println("-----------------");
		DateTimeFormatter dateTimeFormatter2 = DateTimeFormatter.ofPattern("yyyy年MM月dd日 HH:mm:ss");
		String format2 = localDateTime.format(dateTimeFormatter2);
		System.out.println(format2);//输出：2020年04月02日 13:25:38
		String format3 = dateTimeFormatter2.format(localDateTime);
		System.out.println(format3);//输出：2020年04月02日 13:25:38
		
		System.out.println("-----------------");
		LocalDateTime localDateTime2 = localDateTime.parse(format3, dateTimeFormatter2);
		System.out.println(localDateTime2);//输出：2020-04-02T13:25:38
	}
}
```

# 7 时区的处理

Java8中加入了对时区的支持，带时区的时间分别为：ZonedDate、ZonedTime、ZonedDateTime。

其中每个时区都对应着ID，地区ID都为“{区域}/{城市}”的格式，如：Asia/Shanghai等。

ZoneId：该类中包含了所有的时区信息。

- `getAvailableZoneIds()`：可以获取所有时区信息
- `of(id)`：用指定的时区信息获取ZoneId对象。

```java
package com.zh.time;

import java.time.DayOfWeek;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.OffsetDateTime;
import java.time.Period;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAdjusters;
import java.util.Set;

import org.junit.Test;

public class LocalDateTimeTest {
	@Test
	public void test7() {
		Set<String> set = ZoneId.getAvailableZoneIds();
		set.forEach(System.out::println);
	}
	@Test
	public void test8() {
		LocalDateTime localDateTime = LocalDateTime.now();
		System.out.println(localDateTime);//输出：2020-04-02T14:48:14.661
		LocalDateTime localDateTime2 = LocalDateTime.now(ZoneId.of("Europe/Monaco"));
		System.out.println(localDateTime2);//输出：2020-04-02T08:48:14.666
		ZonedDateTime zonedDateTime = localDateTime2.atZone(ZoneId.of("Europe/Monaco"));
		System.out.println(zonedDateTime);//输出：2020-04-02T08:48:14.666+02:00[Europe/Monaco]
	}
}
```
