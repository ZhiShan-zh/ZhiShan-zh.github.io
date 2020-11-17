# 图的定义和术语

图的抽象数据结构：

```c
ADT Graph{
    //数据对象V：V是具有相同特性的数据元素的集合，称为顶点集。
    //数据关系R：
    //      R={VR}
    //      VR={<v, w>| v,w∈且P(v,w),<v, w>表示从v到w的弧，谓词P(v, w)定义了弧<v, w>的意义或信息}
    //基本操作P：
    /*
     * 初始条件：V是图的顶点集，VR是图中弧的集合。
     * 操作结果：按V和VR的定义构造图G。
     **/
    CreateGraph(&G, V, VR);

    /*
     * 初始条件：图G存在。
     * 操作结果：销毁图G。
     **/
    DestroyGraph(&G);

    /*
     * 初始条件：图G存在，u和G中顶点有相同特性。
     * 操作结果：若图G中存在顶点u，则返回该顶点在图中位置；否则返回其他信息。
     **/
    LocateVex(G, u);

    /*
     * 初始条件：图G存在，v是G中某个顶点。
     * 操作结果：返回v的值。
     **/
    GetVex(G, v);

    /*
     * 初始条件：图G存在，v是G中某个顶点。
     * 操作结果：对v赋值value。
     **/
    PutVex(&G, v, value);

    /*
     * 初始条件：图G存在，v是G中某个顶点。
     * 操作结果：返回v的第一个邻接顶点。若顶点在G中没有邻接顶点，则返回“空”。
     **/
    FirstAdjVex(G, v);

    /*
     * 初始条件：图G存在，v是G中某个顶点，w是v的邻接顶点。
     * 操作结果：返回v的（相对于w）下一个邻接顶点。若w是v的最后一个邻接点，则返回“空”。
     **/
    NextAdjVex(G, v);

    /*
     * 初始条件：图G存在，v和图中顶点有相同特性。
     * 操作结果：在图G增添新顶点v。
     **/
    InsertVex(&G, v);

    /*
     * 初始条件：图G存在，v是G中某个顶点。
     * 操作结果：删除G中顶点v及其相关的弧。
     **/
    DeleteVex(&G, v);

    /*
     * 初始条件：图G存在，v和w是G中两个顶点。
     * 操作结果：在图G中增添弧<v, w>，若G是无向图，则还增添对称弧<w, v>。
     **/
    InsertArc(&G, v, w);

    /*
     * 初始条件：图G存在，v和w是G中两个顶点。
     * 操作结果：在图G中删除弧<v, w>，若G是无向图，则还删除对称弧<w, v>。
     **/
    DeleteArc(&G, v, w);

    /*
     * 初始条件：图G存在，Visit是顶点的应用函数。
     * 操作结果：对图进行深度优先遍历。在遍历过程中对每个顶点调用函数Visit一次且仅一次。一旦visit()失败，则操作失败。
     **/
    DFSTraverse(G, Visit());

    /*
     * 初始条件：图G存在，Visit是顶点的应用函数。
     * 操作结果：对图进行广度优先遍历。在遍历过程中对每个顶点调用函数Visit一次且仅一次。一旦visit()失败，则操作失败。
     **/
    BFSTraverse(G, Visit());
}ADT Graph
```

在图中的数据元素通常称做**顶点（Vertex）**，V是顶点的有穷非空集合；VR是两个顶点之间的关系的集合。若$<v, w>∈VR$则$<v, w>$表示从v到w的一条**弧（Arc）**，且称v为**弧尾（Tail）**或初始点（Initial node），称w为**弧头（Head）**或终端点（Terminal node），此时的图称为**有向图（Digraph）**。若$<v, w>∈VR$必有$<w,v>∈VR$，即VR是对称的，则以无序对$<v, w>$代替这两个有序对，表示v和w之间的一条**边（Edge）**，此时的图称为**无向图（Undigraph）**。

我们用n表示图中顶点数目，用e表示边或弧的数目（在以后的讨论中我们不考虑顶点到自身的弧或边）。

- **无向图**：
  - e的取值范围是0~$\frac{1}{2}n(n-1)$
  - 有$\frac{1}{2}n(n-1)$条边的无向图称为**完全图（Completed graph）**。
- **有向图**：
  - e的取值范围是0~n(n-1)。
  - 具有n(n-1)条弧的有向图称为**有向完全图**。

有很少条边或弧（如$e<n\log{n}$；如边的条数|E|远远小于$|V|^2$）的图称为**稀疏图（Sparse graph）**，反之称为**稠密图（Dense graph）**。

有时图的边或弧具有与它相关的数，这种与图的边或弧相关的数叫做**权（Weight）**。这些权可以表示从一个顶点到另一个顶点的距离或耗费。这种带权的图通常称为**网（Network）**。

假设有两个图$G=(V,{E})$和$G`=(V`,{E`})$，如果$V`\subseteq{V}$且$E`\subseteq{E}$则称G\`为G的**子图（Subgraph）**。如：

![image-20201007225039291](https://zhishan-zh.github.io/media/datestruct_graph_20201007225039291.png)

![image-20201007230436704](https://zhishan-zh.github.io/media/datestruct_graph_20201007230436704.png)

对于无向图$G=(V,{E})$，如果边$(v, v`)\in{E}$，则称顶点v和v\`互为**邻接点（Adjacent）**，即v和v\`相邻接。边$(v, v`)$**依附（Incident）**于顶点v和v\`，或者说$(v, v`)$和顶点v和v\`**相关联**。顶点v的**度（degree）**是和v相关联的边的数目，记为TD(V)。例如，$G_2$中顶点$v_3$的度为3。对于有向图$G=(V,{A})$，如果弧$(v, v`)\in{A}$，则称顶点v邻接到顶点v\`，顶点v\`临接自顶点v。弧$(v, v`)$和顶点v和v\`相关联。以顶点v为头的弧的数目称为v的**入度（InDegree）**，记为ID(v)；以v为尾的弧的数目称为v的**出度（Outdegree）**，记为OD(v)；顶点v的度为TD(v)=ID(V)+OD(v)。一般地，如果顶点$v_i$的度记为$TD(v_i)$，那么一个有n个顶点，e条边或弧的图，满足如下关系：
$$
e=\frac{1}{2}\sum_{i=1}^nTD(v_i)
$$
无向图$G=(V,{E})$中从顶点v到顶点v\`的**路径（Path）**是一个顶点序列（）
