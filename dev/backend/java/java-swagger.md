
# Swagger 介绍

- 官网：<https://swagger.io/>

## 依赖

- 项目 Maven 引入依赖
- Maven 仓库地址：<https://search.maven.org/search?q=g:io.springfox>

```
<!--swagger 依赖 start-->
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId>
    <version>2.9.2</version>
    <exclusions>
        <exclusion>
            <artifactId>guava</artifactId>
            <groupId>com.google.guava</groupId>
        </exclusion>
        <exclusion>
            <artifactId>mapstruct</artifactId>
            <groupId>org.mapstruct</groupId>
        </exclusion>
    </exclusions>
</dependency>

<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.9.2</version>
</dependency>
<!--swagger 依赖 end-->
```

-------------------------------------------------------------------

## 常用场景


#### 请求参数

```
package com.cdk8s.sculptor.pojo.dto.param;

import com.cdk8s.sculptor.pojo.dto.param.bases.PageParam;
import com.fasterxml.jackson.annotation.JsonInclude;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.validator.constraints.Range;

@ApiModel(value = "SysUserPageQueryParam")
@Setter
@Getter
@ToString(callSuper = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class SysUserPageQueryParam extends PageParam {

	private static final long serialVersionUID = -1L;

	@ApiModelProperty("ID")
	private String id;

	@ApiModelProperty("用户名")
	private String username;

	@ApiModelProperty("邮箱地址")
	private String userEmail;

	@ApiModelProperty("固话")
	private String telephone;

	@ApiModelProperty("手机号")
	private String mobilePhone;

	@ApiModelProperty("性别")
	@Range(min = 1, max = 4, message = "性别")
	private Integer genderEnum;

	@ApiModelProperty("注册方式")
	@Range(min = 1, max = 4, message = "注册方式")
	private Integer registerTypeEnum;

	@ApiModelProperty("注册来源")
	@Range(min = 1, max = 6, message = "注册来源")
	private Integer registerOriginEnum;

	@ApiModelProperty("状态")
	@Range(min = 1, max = 2, message = "启用状态数值不正确")
	private Integer stateEnum;

	@ApiModelProperty(hidden = true)
	private Integer deleteEnum = 1;

}

```


#### 响应参数


```
package com.cdk8s.sculptor.pojo.dto.response;

import com.cdk8s.sculptor.pojo.entity.bases.BaseEntity;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@ApiModel(value = "SysUserResponseDTO")
@Setter
@Getter
@ToString(callSuper = true)
public class SysUserResponseDTO extends BaseEntity {

	private static final long serialVersionUID = -1L;

	@ApiModelProperty("用户名")
	private String username;

	@ApiModelProperty("邮箱地址")
	private String userEmail;

	@ApiModelProperty("固话")
	private String telephone;

	@ApiModelProperty("手机号")
	private String mobilePhone;

	@ApiModelProperty("性别")
	private Integer genderEnum;

	@ApiModelProperty("性别")
	private String genderEnumString;

}
```

#### Controller 接口

```
package com.cdk8s.sculptor.controller;

import com.cdk8s.sculptor.aop.eventlog.EventLog;
import com.cdk8s.sculptor.constant.GlobalVariable;
import com.cdk8s.sculptor.mapstruct.SysUserMapStruct;
import com.cdk8s.sculptor.pojo.dto.param.SysUserCreateRequestParam;
import com.cdk8s.sculptor.pojo.dto.param.SysUserPageQueryParam;
import com.cdk8s.sculptor.pojo.dto.param.SysUserUpdateRequestParam;
import com.cdk8s.sculptor.pojo.dto.param.bases.BatchUpdateStateRequestParam;
import com.cdk8s.sculptor.pojo.dto.param.bases.IdListRequestParam;
import com.cdk8s.sculptor.pojo.dto.response.SysUserResponseDTO;
import com.cdk8s.sculptor.service.SysUserService;
import com.cdk8s.sculptor.util.response.biz.R;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

@Api(value = "SysUser API")
@Slf4j
@RestController
@RequestMapping("/api/sysUser")
public class SysUserController {

	@Autowired
	private SysUserService sysUserService;

	@Autowired
	private SysUserMapStruct sysUserMapStruct;

	// =====================================查询业务 start=====================================

	@ApiResponses({
			@ApiResponse(code = 200, message = "Core Object Model", response = SysUserResponseDTO.class)
	})
	@RequestMapping(value = "/detail", method = RequestMethod.GET)
	public ResponseEntity<?> detail(@RequestParam Long id) {
		return R.success(sysUserService.findOneById(id));
	}

	@ApiResponses({
			@ApiResponse(code = 200, message = "Core Object Model", response = SysUserResponseDTO.class)
	})
	@RequestMapping(value = "/page", method = RequestMethod.POST)
	public ResponseEntity<?> page(@Valid @RequestBody SysUserPageQueryParam param) {
		return R.success(sysUserService.findPageByParam(param));
	}

	// =====================================查询业务 end=====================================
	// =====================================操作业务 start=====================================

	@EventLog(message = "创建 sysUser 对象", operateType = GlobalVariable.OPERATE_TYPE_CREATE)
	@RequestMapping(value = "/create", method = RequestMethod.POST)
	public ResponseEntity<?> create(@Valid @RequestBody SysUserCreateRequestParam param) {
		sysUserService.create(sysUserMapStruct.createParamToEntity(param));
		return R.success();
	}

	@EventLog(message = "更新 sysUser 对象", operateType = GlobalVariable.OPERATE_TYPE_UPDATE_INFO)
	@RequestMapping(value = "/update", method = RequestMethod.POST)
	public ResponseEntity<?> update(@Valid @RequestBody SysUserUpdateRequestParam param) {
		sysUserService.update(sysUserMapStruct.updateParamToEntity(param));
		return R.success();
	}

	@EventLog(message = "批量更新 sysUser 状态", operateType = GlobalVariable.OPERATE_TYPE_UPDATE_STATE)
	@RequestMapping(value = "/batchUpdateState", method = RequestMethod.POST)
	public ResponseEntity<?> batchUpdateState(@Valid @RequestBody BatchUpdateStateRequestParam param) {
		sysUserService.batchUpdateState(param.getStateEnum(), param.getIdList());
		return R.success();
	}

	@EventLog(message = "批量删除 sysUser 对象", operateType = GlobalVariable.OPERATE_TYPE_DELETE)
	@RequestMapping(value = "/batchDelete", method = RequestMethod.POST)
	public ResponseEntity<?> batchDelete(@Valid @RequestBody IdListRequestParam param) {
		sysUserService.batchDelete(param.getIdList());
		return R.success();
	}

	// =====================================操作业务 end=====================================
	// =====================================私有方法 start=====================================

	// =====================================私有方法 end=====================================

}

```

-------------------------------------------------------------------

## Swagger 衍生出来的项目

- [knife4j（前身叫做 swagger-bootstrap-ui）](https://gitee.com/xiaoym/knife4j)
- [swagger2markup](https://github.com/Swagger2Markup/swagger2markup)
