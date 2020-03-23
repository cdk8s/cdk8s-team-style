# Node 旧版本卸载（Windows）

### 第一步

```
npm cache clean --force
```

### 第二步

```
选择腾讯管家或其自身的卸载工具，卸载 node
```

### 第三步

```
找到类似下面文件夹，手动进行删除。如果不存在就不管它
C:\Program Files\nodejs
C:\Users\你的用户名\AppData\Roaming\npm
C:\Users\你的用户名\AppData\Roaming\npm-cache
C:\Users\你的用户名\.npmrc
C:\Users\你的用户名\AppData\Local\Temp\npm-*
```

### 第四步

```
删除掉 node 相关环境变量
删除环境变量 PATH 中 node 值
```
