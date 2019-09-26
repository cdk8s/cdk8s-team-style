# MyBatis 学习要点

## 核心组成

- SqlSessionFactoryBuilder
- SqlSessionFactory
- SqlSession
    - ExecutorType.SIMPLE 和 ExecutorType.BATCH 区别
- Mapper
- TypeHandler

## 返回

- resultType
- resultMap

## 参数

- @Param 注解
- parameterType
- parameterMap
- #{} 与 ${}

## 动态 SQL

- 精确匹配
- 模糊查询
- In 查询
- 时间区间
- 分页查询
- 批量插入
- 批量更新
- 关联查询
    - 一对一
    - 一对多
    - 多对多

## 拦截器（插件）

- @Intercepts 注解
- MetaObject
- Executor (update, query, flushStatements, commit, rollback, getTransaction, close, isClosed) 
- ParameterHandler (getParameterObject, setParameters) 
- ResultSetHandler (handleResultSets, handleOutputParameters) 
- StatementHandler (prepare, parameterize, batch, update, query) 
- 多个拦截器执行顺序

## 其他

- 关联查询：关联字段要是索引字段
- text 的对待思路
- 数据库连接池连接数数量压测


