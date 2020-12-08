[TOC]

# 第七章 微分方程

## 7.1 概述

**微分方程的定义**：含有导数或者微分的方程。

**微分方程的解**：使得微分方程成立的函数，称为微分方程的解。

**微分方程解的分类**：

- **特解**：不含有任意常数的解。
  - 除了x外其他部分都是确定值的解。
- **通解**：微分方程中相互独立的任意常数的个数与微分方程的阶数相等。

【**解释**】

- 微分方程式的“**阶**”就是这个方程式中出现的**最高的导数**。
- 微分方程式的 “**次**”就是**最高导数项的幂**。
  - 一次又称为线性。

## 7.2 一阶微分方程

### 7.2.1 可分离变量的微分方程

【**定义**】$\frac{d_y}{d_x}=f(x, y)$，若$f(x, y) = \rho_1(x)\rho_2(y)$称$\frac{d_y}{d_x}=f(x, y)$为可分离变量的微分方程。

**【解法】**

1. 分离变量；
2. 两边积分。

> $$
> \begin{array}{l}
> \frac{d_y}{d_x}=f(x, y) \\
> \Rightarrow \frac{d_y}{d_x} = \rho_1(x)\rho_2(y) \\
> \Rightarrow \frac{d_y}{\rho_2(y)} = \rho_1(x)d_x \\
> 两边积分得：\int{\frac{d_y}{\rho_2(y)}} = \int{\rho_1(x)d_x}
> \end{array}
> $$

### 7.2.2 齐次微分方程

【**定义**】对于$\frac{d_x}{d_y} = f(x, y)$，若$f(x, y) = \rho(\frac{d_x}{d_y})$或$f(tx, ty) = f(x, y)$，则称$\frac{d_x}{d_y} = f(x, y)$为齐次微分方程。

**【解法】**
$$
\begin{array}{l}
\frac{d_x}{d_y} = f(x, y) \\
\Rightarrow f(x, y) = \rho(\frac{d_x}{d_y}) \\
令 \frac{y}{x} = u,则y = xu \\
\Rightarrow \frac{d_y}{d_x} = u + xu` \\
又 u是关于x的函数，则 u` = \frac{d_u}{d_x} \\
\Rightarrow u + x\frac{d_u}{d_x} = \rho(u) \\
\Rightarrow x\frac{d_u}{d_x} = \rho(u) - u \\
\Rightarrow \frac{d_u}{\rho(u) - u} = \frac{d_x}{x} \\
\Rightarrow \int{\frac{d_u}{\rho(u) - u}} = \int{\frac{d_x}{x}} + C
\end{array}
$$

### 7.2.3 一阶齐次线性微分方程

【**定义**】形如$\frac{d_y}{d_x} + P(x)y = 0$的方程称为一阶齐次微分方程。

**【解法】**$\frac{d_y}{d_x} + P(x)y = 0$

1. y = 0为方程的解。

2. $y \neq 0$时
   $$
   \begin{array}{l}
   \frac{d_y}{y} = -P(x)d_x \\
   两边积分\Rightarrow \ln{|y|} = -\int{P(x)d_x} + C_0 \\
   |y| = e^{C_0}e^{-\int{P(x)d_x}} \\
   y = \pm{e^{C_0}e^{-\int{P(x)d_x}}} \\
   令\pm{e^{C_0}} = C （C \neq 0） \\
   \therefore y = Ce^{-\int{P(x)d_x}} （C \neq 0）
   \end{array}
   $$

【**通解**】$y = Ce^{-\int{P(x)d_x}} （C为常数）$

### 7.2.4 一阶非齐次线性微分方程

【**定义**】形如$\frac{d_y}{d_x} + P(x)y = 0$的方程称为一阶齐次微分方程。

**【解法】**$\frac{d_y}{d_x} + P(x)y = Q(x)$
$$
\begin{array}{l}

\end{array}
$$
【**通解**】$y = [\int{Q(x)e^{\int{P(x)d_x}}d_x} + C]e^{-\int{P(x)d_x}} （C为常数）$

### 7.2.5 伯努利微分方程

【**形式**】$\frac{d_y}{d_x} + P(x)y = Q(x)y^n$（$n \neq 0,1$）

**【解法】**令$z = y^{1-n}$，代入原方程得$\frac{d_z}{d_x} + (1-n)P(x)z = (1-n)Q(x)$，然后求解该一阶齐次线性微分方程即可。

> $$
> \begin{array}{l}
> \frac{d_y}{d_x} + P(x)y = Q(x)y^n \\
> \Rightarrow \frac{1}{1-n}z^{\frac{n}{1-n}}z^1 + P(x)z^{\frac{1}{1-n}} = Q(x)z^{\frac{n}{1-n}} \\
> \Rightarrow \frac{1}{1-n}z^1 + P(x)z = Q(x) \\
> \Rightarrow z^1 + (1-n)P(x)z = (1-n)Q(x) \\
> \Rightarrow \frac{d_z}{d_x} + (1-n)P(x)z = (1-n)Q(x)
> \end{array}
> $$
>
> 

### 7.2.6 一阶无特定类型得微分方程

【**例**】$\frac{d_y}{d_x} = \frac{1}{x + y}$

【**解法一**】
$$
\begin{array}{l}
\frac{d_y}{d_x} = \frac{1}{x + y} \\
\Rightarrow \frac{d_x}{d_y} = x + y \\
\Rightarrow \frac{d_x}{d_y} - x = y \\
......
\end{array}
$$
【**解法二**】
$$
\begin{array}{l}
令 x + y = u \\
\Rightarrow \frac{d_y}{d_x} = \frac{d_u}{d_x} - 1 \\
代入原式得  \frac{d_u}{d_x} - 1 = \frac{1}{u} \\
\Rightarrow \frac{d_u}{d_x} = \frac{u = 1}{u} \\
\Rightarrow \frac{u}{u + 1}d_u = d_x \\
......
\end{array}
$$

## 7.3 高阶微分方程

### 7.3.1 可降阶得高阶微分方程

####  7.3.1.1 型一：$y^{(n)} = f(x)$（$n \geq 2$）

**【解法】**逐层积分：对方程$y^{(n)} = f(x)$进行n次不定积分即可。

#### 7.3.1.2 型二，缺y型：$f(x,y^`, y^{``}) = 0$

**【解法】**

1. 令$y^` = \frac{d_y}{d_x} = p$，则$y^{``} = \frac{d_p}{d_x}$，代入原方程得$f(x, p, \frac{d_p}{d_x}) = 0$
2. 解出$p = \rho(x, c_1)$，则积分可得原方程得通解：$y = \int{\rho(x, c_1)d_x} + c_2$

#### 7.3.1.3 型三，缺x型：$f(y,y^`, y^{``}) = 0$

**【解法】**

1. 令$y^` = \frac{d_y}{d_x} = p$，则$d_x = p\frac{d_p}{d_y}$，则$y^{``} = \frac{d_p}{d_x} = p\frac{d_p}{d_y}$，原方程可化为$f(y, p, p\frac{d_p}{d_y}) = 0$
2. 解出$p = \rho(y, c_1)$ 或$\frac{d_y}{\rho(y, c_1)} = d_x$，两边积分得$\int{\frac{d_y}{\rho{y, c_1}}} = x + c_2$，进而求出原方程得通解。

## 7.4 高阶线性微分方程

### 7.4.1 定义

n阶齐次线性微分方程：$y^{(n)} + a_{n-1}(x)y^{(n-1)} + ... + a_1(x)y^` + a_0(x)y = 0$ （式1）

n阶非齐次线性微分方程：$y^{(n)} + a_{n-1}(x)y^{(n-1)} + ... + a_1(x)y^` + a_0(x)y = f(x)$ （式2）

若 $f(x) = f_1(x) + f_2(x)$则：

- $y^{(n)} + a_{n-1}(x)y^{(n-1)} + ... + a_1(x)y^` + a_0(x)y = f_1(x)$ （式2_1）
- $y^{(n)} + a_{n-1}(x)y^{(n-1)} + ... + a_1(x)y^` + a_0(x)y = f_2(x)$ （式2_2）

### 7.4.2 解的结构

1. 若$\rho_1(x)$、$\rho_2(x)$、...、$\rho_s(x)$皆为（式1）的解，则$C_1\rho_1(x)$、$C_2\rho_2(x)$、...、$C_s\rho_s(x)$也是（式1）的解；
2. 若$\rho_1(x)$、$\rho_2(x)$分别为（式1）、（式2）的解，则$\rho_1(x) + \rho_2(x)$为（式2）的解；
3. 若$\rho_1(x)$、$\rho_2(x)$为（式2）的解，则$\rho_1(x) - \rho_2(x)$为（式1）的解；
4. 若$\rho_1(x)$、$\rho_2(x)$分别为（式2_1）、（式2_2）的解，则$\rho_1(x) + \rho_2(x)$为（式2）的解；
5. 对$y^{``} + a_1(x)y^` + a_0(x)y = 0$（式3），设$\rho_1(x)$、$\rho_2(x)$为（式3）的两个线性无关解，则（式3）的通解为$y = C_1\rho_1(x) + C_2\rho_2(x)$;
6. 对$y^{``} + a_1(x)y^` + a_0(x)y = f(x)$（式4），设$\rho_1(x)$、$\rho_2(x)$为（式4）的两个线性无关解，$\rho_0(x)$为（式4）的一个特解，则（式4）的通解为$y = C_1\rho_1(x) + C_2\rho_2(x) + \rho_0(x)$。

## 7.5 高阶常系数齐次线性微分方程

**【型】**$y^{(n)} + a_{n-1}y^{(n-1)} + ... + a_1y^` + a_0y = 0$，其中$a_0、a_1、...、a_{n-1}$全是常数。

### 7.5.1 二阶常系数齐次微分方程

**【型式】**$y^{``} + py^` + qy = 0$

**【特征方程】**$\lambda^2 + p\lambda + q = 0$

特征方程是一个一元二次方程，其解有三种情形：

**【情形一】**$\Delta = p^2 - 4q > 0 \Rightarrow \Delta_1 \neq \Delta_2$，通解为：$y = C_1e^{\lambda_1x} + C_2e^{\lambda_2x}$

**【情形二】**$\Delta = p^2 - 4q = 0 \Rightarrow \Delta_1 == \Delta_2$，通解为：$y = (C_1 + C_2x)e^{\lambda x}$

**【情形三】**$\Delta = p^2 - 4q < 0$，特征方程有两个共轭虚根$\lambda_{1,2} = \alpha \pm \beta i$，通解为：$y = e^{\alpha x}[C_1\cos(\beta x) + C_2\sin(\beta x)]$

### 7.5.2 三阶常系数齐次微分方程

**【型式】**$y^{```} + py^{``} + qy^` + ry = 0$

**【特征方程】**$\lambda^3 + p\lambda^2 + q\lambda + r = 0$

特征方程是一个一元三次方程，其解有四种情形：

**【情形一】**$\lambda_1、\lambda_2、\lambda_3 \in R$，且两两不等，则通解为：$y = C_1e^{\lambda_1x} + C_2e^{\lambda_2x} + C_3e^{\lambda_3x}$

**【情形二】**$\lambda_1、\lambda_2、\lambda_3 \in R$，且$\lambda_1 = \lambda_2 \neq \lambda_3$，则通解为：$y = (C_1 + C_2x)e^{\lambda x} + C_3e^{\lambda_3x}$

**【情形三】**$\lambda_1、\lambda_2、\lambda_3 \in R$，且$\lambda_1 = \lambda_2 = \lambda_3$，则通解为：$y = (C_1 + C_2x + C_3x^2)e^{\lambda x}$

**【情形四】**$\lambda_1 \in R,\lambda_{2,3} = \alpha \pm \beta i$（$\beta \neq 0$），则通解为：$y = C_1e^{\lambda_1x} + e^{\alpha x}[C_2\cos(\beta x) + C_3\sin(\beta x)]$

## 7.6 高阶常系数非齐次线性微分方程

### 7.6.1 二阶不含三角函数

**【型式】**$f(y, y^`, y^{``}) = P_n(x)e^{kx}$

**【解法】**

1. 先求出其齐次方程（即$f(y, y^`, y^{``}) = 0$）的特征值；
2. 先求出其齐次方程（即$f(y, y^`, y^{``}) = 0$）的通解；
3. 根据$P_n(x)$中x的幂的次数和k与特征值的关系设置$f(y, y^`, y^{``}) = P_n(x)e^{kx}$的特解$y_0(x) = x^m(a_0 + a_1x + ... + a_nx^n)e^{kx}$：
   1. 使n 等于$P_n(x)$中x的最高的幂次，如果$P_n(x)$是一个常数或常数表达式，则这里只保留$a_0$；
   2. 若k不是特征值（也就是说k和特征值都不相等），令m = 0；若k和其中一个特征值相同，则使m=1；若k和其中两个特征值相同，则使m=2，依次类推。
4. 根据原式$f(y, y^`, y^{``})$的中y的阶数的情况，求出特解的的各级导数；
5. 把特解$y_0(x)$代入原式$f(y, y^`, y^{``}) = P_n(x)e^{kx}$，以求出特解$y_0(x)$；
6. 写出原式的通解：$y = y_0(x) + (f(y, y^`, y^{``}) = 0)的通解$

### 7.6.2 二阶包含三角函数（三角函数为一次）

**【型式】**$f(y, y^`, y^{``}) = P_n(x)e^{\alpha x}\sin{\beta x}$或$f(y, y^`, y^{``}) = P_n(x)e^{\alpha x}\cos{\beta x}$

- $\alpha = 0$时，没有$e^{\alpha x}$

**【解法】**

1. 先求出其齐次方程（即$f(y, y^`, y^{``}) = 0$）的特征值；
2. 先求出其齐次方程（即$f(y, y^`, y^{``}) = 0$）的通解；
3. 根据$e^{\alpha x}\sin{\beta x}$设置特解$y_0(x) = P_n(x)e^{\alpha x}((a_0 + a_1x + ... + a_nx^n)\cos{\beta x} + (b_0 + b_1x + ... + b_nx^n)\sin{\beta x})$；
   1. 按照$f(y, y^`, y^{``}) = e^{\alpha x}\sin{\beta x}$式子右边的样子设定，$\sin$和$\cos$都要有；
   2. 指数函数（$e^{\alpha x}$）放到括号外边；
   3. 若$\alpha \pm i\beta$为特征值，则多乘一个x，且至多乘一个x，x在括号外边。
   4. 根据$P_n(x)$的样子设定$(a_0 + a_1x + ... + a_nx^n)$和$(b_0 + b_1x + ... + b_nx^n)$，使n 等于$P_n(x)$中x的最高的幂次，如果$P_n(x)$是一个常数或常数表达式，则这里只保留$a_0$和$b_0$。