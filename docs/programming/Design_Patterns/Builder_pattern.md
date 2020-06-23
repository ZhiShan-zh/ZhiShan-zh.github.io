# 建造者模式

# 1 建造者模式概述


## 1.1 定义

将一个复杂对象的创建与它的表示分离，使得同样的构建过程可以创建不同的表示。

创建者模式隐藏了复杂对象的创建过程，它把复杂对象的创建过程加以抽象，通过子类继承或者重载的方式，动态的创建具有复合属性的对象。

## 1.2 应用场景


1. 需要生成的对象具有复杂的内部结构
1. 需要生成的对象内部属性本身相互依赖
1. 与不可变对象配合使用

## 1.3 优点


1. 建造者独立，易扩展。
1. 便于控制细节风险。

## 1.4 源码中的应用


- `org.springframework.web.servlet.mvc.method.RequestMappingInfo`
- `org.springframework.beans.factory.support.BeanDefinitionBuilder`

# 2 入门案例


## 2.1 版本1


```java
package com.zh.builder;

public class BuilderTest {
	public static void main(String[] args) {
		ProductBuilder defaultConcreteProductBuilder = new DefaultConcreteProductBuilder();
		Director director = new Director(defaultConcreteProductBuilder);
		Product product = director.makeProduct("productName", "companyName", "part1", "part2", "part3", "part4");
		System.out.println(product);
	}
}

interface ProductBuilder{
	void builderProductName(String productName);
	void builderCompanyName(String companyName);
	void builderPart1(String part1);
	void builderPart2(String part2);
	void builderPart3(String part3);
	void builderPart4(String part4);
	Product build();
}

class DefaultConcreteProductBuilder implements ProductBuilder{
	private String productName;
	private String companyName;
	private String part1;
	private String part2;
	private String part3;
	private String part4;
	
	@Override
	public void builderProductName(String productName) {
		this.productName = productName;
	}

	@Override
	public void builderCompanyName(String companyName) {
		this.companyName = companyName;
	}

	@Override
	public void builderPart1(String part1) {
		this.part1 = part1;
	}

	@Override
	public void builderPart2(String part2) {
		this.part2 = part2;
	}

	@Override
	public void builderPart3(String part3) {
		this.part3 = part3;
	}

	@Override
	public void builderPart4(String part4) {
		this.part4 = part4;
	}

	@Override
	public Product build() {
		return new Product(productName, companyName, part1, part2, part3, part4);
	}
}

class Director{
	private ProductBuilder builder;
	
	public Director(ProductBuilder builder) {
		this.builder = builder;
	}
	
	public Product makeProduct(String productName, String companyName, String part1, String part2, String part3, String part4) {
		builder.builderProductName(productName);
		builder.builderCompanyName(companyName);
		builder.builderPart1(part1);
		builder.builderPart2(part2);
		builder.builderPart3(part3);
		builder.builderPart4(part4);
		Product product = builder.build();
		return product;
	}
}

class Product{
	private String productName;
	private String companyName;
	private String part1;
	private String part2;
	private String part3;
	private String part4;
	
	public Product() {}

	public Product(String productName, String companyName, String part1, String part2, String part3, String part4) {
		super();
		this.productName = productName;
		this.companyName = companyName;
		this.part1 = part1;
		this.part2 = part2;
		this.part3 = part3;
		this.part4 = part4;
	}

	public String getCompanyName() {
		return companyName;
	}

	public void setCompanyName(String companyName) {
		this.companyName = companyName;
	}

	public String getPart1() {
		return part1;
	}

	public void setPart1(String part1) {
		this.part1 = part1;
	}

	public String getPart2() {
		return part2;
	}

	public void setPart2(String part2) {
		this.part2 = part2;
	}

	public String getPart3() {
		return part3;
	}

	public void setPart3(String part3) {
		this.part3 = part3;
	}

	public String getPart4() {
		return part4;
	}

	public void setPart4(String part4) {
		this.part4 = part4;
	}

	public String getProductName() {
		return productName;
	}

	public void setProductName(String productName) {
		this.productName = productName;
	}

	@Override
	public String toString() {
		return "Product [productName=" + productName + ", companyName=" + companyName + ", part1=" + part1 + ", part2="
				+ part2 + ", part3=" + part3 + ", part4=" + part4 + "]";
	}
	
	
}
```


## 2.2 版本2


```java
package com.zh.builder.v2;

public class BuilderTest2 {
	public static void main(String[] args) {
		Product product = new Product.Builder().productName("productName").companyName("companyName").part1("part1").part2("part2").part3("part3").part4("part4").build();
		System.out.println(product);
	}
}

class Product{
	private final String productName;
	private final String companyName;
	private final String part1;
	private final String part2;
	private final String part3;
	private final String part4;

	public Product(String productName, String companyName, String part1, String part2, String part3, String part4) {
		super();
		this.productName = productName;
		this.companyName = companyName;
		this.part1 = part1;
		this.part2 = part2;
		this.part3 = part3;
		this.part4 = part4;
	}

	static class Builder{
		private String productName;
		private String companyName;
		private String part1;
		private String part2;
		private String part3;
		private String part4;
		
		public Builder productName(String productName) {
			this.productName = productName;
			return this;
		}
		
		public Builder companyName(String companyName) {
			this.companyName = companyName;
			return this;
		}
		
		public Builder part1(String part1) {
			this.part1 = part1;
			return this;
		}
		
		public Builder part2(String part2) {
			this.part2 = part2;
			return this;
		}
		
		public Builder part3(String part3) {
			this.part3 = part3;
			return this;
		}
		
		public Builder part4(String part4) {
			this.part4 = part4;
			return this;
		}
		
		public Product build() {
			return new Product(this.productName, this.companyName, this.part1, this.part2, this.part3, this.part4);
		}
	}
	
	@Override
	public String toString() {
		return "Product [productName=" + productName + ", companyName=" + companyName + ", part1=" + part1 + ", part2="
				+ part2 + ", part3=" + part3 + ", part4=" + part4 + "]";
	}
}
```
