

## CentOS 7 温度监控


```
安装包
yum install lm_sensors -y
 
传感器检测
sh -c "yes|sensors-detect"
 
加载模块
modprobe i2c-dev
modprobe coretemp

查看温度：
sensors

结果：
coretemp-isa-0000
Adapter: ISA adapter
Package id 0:  +39.0°C  (high = +74.0°C, crit = +84.0°C)
Core 0:        +32.0°C  (high = +74.0°C, crit = +84.0°C)
Core 1:        +28.0°C  (high = +74.0°C, crit = +84.0°C)
Core 2:        +33.0°C  (high = +74.0°C, crit = +84.0°C)
Core 3:        +32.0°C  (high = +74.0°C, crit = +84.0°C)
Core 4:        +32.0°C  (high = +74.0°C, crit = +84.0°C)
Core 5:        +31.0°C  (high = +74.0°C, crit = +84.0°C)
Core 8:        +31.0°C  (high = +74.0°C, crit = +84.0°C)
Core 9:        +31.0°C  (high = +74.0°C, crit = +84.0°C)
Core 10:       +29.0°C  (high = +74.0°C, crit = +84.0°C)
Core 11:       +30.0°C  (high = +74.0°C, crit = +84.0°C)
Core 12:       +32.0°C  (high = +74.0°C, crit = +84.0°C)
Core 13:       +31.0°C  (high = +74.0°C, crit = +84.0°C)
```

