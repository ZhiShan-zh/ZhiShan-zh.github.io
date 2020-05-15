# 面向对象软件设计SOLID原则

# 1 单一职责原则

单一职责原则（Single responsibility principle，缩写：SRP）

说明：一个类或者模块只负责完成一个职责（A class or module should have single responsibility）。通俗的说：就是**一个模块、类、方法不要承担过多的任务。**

原则上说，我们设计一个类的时候不应该设计成大而全的类，要设计粒度小，功能单一的类，如果一个类包含两个或两个以上互不相干的功能，那我们就说它违反了单一职责原则，应该将它拆分成多个功能单一、粒度更细的类。

实际软件开发工作中，不必严格遵守原则，可以设计一个粗粒度的类，随着业务的发展，再进行重构。

实际开发中可以按照以下参考意见，进行代码的重构或者设计：

1. 类依赖过多其他类，或者代码直接的依赖关系过于复杂时，不符合高内聚低耦合的设计思想，就可以考虑对代码进行拆分。
1. 类的名称和实际的功能关系不大或者没有任何关联性的时候，可以更细粒度的拆分，把无关的功能独立出来。
1. 类的代码函数过多影响可读性和代码维护时，可以对代码进行方法级别的拆分。

# 2 开闭原则

开闭原则（Open-closed principle，缩写为：OCP）

说明：软件实体（模块、类、方法等）应该”对扩展开放，对修改关闭“（software entities （modules，classes，functions，etc.）should be open for extension,but closed for modification)。**通俗理解就是添加一个功能应该是在已有的代码基础上进行扩展，而不是修改已有的代码**。

开闭原则的目的是为了代码的可扩展，并且避免了对现有代码的修改给软件带来风险。可扩展的前提是需要了解到未来的扩展点，那实际软件开发中如何找到所有的可扩展点呢？以下提供几种参考方案：

1. 如果是业务驱动的系统，需要在充分了解了业务需求的前提下，才能找到对应的扩展点，如果不确定因素过多，需求变化过快，则可以对于一些比较确定的，短期内就可能会扩展，通过设置扩展点，能明显提升代码稳定性和开发效率的地方进行设计。
1. 如果是通用型的技术开发，比如开发通用的框架、组件、类库，你需要考虑该技术框架将如何被用户使用，考虑功能的升级需要预留的扩展点以及版本之间的兼容问题。
1. 即使对系统的业务或者技术框架有足够的了解，也不一定要设计所有的扩展点。为未来可能发生变化的所有地方都预留扩展点，也会给系统带来极大的复杂度，实现起来工作量也不可小觑。需要综合开发成本、影响范围、实际收益（包括时间和人员成本）等因素进行考虑。

# 3 里氏替换原则

里氏替换原则（Liskvo substitution principle，缩写为：LSP）：

说明：**子类对象能够替换程序中父类对象出现的任何地方，并且保证原来程序的逻辑行为不变及正确性不被破坏**（If S is a subtype of T,then objects of type T may be replaced with objects of type S,without breaking the program/Functions that use pointers of references to base classes must be able to use objects of derived classes without knowing it）。

可以利用面向对象编程的多态性来实现，多态和里氏原则有点类似，但他们的关注角度是不一样，多态是面向对象编程的特性，而里氏原则是一种设计原则，用来指导继承关系中子类该如何设计，子类的设计要确保在替换父类的时候，不改变原有程序的逻辑以及不破坏原有程序的正确性。

具体实现方式可以理解为，子类在设计的时候，要遵循父类的行为约定。父类定义了方法的行为，子类可以改变方法的内部实现逻辑，但不能改变方法原有的行为约定，如：接口/方法声明要实现的功能，对参数值，返回值，异常的约定，甚至包括注释中所罗列的任何特殊说明。

# 4 接口隔离原则

接口隔离原则（Interface Segregation principle，缩写为：ISP）：

说明：客户端不应该强迫依赖它不需要的接口（Clients should not be forced to depend upon interfaces that they do not use）。

接口隔离原则的时间可以参考如下方法：

1. 对于接口来说，如果某个接口承担了与它无关的接口定义，则说明该接口违反了接口隔离原则。可以把无关的接口剥离出去。对胖而杂的接口瘦身。
1. 对于共通的功能来说，应该细分功能点，按需添加，而不是定义一个大而全的接口，让子类被迫去实现。

# 5 依赖倒置原则

依赖倒置原则（Dependency inversion principle，缩写DIP）：

说明：高层模块不要依赖低层模块。高层模块和低层模块应该通过抽象来相互依赖，除此之外，抽象不要依赖具体实现细节，具体实现细节依赖抽象（High-level modules should not depend on low-level modules. Both modules should depend on abstractions. In addition, abstractions should not depend on details. Details depend on abstractions）。

这里的高层模块，从代码角度来说就是调用者，低层模块就是被调用者。即调用者不要依赖于具体的实现，而应该依赖于抽象，如Spring框架中的各种Aware接口，框架依赖与Aware接口给予具体的实现增加功能，具体的实现通过实现接口来获得功能。而具体的实现与框架直接并没有直接耦合。
