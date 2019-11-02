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

@ApiModel(value = "SysUserCreateRequestParam")
@Setter
@Getter
@ToString
@JsonInclude(JsonInclude.Include.NON_NULL)
public class SysUserCreateRequestParam implements Serializable {

	private static final long serialVersionUID = -1L;

	@ApiModelProperty("用户名")
	@NotBlank(message = "用户名不能为空")
	@Length(min = 1, max = 50, message = "用户名长度不正确")
	private String username;

	@ApiModelProperty("用户密码")
	@NotBlank(message = "用户密码不能为空")
	@Length(min = 1, max = 50, message = "用户密码长度不正确")
	private String userPassword;

	@ApiModelProperty("邮箱地址")
	@NotBlank(message = "邮箱地址不能为空")
	@Length(min = 1, max = 50, message = "邮箱地址长度不正确")
	@Email(message = "邮箱地址格式不正确")
	private String userEmail;

	@ApiModelProperty("固话")
	@NotBlank(message = "固话不能为空")
	@Length(min = 1, max = 20, message = "固话长度不正确")
	private String telephone;

	@ApiModelProperty("手机号")
	@NotBlank(message = "手机号不能为空")
	@Length(min = 1, max = 20, message = "手机号长度不正确")
	private String mobilePhone;

	@ApiModelProperty("性别")
	@NotNull(message = "性别不能为空")
	@Range(min = 1, max = 4, message = "性别数值不正确")
	private Integer genderEnum;

}
```

- 常用非空注解说明

```
用在集合类上：
@NotEmpty(message = "objectList 不能为空")

用在 String 上：
@NotBlank(message = "该字段不能为空")

用在基础对象类型上，比如：Long，Integer。不要使用基本数据类型。
@NotNull(message = "该字段不能为空")

```

- 集合判断

```
@NotEmpty(message = "objectList 不能为空")
@Size(min = 1, message = "objectList 至少需要一个元素")
private List<UpdateStateBean> objectList;
```

```
@Length(max = 500, message = "链接地址最大长度为 500")

正则表达只能用于 String。
@Pattern(regexp = "[a-zA-z]+://[^\\s]*", message = "链接地址必须包含：http:// 或 https:// 等前缀")


@Range(min = 1, max = 100, message = "排序范围只能在 1 ~ 100 的正整数之间，值越小，排序越靠前")
@Length(min = 5, max = 50, message = "邮箱地址最小长度为 5，最大长度为 50，请重试")
@Email(message = "邮箱地址格式不正确")
@Min(value)	 | 被注释的元素必须是一个数字，其值必须大于等于指定的最小值
@Max(value)	| 被注释的元素必须是一个数字，其值必须小于等于指定的最大值
@DecimalMin(value)|	被注释的元素必须是一个数字，其值必须大于等于指定的最小值
@DecimalMax(value)|	被注释的元素必须是一个数字，其值必须小于等于指定的最大值

@Size(max, min)	|被注释的元素的大小必须在指定的范围内
@Digits (integer, fraction)|	被注释的元素必须是一个数字，其值必须在可接受的范围内
@Past |	被注释的元素必须是一个过去的日期
@Future |	被注释的元素必须是一个将来的日期
@URL(protocol=,host=,    port=, regexp=, flags=) |	被注释的字符串必须是一个有效的url
```



## 常用注解


```
@NotBlank(message = "链接地址不能为空")
@Length(max = 500, message = "链接地址最大长度为 500，请重试")
@Pattern(regexp = "[a-zA-z]+://[^\\s]*", message = "链接地址必须包含：http:// 或 https:// 等前缀")
private String url;


@NotNull(message = "排序不能为空")
@Range(min = 1, max = 100, message = "排序范围只能在 1 ~ 100 的正整数之间，值越小，排序越靠前")
private Integer rank;


@NotBlank(message = "邮箱地址不能为空")
@Length(min = 5, max = 50, message = "邮箱地址最小长度为 5，最大长度为 50，请重试")
@Email(message = "邮箱地址格式不正确")
private String email;


@Pattern(regexp="(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{5,10}",message="密码必须是5~10位数字和字母的组合")
private String password;
```



## 子对象嵌套场景

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

## 分组校验

- 分组校验只能用：`@Validated` 注解
- 场景：如果不同接口相同请求参数下需要不同的校验方式，如在add接口中id字段要为null(id后台生成)，update接口中id不能为null，怎么办？
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
