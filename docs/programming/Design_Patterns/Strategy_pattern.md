# 策略模式

# 1 策略模式概述
## 1.1 定义
定义了算法家族，分别封装起来，让它们之间可以相互替换，此模式的变化独立于算法的使用者。

## 1.2 应用场景

- 容错恢复机制
    - 容错恢复机制是应用程序开发中非常常见的功能。那么什么是容错恢复呢？简单点说就是：程序运行的时候，正常情况下应该按照某种方式来做，如果按照某种方式来做发生错误的话，系统并不会崩溃，也不会就此不能继续向下运行了，而是有容忍出错的能力，不但能容忍程序运行出现错误，还提供出现错误后的备用方案，也就是恢复机制，来代替正常执行的功能，使程序继续向下运行。

# 2 入门案例
## 2.1 版本1

```java
package com.zh.strategy.v1;
public class ZombieTest {
    public static void main(String[] args) {
        AbstractZombie normalZombie = new NormalZombie();
        AbstractZombie flagZombie = new FlagZombie();
        
        normalZombie.display();
        normalZombie.move();
        normalZombie.attack();
        System.out.println("----------------");
        flagZombie.display();
        flagZombie.move();
        flagZombie.attack();
    }
}
abstract class AbstractZombie{
    public abstract void display();
    
    public void attack() {
        System.out.println("咬");
    }
    
    public void move() {
        System.out.println("一步一步向前移动");
    }
}
class NormalZombie extends AbstractZombie{
    @Override
    public void display() {
        System.out.println("我是普通僵尸");
    }
}
class FlagZombie extends AbstractZombie{
    @Override
    public void display() {
        System.out.println("我是旗手僵尸");
    }
    
}
class BigHeadZombie extends AbstractZombie{
    @Override
    public void display() {
        System.out.println("大头");
    }
    @Override
    public void attack() {
        System.out.println("头撞");
    }
}
```


## 2.2 版本2

```java
package com.zh.strategy.v2;
public class StrategyTest {
    public static void main(String[] args) {
        Zombie normalZombie = new NormalZombie();
        Zombie flagZombie = new FlagZombie();
        
        normalZombie.display();
        normalZombie.move();
        normalZombie.attack();
        normalZombie.setAttackable(new HitAttack());
        normalZombie.attack();
        System.out.println("--------------");
        flagZombie.display();
        flagZombie.move();
        flagZombie.attack();
    }
}
interface Moveable{
    void move();
}
interface Attackable{
    void attack();
}
abstract class Zombie{
    public Zombie(Moveable moveable, Attackable attackable) {
        super();
        this.moveable = moveable;
        this.attackable = attackable;
    }
    abstract public void display();
    Moveable moveable;
    Attackable attackable;
    abstract void move();
    abstract void attack();
    public Moveable getMoveable() {
        return moveable;
    }
    public void setMoveable(Moveable moveable) {
        this.moveable = moveable;
    }
    public Attackable getAttackable() {
        return attackable;
    }
    public void setAttackable(Attackable attackable) {
        this.attackable = attackable;
    }
}
//一步一步移动
class StepByStep implements Moveable{
    @Override
    public void move() {
        System.out.println("一步一步移动");
    }
}
//咬
class BiteAttack implements Attackable{
    @Override
    public void attack() {
        System.out.println("咬");
    }
}
//打
class HitAttack implements Attackable{
    @Override
    public void attack() {
        System.out.println("打");
    }
    
}
//普通僵尸
class NormalZombie extends Zombie{
    public NormalZombie() {
        super(new StepByStep(), new BiteAttack());
    }
    
    public NormalZombie(Moveable moveable, Attackable attackable) {
        super(moveable, attackable);
    }
    @Override
    public void display() {
        System.out.println("我是普通僵尸");
    }
    @Override
    void move() {
        moveable.move();
    }
    @Override
    void attack() {
        attackable.attack();
    }
}
//旗子僵尸
class FlagZombie extends Zombie{
    public FlagZombie() {
        super(new StepByStep(), new BiteAttack());
    }
    
    public FlagZombie(Moveable moveable, Attackable attackable) {
        super(moveable, attackable);
    }
    @Override
    public void display() {
        System.out.println("我是旗子僵尸");
    }
    @Override
    void move() {
        moveable.move();
    }
    @Override
    void attack() {
        attackable.attack();
    }
}
```



