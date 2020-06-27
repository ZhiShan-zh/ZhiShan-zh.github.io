# 网络编程基础

# 1 基本概念
## 1.1 Socket套接字
Socket又称“套接字”，应用程序通常通过“套接字”向网络发出请求或者应答网络请求。


Socket和ServerSocket类库位于 `java.net` 包中。ServerSocket用于服务器端，Socket是建立网络连接时使用的。在连接成功时，应用程序两端都会产生一个Socket实例，操作这个实例，完成所需的会话。对于一个网络连接来说，套接字是平等的，不因为在服务器端或在客户端而产生不同级别。不管是Socket还是ServerSocket它们工作都是通过SocketImpl类及其子类完成的。


套接字之间的连接过程可以分为四个步骤：

1. **服务器监听**：服务器端套接字并不定位具体的客户端套接字，而是处于等待连接的状态，实时监控网络状态。
1. **客户端请求服务器**：指由客户端的套接字提出连接请求，要连接的目标是服务器端的套接字。为此，客户端的套接字必须首先描述它要连接的服务器的套接字，指出服务器端套接字的地址和端口号，然后就向服务器端套接字提出连接请求。
1. **服务器确认**：服务端套接字监听到或者说接受到客户端套接字的连接请求，它就响应客户端套接字的请求，建立一个新的线程，把服务端套接字的描述发给客户端。
1. **客户端确认**：一旦客户端确认了此描述，连接就建立好了。双方开始进行通信。而服务端套接字继续处于监听状态，继续接收其他客户端套接字的连接请求。
1. **进行通信。**



## 1.2 IO&NIO
IO（BIO）和NIO的区别：其本质就是阻塞和非阻塞的区别。

- **阻塞**：应用程序在获取网络数据的时候，如果网络传输数据很慢，那么程序就一直等着，直到传输完毕为止。
- **非阻塞**：应用程序直接可以获取已经准备就绪的数据，无须等待。
- BIO为同步阻塞形式，NIO为同步非阻塞形式。NIO并没有实现异步，在JDK1.7之后，升级了NIO库包，支持异步非阻塞通信模型NIO2.0（AIO）。



同步和异步：同步和异步一般是面向操作系统与应用程序对IO操作的层面上来区别的。

- **同步**时，应用程序会直接参与IO读写操作，并且我们的应用程序会直接阻塞到某一个方法上，直到数据准备就绪；或者采用轮询的策略实时检查数据的就绪状态，如果就绪则获取数据。
- **异步**时，则所有的IO读写操作交给操作系统处理，与我们的应用程序没有直接关系，我们程序不需要关心IO读写，当操作系统完成了IO读写操作时，会给我们应用程序发送通知，我们的应用程序直接拿走数据即可。



同步说的是你的server服务器端的执行方式。
阻塞说的是具体的技术，接收数据的方式、状态（IO、NIO）。


# 2 传统的BIO编程
网络编程的基本模型是Client/Server模型，也就是两个进程直接进行相互通信，其中服务端提供配置信息（绑定的IP地址和监听端口），客户端通过连接操作向服务端监听的地址发起连接请求，通过三次握手建立连接，如果连接成功，则双方即可进行通信（网络套接字socket）。
![image.png](https://zhishan-zh.github.io/media/1587634826057-b94849d8-eddf-408f-a92c-721434843e06.png)


```java
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
	final static int PROT = 8765;	
	public static void main(String[] args) {		
		ServerSocket server = null;
		try {
			server = new ServerSocket(PROT);
			System.out.println(" server start .. ");
			//进行阻塞
			Socket socket = server.accept();
			//新建一个线程执行客户端的任务
			new Thread(new ServerHandler(socket)).start();
			
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if(server != null){
				try {
					server.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			server = null;
		}		
	}	
}
```


```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class ServerHandler implements Runnable{
	private Socket socket ;	
	public ServerHandler(Socket socket){
		this.socket = socket;
	}
	
	@Override
	public void run() {
		BufferedReader in = null;
		PrintWriter out = null;
		try {
			in = new BufferedReader(new InputStreamReader(this.socket.getInputStream()));
			out = new PrintWriter(this.socket.getOutputStream(), true);
			String body = null;
			while(true){
				body = in.readLine();
				if(body == null) break;
				System.out.println("Server :" + body);
				out.println("服务器端回送响的应数据.");
			}
			
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if(in != null){
				try {
					in.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			if(out != null){
				try {
					out.close();
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
			if(socket != null){
				try {
					socket.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			socket = null;
		}				
	}
}
```


```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Client {

	final static String ADDRESS = "127.0.0.1";
	final static int PORT = 8765;
	
	public static void main(String[] args) {
		
		Socket socket = null;
		BufferedReader in = null;
		PrintWriter out = null;
		
		try {
			socket = new Socket(ADDRESS, PORT);
			in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			out = new PrintWriter(socket.getOutputStream(), true);
			
			//向服务器端发送数据
			out.println("接收到客户端的请求数据...");
			String response = in.readLine();
			System.out.println("Client: " + response);
			
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if(in != null){
				try {
					in.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			if(out != null){
				try {
					out.close();
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
			if(socket != null){
				try {
					socket.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			socket = null;
		}
	}
}
```


# 3 伪异步IO
采用线程池和任务队列可以实现一种伪异步的IO通信框。
将客户端的socket封装成一个task任务（实现runnable接口的类）然后投递到线程池中去，配置相应的队列进行实现。
![image.png](https://zhishan-zh.github.io/media/1587689200567-43cb98e2-ed8c-440e-8e8d-a04af87cff1a.png)


```java
import java.io.BufferedReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
	final static int PORT = 8765;

	public static void main(String[] args) {
		ServerSocket server = null;
		BufferedReader in = null;
		PrintWriter out = null;
		try {
			server = new ServerSocket(PORT);
			System.out.println("server start");
			Socket socket = null;
			HandlerExecutorPool executorPool = new HandlerExecutorPool(50, 1000);
			while(true){
				socket = server.accept();
				executorPool.execute(new ServerHandler(socket));
			}
			
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if(in != null){
				try {
					in.close();
				} catch (Exception e1) {
					e1.printStackTrace();
				}
			}
			if(out != null){
				try {
					out.close();
				} catch (Exception e2) {
					e2.printStackTrace();
				}
			}
			if(server != null){
				try {
					server.close();
				} catch (Exception e3) {
					e3.printStackTrace();
				}
			}
			server = null;				
		}	
	}	
}
```


```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class HandlerExecutorPool {

	private ExecutorService executor;
	public HandlerExecutorPool(int maxPoolSize, int queueSize){
		this.executor = new ThreadPoolExecutor(
				Runtime.getRuntime().availableProcessors(),
				maxPoolSize, 
				120L, 
				TimeUnit.SECONDS,
				new ArrayBlockingQueue<Runnable>(queueSize));
	}
	
	public void execute(Runnable task){
		this.executor.execute(task);
	}	
}
```
# 4 NIO
有的人叫NIO伪new IO，有的人把NIO叫做Non-block IO，这里我们还是习惯说后者，即非阻塞IO。
NIO有几个比较关键的概念，即为Buffer（缓冲区）、Channel（管道、通道）、Selector（连接器、多路复用器）
**NIO的本质就是避免原始的TCP建立连接使用3次握手的操作，减少连接的开销。**


![image.png](https://zhishan-zh.github.io/media/1583374336201-2e239a0e-7fdd-4f47-9786-c44c5e14c7c3.png)


## 4.1 Buffer
Buffer是一个对象，它包含一些要写入或者要读取的数据。在NIO类库中加入Buffer对象，体现了新库与原IO的一个重要的区别。在面向流的IO中，可以将数据直接写入或读取到Stream对象中。**在NIO库中，所有数据都是用缓冲区处理的（读写）**。缓冲区实质上是一个数组，通常它是一个字节数组（ByteBuffer），也可以使用其他类型的数组。这个数组为缓冲区提供了数据访问读写等操作属性，如位置、容量、上限等概念，参考api文档。
Buffer类型：我们最常用的就是ByteBuffer，实际上每一种java基本类型都对于了一种缓存区（除了Boolean类型）：

- ByteBuffer
- CharBuffer
- ShortBuffer
- IntBuffer
- LongBuffer
- FloatBuffer
- DoubleBuffer
### 4.1.1 flip()复位方法使用
```java
//创建指定长度的缓冲区
IntBuffer buf = IntBuffer.allocate(10);
buf.put(13);// position位置：0 - > 1
buf.put(21);// position位置：1 - > 2
buf.put(35);// position位置：2 - > 3

System.out.println("没有复位：" + buf);
//容量一旦初始化后不允许改变（warp方法包裹数组除外）
System.out.println("容量为: " + buf.capacity());
//由于只装载了三个元素,所以可读取或者操作的元素为3 则limit=3
System.out.println("限制为: " + buf.limit());		
```
输出：

```
没有复位：java.nio.HeapIntBuffer[pos=3 lim=10 cap=10]
容量为： 10
限制为： 10
```



```java
//创建指定长度的缓冲区
IntBuffer buf = IntBuffer.allocate(10);
buf.put(13);// position位置：0 - > 1
buf.put(21);// position位置：1 - > 2
buf.put(35);// position位置：2 - > 3
//把位置复位为0，也就是position位置：3 - > 0
buf.flip();
System.out.println("使用flip复位：" + buf);
//容量一旦初始化后不允许改变（warp方法包裹数组除外）
System.out.println("容量为: " + buf.capacity());
//由于只装载了三个元素,所以可读取或者操作的元素为3 则limit=3
System.out.println("限制为: " + buf.limit());		
```
输出：

```
使用flip复位：java.nio.HeapIntBuffer[pos=0 lim=10 cap=10]
容量为： 10
限制为： 10
```



```java
//创建指定长度的缓冲区
IntBuffer buf = IntBuffer.allocate(10);
buf.put(13);// position位置：0 - > 1
buf.put(21);// position位置：1 - > 2
buf.put(35);// position位置：2 - > 3
//把位置复位为0，也就是position位置：3 - > 0
//buf.flip();
System.out.println("没有复位：" + buf);
//容量一旦初始化后不允许改变（warp方法包裹数组除外）
System.out.println("容量为: " + buf.capacity());
//由于只装载了三个元素,所以可读取或者操作的元素为3 则limit=3
System.out.println("限制为: " + buf.limit());	

System.out.println("获取下标为1的元素：" + buf.get(1));
System.out.println("get(index)方法，position位置不改变：" + buf);
buf.put(1, 4);
System.out.println("put(index, change)方法，position位置不变：" + buf);;

for (int i = 0; i < buf.limit(); i++) {
    //调用get方法会使其缓冲区位置（position）向后递增一位
    System.out.print(buf.get() + "\t");
}
System.out.println("buf对象遍历之后为: " + buf);
```
输出：

```
没有复位：java.nio.HeapIntBuffer[pos=3 lim=10 cap=10]
容量为: 10
限制为: 10
获取下标为1的元素：21
get(index)方法，position位置不改变：java.nio.HeapIntBuffer[pos=3 lim=10 cap=10]
put(index, change)方法，position位置不变：java.nio.HeapIntBuffer[pos=3 lim=10 cap=10]
0       0       0       0       0       0       0       Exception in thread "main" java.nio.BufferUnderflowException
       at java.nio.Buffer.nextGetIndex(Buffer.java:500)
       at java.nio.HeapIntBuffer.get(HeapIntBuffer.java:135)
       at bhz.nio.test.TestBuffer.main(TestBuffer.java:30)
```



```java
//创建指定长度的缓冲区
IntBuffer buf = IntBuffer.allocate(10);
buf.put(13);// position位置：0 - > 1
buf.put(21);// position位置：1 - > 2
buf.put(35);// position位置：2 - > 3
//把位置复位为0，也就是position位置：3 - > 0
buf.flip();
System.out.println("使用flip复位：" + buf);
//容量一旦初始化后不允许改变（warp方法包裹数组除外）
System.out.println("容量为: " + buf.capacity());
//由于只装载了三个元素,所以可读取或者操作的元素为3 则limit=3
System.out.println("限制为: " + buf.limit());	

System.out.println("获取下标为1的元素：" + buf.get(1));
System.out.println("get(index)方法，position位置不改变：" + buf);
buf.put(1, 4);
System.out.println("put(index, change)方法，position位置不变：" + buf);;

for (int i = 0; i < buf.limit(); i++) {
    //调用get方法会使其缓冲区位置（position）向后递增一位
    System.out.print(buf.get() + "\t");
}
System.out.println("buf对象遍历之后为: " + buf);
```
输出：

```
使用flip复位：java.nio.HeapIntBuffer[pos=0 lim=3 cap=10]
容量为: 10
限制为: 3
获取下标为1的元素：21
get(index)方法，position位置不改变：java.nio.HeapIntBuffer[pos=0 lim=3 cap=10]
put(index, change)方法，position位置不变：java.nio.HeapIntBuffer[pos=0 lim=3 cap=10]
13      4       35      buf对象遍历之后为: java.nio.HeapIntBuffer[pos=3 lim=3 cap=10]
```



**flip()源码：**
```java
/**
     * Flips this buffer.  The limit is set to the current position and then
     * the position is set to zero.  If the mark is defined then it is
     * discarded.
     *
     * <p> After a sequence of channel-read or <i>put</i> operations, invoke
     * this method to prepare for a sequence of channel-write or relative
     * <i>get</i> operations.  For example:
     *
     * <blockquote><pre>
     * buf.put(magic);    // Prepend header
     * in.read(buf);      // Read data into rest of buffer
     * buf.flip();        // Flip buffer
     * out.write(buf);    // Write header + data to channel</pre></blockquote>
     *
     * <p> This method is often used in conjunction with the {@link
     * java.nio.ByteBuffer#compact compact} method when transferring data from
     * one place to another.  </p>
     *
     * @return  This buffer
     * this method to prepare for a sequence of channel-write or relative
     * <i>get</i> operations.  For example:
     *
     * <blockquote><pre>
     * buf.put(magic);    // Prepend header
     * in.read(buf);      // Read data into rest of buffer
     * buf.flip();        // Flip buffer
     * out.write(buf);    // Write header + data to channel</pre></blockquote>
     *
     * <p> This method is often used in conjunction with the {@link
     * java.nio.ByteBuffer#compact compact} method when transferring data from
     * one place to another.  </p>
     *
     * @return  This buffer
     */
public final Buffer flip() {
    limit = position;
    position = 0;
    mark = -1;
    return this;
}
```


### 4.1.2 wrap方法使用
```java
//  wrap方法会包裹一个数组: 一般这种用法不会先初始化缓存对象的长度，因为没有意义，
//  最后还会被wrap所包裹的数组覆盖掉。 
//  并且wrap方法修改缓冲区对象的时候，数组本身也会跟着发生变化。                     
int[] arr = new int[]{1,2,5};
IntBuffer buf1 = IntBuffer.wrap(arr);
System.out.println(buf1);

IntBuffer buf2 = IntBuffer.wrap(arr, 0 , 2);
//这样使用表示容量为数组arr的长度，但是可操作的元素只有实际进入缓存区的元素长度
System.out.println(buf2);
```
输出：

```
java.nio.HeapIntBuffer[pos=0 lim=3 cap=3]
java.nio.HeapIntBuffer[pos=0 lim=2 cap=3]
```




**wrap()源码：**
```java
    /**
     * Wraps an int array into a buffer.
     *
     * <p> The new buffer will be backed by the given int array;
     * that is, modifications to the buffer will cause the array to be modified
     * and vice versa.  The new buffer's capacity will be
     * <tt>array.length</tt>, its position will be <tt>offset</tt>, its limit
     * will be <tt>offset + length</tt>, and its mark will be undefined.  Its
     * {@link #array backing array} will be the given array, and
     * its {@link #arrayOffset array offset} will be zero.  </p>
     *
     * @param  array
     *         The array that will back the new buffer
     *
     * @param  offset
     *         The offset of the subarray to be used; must be non-negative and
     *         no larger than <tt>array.length</tt>.  The new buffer's position
     *         will be set to this value.
     *
     * @param  length
     *         The length of the subarray to be used;
     *         must be non-negative and no larger than
     *         <tt>array.length - offset</tt>.
     *         The new buffer's limit will be set to <tt>offset + length</tt>.
     *
     * @return  The new int buffer
     *
     * @throws  IndexOutOfBoundsException
     *          If the preconditions on the <tt>offset</tt> and <tt>length</tt>
     *          parameters do not hold
     */
    public static IntBuffer wrap(int[] array,
                                    int offset, int length)
    {
        try {
            return new HeapIntBuffer(array, offset, length);
        } catch (IllegalArgumentException x) {
            throw new IndexOutOfBoundsException();
        }
    }
```


### 4.1.3 其他方法


```java
IntBuffer buf1 = IntBuffer.allocate(10);
int[] arr = new int[]{1,2,5};
buf1.put(arr);
System.out.println(buf1);
//一种复制方法
IntBuffer buf3 = buf1.duplicate();
System.out.println(buf3);

//设置buf1的位置属性
//buf1.position(0);
buf1.flip();
System.out.println(buf1);

System.out.println("可读数据为：" + buf1.remaining());

int[] arr2 = new int[buf1.remaining()];
//将缓冲区数据放入arr2数组中去
buf1.get(arr2);
for(int i : arr2){
    System.out.print(Integer.toString(i) + ",");
}
```
输出：

```
java.nio.HeapIntBuffer[pos=3 lim=10 cap=10]
java.nio.HeapIntBuffer[pos=3 lim=10 cap=10]
java.nio.HeapIntBuffer[pos=0 lim=3 cap=10]
可读数据为：3
1,2,5,
```




## 4.2 Channel
通道（Channel），它就像自来水管道一样，网络数据通过Channel读取和写入，通道与流不同之处在于**通道是双向的**，而流只是一个方向上移动（一个流必须是InputStream或者OutputStream的子类），而通道可以用于读、写或者二者同时进行，最关键的是可以与多路复用器结合起来，有多种状态位，方便多路复用器去识别。
事实上通道分为两大类，一类是网络读写的（SelectableChannel），一类是用于文件操作的（FileChannel），我们使用的SocketChannel和ServerSocketChannel都是SelectableChannel的子类。


## 4.3 Selector
多路复用器（Selector），他是NIO编程的基础，非常重要。多路复用器提供选择已经就绪的任务的能力。


简单说，就是Selector会不断地轮询注册在其上的通道（Channel），如果某个通道发生了读写操作，这个通道就处于就绪状态，会被Selector轮询出来，然后通过SelectionKey可以取得就绪的Channel集合，从而进行后续的IO操作。


一个多路复用器（Selector）可以负责成千上万Channel通道，没有上限，这也是JDK使用了epoll代替了传统的select实现，获得连接句柄没有限制。这也就意味着我们只要一个线程负责Selector的轮询，就可以接入成千上万个客户端，这是JDK NIO库的巨大进步。


Selector线程就类似一个管理者（Master），管理了成千上万个管道，然后轮询哪个管道的数据已经准备好，通知cpu执行IO的读取或写入操作。


Selector模式：当IO事件（管道）注册到选择器以后，selector会分配给每个管道一个key值，相当于标签。selector选择器是以轮询的方式进行查找注册的所有IO事件（管道），当我们的IO时间（管道）准备就绪后，select就会识别，会通过key值来找到相应的管道，进行相关的数据处理操作（从管道里读或写操作，写到我们的数据缓冲区中）。


每个管道都会对选择器进行注册不同的事件状态，以便选择器查找。

- `SelectionKey.OP_CONNECT` 
- `SelectionKey.OP_ACCEPT` 
- `SelectionKey.OP_READ` 
- `SelectionKey.OP_WRITE` 



## 4.4 NIO简单实例
使用单纯的NIO会非常麻烦，但可以用netty。


```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

public class Server implements Runnable{
	//1 多路复用器（管理所有的通道）
	private Selector selector;
	//2 建立缓冲区
	private ByteBuffer readBuf = ByteBuffer.allocate(1024);
	//3 
	private ByteBuffer writeBuf = ByteBuffer.allocate(1024);
	public Server(int port){
		try {
			//1 打开路复用器
			this.selector = Selector.open();
			//2 打开服务器通道
			ServerSocketChannel ssc = ServerSocketChannel.open();
			//3 设置服务器通道为非阻塞模式
			ssc.configureBlocking(false);
			//4 绑定地址
			ssc.bind(new InetSocketAddress(port));
			//5 把服务器通道注册到多路复用器上，并且监听阻塞事件
			ssc.register(this.selector, SelectionKey.OP_ACCEPT);
			
			System.out.println("Server start, port :" + port);
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@Override
	public void run() {
		while(true){
			try {
				//1 必须要让多路复用器开始监听
				this.seletor.selector();
				//2 返回多路复用器已经选择的结果集
				Iterator<SelectionKey> keys = this.selector.selectedKeys().iterator();
				//3 进行遍历
				while(keys.hasNext()){
					//4 获取一个选择的元素
					SelectionKey key = keys.next();
					//5 直接从容器中移除就可以了
					keys.remove();
					//6 如果是有效的
					if(key.isValid()){
						//7 如果为阻塞状态
						if(key.isAcceptable()){
							this.accept(key);
						}
						//8 如果为可读状态
						if(key.isReadable()){
							this.read(key);
						}
						//9 写数据
						if(key.isWritable()){
							//this.write(key); //ssc
						}
					}
					
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	private void write(SelectionKey key){
		//ServerSocketChannel ssc =  (ServerSocketChannel) key.channel();
		//ssc.register(this.seletor, SelectionKey.OP_WRITE);
	}

	private void read(SelectionKey key) {
		try {
			//1 清空缓冲区旧的数据
			this.readBuf.clear();
			//2 获取之前注册的socket通道对象
			SocketChannel sc = (SocketChannel) key.channel();
			//3 读取数据
			int count = sc.read(this.readBuf);
			//4 如果没有数据
			if(count == -1){
				key.channel().close();
				key.cancel();
				return;
			}
			//5 有数据则进行读取 读取之前需要进行复位方法(把position 和limit进行复位)
			this.readBuf.flip();
			//6 根据缓冲区的数据长度创建相应大小的byte数组，接收缓冲区的数据
			byte[] bytes = new byte[this.readBuf.remaining()];
			//7 接收缓冲区数据
			this.readBuf.get(bytes);
			//8 打印结果
			String body = new String(bytes).trim();
			System.out.println("Server : " + body);
			
			// 9..可以写回给客户端数据 
			
		} catch (IOException e) {
			e.printStackTrace();
		}		
	}

	private void accept(SelectionKey key) {
		try {
			//1 获取服务通道
			ServerSocketChannel ssc =  (ServerSocketChannel) key.channel();
			//2 执行阻塞方法
			SocketChannel sc = ssc.accept();
			//3 设置阻塞模式
			sc.configureBlocking(false);
			//4 注册到多路复用器上，并设置读取标识
			sc.register(this.selector, SelectionKey.OP_READ);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {		
		new Thread(new Server(8765)).start();;
	}	
}
```


```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;

public class Client {
	//需要一个Selector 
	public static void main(String[] args) {
		
		//创建连接的地址
		InetSocketAddress address = new InetSocketAddress("127.0.0.1", 8765);
		
		//声明连接通道
		SocketChannel sc = null;
		
		//建立缓冲区
		ByteBuffer buf = ByteBuffer.allocate(1024);
		
		try {
			//打开通道
			sc = SocketChannel.open();
			//进行连接
			sc.connect(address);
			
			while(true){
				//定义一个字节数组，然后使用系统录入功能：
				byte[] bytes = new byte[1024];
				System.in.read(bytes);
				
				//把数据放到缓冲区中
				buf.put(bytes);
				//对缓冲区进行复位
				buf.flip();
				//写出数据
				sc.write(buf);
				//清空缓冲区数据
				buf.clear();
			}
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if(sc != null){
				try {
					sc.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}		
	}	
}
```


# AIO
AIO编程，在NIO基础之上引入了异步通道的概念，并提供了异步文件和异步套接字通道的实现，从而在真正意义上实现了异步非阻塞，之前的NIO只是非阻塞并非异步。而AIO不需要通过多路复用器对注册的通道进行轮询操作即可实现异步读写，从而简化了NIO编程模型。也可以称之为NIO2.0，这种模式才真正的属于异步非阻塞的模型。
AsychronousServerSocketChannel
AsychronousSocketChannel


```java
import java.net.InetSocketAddress;
import java.nio.channels.AsynchronousChannelGroup;
import java.nio.channels.AsynchronousServerSocketChannel;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Server {
	//线程池
	private ExecutorService executorService;
	//线程组
	private AsynchronousChannelGroup threadGroup;
	//服务器通道
	public AsynchronousServerSocketChannel assc;
	
	public Server(int port){
		try {
			//创建一个缓存池
			executorService = Executors.newCachedThreadPool();
			//创建线程组
			threadGroup = AsynchronousChannelGroup.withCachedThreadPool(executorService, 1);
			//创建服务器通道
			assc = AsynchronousServerSocketChannel.open(threadGroup);
			//进行绑定
			assc.bind(new InetSocketAddress(port));
			
			System.out.println("server start , port : " + port);
			//进行阻塞
			assc.accept(this, new ServerCompletionHandler());
			//一直阻塞 不让服务器停止
			Thread.sleep(Integer.MAX_VALUE);
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		Server server = new Server(8765);
	}
	
}
```


```java
import java.nio.ByteBuffer;
import java.nio.channels.AsynchronousSocketChannel;
import java.nio.channels.CompletionHandler;
import java.util.concurrent.ExecutionException;

public class ServerCompletionHandler implements CompletionHandler<AsynchronousSocketChannel, Server> {

	@Override
	public void completed(AsynchronousSocketChannel asc, Server attachment) {
		//当有下一个客户端接入的时候 直接调用Server的accept方法，这样反复执行下去，保证多个客户端都可以阻塞
		attachment.assc.accept(attachment, this);
		read(asc);
	}

	private void read(final AsynchronousSocketChannel asc) {
		//读取数据
		ByteBuffer buf = ByteBuffer.allocate(1024);
		asc.read(buf, buf, new CompletionHandler<Integer, ByteBuffer>() {
			@Override
			public void completed(Integer resultSize, ByteBuffer attachment) {
				//进行读取之后,重置标识位
				attachment.flip();
				//获得读取的字节数
				System.out.println("Server -> " + "收到客户端的数据长度为:" + resultSize);
				//获取读取的数据
				String resultData = new String(attachment.array()).trim();
				System.out.println("Server -> " + "收到客户端的数据信息为:" + resultData);
				String response = "服务器响应, 收到了客户端发来的数据: " + resultData;
				write(asc, response);
			}
			@Override
			public void failed(Throwable exc, ByteBuffer attachment) {
				exc.printStackTrace();
			}
		});
	}
	
	private void write(AsynchronousSocketChannel asc, String response) {
		try {
			ByteBuffer buf = ByteBuffer.allocate(1024);
			buf.put(response.getBytes());
			buf.flip();
			asc.write(buf).get();
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		}
	}
	
	@Override
	public void failed(Throwable exc, Server attachment) {
		exc.printStackTrace();
	}

}
```


```java
import java.io.UnsupportedEncodingException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.AsynchronousSocketChannel;
import java.util.concurrent.ExecutionException;

public class Client implements Runnable{

	private AsynchronousSocketChannel asc ;
	
	public Client() throws Exception {
		asc = AsynchronousSocketChannel.open();
	}
	
	public void connect(){
		asc.connect(new InetSocketAddress("127.0.0.1", 8765));
	}
	
	public void write(String request){
		try {
			asc.write(ByteBuffer.wrap(request.getBytes())).get();
			read();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private void read() {
		ByteBuffer buf = ByteBuffer.allocate(1024);
		try {
			asc.read(buf).get();
			buf.flip();
			byte[] respByte = new byte[buf.remaining()];
			buf.get(respByte);
			System.out.println(new String(respByte,"utf-8").trim());
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
	}
	
	@Override
	public void run() {
		while(true){
			
		}
	}
	
	public static void main(String[] args) throws Exception {
		Client c1 = new Client();
		c1.connect();
		
		Client c2 = new Client();
		c2.connect();
		
		Client c3 = new Client();
		c3.connect();
		
		new Thread(c1, "c1").start();
		new Thread(c2, "c2").start();
		new Thread(c3, "c3").start();
		
		Thread.sleep(1000);
		
		c1.write("c1 aaa");
		c2.write("c2 bbbb");
		c3.write("c3 ccccc");
	}
	
}
```












































