# KNN入门

# 1 使用Python

## 1.1 依赖包

- scikit-learn：0.19.1
  - Numpy
  - Scipy

## 1.2 KNN API

`sklearn.neighbors.KNeighborsClassifier(n_neighbors=5) `

参数说明：

- n_neighbors：int,可选（默认= 5），k_neighbors查询默认使用的邻居数

## 1.3 入门案例

```python
from sklearn.neighbors import KNeighborsClassifier

# 构造数据集
x = [[0], [1], [2], [3]]
y = [0, 0, 1, 1]

# 实例化APIabs
estimator = KNeighborsClassifier(n_neighbors=1)

# 使用fit方法进行训练
estimator.fit(x, y)
# 预测
estimator.predict([[20]])
```

输出：array([1])