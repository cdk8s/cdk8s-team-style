# Hibernate Validator 接口请求参数校验

## 添加依赖

- **默认：spring-boot-starter-web 已经集成，用 Spring Boot 和 Spring Cloud 可以不用主动依赖**
- 官网：<https://search.maven.org/search?q=g:org.hibernate.validator%20AND%20a:hibernate-validator&core=gav>

```xml
<dependency>
    <groupId>org.hibernate.validator</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>6.1.0.Final</version>
</dependency>
```

-------------------------------------------------------------------

## 添加校验规则示例

```
package com.cdk8s.sculptor.pojo.dto.param;

import com.fasterxml.jackson.annotation.JsonInclude;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.validator.constraints.Length;
import org.hibernate.validator.constraints.Range;
import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.io.Serializable;

@Setter
@Getter
@ToString
@JsonInclude(JsonInclude.Include.NON_NULL)
public class SysUserCreateRequestParam implements Serializable {

	private static final long serialVersionUID = -1L;

	@NotBlank(message = "用户名不能为空")
	@Length(min = 1, max = 50, message = "用户名长度不正确")
	private String username;

	@NotBlank(message = "用户密码不能为空")
	@Length(min = 1, max = 50, message = "用户密码长度不正确")
	private String userPassword;

	@NotBlank(message = "邮箱地址不能为空")
	@Length(min = 1, max = 50, message = "邮箱地址长度不正确")
	@Email(message = "邮箱地址格式不正确")
	private String userEmail;

	@NotBlank(message = "固话不能为空")
	@Length(min = 1, max = 20, message = "固话长度不正确")
	private String telephone;

	@NotBlank(message = "手机号不能为空")
	@Length(min = 1, max = 20, message = "手机号长度不正确")
	private String mobilePhone;

	@NotNull(message = "性别不能为空")
	@Range(min = 1, max = 4, message = "性别数值不正确")
	private Integer genderEnum;

}
```

## 带有子对象嵌套场景

- 在父对象上加有注解：`@Valid`

```
@Setter
@Getter
@ToString
@JsonInclude(JsonInclude.Include.NON_NULL)
public class OauthClientBatchUpdateStateRequestParam implements Serializable {

	private static final long serialVersionUID = 7650165913458884946L;

	@Valid
	@NotEmpty(message = "objectList 不能为空")
	@Size(min = 1, message = "objectList 至少需要一个元素")
	private List<UpdateStateBean> objectList;

	@Setter
	@Getter
	@ToString
	public static class UpdateStateBean implements Serializable{

		private static final long serialVersionUID = 1782063865018444303L;

		@NotNull(message = "ID 不能为空")
		@Pattern(regexp = "[1-9]\\d*$", message = "ID 必须是正整数")
		private Integer id;

		@NotNull(message = "状态不能为空")
		@Range(min = 1, max = 2, message = "状态值只能是 1：启用 和 2：禁用")
		private Integer stateEnum;
	}
}
```

## Controller 位置的注解

```
@RequestMapping(value = "/create", method = RequestMethod.POST)
public ResponseEntity<?> create(@Valid @RequestBody SysUserCreateRequestParam param) {
    sysUserService.create(sysUserMapStruct.createParamToEntity(param));
    return R.success();
}
```


-------------------------------------------------------------------

## 常用注解

- 官网内置约束文档：
    - Jakarta Bean 规范部分：<https://docs.jboss.org/hibernate/validator/6.1/reference/en-US/html_single/#validator-defineconstraints-spec>
    - Hibernate Validator 额外扩充部分：<https://docs.jboss.org/hibernate/validator/6.1/reference/en-US/html_single/#validator-defineconstraints-hv-constraints>
- 说明有哪些注解，以及可以修饰于什么对象场景

#### 不同非空注解说明

```
一般用在集合、Map、数组类上：
@NotEmpty(message = "objectList 不能为空")
private List<UpdateStateBean> objectList;

只能用在 String 上：
@NotBlank(message = "该字段不能为空")
private String username;

一般用在基础对象类型上，比如：Long，Integer（不推荐使用基础数据类型）
@NotNull(message = "该字段不能为空")
private Integer genderEnum;
```

#### 集合判断（带有嵌套对象判断）

```
@Valid
@NotEmpty(message = "objectList 不能为空")
@Size(min = 1, message = "objectList 至少需要一个元素")
private List<UpdateStateBean> objectList;
```

#### 字符串（String）

```
@NotBlank(message = "邮箱地址不能为空")
@Length(min = 1, max = 50, message = "邮箱地址长度不正确")
@Email(message = "邮箱地址格式不正确")
private String userEmail;

正则表达只能用于 String。
@Pattern(regexp = "[a-zA-z]+://[^\\s]*", message = "链接地址必须包含：http:// 或 https:// 等前缀")
```

#### 基础对象类型（Integer、Long 等）

```
@NotNull(message = "性别不能为空")
@Range(min = 1, max = 4, message = "性别数值不正确")
private Integer genderEnum;
```

#### 其他

```
大于等于 0.01（inclusive=包含）
@NotNull
@DecimalMin(value = "0.01", inclusive = true)
private BigDecimal greatOrEqualThan;

小于等于 1.01（inclusive=包含）
@NotNull
@DecimalMax(value = "1.01", inclusive = true)
private BigDecimal greatOrEqualThan;

@Past 被注释的元素必须是一个过去的日期
@Future 被注释的元素必须是一个将来的日期
@FutureOrPresent
@PastOrPresent
都是对日期的数据类型有要求，Long 类型的时间戳是不支持（官网有说明）

@Negative 必须是负数，0 不算负数
@NegativeOrZero 负数或 0
@Positive 必须是正数，0 不算正数
@PositiveOrZero 正数或 0
适用于：数值类型，包含：BigDecimal

@SafeHtml(whitelistType= , additionalTags=, additionalTagsWithAttributes=, baseURI=)
检查否包含潜在的恶意片段（适用于：String 类型）

@URL(protocol=, host=, port=, regexp=, flags=)
地址校验（适用于：String 类型）

其他常用：
@Pattern(regexp = "[a-zA-z]+://[^\\s]*", message = "链接地址必须包含：http:// 或 https:// 等前缀")
@Range(min = 1, max = 100, message = "排序范围只能在 1 ~ 100 的正整数之间，值越小，排序越靠前")
@Email(message = "邮箱地址格式不正确")
@Pattern(regexp="(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{5,10}",message="密码必须是5~10位数字和字母的组合")
```


-------------------------------------------------------------------

## 分组校验

- 分组校验只能用：`@Validated` 注解
- 场景：如果不同接口相同请求参数下需要不同的校验方式，如在 add 接口中 id 字段要为 null(id 后台生成)，update 接口中 id 不能为 null，怎么办？
- 创建组：

```
public interface AddGroup {
}

public interface UpdateGroup {
}
```

- 字段校验添加分组

```
@Null(message = "id必须为null", groups = AddGroup.class)
@NotNull(message = "id不能为null", groups = UpdateGroup.class)
@Length(max = 20, message = "id长度不能超过20", groups = UpdateGroup.class)
private String id;
```

- 接口指定校验组

```
@RequestMapping(value = "/add", method = RequestMethod.POST)
public boolean add(@Validated(AddGroup.class) @RequestBody UserDTO UserDTO) {

}

@RequestMapping(value = "/update", method = RequestMethod.POST)
public boolean update(@Validated(UpdateGroup.class) @RequestBody UserDTO UserDTO) {

}
```

-------------------------------------------------------------------

## 自定义约束注解

- 可以参考：
- <https://www.jianshu.com/p/86c318c023cb>
- <https://juejin.im/post/5d3fbeb46fb9a06b317b3c48>
- <http://blog.healerjean.com/springboot/2019/04/18/%E8%87%AA%E5%AE%9A%E4%B9%89%E5%B7%A5%E5%85%B7%E7%B1%BB%E5%AE%9E%E7%8E%B0validate%E5%8F%82%E6%95%B0%E6%A0%A1%E9%AA%8C/>
