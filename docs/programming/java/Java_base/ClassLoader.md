# 类加载器

# 1 类加载器概述

我们编写的”.java“扩展名的源代码文件中存储者要执行的程序逻辑，这些文件需要经过java编译器编译成”.class“文件。”.class“文件中存放者编译后虚拟机指令的二进制信息。当需要用到某个类时，虚拟机将会加载它，并在内存中创建对应的class对象，这个过程称之为类加载。一个类的生命周期从类加载，连接和初始化开始，只有在虚拟机内存中，我们的java程序才可以使用它。整个过程如下图所示：

![classloader.png](https://zhishan-zh.github.io/media/java_base-bc2c-762a4b027ed5.png)

# 2 类加载器

类的加载是由类加载器完成的。

类加载器可以分为两种：

- Java虚拟机自带的类加载器：启动类加载器、扩展类加载器和系统类加载器。
- 用户自定义的类加载器，是`java.lang.ClassLoader`的子类实例。

## 2.1 虚拟机内置加载器


### 2.1.1 根类加载器（Bootstrap）

根类加载器是最底层的类加载器，是虚拟机的一部分，它是由C++实现的，且没有父加载器，也没有继承`java.lang.ClassLoader`类。

根类加载器主要负责加载由系统属性`sun.boot.class.path`指定的路径下的核心类库（即`<JAVA_HOME>\jre\lib`），出于安全考虑，根类加载器只加载java、javax、sun开头的类。

根类加载器，我们自己编写的程序中是无法使用的。

```java
package com.zh.classloader;

public class ClassLoaderTest {
    /**
	 * 测试根类加载器
	 * 输出：null
	 * @param args
	 */
	public static void main(String[] args) {
		ClassLoader classLoader = Object.class.getClassLoader();
		System.out.println(classLoader);//输出为：null
	}
}
```


### 2.1.2 扩展类加载器（Extension）

扩展类加载器是指由原SUN公司实现的`sun.misc.Launcher$ExtClassLoader`类（JDK9是`jdk.internal.loader.ClassLoader$PlatformClassLoader`类），它是由java语言编写的，继承关系图为：

> sun.misc.Launcher.ExtClassLoader
> > java.net.URLClassLoader
> > java.security.SecureClassLoader
> > java.lang.ClassLoader

> java.io.Closeable

扩展类加载器负责加载`<JAVA_HOME>\jre\lib\ext`目录下的类库或者系统变量`java.ext.dirs`指定的目录下的类库。

`sun.misc.Launcher.ExtClassLoader`加载目录的源码：

```java
private static File[] getExtDirs() {
    String s = System.getProperty("java.ext.dirs");
    File[] dirs;
    if (s != null) {
        StringTokenizer st =
            new StringTokenizer(s, File.pathSeparator);
        int count = st.countTokens();
        dirs = new File[count];
        for (int i = 0; i < count; i++) {
            dirs[i] = new File(st.nextToken());
        }
    } else {
        dirs = new File[0];
    }
    return dirs;
}
```

测试扩展类加载器：

```java
package com.zh.classloader;

import sun.net.spi.nameservice.dns.DNSNameService;

public class ClassLoaderTest {
	/**
	 * 测试扩展类加载器
	 * 输出：sun.misc.Launcher$ExtClassLoader@4e25154f
	 * @param args
	 */
	public static void main(String[] args) {
		ClassLoader classLoader = DNSNameService.class.getClassLoader();
		System.out.println(classLoader);
	}
}
```

### 2.1.3 系统类加载器（System）

系统类加载器也称之为应用类加载器，它也是由Java实现的加载器。它是由原SUN公司实现的`sun.misc.Launcher$AppClassLoader`类（JDK9为`jdk.internal.loader.ClassLoaders$AppClassLoader`）。

它的继承关系为：

> sun.misc.Launcher.AppClassLoader
> > java.net.URLClassLoader
> > java.security.SecureClassLoader
> > java.lang.ClassLoader

> java.io.Closeable

它负责从classpath环境变量或者系统属性`java.class.path`指定的目录中加载类。

它是用户自定义的类加载器的默认父加载器。

一般情况下，该类加载器是程序中默认的类加载器，可以通过`ClassLoader.getSystemClassLoader()`直接获得。

测试自己编写的类所使用的类加载器：

```java
package com.zh.classloader;

import sun.net.spi.nameservice.dns.DNSNameService;

public class ClassLoaderTest {
	/**
	 * 测试自己编写的类所用的类加载器
	 * 输出：sun.misc.Launcher$AppClassLoader@4e0e2f2a
	 * @param args
	 */
	public static void main(String[] args) {
		ClassLoader classLoader = ClassLoaderTest.class.getClassLoader();
		System.out.println(classLoader);
	}
}
```


## 3.2 类加载器的双亲委派机制


### 3.2.1 概述

除了根类加载器之外，其它的类加载器都需要有自己的父加载器。从JDK1.2开始，类的加载过程采用双亲委派机制，这种机制能够很好地保护Java程序的安全。除了根类加载器之外，其余的类加载器都有唯一的父加载器。

比如，如果需要一个类加载器加载一个类时，该类加载器先委托自己的父类加载器先去加载这个类，若父类加载器能够加载，则由父类加载器加载，否则才有该类加载器来加载这个类。也就是说，每个类加载器都很懒，加载类时先让父类加载器去尝试加载，一直委托到根类加载器，委托父类加载器加载不成功时才自己去加载。真正加载类的加载器我们叫做启动类加载器。

注意：双亲委派机制的父子关系并非面向对象程序涉及中的继承关系，而是通过使用组合模式来复用父类加载器代码。这种机制如下图所示：

![classloeaderorder.png](https://zhishan-zh.github.io/media/java_base-9fb1-226a850219a6.png)

测试父子加载器：

```java
package com.zh.classloader;

import sun.net.spi.nameservice.dns.DNSNameService;

public class ClassLoaderTest {
	/**
	 * 测试父子加载器
	 * 输出：
	 * 	sun.misc.Launcher$AppClassLoader@4e0e2f2a
	 *	sun.misc.Launcher$ExtClassLoader@2a139a55
	 * @param args
	 */
	public static void main(String[] args) {
		ClassLoader classLoader = ClassLoaderTest.class.getClassLoader();
		while(null != classLoader) {
			System.out.println(classLoader);
			classLoader = classLoader.getParent();
		}
	}
}
```


### 3.2.2 使用双亲委派机制的好处


1. 可以避免类的重复加载，当父类加载器已经加载了该类时，就没有必要子类加载器再加载一次。
2. 考虑到安全因素，Java核心api中定义的类型不会被随意替换。
> 假设通过网络传递一个名为java.lang.Object的类，通过双亲委派机制传递到根类加载器，而根类加载器再核心Java API中发现了这个名字的类，发现该类已经被加载，就不会创新加载网络传递过来的java.lang.Object，而直接返回已加载的Object.class，这样便可以防止核心API库被随意篡改。


自定的包不能为`java.lang`等：

```java
package java.lang;

public class MyObject {
	public static void main(String[] args) {
		ClassLoader classLoader = MyObject.class.getClassLoader();
		System.out.println(classLoader);
	}
}
```

输出：

```
Error: A JNI error has occurred, please check your installation and try again
Exception in thread "main" java.lang.SecurityException: Prohibited package name: java.lang
at java.lang.ClassLoader.preDefineClass(ClassLoader.java:656)
at java.lang.ClassLoader.defineClass(ClassLoader.java:755)
at java.security.SecureClassLoader.defineClass(SecureClassLoader.java:142)
at java.net.URLClassLoader.defineClass(URLClassLoader.java:468)
at java.net.URLClassLoader.access$100(URLClassLoader.java:74)
at java.net.URLClassLoader$1.run(URLClassLoader.java:369)
at java.net.URLClassLoader$1.run(URLClassLoader.java:363)
at java.security.AccessController.doPrivileged(Native Method)
at java.net.URLClassLoader.findClass(URLClassLoader.java:362)
at java.lang.ClassLoader.loadClass(ClassLoader.java:419)
at sun.misc.LauncherAppClassLoader.loadClass(Launcher.java:352)
at java.lang.ClassLoader.loadClass(ClassLoader.java:352)
at sun.launcher.LauncherHelper.checkAndLoadMain(LauncherHelper.java:495)
```

## 3.3 ClassLoader

所有的类加载器（除了根类加载器）都必须继承`java.lang.ClassLoader`。它是一个抽象类。

### 3.3.1 loadClass()

在ClassLoader的源码中，有一个方法`protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException`，这就是双亲委派机制的代码实现。从源代码中我们可以观察到它的执行顺序。需要注意的是，只有父类加载器加载不到类时，会调用findClass方法进行类的查找，所以，再定义自己的类加载器时，不要覆盖掉loadClass方法，而应该覆盖掉findClass方法。

`java.lang.ClassLoader`的loadClass方法源码：

```java
protected Class<?> loadClass(String name, boolean resolve)
    throws ClassNotFoundException {
    synchronized (getClassLoadingLock(name)) {
        // First, check if the class has already been loaded
        Class<?> c = findLoadedClass(name);
        if (c == null) {
            long t0 = System.nanoTime();
            try {
                if (parent != null) {
                    c = parent.loadClass(name, false);
                } else {
                    c = findBootstrapClassOrNull(name);
                }
            } catch (ClassNotFoundException e) {
                // ClassNotFoundException thrown if class not found
                // from the non-null parent class loader
            }

            if (c == null) {
                // If still not found, then invoke findClass in order to find the class.
                long t1 = System.nanoTime();
                c = findClass(name);

                // this is the defining class loader; record the stats
                sun.misc.PerfCounter.getParentDelegationTime().addTime(t1 - t0);
                sun.misc.PerfCounter.getFindClassTime().addElapsedTimeFrom(t1);
                sun.misc.PerfCounter.getFindClasses().increment();
            }
        }
        if (resolve) {
            resolveClass(c);
        }
        return c;
    }
}
```

**官方API解释**：

使用指定的二进制名称来加载类。此方法的默认实现将按以下顺序搜索类：

1. 调用`findLoadedClass(String)`来检查是否已经加载类。
2. 在父类加载器上调用loadClass方法，如果父类加载器为null，则使用虚拟机内置类加载器。
3. 调用`findClass(String)`方法查找类。

如果使用上述步骤找到类，并且resolve标识为真，则此方发将在得到的Class对象上调用`resolveClass(Class)`方法。

鼓励用ClassLoader的子类重写`findClass(String)`，而不是使用此方法（loadClass）。

**参数：**

- name：类的二进制名称
- resolve：如果该参数为true，则分析这个类。

**返回：**得到的Class对象

**抛出：**ClassNotFoundException：如果无法找到类

### 3.3.2 findClass()

在自定义类加载器时，一般我们需要覆盖这个方法，且ClassLoader中给出了一个默认的错误实现：

```java
protected Class<?> findClass(String name) throws ClassNotFoundException {
    throw new ClassNotFoundException(name);
}
```


### 3.3.3 defineClass()

该方法用来将byte字节解析成虚拟机能够识别的Class对象。`defineClass()`方法通常与`findClass()`方法一起使用。再自定义类加载器时，会直接覆盖ClassLoader的`findClass()`方法获取要加载类的字节码，然后调用`defineClass()`方法生成Class对象。

方法签名：

```java
protected final Class<?> defineClass(String name, byte[] b, int off, int len)
        throws ClassFormatError
```


### 3.3.4 resolveClass()

连接指定的类。类加载器可以使用此方法来连接类。

## 3.4 URLClassLoader


### 3.4.1 概述

在`java.net`包中，JDK提供了一个更加易用的类加载器URLClassLoader，它扩展俩ClassLoader，能够从本地或者网络上指定的位置加载类。我们可以使用该类作为自定义的类加载器使用。

构造方法：

- `public URLClassLoader(URL[] urls)`：指定要加载的类所在的URL地址，父类加载器默认为系统类加载器。
- `public URLClassLoader(URL[] urls, ClassLoader parent)`：指定要加载的类所在的URL地址，并指定父类加载器。

### 3.4.2 加载磁盘上的类

要加载类的位置：`/home/zh/文档/Demo.java`

```java
package com.zh.urlclassloadertest;

public class Demo{
	public Demo(){
		System.out.println("create Demo instance!");
	}
}
```

编译此类：

```shell
[zh@zh-inspironn4050 文档]$ javac -d . Demo.java
```

编译后类的路径：`/home/zh/文档/com/zh/urlclassloadertest/Demo.class`

使用URLClassLoader加载磁盘上的类：

```java
package com.zh.classloader;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;
import java.net.URLClassLoader;

public class ClassLoaderTest {
	/**
	 * 使用URLClassLoader加载磁盘的上自定义的类
	 * 输出：
	 * 		父类加载器：sun.misc.Launcher$AppClassLoader@4e0e2f2a
	 * 		create Demo instance!
	 * @param args
	 * @throws MalformedURLException 
	 * @throws ClassNotFoundException 
	 * @throws IllegalAccessException 
	 * @throws InstantiationException 
	 */
	public static void main(String[] args) throws MalformedURLException, ClassNotFoundException, InstantiationException, IllegalAccessException {
		File file = new File("/home/zh/文档");
		URI uri = file.toURI();
		URL url = uri.toURL();
		URLClassLoader urlClassLoader = new URLClassLoader(new URL[] {url});
		System.out.println("父类加载器：" + urlClassLoader.getParent());
		Class clazz = urlClassLoader.loadClass("com.zh.urlclassloadertest.Demo");
		clazz.newInstance();
	}
}
```


### 3.4.3 加载网络上的类

把上边编译好的类放在apache-tomcat-8.5.40里边，此时类的路径为：`apache-tomcat-8.5.40/webapps/ROOT/com/zh/urlclassloadertest/Demo.class`

然后启动tomcat，并在浏览器访问：`http://localhost:8080/com/zh/urlclassloadertest/Demo.class`，如果发现可以下载此类则说明部署成功。

```java
package com.zh.classloader;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;
import java.net.URLClassLoader;

import sun.net.spi.nameservice.dns.DNSNameService;

public class ClassLoaderTest {
	/**
	 * 使用URLClassLoader加载网络上自定义的类
	 * 输出：
	 * 		父类加载器：sun.misc.Launcher$AppClassLoader@4e0e2f2a
	 * 		create Demo instance!
	 * @param args
	 * @throws MalformedURLException
	 * @throws ClassNotFoundException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 */
	public static void main(String[] args) throws MalformedURLException, ClassNotFoundException, InstantiationException, IllegalAccessException {
		URL url = new URL("http://localhost:8080/");
		URLClassLoader urlClassLoader = new URLClassLoader(new URL[] {url});
		System.out.println("父类加载器：" + urlClassLoader.getParent());
		Class clazz = urlClassLoader.loadClass("com.zh.urlclassloadertest.Demo");
		clazz.newInstance();
	}
}
```


## 3.5 自定义类加载器

我们如果需要自定义类加载器，只需要继承ClassLoader类，并覆盖掉findClass方法即可。

### 3.5.1 自定义文件类加载器


```java
package com.zh.classloader;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

public class MyFileClassLoader extends ClassLoader{
	private String dir;//被加载类所在的目录
    /**
	 * 默认父类加载器就是系统类加载器AppClassLoader
	 * @param dir
	 */
	public MyFileClassLoader(String dir) {
		this.dir = dir;
	}
	public MyFileClassLoader(String dir, ClassLoader parent) {
		super(parent);
		this.dir = dir;
	}
	@Override
	protected Class<?> findClass(String name) throws ClassNotFoundException {
		try {
			// 第一步：把全路径类名转换为目录
			String filePath = dir + File.separator + name.replace(".", File.separator) + ".class";
			// 第二步：构造输入流
			InputStream inputStream = new FileInputStream(filePath);
			//第三步：构造字节输出流
			ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
			byte buf[] = new byte[1024];
			int len = -1;
			while((len = inputStream.read(buf)) != -1) {
				byteArrayOutputStream.write(buf, 0, len);
			}
			//第四步：读取到字节码的二进制数据
			byte data[] = byteArrayOutputStream.toByteArray();
			inputStream.close();
			byteArrayOutputStream.close();
			//第五步：调用父类加载器的defineClass，根据字节码返回字节码对象
			return defineClass(name, data, 0, data.length);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}
	/**
	 * 测试自定义本地类加载器
	 * 输出：create Demo instance!
	 * @param args
	 * @throws ClassNotFoundException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 */
	public static void main(String[] args) throws ClassNotFoundException, InstantiationException, IllegalAccessException {
		MyFileClassLoader myFileClassLoader = new MyFileClassLoader("/home/zh/文档/");
		Class clazz = myFileClassLoader.loadClass("com.zh.urlclassloadertest.Demo");
		clazz.newInstance();
	}
}
```


### 2.5.2 自定义网络类加载器

把上边编译好的类放在apache-tomcat-8.5.40里边，此时类的路径为：`apache-tomcat-8.5.40/webapps/ROOT/com/zh/urlclassloadertest/Demo.class`

然后启动tomcat，并在浏览器访问：`http://localhost:8080/com/zh/urlclassloadertest/Demo.class`，如果发现可以下载此类则说明部署成功。

```java
package com.zh.classloader;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;

public class MyURLClassLoader extends ClassLoader {
	private String url;

	// 默认父类加载器就是系统类加载器AppClassLoader
	public MyURLClassLoader(String url) {
		this.url = url;
	}

	public MyURLClassLoader(String url, ClassLoader parent) {
		super(parent);
		this.url = url;
	}

	@Override
	protected Class<?> findClass(String name) throws ClassNotFoundException {
		// 第一步：把全路径类名转换为网络地址
		String urlPath = url + "/" + name.replace(".", "/") + ".class";
		try {
			// 第二步：构造输入流
			URL url2 = new URL(urlPath);
			InputStream inputStream = url2.openStream();
			//第三步：构造字节输出流
			ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
			byte buf[] = new byte[1024];
			int len = -1;
			while((len = inputStream.read(buf)) != -1) {
				byteArrayOutputStream.write(buf, 0, len);
			}
			//第四步：读取到字节码的二进制数据
			byte data[] = byteArrayOutputStream.toByteArray();
			inputStream.close();
			byteArrayOutputStream.close();
			//第五步：调用父类加载器的defineClass，根据字节码返回字节码对象
			return defineClass(name, data, 0, data.length);
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}
	/**
	 * 测试自定义网络类加载器
	 * 输出：create Demo instance!
	 * @param args
	 * @throws ClassNotFoundException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 */
	public static void main(String[] args) throws ClassNotFoundException, InstantiationException, IllegalAccessException {
		MyURLClassLoader myURLClassLoader = new MyURLClassLoader("http://localhost:8080/");
		Class clazz = myURLClassLoader.loadClass("com.zh.urlclassloadertest.Demo");
		clazz.newInstance();
	}
}
```


### 2.5.3 热部署类加载器

当我们调用loadClass方法加载类时，会采用双亲委派模式，即如果类已经被加载，就从缓存中获取，不会重新加载。如果同一个class被同一个类加载器多次加载，则会报错。因此，我们要实现热部署让同一个class文件被不同的类加载器重复加载即可。但是不能调用loadClass方法，而应该调用findClass方法，避开双亲委托模式，从而实现同一个类被多次加载，实现热部署。

使用自定义类加载器调用loadClass测试双亲委派机制：

```java
package com.zh.classloader;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

public class MyFileClassLoader extends ClassLoader{
	// 就是上边的自定义文件类加载器的代码，这里省略.....
	/**
	 * 使用自定义类加载器测试双亲委派机制
	 * 输出：
	 * 		1829164700
	 *		1829164700
	 * @param args
	 * @throws ClassNotFoundException
	 */
	public static void main(String[] args) throws ClassNotFoundException {
		MyFileClassLoader myFileClassLoader = new MyFileClassLoader("/home/zh/文档/");//父类加载器时AppClassLoader
		MyFileClassLoader myFileClassLoader2 = new MyFileClassLoader("/home/zh/文档/", myFileClassLoader);
		Class clazz = myFileClassLoader.loadClass("com.zh.urlclassloadertest.Demo");
		Class clazz2 = myFileClassLoader2.loadClass("com.zh.urlclassloadertest.Demo");
		System.out.println(clazz.hashCode());
		System.out.println(clazz2.hashCode());
	}
}
```

使用自定义类加载器调用findClass实现一个类重复加载，从而实现热部署：

```java
package com.zh.classloader;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

public class MyFileClassLoader extends ClassLoader{
	// 就是上边的自定义文件类加载器的代码，这里省略.....
	/**
	 * 使用自定义类加载器调用findClass实现一个类重复加载，从而实现热部署
	 * 输出：
	 * 		1311053135
	 *		118352462
	 * @param args
	 * @throws ClassNotFoundException
	 */
	public static void main(String[] args) throws ClassNotFoundException {
		MyFileClassLoader myFileClassLoader = new MyFileClassLoader("/home/zh/文档/");//父类加载器时AppClassLoader
		MyFileClassLoader myFileClassLoader2 = new MyFileClassLoader("/home/zh/文档/", myFileClassLoader);
		Class clazz = myFileClassLoader.findClass("com.zh.urlclassloadertest.Demo");
		Class clazz2 = myFileClassLoader2.findClass("com.zh.urlclassloadertest.Demo");
		System.out.println(clazz.hashCode());
		System.out.println(clazz2.hashCode());
	}
}
```


## 3.6 类的显式与隐式加载

类的加载方式是指虚拟机将class文件加载到内存的方式。

显式加载是指在Java代码中通过调用ClassLoader加载class对象，比如：

- `Class.forName(String name)`：通过传入类的全路径名加载类到虚拟机内存当中；
- 通过`this.getClass().getClassLoader().loadClass()`来加载。


隐式加载指不需要再Java代码中明确调用加载的代码，而是通过虚拟机自动加载到内存中。比如在加载某个class时，该class引用了另外一个类的对象，那么这个对象的字节码文件就会被虚拟机自动加载到内存中。

## 3.7 线程上下文类加载器

在Java中存在着很多的服务提供者接口SPI（Service Provider Interface），是Java提供的一套用来被第三方实现或者扩展的API，这些接口一般由第三方提供实现，常用的SPI由JDBC、JNDI等。这些SPI的接口（比如JDBC中的`java.sql.Driver`）属于核心类库，一般存在`rt.jar`包中，由根类加载器加载。而第三方实现的代码一般作为依赖jar包存放再classpath路径下，由于SPI接口中的代码需要加载具体的第三方实现类并调用其相关方法，SPI的接口类是由根类加载器加载的，Bootstrap类加载器无法直接加载位于classpath下的具体实现类。由于双亲委派模式的存在，Bootstrap类加载器也无法反向委托AppClassLoader加载SPI的具体实现类。在这种情况下，Java提供了线程上下文类加载器用于解决以上问题。

线程上下文加载器可以通过`java.lang.Thread`的`getContextClassLoader()`来获得，或者通过`setContextClassLoader(ClassLoader cl)`来设置线程的上下文类加载器。如果没有手动设置上下文类加载器，线程将继承其父线程的上下文类加载器，初始线程的上下文类加载器是系统类加载器（AppClassLoader)，在线程中运行的代码可以通过此类加载器来加载类或资源。

虽然这种加载类的方式破坏了双亲委托模型，但它使得Java类加载器变得更加灵活。

![contextclassloader.png](https://zhishan-zh.github.io/media/java_base-a708-3f800df19ca1.png)

比如JDBC中有一个类`java.sql.DriverManager`，它是`rt.jar`中的类，用来注册实现了`java.sql.Driver`接口的驱动类，而`java.sql.Driver`的实现位于数据库的驱动jar包中的。

`java.sql.DriverManager`部分源码：

```java
/**
     * Load the initial JDBC drivers by checking the System property
     * jdbc.properties and then use the {@code ServiceLoader} mechanism
     */
static {
    loadInitialDrivers();
    println("JDBC DriverManager initialized");
}
```


```java
private static void loadInitialDrivers() {
    String drivers;
    try {
        drivers = AccessController.doPrivileged(new PrivilegedAction<String>() {
            public String run() {
                return System.getProperty("jdbc.drivers");
            }
        });
    } catch (Exception ex) {
        drivers = null;
    }
    // If the driver is packaged as a Service Provider, load it.
    // Get all the drivers through the classloader
    // exposed as a java.sql.Driver.class service.
    // ServiceLoader.load() replaces the sun.misc.Providers()

    AccessController.doPrivileged(new PrivilegedAction<Void>() {
        public Void run() {

            ServiceLoader<Driver> loadedDrivers = ServiceLoader.load(Driver.class);
            Iterator<Driver> driversIterator = loadedDrivers.iterator();

            /* Load these drivers, so that they can be instantiated.
                 * It may be the case that the driver class may not be there
                 * i.e. there may be a packaged driver with the service class
                 * as implementation of java.sql.Driver but the actual class
                 * may be missing. In that case a java.util.ServiceConfigurationError
                 * will be thrown at runtime by the VM trying to locate
                 * and load the service.
                 *
                 * Adding a try catch block to catch those runtime errors
                 * if driver not available in classpath but it's
                 * packaged as service and that service is there in classpath.
                 */
            try{
                while(driversIterator.hasNext()) {
                    driversIterator.next();
                }
            } catch(Throwable t) {
                // Do nothing
            }
            return null;
        }
    });

    println("DriverManager.initialize: jdbc.drivers = " + drivers);

    if (drivers == null || drivers.equals("")) {
        return;
    }
    String[] driversList = drivers.split(":");
    println("number of Drivers:" + driversList.length);
    for (String aDriver : driversList) {
        try {
            println("DriverManager.Initialize: loading " + aDriver);
            Class.forName(aDriver, true,
                          ClassLoader.getSystemClassLoader());
        } catch (Exception ex) {
            println("DriverManager.Initialize: load failed: " + ex);
        }
    }
}
```

`java.util.ServiceLoader`部分源码：

```java
public static <S> ServiceLoader<S> load(Class<S> service) {
    ClassLoader cl = Thread.currentThread().getContextClassLoader();
    return ServiceLoader.load(service, cl);
}
```

