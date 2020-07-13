# 编译SQL接口Statement

# 1 Statement

`java.sql.Statement`接口用于在已经建立数据库连接的基础上，向数据库发送要执行的SQL语句。

在包`java.sql`下有三种Statement接口：

- `java.sql.Statement`：用于执行不带参数的简单SQL语句；
- `java.sql.PreparedStatement`：
    - 是`java.sql.Statement`的子接口；
    - 用于执行带或不带 IN参数的预编译 SQL 语句；
    - IN参数的值在 SQL 语句创建时未被指定。相反的，该语句为每个 IN 参数保留一个问号（`?`）作为占位符。每个问号的值必须在该语句执行之前，通过适当的setXXX方法来提供。
    - 由于 PreparedStatement 对象已预编译过，所以其执行速度要快于 Statement 对象。因此，多次执行的 SQL 语句经常创建为 PreparedStatement 对象，以提高效率。
    - PreparedStatement对象可以防止SQL注入，而Statement不能防止SQL注入，PreparedStatement对象防止SQL注入的方式是把用户非法输入的单引号用\反斜杠做了转义，从而达到了防止SQL注入的目的。
        - 原来是MySQL数据库产商，在实现PreparedStatement接口的实现类中的setString(int parameterIndex, String x)函数中做了一些处理，把单引号做了转义（只要用户输入的字符串中有单引号，那MySQL数据库产商的setString()这个函数，就会把单引号做转义）。
    - 应该始终以PreparedStatement代替Statement.也就是说,在任何时候都不要使用Statement。
- `java.sql.CallableStatement`：是`java.sql.PreparedStatement`的子接口，用于执行对数据库已存储过程的调用。

# 2`java.sql.Statement`字段和方法

| 字段                             | 解释                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| `int CLOSE_CURRENT_RESULT = 1;`  | （JDBC 3.0）该常量指示调用 getMoreResults 时应该关闭当前 ResultSet 对象。 |
| `int KEEP_CURRENT_RESULT = 2;`   | （JDBC 3.0）该常量指示调用 getMoreResults 时不会关闭当前 ResultSet 对象。 |
| `int CLOSE_ALL_RESULTS = 3;`     | （JDBC 3.0）该常量指示调用 getMoreResults 时应该关闭以前一直打开的所有 ResultSet 对象。 |
| `int SUCCESS_NO_INFO = -2;`      | （JDBC 3.0）该常量指示批量语句执行成功但不存在受影响的可用行数计数。 |
| `int EXECUTE_FAILED = -3;`       | （JDBC 3.0）该常量指示在执行批量语句时发生错误。             |
| `int RETURN_GENERATED_KEYS = 1;` | （JDBC 3.0）该常量指示生成的键应该可用于获取。               |
| `int NO_GENERATED_KEYS = 2;`     | （JDBC 3.0）该常量指示生成的键应该不可用于获取。             |

| 方法                                                         | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `ResultSet executeQuery(String sql)`                         | 对查询类型的sql语句的执行方法，执行给定的 SQL 语句，该语句返回单个 ResultSet 对象。 |
| `int executeUpdate(String sql)`                              | 对更新类的sql语句的执行方法，执行给定 SQL 语句，该语句可能为 INSERT、UPDATE 或 DELETE 语句，或者不返回任何内容的 SQL 语句（如 SQL DDL 语句）。 |
| `void close()`                                               | 立即释放此 Statement 对象的数据库和 JDBC 资源，而不是等待该对象自动关闭时发生此操作。 |
| `int getMaxFieldSize()`                                      | 获取可以为此 Statement 对象所生成 ResultSet 对象中的字符和二进制列值返回的最大字节数。 |
| `void setMaxFieldSize(int max)`                              | 设置此 Statement 对象生成的 ResultSet 对象中字符和二进制列值可以返回的最大字节数限制。 |
| `int getMaxRows()`                                           | 获取由此 Statement 对象生成的 ResultSet 对象可以包含的最大行数。 |
| `void setMaxRows(int max)`                                   | 将此 Statement 对象生成的所有 ResultSet 对象可以包含的最大行数限制设置为给定数。 |
| `void setEscapeProcessing(boolean enable)`                   | 将转义处理设置为开或关。                                     |
| `int getQueryTimeout()`                                      | 获取驱动程序等待 Statement 对象执行的秒数。                  |
| `void setQueryTimeout(int seconds)`                          | 将驱动程序等待 Statement 对象执行的秒数设置为给定秒数。      |
| `void cancel()`                                              | 如果 DBMS 和驱动程序都支持中止 SQL 语句，则取消此 Statement 对象。 |
| `SQLWarning getWarnings()`                                   | 获取此 Statement 对象上的调用报告的第一个警告。              |
| `void clearWarnings()`                                       | 清除在此 Statement 对象上报告的所有警告。                    |
| `void setCursorName(String name)`                            | 将 SQL指针名称设置为给定的 String，后续 Statement 对象的 execute 方法将使用此字符串。 |
| `boolean execute(String sql)`                                | （Multiple Results）执行给定的 SQL 语句，该语句在返回一个布尔值时用于反映SQL语句是否执行成功。<br />对sql语句类型不进行区分，执行sql语句的方法。该语句可能会返回多个结果<br />如果执行的SQL是查询类型select语句，此方法返回true，需要自己再调用`statement.getResultSet()`方法来获取ResultSet结果集；<br />如果执行的是更新类型语句如update、delete、insert语句，此方法返回false，自己调用`statement.getUpdateCount()`获取SQL语句影响的行数 |
| `ResultSet getResultSet()`                                   | （Multiple Results）以 ResultSet 对象的形式获取当前结果。    |
| `int getUpdateCount()`                                       | （Multiple Results）以更新计数的形式获取当前结果；如果结果为 ResultSet 对象或没有更多结果，则返回 -1。 |
| `boolean getMoreResults()`                                   | （Multiple Results）移动到此 Statement 对象的下一个结果，如果其为 ResultSet 对象，则返回 true，并隐式关闭利用方法 getResultSet 获取的所有当前 ResultSet 对象。 |
| `void setFetchDirection(int direction)`                      | （JDBC 2.0）向驱动程序提供关于方向的提示，在使用此 Statement 对象创建的 ResultSet 对象中将按该方向处理行。 |
| `int getFetchDirection()`                                    | （JDBC 2.0）获取从数据库表获取行的方向，该方向是根据此 Statement 对象生成的结果集合的默认值。 |
| `void setFetchSize(int rows)`                                | （JDBC 2.0）为 JDBC驱动程序提供一个提示，它提示此 Statement 生成的 ResultSet 对象需要更多行时应该从数据库获取的行数。 |
| `int getFetchSize()`                                         | （JDBC 2.0）获取结果集合的行数，该数是根据此 Statement 对象生成的 ResultSet 对象的默认获取大小。 |
| `int getResultSetConcurrency()`                              | （JDBC 2.0）获取此 Statement 对象生成的 ResultSet 对象的结果集合并发性。 |
| `int getResultSetType()`                                     | （JDBC 2.0）获取此 Statement 对象生成的 ResultSet 对象的结果集合类型。 |
| `void addBatch( String sql )`                                | （JDBC 2.0）将给定的 SQL 命令添加到此 Statement 对象的当前命令列表中。 |
| `void clearBatch()`                                          | （JDBC 2.0）清空此 Statement 对象的当前 SQL 命令列表。       |
| `int[] executeBatch()`                                       | （JDBC 2.0）将一批命令提交给数据库来执行，如果全部命令执行成功，则返回更新计数组成的数组。 |
| `Connection getConnection()`                                 | （JDBC 2.0）获取生成此 Statement 对象的 Connection 对象。    |
| `boolean getMoreResults(int current)`                        | （JDBC 3.0）将此 Statement 对象移动到下一个结果，根据给定标志指定的指令处理所有当前 ResultSet 对象；如果下一个结果为 ResultSet 对象，则返回 true。 |
| `ResultSet getGeneratedKeys()`                               | （JDBC 3.0）获取由于执行此 Statement 对象而创建的所有自动生成的键。 |
| `int executeUpdate(String sql, int autoGeneratedKeys)`       | （JDBC 3.0）执行给定的 SQL 语句，并用给定标志通知驱动程序由此 Statement 生成的自动生成键是否可用于获取。 |
| `int executeUpdate(String sql, int columnIndexes[])`         | （JDBC 3.0）执行给定的 SQL 语句，并通知驱动程序在给定数组中指示的自动生成的键可用于获取。 |
| `int executeUpdate(String sql, String columnNames[])`        | （JDBC 3.0）执行给定的 SQL 语句，通知驱动程序在给定数组中指示的自动生成的键可用于获取。 |
| `boolean execute(String sql, int autoGeneratedKeys)`         | （JDBC 3.0）执行给定的 SQL 语句（该语句返回一个布尔值用于反映SQL语句是否成功执行），并通知驱动程序所有自动生成的键都应该可用于获取。 |
| `boolean execute(String sql, int columnIndexes[])`           | （JDBC 3.0）执行给定的 SQL 语句，（该语句返回一个布尔值用于反映SQL语句是否执行成功），并通知驱动程序在给定数组中指示的自动生成的键应可用获取。 |
| `boolean execute(String sql, String columnNames[])`          | （JDBC 3.0）执行给定的 SQL 语句，该语句返回一个布尔值用于反映SQL语句是否成功执行，并通知驱动程序在给定数组中指示的自动生成的键用于获取。 |
| `int getResultSetHoldability()`                              | （JDBC 3.0）获取此 Statement 对象生成的 ResultSet 对象的结果集合可保存性。 |
| `boolean isClosed()`                                         | （JDBC 3.0）                                                 |
| `void setPoolable(boolean poolable)`                         | （JDBC 3.0）请求将 Statement 池化或非池化。                  |
| `boolean isPoolable()`                                       | （JDBC 3.0）返回指示 Statement 是否是可池化的值。            |
| `public void closeOnCompletion()`                            | （JDBC 4.1）                                                 |
| `public boolean isCloseOnCompletion()`                       | （JDBC 4.1）                                                 |
| `default long getLargeUpdateCount()`                         | （JDBC 4.2）                                                 |
| `default void setLargeMaxRows(long max)`                     | （JDBC 4.2）                                                 |
| `default long getLargeMaxRows()`                             | （JDBC 4.2）                                                 |
| `default long[] executeLargeBatch()`                         | （JDBC 4.2）                                                 |
| `default long executeLargeUpdate(String sql)`                | （JDBC 4.2）                                                 |
| `default long executeLargeUpdate(String sql, int autoGeneratedKeys)` | （JDBC 4.2）                                                 |
| `default long executeLargeUpdate(String sql, int columnIndexes[])` | （JDBC 4.2）                                                 |
| `default long executeLargeUpdate(String sql, String columnNames[])` | （JDBC 4.2）                                                 |

# 2`com.mysql.jdbc.StatementImpl`

## 2.1 `public java.sql.ResultSet executeQuery(String sql)`

```java
public java.sql.ResultSet executeQuery(String sql) throws SQLException {
    synchronized (checkClosed().getConnectionMutex()) {
        MySQLConnection locallyScopedConn = this.connection;

        this.retrieveGeneratedKeys = false;
		// 如果sql字符串为Null或空，则报错
        checkNullOrEmptyQuery(sql);
		//重置为没有Cancel
        resetCancelledState();
		//关闭当前Statement所有结果集
        implicitlyCloseAllOpenResults();
		//判断是否为以"/* ping */"开头的字符串，如果是则执行ping操作
        if (sql.charAt(0) == '/') {
            if (sql.startsWith(PING_MARKER)) {
                doPingInstead();

                return this.results;
            }
        }
		//如果我们要流式传输结果集，请将net_write_timeout调整为更高的值。 
        setupStreamingTimeout(locallyScopedConn);
		//判断是否开启逃逸（转义）字符
        if (this.doEscapeProcessing) {
            Object escapedSqlResult = EscapeProcessor.escapeSQL(sql, locallyScopedConn.serverSupportsConvertFn(), this.connection);

            if (escapedSqlResult instanceof String) {
                sql = (String) escapedSqlResult;
            } else {
                sql = ((EscapeProcessorResult) escapedSqlResult).escapedSql;
            }
        }
		//获取SQL语句第一个字符
        char firstStatementChar = StringUtils.firstAlphaCharUc(sql, findStartOfStatement(sql));
		//根据SQL第一个字符检查给定SQL查询是否为DML语句。 如果是，则引发异常。
        checkForDml(sql, firstStatementChar);

        CachedResultSetMetaData cachedMetaData = null;

        if (useServerFetch()) {
            this.results = createResultSetUsingServerFetch(sql);

            return this.results;
        }

        CancelTask timeoutTask = null;

        String oldCatalog = null;

        try {
            if (locallyScopedConn.getEnableQueryTimeouts() && this.timeoutInMillis != 0 && locallyScopedConn.versionMeetsMinimum(5, 0, 0)) {
                timeoutTask = new CancelTask(this);
                locallyScopedConn.getCancelTimer().schedule(timeoutTask, this.timeoutInMillis);
            }

            if (!locallyScopedConn.getCatalog().equals(this.currentCatalog)) {
                oldCatalog = locallyScopedConn.getCatalog();
                locallyScopedConn.setCatalog(this.currentCatalog);
            }

            //
            // Check if we have cached metadata for this query...
            //

            Field[] cachedFields = null;

            if (locallyScopedConn.getCacheResultSetMetadata()) {
                cachedMetaData = locallyScopedConn.getCachedMetaData(sql);

                if (cachedMetaData != null) {
                    cachedFields = cachedMetaData.fields;
                }
            }

            locallyScopedConn.setSessionMaxRows(this.maxRows);

            statementBegins();

            this.results = locallyScopedConn.execSQL(this, sql, this.maxRows, null, this.resultSetType, this.resultSetConcurrency,
                                                     createStreamingResultSet(), this.currentCatalog, cachedFields);

            if (timeoutTask != null) {
                if (timeoutTask.caughtWhileCancelling != null) {
                    throw timeoutTask.caughtWhileCancelling;
                }

                timeoutTask.cancel();

                locallyScopedConn.getCancelTimer().purge();

                timeoutTask = null;
            }

            synchronized (this.cancelTimeoutMutex) {
                if (this.wasCancelled) {
                    SQLException cause = null;

                    if (this.wasCancelledByTimeout) {
                        cause = new MySQLTimeoutException();
                    } else {
                        cause = new MySQLStatementCancelledException();
                    }

                    resetCancelledState();

                    throw cause;
                }
            }
        } finally {
            this.statementExecuting.set(false);

            if (timeoutTask != null) {
                timeoutTask.cancel();

                locallyScopedConn.getCancelTimer().purge();
            }

            if (oldCatalog != null) {
                locallyScopedConn.setCatalog(oldCatalog);
            }
        }

        this.lastInsertId = this.results.getUpdateID();

        if (cachedMetaData != null) {
            locallyScopedConn.initializeResultsMetadataFromCache(sql, cachedMetaData, this.results);
        } else {
            if (this.connection.getCacheResultSetMetadata()) {
                locallyScopedConn.initializeResultsMetadataFromCache(sql, null /* will be created */, this.results);
            }
        }

        return this.results;
    }
}
```

