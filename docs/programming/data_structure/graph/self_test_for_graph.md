# 图的自测

# 1 图的定义和术语

## 1.1 图的抽象数据结构是怎样的？

- 图操作：创建、销毁
- 顶点操作：定位、获取、赋值、添加、删除
- 邻接顶点操作：获取第一个和下一个邻接顶点
- 弧操作：添加、删除
- 遍历：深度优先遍历、广度优先遍历

## 1.2 n 个结点的完全有向图含有边的数目？

【答】n*（ n－ l）

【解析】

我们用n表示图中顶点数目，用e表示边或弧的数目（在以后的讨论中我们不考虑顶点到自身的弧或边）。

- **无向图**：
  - e的取值范围是0~$\frac{1}{2}n(n-1)$
  - 有$\frac{1}{2}n(n-1)$条边的无向图称为**完全图（Completed graph）**。
- **有向图**：
  - e的取值范围是0~n(n-1)。
  - 具有n(n-1)条弧的有向图称为**有向完全图**。

# 2 图的存储结构

## 2.1 图的常用表示方法有哪几种？各自有什么特点？存储结构是怎样的？

【解析】

**图的常用表示方法**：

- 数组表示法：用两个数组分别存储数据元素（顶点）的信息和数据元素之间的关系（边或弧）的信息。

  - 适用范围：无向图、有向图

    ```c
    //----------图的数组（邻接矩阵）存储表示----------
    #define INFINTY INT_MAX             //最大值
    #define MAX_VERTEX_NUM 20           //最大顶点个数
    typedef enum {DG, DN, UDG, UDN} GraphKind;    //{有向图，有向网， 无向图， 无向网}
    typedef struct ArcCell{
        VRType      adj;        //VRType是顶点关系类型，对无权图，用1或0表示相邻否；对带权图，则为权值类型
        InfoType    *info;      //该弧相关信息的指针
    } ArcCell, AdjMatrix[MAX_VERTEX_NUM][MAX_VERTEX_NUM];
    typedef struct{
        VertexType      vexs[MAX_VERTEX_NUM];       //顶点向量
        AdjMatrix       arcs;                       //邻接矩阵
        int             vexnum,arcnum;              //图的当前顶点数和弧数
        GraphKind       kind;                       //图的种类标志
    }MGraph;
    ```

    

- 邻接表（Adjacency List）：是图的一种链式存储结构。在邻接表中，对图中每个顶点建立一个单链表，第i个单链表中的结点表示依附于顶点$v_i$的边（对有向图是以顶点$v_i$为尾得弧）。

  - 适用范围：无向图、有向图

  - 若无向图中有n个顶点、e条边，则它的邻接表需n个头结点和2e个表结点。显然，在边稀疏（$e<<\frac{n(n-1)}{2}$）情况下，用邻接表表示图比邻接矩阵节省存储空间，当和边相关的信息较多时更是如此。

  - 在邻接表上容易找到任一顶点的第一个邻接点和下一个邻接点，但要判定任意两个顶点（$v_i$和$v_j$）之间是否有边或弧相连，则需搜索第i个或第j个链表，因此，不及邻接矩阵方便。

    ```c
    //----------图的邻接表存储表示----------
    #define MAX_VERTEX_NUM 20
    typedef struct ArcNode{
        int             adjvex;//该弧所指向的顶点的位置
        struct ArcNode  *nextarc;//指向下一条弧的指针
        InfoType        *info;//该弧相关信息的指针
    } ArcNode;
    typedef struct VNode{
        VertexType      data;//顶点信息
        ArcNode         *firstarc;//指向第一条依附该顶点的弧的指针
    }VNode, AdjList[MAX_VERTEX_NUM];
    typedef struct {
        AdjList     vertices;
        int         vexnum, arcnum;//图的当前顶点数和弧数
        int         kind;//图的种类标志
    } ALGraph;
    ```

    

- 十字链表（Orthogonal List）：是**有向图**的另一种链式存储结构。可以看成是将有向图的邻接表和逆邻接表结合起来得到的一种链表。在十字链表中，对应于有向图中每一条弧有一个结点，对应于每个顶点也有一个结点。

  - 适用范围：有向图

  - 在十字链表中既容易找到以$v_i$为尾的弧，也容易找到以$v_i$为头的弧，因而容易求得顶点的出度和入度（或需要，可在建立十字链表的同时求出）

    ```c
    //----------有向图的十字链表存储表示----------
    #define MAX_VERTEX_NUM 20
    typedef struct ArcBox{
        int             tailvex, headvex;//该弧的尾和头顶点的位置
        struct ArcBox   *hlink, *tlink;//分别尾弧头相同和弧尾相同的弧的链表
        InfoType        *info;//该弧相关信息的指针
    } ArcBox;
    typedef struct VexNode{
        VertexType      data;
        ArcBox          *firstin, *firstout;//分别指向该顶点第一条入弧和出弧
    } vexNode;
    typedef struct {
        vexNode     xlist[MAX_VERTEX_NUM];//表头向量
        int         vexnum, arcnum;//有向图的当前顶点数和弧数
    } OLGraph;
    ```

    

- 邻接多重表（Adjacency Multilist）：是**无向图**的另一个链式存储结构。虽然邻接表是无向图的一种很有效的存储结构，在邻接表中容易求得顶点和边的各种信息。但是，在邻接表中每一条边$(v_i, v_j)$有两个结点，分别在第i个和第j个链表中，这给某些图的操作带来了不便。例如在某些图的应用问题中需要对边进行某种操作，如对已被搜索过的边作记号或删除一条边等，此时需要找到表示同一条边的两个结点。因此，在进行这一类操作的无向图的问题中采用邻接多重表作存储结构更为适宜。

  - 适用范围：无向图

  - 在邻接多重表中，所有依附于同一顶点的边串联在同一链表中，由于每条边依附于两个顶点，则每个边结点同时链接在两个链表中。可见，对无向图而言，其邻接多重表和邻接表的差别，仅仅在于同一条边在邻接表中用两个结点表示，而在邻接多重表中只有一个结点。因此，除了在边结点中增加一个标志域外，邻接多重表所需的存储量和邻接表相同。在邻接多重表上，各种基本操作的实现亦和邻接表相似。

    ```c
    //----------无向图的邻接多重表存储表示----------
    #define MAX_VERTEX_NUM 20
    typedef enum {unvisited, visited} VisitIf;
    typedef struct EBox{
        VisitIf         mark;//访问标记
        int             ivex, jvex;//该边依附的两个顶点的位置
        struct EBox     *ilink, *jlink;//分别指向依附这两个顶点的下一条边
        InfoType        *info;
    } EBox;
    typedef struct VexBox{
        VertexType      data;
        EBox            *firstedge;//指向第一条依附该顶点的边
    } VexBox;
    typedef struct {
        VexBox      adjmulist[MAX_VERTEX_NUM];
        int         vexnum, edgenum;//无向图的当前顶点数和边数
    } AMLGraph;
    ```

## 2.2 用相邻矩阵 A 表示图，判定任意两个顶点 Vi 和 Vj 之间是否有长度为 m 的路径相连，则只要检查（ ）的第 i 行第 j 列的元素是否为零即可。
【解】长度为m的路径应该是从$V_i$起经过m-1个点到达$V_j$。

设A为邻接矩阵，若顶点$V_i$和顶点$V_j$之间有路径，则A(i, j)非零。

先解释$A^2$的含义：

根据矩阵相乘的公式，得：$A^2(i,j) = \sum_{k=1}^{n}{A(i, k)*A(k, j)}$
$$
\begin{array}{l}
A = \left[
        \begin{array}{ccc}
            a_{11} & a_{12} & a_{13} \\
            a_{21} & a_{22} & a_{23} \\
            a_{31} & a_{32} & a_{33} \\
        \end{array}
    \right] \\
A^2 = \left[
        \begin{array}{ccc}
            a_{11}*a_{11} + a_{12}*a_{21} +  a_{13}*a_{31} & a_{11}*a_{12} + a_{12}*a_{22} +  a_{13}*a_{32} & a_{11}*a_{13} + a_{12}*a_{23} +  a_{13}*a_{33} \\
            a_{21}*a_{11} + a_{22}*a_{21} +  a_{23}*a_{31} & a_{21}*a_{12} + a_{22}*a_{22} +  a_{23}*a_{32} & a_{21}*a_{13} + a_{22}*a_{23} +  a_{23}*a_{33} \\
            a_{31}*a_{11} + a_{32}*a_{21} +  a_{33}*a_{31} & a_{31}*a_{12} + a_{32}*a_{22} +  a_{33}*a_{32} & a_{31}*a_{13} + a_{32}*a_{23} +  a_{33}*a_{33} \\
        \end{array}
    \right]
\end{array}
$$
A(i, k)和A(k, j)分别表示$V_i$和$V_k$与$V_k$和$V_i$是否存在路径，只要存在一个k使得$A(i, k)*A(k, j)$非零，则表明存在一个中转点k使得$V_i$和$V_k$之间存在一条长度为2得路径。

因为邻接矩阵元素$a_{ii}$肯定为0，则上边得$A^2$退化为：
$$
\begin{array}{l}
A = \left[
        \begin{array}{ccc}
            a_{11} & a_{12} & a_{13} \\
            a_{21} & a_{22} & a_{23} \\
            a_{31} & a_{32} & a_{33} \\
        \end{array}
    \right] \\
A^2 = \left[
        \begin{array}{ccc}
            a_{12}*a_{21} +  a_{13}*a_{31} & a_{13}*a_{32} & a_{12}*a_{23} \\
            a_{23}*a_{31} & a_{21}*a_{12} +  a_{23}*a_{32} & a_{21}*a_{13} \\
            a_{32}*a_{21} & a_{31}*a_{12} & a_{31}*a_{13} + a_{32}*a_{23}\\
        \end{array}
    \right]
\end{array}
$$
因为同一个顶点不存在路径即$a_{ii} = 0$，且则$A^2(i, j) \neq 0$（$i\neq j$）则可表示存在一个顶点k使得$A(i, k)$和$A(k, j)$同时不为零，即$V_i$和$V_k$与$V_k$和$V_j$都存在路径，因此也就说明从顶点$V_i$到顶点$V_j$存在一条长度为2的路径。

同上理，若$A^m(i, j)$非零，则表明从顶点$V_i$到顶点$V_j$存在一条长度为3的路径。

# 3 图的遍历

## 3.1 简述图的遍历

**图的遍历（Traversing Graph）**定义：从图中某一顶点出发访遍图中其余顶点，且使每一个顶点仅被访问一次，这一过程称为图的遍历。

通常有两种遍历图的路径：深度优先搜索和广度优先搜索。它们对于无向图和有向图都适用。