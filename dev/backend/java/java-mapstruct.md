
# MapStruct - Java bean 映射工具

- 官网：<https://mapstruct.org/>

## 依赖

- 项目 Maven 引入依赖
- Maven 仓库地址：<https://search.maven.org/search?q=org.mapstruct>

```
<!--mapstruct 对象属性映射工具 start-->
<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct</artifactId>
    <version>1.3.1.Final</version>
</dependency>
<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct-processor</artifactId>
    <version>1.3.1.Final</version>
    <scope>provided</scope>
</dependency>
<!--mapstruct 对象属性映射工具 end-->
```

## IntelliJ IDEA 支持

- IntelliJ IDEA 安装插件，在插件库中搜索：`mapstruct`
    - 或者官网地址：<https://plugins.jetbrains.com/plugin/10036-mapstruct-support/>
- 不需要额外配置

-------------------------------------------------------------------

## 实例

- 官网文档：<https://mapstruct.org/documentation/stable/reference/html/>


#### 常规映射

```
@Component
@Mapper(componentModel = "spring")
public interface SysUserMapStruct {

	@Mappings({
			@Mapping(target = "genderEnumString", expression = "java(com.cdk8s.sculptor.enums.GenderEnum.getDescriptionByCode(source.getGenderEnum()))"),
	})
	SysUserResponseDTO toResponseDTO(SysUser source);

	List<SysUserResponseDTO> toResponseDTOList(List<SysUser> source);

	SysUser createParamToEntity(SysUserCreateRequestParam source);

	SysUser updateParamToEntity(SysUserUpdateRequestParam source);

}
```

#### 规则继承（InheritInverseConfiguration）

```
@Mapper
public interface CarMapper {

    @Mapping(source = "numberOfSeats", target = "seatCount")
    CarDto entityToDTO(Car car);

    @InheritInverseConfiguration >> 在上一行 entityToDTO 中已经有一个 mapping 规则，在 dtoToEntity 中也要反向适用。这样可以省写点代码
    @Mapping(target = "numberOfSeats", ignore = true)
    Car dtoToEntity(CarDto carDto);
}
```

#### 其他

```
ignore
@Mapping(target = "userPassword", ignore = true)

expression
@Mapping(target = "genderEnumString", expression = "java(com.cdk8s.sculptor.enums.GenderEnum.getDescriptionByCode(source.getGenderEnum()))"),

defaultExpression
@Mapping(target="id", source="sourceId", defaultExpression = "java( UUID.randomUUID().toString() )")

如果为 null 的时候采用默认值
@Mapping(target = "stringProperty", source = "stringProp", defaultValue = "undefined")

常量，永远不变
@Mapping(target = "stringListConstants", constant = "jack-jill-tom")

格式转换
@Mapping(source = "price", numberFormat = "$#.00")
@Mapping(source = "manufacturingDate", dateFormat = "yyyy-MM-dd")
@Mapping(source = "power", numberFormat = "#.##E0") >> BigDecimal to String
```