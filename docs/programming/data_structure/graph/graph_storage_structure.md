# 图的存储结构

由于图的结构比较复杂，任意两个顶点之间都可能存在联系，因此无法以数据元素在存储区中的物理位置来表示元素之间的关系，即图没有顺序映像的存储结构，但可以借助数组的数据类型表示元素之间的关系。另一方面，用多重链表表视图是自然的事，它是一种最简单的链式映像结构，即以一个由一个数据域和多个指针域组成的节点表示图中的一个顶点，其中数据域存储该顶点的信息，指针域存储指向其邻接点的指针。

![image-20201007225039291](https://zhishan-zh.github.io/media/datestruct_graph_20201007225039291.png)

![](https://zhishan-zh.github.io/media/datestruct_graph_2020100921342101.png)

# 1 数组表示法

用两个数组分别存储数据元素（顶点）的信息和数据元素之间的关系（边或弧）的信息。

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

以二维数组表示有n个顶点的图时，需存放n个顶点信息和$n^2$个弧信息的存储量。若考虑无向图的邻接矩阵的对称性，则可采用压缩存储的方式只存储入矩阵的下三角（或上三角）元素。
$$
G_1.arcs=\left[
	\begin{array}{cccc} 
		0 & 1 & 1 & 0 \\ 
		0 & 0 & 0 & 0 \\ 
		0 & 0 & 0 & 1 \\ 
		1 & 0 & 0 & 0 
	\end{array} 
\right], 
G_2.arcs=\left[
    \begin{array}{cccc} 
    	0 & 1 & 0 & 1 & 0 \\ 
    	1 & 0 & 1 & 0 & 1 \\ 
    	0 & 1 & 0 & 1 & 1 \\ 
    	1 & 0 & 1 & 0 & 1 \\ 
    	0 & 1 & 1 & 0 & 0 
    \end{array} 
\right]
$$
借助于邻接矩阵容易判断任意两个顶点之间是否有边（或弧）相连，并容易求得各个顶点得度。对于无向图，顶点$v_i$得度时邻接矩阵中第i行（或第i列）得元素之和，即
$$
TD(v_i) = \sum_{j=0}^{n-1}A[i][j](n=MAX_VERTEX_NUM)
$$
对于有向图，第i行得元素之和为顶点$v_i$的出度$OD(v_i)$，第j列的元素之和为顶点$v_i$的入度$ID(v_j)$。

网的邻接矩阵可以定义为：
$$
A[i][j] = \left\{
	\begin{array}{cc}
		w_{i,j} & 若<v_i,v_j>或(v_i,v_j)\in{VR} \\
		∞ & 反之
	\end{array}
\right.
$$
![](https://zhishan-zh.github.io/media/datestruct_graph_20201010090701.png)
$$
\left[
    \begin{array}{cccc} 
    	∞ & 5 & ∞ & 7 & ∞ & ∞ \\ 
    	∞ & ∞ & 4 & ∞ & ∞ & ∞ \\
        8 & ∞ & ∞ & ∞ & ∞ & 9 \\
        ∞ & ∞ & 5 & ∞ & ∞ & 6 \\
        ∞ & ∞ & ∞ & 5 & ∞ & ∞ \\
        3 & ∞ & ∞ & ∞ & 1 & ∞ \\
    \end{array}
\right]
$$
构造一个具有n个点和e条边的无向网G的时间复杂度是$O(n^2 + e*n)$，其中对邻接矩阵G.arcs的初始化耗费了$O(n^2)$的时间。

# 2 邻接表

**邻接表**（Adjacency List）是图得一种链式存储结构。在邻接表中，对图中每个顶点建立一个单链表，第i个单链表中得结点表示依附于顶点$v_i$得边（对有向图是以顶点$v_i$为尾得弧）。

**表结点**：每个结点由3个域组成

- adjvex：邻接点域，指示与顶点$v_i$邻接的点在图中的位置
- nextarc：链域，指示下一条边或弧的结点
- info：数据域， 存储和边或弧相关的信息，如权值等

**头结点**：每个链表上附设一个表头结点，表头结点（可以链相接）通常以顺序结构的形式存储，以便随机访问任一顶点的链表。

- data：数据域，存储顶点$v_i$的名或其他有关信息
- firstarc：链域，指向链表中第一个结点



# 3 十字链表

# 4 邻接多重表

