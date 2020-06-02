# Node

参考官方文档：[Node](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#modules-node)

# 1 概述

- **结点**
  - 一个Elasticsearch实例。
  - 默认情况下，节点为以下所有类型：候选Master，数据，ingest和机器学习（如果可用）和转换。

- 集群
  - 连接的节点的集合称为群集。
  - 一个Elasticsearch集群可以只有一个结点。
  - 所有节点都知道群集中的所有其他节点，并且可以将客户端请求转发到适当的节点。
  - 默认情况下，群集中的每个节点都可以处理[HTTP](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-http.html)和[Transport](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-transport.html)交互。 传输层专门用于节点之间的通信。 HTTP层由REST客户端使用。
  - 随着集群的增长，特别是如果你有大型机器学习或连续转换工作，请考虑将候选Master结点与专用数据节点，机器学习节点和转换节点分开。

**[Master-eligible node](#2 Master-eligible node)**

候选主结点（Master-eligible node）为将`node.master`设置为`true`（默认值）的节点，这使其有资格被选作控制群集的主节点。

**[Data node](#4 Data node)**

数据结点（Data node）为将 `node.data` 设置为 `true`（默认值）的结点。数据节点被用于保存数据并执行与数据相关的操作，例如CRUD，搜索和聚合。

**[Ingest node](#5 Ingest node)**

Ingest结点为将`node.ingest`设置为 `true` （默认值）的节点。 Ingest节点能够对文档应用[ingest pipeline](https://www.elastic.co/guide/en/elasticsearch/reference/current/pipeline.html)，以便在建立索引之前转换和丰富文档。 在繁重的ingest负载下，使用专用的ingest节点并将主节点和数据节点标记为`node.ingest: false`是有意义的。

**[Machine learning node](#7 Machine learning node)**

机器学习结点（Machine learning node）为将`xpack.ml.enabled`和`node.ml`设置为`true`的结点，这也是ElasticSearch默认发行版中默认的设置。如果你想使用机器学习功能，则集群中必须至少拥有一个机器学习节点。获取更多有关机器学习功能的信息，参见[Machine learning in the Elastic Stack](https://www.elastic.co/guide/en/machine-learning/7.7/index.html)。

重要提示：如果仅使用OSS发行版，则不要设置`node.ml`。 否则，节点将无法启动。

**[Transform node](#8 Transform node)**

转换（Transform）节点将`xpack.transform.enabled`和`node.transform`设置为`true`的节点。 如果要使用转换，则群集中必须至少有一个转换节点。更多信息，参见[Transforms settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-settings.html)和[*Transforming data*](https://www.elastic.co/guide/en/elasticsearch/reference/current/transforms.html)。

**[Coordinating node](#7 Coordinating only node)**

诸如搜索请求或批量索引请求之类的请求可能涉及保存在不同数据节点上的数据。 例如，搜索请求在两个阶段中执行，这两个阶段由接收客户请求的节点（即协调节点）协调。

在分散阶段，协调节点将请求转发到保存数据的数据节点。 每个数据节点在本地执行该请求，并将其结果返回给协调节点。 在收集阶段，协调节点将每个数据节点的结果归约到单个全局结果集中。

每个节点都隐式地为一个协调节点。 这意味着将`node.master`，`node.data`和`node.ingest`三个角色全部设置为`false`的节点将仅充当协调节点，无法禁用。 那么这样的节点就需要具有足够的内存和CPU才能处理收集阶段。

# 2 Master-eligible node

主节点负责集群范围内的轻量级操作，例如创建或删除索引，跟踪哪些节点是集群的一部分以及确定将哪些分片分配给哪些节点。 拥有稳定的主节点对于群集健康非常重要。

可以通过主选举过程选举出非仅投票节点的任何候选主节点，以成为主节点。

主节点必须有权访问`data/`目录（就像数据节点一样），因为这是节点重新启动时保存群集状态的位置。

# 3 Dedicated master-eligible node

对于群集的健康状况而言，重要的一点是当选的主节点拥有履行职责所需的资源。 如果当选的主节点过载其他任务，则群集可能无法正常运行。 特别是，索引和搜索数据可能会占用大量资源，因此在大型或高吞吐量的群集中，最好避免使用候选主节点来执行诸如索引和搜索之类的任务。你可以通过将三个节点配置为专用的候选主节点来完成此操作。 专用的候选主节点仅具有`master`角色，从而使他们可以专注于管理集群。 虽然主节点也可以充当协调节点（[coordinating nodes](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#coordinating-node)），并将搜索和索引请求从客户端路由到数据节点，但最好不要为此目的使用专用的主节点。

在默认发行版中创建专用的候选主节点，设置如下：

```yaml
node.master: true 
node.voting_only: false 
node.data: false 
node.ingest: false 
node.ml: false 
xpack.ml.enabled: true 
node.transform: false 
xpack.transform.enabled: true 
node.remote_cluster_client: false 
```

| 配置项                              | 描述                                    |
| ----------------------------------- | --------------------------------------- |
| `node.master: true`                 | 默认启用`node.master`角色。             |
| `node.voting_only: false`           | 默认禁用`node.voting_only`角色。        |
| `node.data: false`                  | 禁用`node.data`角色（默认为启用）。     |
| `node.ingest: false`                | 禁用`node.ingest`角色（默认为启用）。   |
| `node.ml: false`                    | 禁用`node.ml`角色（默认为启用）。       |
| `xpack.ml.enabled: true`            | 默认启用`xpack.ml.enabled`设置。        |
| `node.transform: false`             | 禁用`node.transform`角色。              |
| `xpack.transform.enabled: true`     | 默认启用`xpack.transform.enabled`角色。 |
| `node.remote_cluster_client: false` | 禁用远程集群连接（默认为启用）。        |

在仅为OSS的发行版中创建专用的候选主节点，设置如下：

```yaml
node.master: true 
node.data: false 
node.ingest: false 
node.remote_cluster_client: false 
```

| 配置项                              | 描述                                  |
| ----------------------------------- | ------------------------------------- |
| `node.master: true`                 | 默认启用`node.master`角色。           |
| `node.data: false`                  | 禁用`node.data`角色（默认为启用）。   |
| `node.ingest: false`                | 禁用`node.ingest`角色（默认为启用）。 |
| `node.remote_cluster_client: false` | 禁用远程集群连接（默认为启用）。      |

# 4 Voting-only master-eligible node

仅投票的候选主节点是参与主节点选举（[master elections](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-discovery.html)）但不会充当群集的经选举的主节点的节点。 特别是，仅投票节点可以在选举中充当决胜局。

使用术语“候选主节点”来描述仅投票的节点似乎令人困惑，因为这样的节点实际上根本没有资格成为主节点。 此术语是历史的不幸结果：候选主节点是那些参与选举并在集群状态发布期间执行某些任务的节点，并且仅投票节点具有相同的职责，即使它们永远无法成为当选的主机。

To configure a master-eligible node as a voting-only node, set the following setting:

要将候选主节点配置为仅投票节点，设置如下：

```yaml
node.voting_only: true
```

| 配置项                   | 描述                              |
| ------------------------ | --------------------------------- |
| `node.voting_only: true` | `node.voting_only`默认为`false`。 |

仅Elasticsearch的默认发行版支持投票角色，仅OSS发行版不支持该角色。 如果您使用仅OSS发行版并设置为`node.voting_only`，则该节点将无法启动。 另请注意，只有符合主机资格的节点才能标记为仅投票。

高可用性（HA，High availability）群集至少需要三个候选主节点，其中至少两个不是仅投票节点。 即使其中一个节点发生故障，这样的群集也将能够选举一个主节点。

由于仅投票节点从不充当集群的当选主节点，因此与真正的主节点相比，它们可能需要更少的堆和功率更小的CPU。 但是，所有候选主节点（包括仅投票节点）都需要合适的快速的持久存储以及到集群其余部分的可靠且低延迟的网络连接，因为它们位于发布集群状态更新（[publishing cluster state updates](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-state-publishing.html)）的关键路径上。

仅具有表决权限的候选主节点也可以充当群集中的其他角色。 例如，一个节点既可以是数据节点又可以是仅投票的候选主节点。 专用的仅投票候选主节点是仅投票候选主节点，不具有群集中的其他任何角色。 要在默认发行版中创建专用的仅投票的候选主节点，请设置：

```yaml
node.master: true 
node.voting_only: true 
node.data: false 
node.ingest: false 
node.ml: false 
xpack.ml.enabled: true 
node.transform: false 
xpack.transform.enabled: true 
node.remote_cluster_client: false 
```

| 配置项                              | 描述                                       |
| ----------------------------------- | ------------------------------------------ |
| `node.master: true`                 | 默认启动`node.master`角色。                |
| `node.voting_only: true`            | 启用`node.voting_only`角色（默认为禁用）。 |
| `node.data: false`                  | 禁用`node.data`角色（默认为启用）。        |
| `node.ingest: false`                | 禁用`node.ingest`角色（默认为启用）。      |
| `node.ml: false`                    | 禁用`node.ml`角色（默认为启用）。          |
| `xpack.ml.enabled: true`            | 默认启用`xpack.ml.enabled`配置。           |
| `node.transform: false`             | 禁用`node.transform`角色。                 |
| `xpack.transform.enabled: true`     | 默认启用`xpack.transform.enabled`角色。    |
| `node.remote_cluster_client: false` | 禁用远程集群连接（默认为启用）。           |

# 5 Data node

数据节点包含你已建立索引的文档的分片。 数据节点处理与数据相关的操作，例如CRUD，搜索和聚合。 这些操作是I/O，内存和CPU密集型的。监视这些资源并在过载时添加更多数据节点非常重要。

具有专用数据节点的主要好处是将主角色和数据角色分开。

在默认发行版中创建专用的数据节点，设置如下：

```yaml
node.master: false 
node.voting_only: false 
node.data: true 
node.ingest: false 
node.ml: false 
node.transform: false 
xpack.transform.enabled: true 
node.remote_cluster_client: false 
```

| 配置项                              | 描述                                    |
| ----------------------------------- | --------------------------------------- |
| `node.master: false`                | 禁用`node.master`角色（默认为启用）。   |
| `node.voting_only: false`           | 默认禁用`node.voting_only`角色。        |
| `node.data: true`                   | 默认启用`node.data`角色。               |
| `node.ingest: false`                | 禁用`node.ingest`角色（默认为启用）。   |
| `node.ml: false`                    | 禁用`node.ml`角色（默认为启用）。       |
| `node.transform: false`             | 禁用`node.transform`角色。              |
| `xpack.transform.enabled: true`     | 默认启用`xpack.transform.enabled`配置。 |
| `node.remote_cluster_client: false` | 禁用远程集群连接（默认为启用）。        |

在仅为OSS的发行版中创建专用的数据节点，设置如下：

```yaml
node.master: false 
node.data: true 
node.ingest: false 
node.remote_cluster_client: false 
```

| 配置项                              | 描述                                  |
| ----------------------------------- | ------------------------------------- |
| `node.master: false`                | 禁用`node.master`角色（默认为启用）。 |
| `node.data: true`                   | 默认启用`node.data`角色。             |
| `node.ingest: false`                | 禁用`node.ingest`角色（默认为启用）。 |
| `node.remote_cluster_client: false` | 禁用远程集群连接（默认为启用）。      |

# 6 Ingest node

预处理节点（ingest node）可以执行由一个或多个接收处理器组成的预处理管道。 根据摄取处理器执行的操作类型和所需的资源，拥有专用的预处理节点可能有意义，该节点仅执行此特定任务。

在默认发行版中创建专用的预处理节点，设置如下：

```yaml
node.master: false 
node.voting_only: false 
node.data: false 
node.ingest: true 
node.ml: false 
node.transform: false 
node.remote_cluster_client: false 
```

| 配置项                              | 描述                                  |
| ----------------------------------- | ------------------------------------- |
| `node.master: false`                | 禁用`node.master`角色（默认为启用）。 |
| `node.voting_only: false`           | 默认禁用`node.voting_only`角色。      |
| `node.data: false`                  | 禁用`node.data`角色（默认为启用）。   |
| `node.ingest: true`                 | 默认启用`node.ingest`角色。           |
| `node.ml: false`                    | 禁用`node.ml`角色（默认为启用）。     |
| `node.transform: false`             | 禁用`node.transform`角色。            |
| `node.remote_cluster_client: false` | 禁用远程集群连接（默认为启用）。      |

在仅为OSS的发行版中创建专用的预处理节点，设置如下：

```yaml
node.master: false 
node.data: false 
node.ingest: true 
node.remote_cluster_client: false 
```

| 配置项                              | 描述                                  |
| ----------------------------------- | ------------------------------------- |
| `node.master: false`                | 禁用`node.master`角色（默认为启用）。 |
| `node.data: false`                  | 禁用`node.data`角色（默认为启用）。   |
| `node.ingest: true`                 | 默认启用`node.ingest`角色。           |
| `node.remote_cluster_client: false` | 禁用远程集群连接（默认为启用）。      |

# 7 Coordinating only node

如果您不具备处理主要职责，保存数据和预处理文档的能力，那么您将拥有一个仅可路由请求，处理搜索缩减阶段并分配批量索引的协调节点。 本质上，仅协调节点充当智能负载均衡器。

仅协调节点可以通过从数据和候选主节点上去除协调节点角色来使大型集群受益。 他们加入群集并像其他所有节点一样接收完整的群集状态（[cluster state](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-state.html)），并且使用群集状态将请求直接路由到适当的位置。

在集群中添加过多的仅协调节点会增加整个集群的负担，因为被选举出来的主节点必须等待每个节点的集群状态更新确认！ 仅协调节点的好处不应被夸大-数据节点可以很好地达到相同的目的。

在默认发行版中创建专用的协调节点，设置如下：

```yaml
node.master: false 
node.voting_only: false 
node.data: false 
node.ingest: false 
node.ml: false 
xpack.ml.enabled: true 
node.transform: false 
xpack.transform.enabled: true 
node.remote_cluster_client: false 
```

| 配置项                              | 描述                                    |
| ----------------------------------- | --------------------------------------- |
| `node.master: false`                | 禁用`node.master`角色（默认为启用）。   |
| `node.voting_only: false`           | 默认禁用`node.voting_only`角色。        |
| `node.data: false`                  | 禁用`node.data`角色（默认为启用）。     |
| `node.ingest: false`                | 禁用`node.ingest`角色（默认为启用）。   |
| `node.ml: false`                    | 禁用`node.ml`角色（默认为启用）。       |
| `xpack.ml.enabled: true`            | 默认启用`xpack.ml.enabled`配置。        |
| `node.transform: false`             | 禁用`node.transform`角色。              |
| `xpack.transform.enabled: true`     | 默认启用`xpack.transform.enabled`配置。 |
| `node.remote_cluster_client: false` | 禁用远程集群连接（默认为启用）。        |

在仅为OSS的发行版中创建专用的协调节点，设置如下：

```yaml
node.master: false 
node.data: false 
node.ingest: false 
node.remote_cluster_client: false 
```

| 配置项                              | 描述                                  |
| ----------------------------------- | ------------------------------------- |
| `node.master: false`                | 禁用`node.master`角色（默认为启用）。 |
| `node.data: false`                  | 禁用`node.data`角色（默认为启用）。   |
| `node.ingest: false`                | 禁用`node.ingest`角色（默认为启用）。 |
| `node.remote_cluster_client: false` | 禁用远程集群连接（默认为启用）。      |

# 8 Machine learning node

机器学习功能提供了机器学习节点，该节点运行作业和处理机器学习API请求。 如果`xpack.ml.enabled` 设置为`true`，而`node.ml`设置为`false`，则该节点可以处理API请求，但不能运行作业。

如果要在群集中使用机器学习功能，则必须在所有主机候选节点上启用机器学习（将`xpack.ml.enabled`设置为`true`）。 如果要在客户端（包括Kibana）中使用机器学习功能，则还必须在所有协调节点（coordinating nodes）上将其启用。 如果您只有OSS发行版，请不要使用这些设置。

有关这些设置的更多信息，参见[Machine learning settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-settings.html).

在默认发行版中创建专用的机器学习节点，设置如下：

```yaml
node.master: false 
node.voting_only: false 
node.data: false 
node.ingest: false 
node.ml: true 
xpack.ml.enabled: true 
node.transform: false 
xpack.transform.enabled: true 
node.remote_cluster_client: false 
```

| 项目                                | 解释                                    |
| ----------------------------------- | --------------------------------------- |
| `node.master: false`                | 禁用`node.master`角色（默认为启用）。   |
| `node.voting_only: false`           | 默认禁用`node.voting_only`角色。        |
| `node.data: false`                  | 禁用`node.data`角色（默认为启用）。     |
| `node.ingest: false`                | 禁用`node.ingest`角色（默认为启用）。   |
| `node.ml: true`                     | 默认启用`node.ml`角色。                 |
| `xpack.ml.enabled: true`            | 默认禁用`xpack.ml.enabled`设置。        |
| `node.transform: false`             | 禁用`node.transform`角色。              |
| `xpack.transform.enabled: true`     | 默认启用`xpack.transform.enabled`设置。 |
| `node.remote_cluster_client: false` | 禁用远程集群连接（默认允许）。          |

# 9 Transform node

转换节点运行转换并处理转换API请求。

如果想在集群中使用转换，必须在所有的候选主节点和数据节点上将`xpack.transform.enabled`设置为`true`。如果想在客户端（包括Kibana），也必须在所有的协调（coordinating）节点上开启。必须至少在一个节点上将`node.transform`设置为`true`，这也是默认行为。如果您只有OSS发行版，请不要使用这些设置。更多信息，参见[Transforms settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-settings.html)。

在默认的发行版中创建一个专门的转换节点，设置如下：

```yaml
node.master: false 
node.voting_only: false 
node.data: false 
node.ingest: false 
node.ml: false 
node.transform: true 
xpack.transform.enabled: true 
node.remote_cluster_client: false 
```

| 配置项                              | 描述                                |
| ----------------------------------- | ----------------------------------- |
| `node.master: false`                | 禁用`node.master`角色。             |
| `node.voting_only: false`           | 禁用`node.voting_only`.             |
| `node.data: false`                  | 禁用`node.data`角色                 |
| `node.ingest: false`                | 禁用`node.ingest`角色。             |
| `node.ml: false`                    | 禁用`node.ml`角色。                 |
| `node.transform: true`              | 启用`node.transform`角色。          |
| `xpack.transform.enabled: true`     | 开启`xpack.transform.enabled`设置。 |
| `node.remote_cluster_client: false` | 禁用集群远程连接。                  |

# 10 Changing the role of a node

每个数据节点在磁盘上维护以下数据：

- 分配给该节点的每个分片的分片数据；
- 与分配给该节点的每个分片相对应的索引元数据；
- 集群范围的元数据，例如设置和索引模板。

同样，每个候选主节点都会在磁盘上维护以下数据

- 集群中每个索引的索引元数据；
- 集群范围的元数据，例如设置和索引模板。

每个节点在启动时都会检查其数据路径下的内容。 如果发现意外数据，它将拒绝启动。这是为了避免导入可能导致存在主分片运行不正常的群集运行状况（a red cluster health）的不必要的悬空索引（[dangling indices](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-gateway-dangling-indices.html)）。 更确切地说，如果设置`node.data: false`的节点在启动时在磁盘上找到任何分片数据，则此节点将拒绝启动，而具有`node.master: false`和`node.data: false`的节点如果在启动的时候在磁盘上有任何的索引元数据，此节点将拒绝启动。

可以通过调整节点的`elasticsearch.yml`文件并重新启动来更改其角色。 这称为重新利用节点。 为了满足上述对意外数据的检查，在将节点的`node.data`或`node.master`角色设置为`false`时，必须执行一些额外的步骤来准备重新使用该节点：

- 如果要通过将`node.data`更改为false来重新利用数据节点，则应首先使用分配过滤器（[allocation filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/allocation-filtering.html)）将所有分片数据安全地迁移到群集中的其他节点上。
- 如果要重新使用节点使其同时具有`node.master: false`和`node.data: false`，那么最简单的方法是启动一个具有空的数据路径和所需角色的全新节点。您可能会发现使用分配过滤器（[allocation filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/allocation-filtering.html)）首先将分片数据迁移到集群中其他位置最安全。

如果无法执行这些额外的步骤，则可以使用[`elasticsearch-node repurpose`](https://www.elastic.co/guide/en/elasticsearch/reference/current/node-tool.html#node-tool-repurpose)工具删除任何阻止节点启动的多余数据。

# 11 Node data path settings

## 11.1 `path.data`

每个数据和候选主节点都需要访问数据目录，在该目录中将存储分片、索引和集群元数据。 `path.data`默认为 `$ES_HOME/data` ，但是可以在`elasticsearch.yml`配置文件中配置绝对路径或相对于`$ ES_HOME`的路径，如下所示：

```yaml
path.data:  /var/elasticsearch/data
```

与所有节点设置一样，也可以在命令行上将其指定为：

```shell
./bin/elasticsearch -Epath.data=/var/elasticsearch/data
```

使用`.zip`或`.tar.gz`发行版时，`path.data`设置以将数据目录定位在Elasticsearch主目录之外，以便可以删除主目录而不删除数据！ RPM和Debian发行版已经这样做了。

## 11.2 `node.max_local_storage_nodes`

数据路径可以由多个节点共享，甚至可以由来自不同群集的节点共享。 但是，建议仅使用同一数据路径运行Elasticsearch的一个节点。 此设置在7.x中已弃用，并将在8.0版中删除。

默认情况下，Elasticsearch被配置为防止多个节点共享同一数据路径。 要允许一个以上的节点（例如，在您的开发机器上），则要使用`node.max_local_storage_nodes`设置并将其设置为大于1的正整数。

切勿在同一数据目录中运行不同的节点类型（即主节点，数据）。 这可能会导致意外的数据丢失。

## 12 Other node settings

可以在[Modules](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules.html)中找到更多的节点设置。 特别要注意的是`cluster.name`，`node.name`和[network settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-network.html)。

