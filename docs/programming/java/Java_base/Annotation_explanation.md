# 注解解释

# 1 注解的本质

其实单纯说注解，注解本身没有任何的作用。简单说和注释没啥区别，而它起作用的原因是：注解解释类，也就是相关对代码进行解释的特定类。

所有的注解都实现自`java.lang.annotation.Annotation`接口，此接口的声明为：

```java
package java.lang.annotation;

public interface Annotation {
    boolean equals(Object obj);
    int hashCode();
    String toString();
    Class<? extends Annotation> annotationType();
}
```

例如注解`@Override`：

```java
package java.lang;

import java.lang.annotation.*;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.SOURCE)
public @interface Override {
}
```

# 2 使用`@interface`自定义注解

- `@interface`自定义注解自动继承了`java.lang.annotation.Annotation`接口，由编译程序自动完成其他细节。
- 在定义注解时，不能继承其他的注解或接口。
- 注解中每一个方法实际上是声明了一个配置参数，方法的名称就是参数的名称
    - 返回值类型就是参数的类型
    - 返回值类型只能是基本类型、Class、String、enum
    - 可以通过default来声明参数的默认值

# 3 注解的分类

- **Java自带的标准注解**：使用这些注解后编译器就会进行检查。
    - `@Override`：检查该方法是否是重载方法。如果发现其父类，或者是引用的接口中并没有该方法时，会报编译错误。
    - `@Deprecated`：标记过时方法。如果使用该方法，会报编译警告。
    - `@SuppressWarnings`：指示编译器去忽略注解中声明的警告。
- **元注解**：元注解是用于定义注解的注解，包括
    - `@Retention`：注解的生命周期，标明注解被保留的阶段
        - `RetentionPolicy.SOURCE`：当前注解编译期可见，不会写入 class 文件；
        - `RetentionPolicy.CLASS`：类加载阶段丢弃，会写入 class 文件；
        - `RetentionPolicy.RUNTIME`：将在运行期也保留，可以反射获取。
    - `@Target`：注解的作用目标，标明注解使用的范围
        - `ElementType.TYPE`：允许被修饰的注解作用在类、接口和枚举上；
        - `ElementType.FIELD`：允许作用在属性字段上；
        - `ElementType.METHOD`：允许作用在方法上；
        - `ElementType.PARAMETER`：允许作用在方法参数上；
        - `ElementType.CONSTRUCTOR`：允许作用在构造器上；
        - `ElementType.LOCAL_VARIABLE`：允许作用在本地局部变量上；
        - `ElementType.ANNOTATION_TYPE`：允许作用在注解上；
        - `ElementType.PACKAGE`：允许作用在包上。
    - `@Inherited`：是否允许子类继承该注解，标明注解可继承
    - `@Documented`：标明是否生成javadoc文档
- **自定义注解**：可以根据自己的需求定义注解

# 4 解析注解的方式

解析一个类或者方法的注解往往有两种形式：

- **编译期直接的扫描**：
    - 编译器的扫描指的是编译器在对 java 代码编译字节码的过程中会检测到某个类或者方法被一些注解修饰，这时它就会对于这些注解进行某些处理。
    - 这一种情况只适用于那些编译器已经熟知的注解类，比如 JDK 内置的几个注解，而你自定义的注解，编译器是不知道你这个注解的作用的，当然也不知道该如何处理，往往只是会根据该注解的作用范围来选择是否编译进字节码文件，仅此而已。
- **运行期反射**：
    - 注解解释类会使用反射的方式获取被注解的目标
        - `java.lang.Class<T>`实例
        - `java.lang.reflect.Method`实例
        - `java.lang.reflect.Parameter`实例
        - `java.lang.reflect.Field`实例
    - 然后使用被注解的对象调用`java.lang.reflect.AnnotatedElement`的方法`<T extends Annotation> T getAnnotation(Class<T> annotationClass)`获取注解对象（`java.lang.annotation.Annotation`的子类实例）

# 5 自定义注解：通过注解拼装SQL语句

## 5.1 自定义注解

```java
package com.lifeng.annotation.myannotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface Table {
	String value();
}
```

```java
package com.lifeng.annotation.myannotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Column {
	String value();
}
```

## 5.2 实体类

```java
package com.lifeng.annotation.entity;

import com.lifeng.annotation.myannotation.Column;
import com.lifeng.annotation.myannotation.Table;

@Table("user")
public class User {
	@Column("name")
	public String name;
	@Column("sex")
	public String sex;
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getSex() {
		return sex;
	}
	public void setSex(String sex) {
		this.sex = sex;
	}
}
```

## 5.3 注解解析类和测试

```java
package com.lifeng.annotation.myparse;

import java.lang.reflect.Field;
import java.lang.reflect.Method;

import com.lifeng.annotation.entity.User;
import com.lifeng.annotation.myannotation.Column;
import com.lifeng.annotation.myannotation.Table;

public class SQLParse {
	public static String sqlParse(User user) {
		StringBuilder sb = new StringBuilder();
		Class<? extends User> userClazz = user.getClass();
		boolean exist = userClazz.isAnnotationPresent(Table.class);
		if (!exist) {
			return null;
		}
		Table table = userClazz.getAnnotation(Table.class);
		sb.append("select * from ").append(table.value()).append(" where 1=1");
		Field[] fields = userClazz.getDeclaredFields();
		for(Field field:fields) {
			boolean existFieldAnno = field.isAnnotationPresent(Column.class);
			if (!existFieldAnno) {
				continue;
			}
			Column column = field.getAnnotation(Column.class);
			String columnName = column.value();
			String fieldName = field.getName();
			Object fieldValue = null;
			String getMethodName = "get" + fieldName.substring(0, 1).toUpperCase() + fieldName.substring(1);
			try {
				Method method = userClazz.getMethod(getMethodName);
				fieldValue = method.invoke(user);
			} catch (Exception e) {
				e.printStackTrace();
			}
			sb.append(" and ").append(columnName).append("=").append(fieldValue);
		}
		return sb.toString();
	}
	public static void main(String[] args) {
		User user = new User();
		user.setName("zhishan");
		user.setSex("man");
		String sqlString = sqlParse(user);
		System.out.println("sql语句为：" + sqlString);
	}
}
```

输出：

```
sql语句为：select * from user where 1=1 and name=zhishan and sex=man
```



