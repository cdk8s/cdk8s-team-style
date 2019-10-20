
# Spring 基础

## 核心

- IoC 容器：管理组件的生命周期和依赖
    - 传统：组件A依赖B,B依赖C,C依赖D和B...，如果要得到组件A就需要相应的一层层的初始化其他组件，其他组件之间可能存在相互依赖这种情况，这种层层依赖的管理如果人工管理就会非常麻烦，而容器能帮助你管理组件，让你要一个对象轻轻松松
- BeanFactory 接口
    - Ioc 容器
    - 类通用工厂
    - Spring 框架底层使用
- ApplicationContext 接口
    - 应用上下文
    - 开发者使用
- 反射

## 资源文件（配置文件）加载、访问

- ClassPathResource
- FileSystemResource
- ServletContextResource
- UrlResource
- PropertiesLoaderUtils
- 底层：
    - java.lang.ClassLoader（反射）
    - java.lang.Class（反射）
    - java.io.InputStream
    - java.util.Properties

## 装配 Bean

- Spring 的启动过程实际上就是 IoC 容器初始化以及装配 Bean 的过程
- AbstractApplicationContext 中的 refresh() 方法定义了容器加载配置文件及装配 Bean 的过程
    - Spring Boot 多走了几步：SpringApplication.run 中执行了 refreshContext()

## 定义 Bean

- 基于 XML 方式：声明与实现类分离
- 基于注解方式
    - @Component
    - @Repository
    - @Service
    - @Controller
- 基于 POJO Java 类的配置
    - @Configuration
    - @Bean
- 通过编码方式：implements BeanFactoryPostProcessor
- 基于 Groovy DSL
    
## AOP

- 动态代理
    - JDK 动态代理
    - CGLib 动态代理

## 事务

- 本质：解决旧时代繁琐的数据库事务书写，抽象出一套简单的写法
- 数据库锁机制：表锁、行锁
- 数据库并发问题：
    - 3 种读问题
        - 幻读：事务1读取记录时事务2增加了记录并提交，事务1再次读取时可以看到事务2新增的记录； 
        - 不可重复读取：事务1读取记录时，事务2更新了记录并提交，事务1再次读取时可以看到事务2修改后的记录； 
        - 脏读：事务1更新了记录，但没有提交，事务2读取了更新后的行，然后事务T1回滚，现在T2读取无效。
    - 2 种数据更新问题
        - 第一类丢失更新
        - 第二类丢失更新
- java.lang.ThreadLocal 工作机制
- MySQL 4 种会话隔离级别
    - 未提交读(Read Uncommitted)：允许脏读，也就是可能读取到其他会话中未提交事务修改的数据
    - 提交读(Read Committed)：只能读取到已经提交的数据。Oracle等多数数据库默认都是该级别 (不重复读)
    - 可重复读(Repeated Read)：可重复读。在同一个事务内的查询都是事务开始时刻一致的，InnoDB默认级别。在SQL标准中，该隔离级别消除了不可重复读，但是还存在幻象读
    - 串行读(Serializable)：完全串行化的读，每次读都需要获得表级共享锁，读写相互都会阻塞
- Spring 5 种隔离级别：相应级别会自动添加合适的锁
    - ISOLATION_DEFAULT：这是一个 PlatfromTransactionManager 默认的隔离级别，使用数据库默认的事务隔离级别.
    - 另外四个与JDBC的隔离级别相对应；
        - ISOLATION_READ_UNCOMMITTED：这是事务最低的隔离级别，它充许别外一个事务可以看到这个事务未提交的数据。这种隔离级别会产生脏读，不可重复读和幻像读。
        - ISOLATION_READ_COMMITTED：保证一个事务修改的数据提交后才能被另外一个事务读取。另外一个事务不能读取该事务未提交的数据。这种事务隔离级别可以避免脏读出现，但是可能会出现不可重复读和幻像读。
        - ISOLATION_REPEATABLE_READ：这种事务隔离级别可以防止脏读，不可重复读。但是可能出现幻像读。它除了保证一个事务不能读取另一个事务未提交的数据外，还保证了避免下面的情况产生(不可重复读)。
        - ISOLATION_SERIALIZABLE：这是花费最高代价但是最可靠的事务隔离级别。事务被处理为顺序执行。除了防止脏读，不可重复读外，还避免了幻像读。
- 7 种传播行为类型：控制当前事务如何传播到被嵌套调用的目标服务
    - 支持当前事物：
        - 1）支持当前事物 —— PROPAGATION_REQUIRED：如果当前没有事物，就新建一个事务；如果有事物，就直接使用当前前事物、
        - 2）支持当前事物 ——PROPAGATION_SUPPORTS ：如果当前没有事务，就以非事务方式执行、
        - 3）支持当前事物 ——PROPAGATION_MANDATORY：如果当前没有事务，就抛出异常。
    - 不支持当前事物：
        - 1）不支持当前事物 —— PROPAGATION_REQUIRES_NEW：如果当前有事物，就将当前前事物挂起，新建一个事物、
        - 2）不支持当前事物 —— PROPAGATION_NOT_SUPPORTED：如果有事务，就将当前前事物挂起，并以非事务方式执行、
        - 3）不支持当前事物 —— PROPAGATION_NEVER：如果有事物，就抛异常，即必须以非事务方式执行。
    - 奇葩类型：
        - 其实这是支持当前事物的特例 —— PROPAGATION_NESTED： 如果有事物，也新建一个事务，以事务嵌套事物的方式执行。
- @Transactional 注解默认值
    - 事务传播行为：@Transactional(propagation=Propagation.PROPAGATION_REQUIRED)
    - 事务隔离级别：@Transactional(isolation=Isolation.ISOLATION_DEFAULT)
    - 读写事务属性：@Transactional(readOnly=false)
    - 回滚色泽：任何运行期异常会引发回滚（RuntimeException）
    - 类和方法都有注解，方法注解配置优先级更高