# 层次架构设计

# 1 体系结构设计

软件体系结构可定义为：软件体系结构为软件系统提供了结构、行为和属性的高级抽象，由构成系统的元素描述、这些元素的相互作用、知道元素集成的模式以及这些模式的约束组成。

软件体系结构不仅指定了系统的组织结构和拓扑结构，并且显示了系统需求和构成系统的元素之间的对应关系，提供了一些设计决策的基本原理，是构建于软件系统之上的系统级复用。

分层设计是一种最常见的架构设计方法，能有效地使设计简化，使设计的系统机构清晰，便于提高复用能力和产品维护能力。



# 2 表现层框架设计

## 2.1 使用MVC模式设计表现层

随着J2EE（Java 2Enterprise Edition）的成熟，MVC成为了J2EE平台上推荐的一种设计模式。

MVC强制性地把一个应用的输入、处理、输出流程按照视图、控制、模型的方式进行分离，形成了控制器、模型、视图三个核心模块：

- 控制器（Controller）：接受用户的输入并调用模型和视图去完成用户的需求。该部分是用户界面与Model的接口。
  - 一方面它解释来自于视图的输入，将其解释成为系统能够理解的对象，同时它也识别用户动作，并将其解释为对模型特定方法的调用；
  - 另一方面，它处理来自于模型的事件和模型逻辑执行的结果，调用适当的视图为用户提供反馈。
- 模型（Model）：应用程序的主体部分。模型表示业务数据和业务逻辑。
  - 一个模型能为多个视图提供数据。也因此提高了应用的可重用性。
- 视图（View）：用户看到并与之交互的界面。
  - 视图向用户显示相关的数据，并能接收用户输入的数据，但是它并不进行任何实际的业务处理。
  - 视图可以向模型查询业务状态，但不能改变模型。
  - 视图还能接受模型发出的数据更新事件，从而对用户界面进行同步更新。

MVC处理流程：

- 首先，控制器接受用户的请求，并决定应该调用哪个模型来处理；
- 然后，模型根据用户请求进行相关的业务逻辑处理，并返回数据；
- 最后，控制器调用相应的视图来格式化模型返回的数据，并通过视图呈现给用户。



使用MVC模式来设计表现层的优点如下：

- 允许多个用户界面的扩展。
  - 在MVC模式中，视图与模型没有必然的联系，都是通过控制器发生关系的，这样如果要增加新类型的用户界面，只需要改动相应的视图和控制器即可，而模型则无需发生改动。
- 易于维护。
  - 控制器和视图可以随着模型的扩展而进行相应的扩展，只要保持一种公共的接口，控制器和视图的旧版本也可以继续使用。
- 功能强大的用户界面。
  - 用户界面与模型方法调用组合起来，使程序的使用更清晰，可将友好的界面发布给用户。

## 2.2 使用XML设计表现层，统一Web Form与Windows Form的外观

XML和HTML：

- XML（可扩展标记语言）与HTML类似，是一种标记语言。
- HTML主要用于控制数据的显示和外观；XML用于定义数据本身的结构和数据类型。XML已被公认是优秀的数据描述语言。

Web应用程序（对特定浏览器的局限以及性能问题），基于窗体表现形式的胖客户端应用程序，两种应用程序各有优势，在未来很长一段时间这两种架构都会并存。许多开发厂商在开发新产品时提出了既要支持胖客户端的表现形式，又要支持Web的表现形式。有人提出将GUI用一个标准的形式描述，对于不同的表现形式，提供特定形式的转换器，根据GUI的描述转换成相应的表现形式。这就要求描述语言有非常好的通用性和扩展性，XML恰恰是这种描述语言理想的载体。

对于大多数应用系统，GUI主要是由GUI控件组成。控件可以看成是一个数据对象，其包含位置信息、类型和绑定的事件等。这些信息在XML中都可以作为数据结点保存下来，每一个控件都可以被描述成一个XML结点，而控件的那些相关属性都可以描述成这个XML结点的Attribute。由于XML本身就是一种树形结构描述语言，所以可以很好地支持控件之间的层次结构。同时，XML标记由架构或文档的作者定义，并且是无限制的，所以架构开发人员可以随意约定控件的属性，例如可以约定type=“button”是一个按钮，type=“panel”是一个控件容器，type=“Constraint”是位置等。这样，整个GUI就可以完整而且简单地通过XML来描述。例如：

```xml
<componet type="panel" constraint="16,22,78,200"/>
<componet type="button" isvisible="false" constraint="17,222,78,20"/></componet>
```

对于特定的表现技术，实现不同的解析器解析XML配置文件。根据XML中的标签，按照特有的表现机会实例化的GUI控件实例对象。

从设计模式的角度来说，整个XML表现层解析的机制是一种策略模式。在调用显示GUI时，不是直接的调用特定的表现层的API，而是装载GUI对应的XML配置文件，然后根据特定的表现技术的解析器解析XML，得到GUI视图实例对象。这样，对于GUI开发人员来说，GUI视图只需要维护一套XML文件即可。

## 2.3 表现层中UIP设计思想

UIP（User Interface Porcess Application Block）：

- 是微软社区开发的众多Application Block中的其中之一，它是开源的。
- UIP提供了一个扩展框架，用于简化用户界面与商业逻辑代码的分离的方法，可以用它来写复杂的用户界面导航和工作流处理，并且它能够复用在不同的场景、并可以随着应用的增加而进行扩展。

使用UIP框架的应用程序把表现层分为以下几层：

- User Interface Components：这个组件就是原来的表现层，用户看到的和进行交互都是这个组件，它负责获取用户的数据并且返回结果。
- User Interface Process Components：这个组件用于协调用户界面的各部分，使其配合后台的活动，例如导航和工作流控制，以及状态和视图的管理。用户看不到这一组件，但是这些组件为User Interface Components提供了重要的支持功能。

UIP的组件主要负责的功能：

- 管理经过User Interface Components的信息流；
- 管理UIP中各个事件之间的事务；
- 修改用户过程的流程以响应异常；
- 将概念上的用户交互流程从实现或者涉及的设备上分离出来；
- 保持内部的事务关联状态，通过持有一个或者多个与用户交互的事务实体。
- 因此，这些组件也能进行从UI组件收集数据以执行服务器的成组的升级或跟踪UIP中的任务过程的管理。

## 2.4 表现层动态生成设计思想

基于XML的界面管理技术可实现灵活的界面配置、界面动态生成和界面定制。

实现思路：用XML生成配置文件及界面所需的元数据，按不同需求生成界面元素及软件界面。

![](./media/system_architecture_202101101046.png)

基于XML界面管理技术，包括界面配置、界面动态生成和界面定制三部分：

- 界面配置是对用户界面的静态定义，通过读取配置文件的初始值对界面配置。
  - 由界面配置对软件功能进行裁剪、重组和扩充，以实现特殊需求。
- 界面定制是对用户界面的动态修改过程，在软件运行过程中，用户可按需求和使用习惯，对界面元素（如菜单、工具栏、键盘命令）的属性（如文字、图标、大小和位置等）进行修改。软件运行结束，界面定制的结果被保存。

基于XML的界面管理技术实现的管理信息系统实现了用户界面描述信息与功能实现代码的分离，可针对不同用户需求进行界面配置和定制，能适应一定程度内的数据库结构改动。只需对XML文件稍加修改，即可实现系统的移植。

# 3 中间层架构设计

业务逻辑组件分为接口和实现类。

接口用于定义业务逻辑组件，定义业务逻辑组件必须实现的方法时整个系统运行的核心。

通常按模块来设计业务逻辑组件，每个模块设计一个业务逻辑组件，并且每个业务逻辑组件以多个DAO层作为基础，从而实现对外提供系统的业务逻辑服务。

增加业务逻辑组件的的接口是为了提供更好的解耦，控制器无需与具体的业务逻辑组件耦合，而是面向接口编程。

