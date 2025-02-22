# Bash 常用命令

## 常用权限

```
三位数：分别为所有者（Owner）、所属组（Group）、其他用户（Others）
0：没有权限
1：执行权限
2：写权限
3：写和执行权限
4：读权限
5：读和执行权限
6：读和写权限
7：读、写和执行权限
```

## 基础常用命令

- `某个命令 --h`，对这个命令进行解释
- `某个命令 --help`，解释这个命令(更详细)
- `man某个命令`，文档式解释这个命令(更更详细)(执行该命令后,还可以按/+关键字进行查询结果的搜索)
- `Ctrl + c`，结束命令
- `TAB键`，自动补全命令（按一次自动补全，连续按两次，提示所有以输入开头字母的所有命令）
- `键盘上下键`，输入临近的历史命令
- `history`，查看所有的历史命令
- `Ctrl + r`，进入历史命令的搜索功能模式
- `clear`，清除屏幕里面的所有命令
- `pwd`，显示当前目录路径（常用）
- `firefox&`，最后后面的 **&** 符号，表示使用后台方式打开 Firefox，然后显示该进程的 PID 值
- `jobs`，查看后台运行的程序列表
- `ifconfig`，查看内网 IP 等信息（常用）
- `curl ifconfig.me`，查看外网 IP 信息
- `curl ip.cn`，查看外网 IP 信息
- `locate 搜索关键字`，快速搜索系统文件/文件夹（类似 Windows 上的 everything 索引式搜索）（常用）
	- `updatedb`，配合上面的 locate，给 locate 的索引更新（locate 默认是一天更新一次索引）（常用）
- `date`，查看系统时间（常用）
	- `date -s20080103`，设置日期（常用）
	- `date -s18:24`，设置时间，如果要同时更改 BIOS 时间，再执行 `hwclock --systohc`（常用）
- `cal`，在终端中查看日历，肯定没有农历显示的
- `uptime`，查看系统已经运行了多久，当前有几个用户等信息（常用）
- `cat 文件路名`，显示文件内容（属于打印语句）
- `cat -n 文件名`，显示文件，并每一行内容都编号
- `more 文件名`，用分页的方式查看文件内容（按 space 翻下一页，按 *Ctrl + B* 返回上页）
- `less`文件名，用分页的方式查看文件内容（带上下翻页）
	- 按 **j** 向下移动，按 **k** 向上移动
	- 按 **/** 后，输入要查找的字符串内容，可以对文件进行向下查询，如果存在多个结果可以按 **n** 调到下一个结果出
	- 按 **？** 后，输入要查找的字符串内容，可以对文件进行向上查询，如果存在多个结果可以按 **n** 调到下一个结果出
- `shutdown`
    - `shutdown -hnow`，立即关机
    - `shutdown -h+10`，10 分钟后关机
    - `shutdown -h23:30`，23:30 关机
    - `shutdown -rnew`，立即重启
- `poweroff`，立即关机（常用）
- `reboot`，立即重启（常用）
- `zip mytest.zip /opt/test/`，把 /opt 目录下的 test/ 目录进行压缩，压缩成一个名叫 mytest 的 zip 文件
	- `unzip mytest.zip`，对 mytest.zip 这个文件进行解压，解压到当前所在目录
	- `unzip mytest.zip -d /opt/setups/`，对 mytest.zip 这个文件进行解压，解压到 /opt/setups/ 目录下
- `tar -cvf mytest.tar mytest/`，对 mytest/ 目录进行归档处理（归档和压缩不一样）
- `tar -xvf mytest.tar`，释放 mytest.tar 这个归档文件，释放到当前目录
	- `tar -xvf mytest.tar -C /opt/setups/`，释放 mytest.tar 这个归档文件，释放到 /opt/setups/ 目录下
- `last`，显示最近登录的帐户及时间
- `lastlog`，显示系统所有用户各自在最近登录的记录，如果没有登录过的用户会显示 **从未登陆过**
- `ls`，列出当前目录下的所有没有隐藏的文件 / 文件夹。
	- `ls -a`，列出包括以.号开头的隐藏文件 / 文件夹（也就是所有文件）
	- `ls -R`，显示出目录下以及其所有子目录的文件 / 文件夹（递归地方式，不显示隐藏的文件）
	- `ls -a -R`，显示出目录下以及其所有子目录的文件 / 文件夹（递归地方式，显示隐藏的文件）
	- `ls -al`，列出目录下所有文件（包含隐藏）的权限、所有者、文件大小、修改时间及名称（也就是显示详细信息）
	- `ls -ld 目录名`，显示该目录的基本信息
	- `ls -t`，依照文件最后修改时间的顺序列出文件名。
	- `ls -F`，列出当前目录下的文件名及其类型。以 **/** 结尾表示为目录名，以 **\*** 结尾表示为可执行文件，以 **@** 结尾表示为符号连接
	- `ls -lg`，同上，并显示出文件的所有者工作组名。
	- `ls -lh`，查看文件夹类文件详细信息，文件大小，文件修改时间
	- `ls /opt | head -5`，显示 opt 目录下前 5 条记录
	- `ls -l | grep '.jar'`，查找当前目录下所有 jar 文件
	- `ls -l /opt |grep "^-"|wc -l`，统计 opt 目录下文件的个数，不会递归统计
	- `ls -lR /opt |grep "^-"|wc -l`，统计 opt 目录下文件的个数，会递归统计
	- `ls -l /opt |grep "^d"|wc -l`，统计 opt 目录下目录的个数，不会递归统计
	- `ls -lR /opt |grep "^d"|wc -l`，统计 opt 目录下目录的个数，会递归统计
	- `ls -lR /opt |grep "js"|wc -l`，统计 opt 目录下 js 文件的个数，会递归统计
	- `ls -l`，列出目录下所有文件的权限、所有者、文件大小、修改时间及名称（也就是显示详细信息，不显示隐藏文件）。显示出来的效果如下：
    
``` nginx
-rwxr-xr-x. 1 root root 4096 3月 26 10:57，其中最前面的 - 表示这是一个普通文件
lrwxrwxrwx. 1 root root 4096 3月 26 10:57，其中最前面的 l 表示这是一个链接文件，类似 Windows 的快捷方式
drwxr-xr-x. 5 root root 4096 3月 26 10:57，其中最前面的 d 表示这是一个目录
```

- `cd`，目录切换
	- `cd ..`，改变目录位置至当前目录的父目录(上级目录)。
	- `cd ~`，改变目录位置至用户登录时的工作目录。
	- `cd 回车`，回到家目录
	- `cd -`，上一个工作目录
	- `cd dir1/`，改变目录位置至 dir1 目录下。
	- `cd ~user`，改变目录位置至用户的工作目录。
	- `cd ../user`，改变目录位置至相对路径user的目录下。
	- `cd /../..`，改变目录位置至绝对路径的目录位置下。
- `cp 源文件 目标文件`，复制文件
	- `cp -r 源文件夹 目标文件夹`，复制文件夹
	- `cp -r -v 源文件夹 目标文件夹`，复制文件夹(显示详细信息，一般用于文件夹很大，需要查看复制进度的时候)
	- `cp /usr/share/easy-rsa/2.0/keys/{ca.crt,server.{crt,key},dh2048.pem,ta.key} /etc/openvpn/keys/`，复制同目录下花括号中的文件
	- `cp -arp /opt/* /mnt/` 复制文件、文件夹，以及它们的属性（最全面的复制）
        - -a：此选项通常在复制目录时使用，它保留链接、文件属性，并复制目录下的所有内容
        - -p：除复制文件的内容外，还把修改时间和访问权限也复制到新文件中。
        - -r：若给出的源文件是一个目录文件，此时将复制该目录下所有的子目录和文件。
- `rsync`，远程传输文件
    - 本地传输
        - `rsync -a source destination`，传输文件夹
            - -a：归档模式，表示递归传输并保持文件属性，包括递归目录、文件元信息。等同于"-rtopgDl"。
            - 如果目标目录不存在则会自动创建目录
            - 最终效果会变成：`destination/source`
        - `rsync -a source/ destination`，传输文件夹
            - 效果会变成：`destination 就是代表 source 目录`
    - 远程传输（默认使用 SSH 进行远程登录和数据传输，已经已经做了免密是不需要输入认证信息的）
        - `rsync -a source/ username@remote_host:destination`，传输文件夹
- `tar cpf - . | tar xpf - -C /opt`，复制当前所有文件到 /opt 目录下，一般如果文件夹文件多的情况下用这个更好，用 cp 比较容易出问题
- `mv 文件 目标文件夹`，移动文件到目标文件夹
	- `mv 文件`，不指定目录重命名后的名字，用来重命名文件
- `touch 文件名`，创建一个空白文件/更新已有文件的时间(后者少用)
- `mkdir 文件夹名`，创建文件夹
- `mkdir -p /opt/setups/nginx/conf/`，创建一个名为 conf 文件夹，如果它的上级目录 nginx 没有也会跟着一起生成，如果有则跳过
- `rmdir 文件夹名`，删除文件夹(只能删除文件夹里面是没有东西的文件夹)
- `rm 文件`，删除文件
	- `rm -r 文件夹`，删除文件夹
	- `rm -r -i 文件夹`，在删除文件夹里的文件会提示(要的话,在提示后面输入yes)
	- `rm -r -f 文件夹`，强制删除
	- `rm -r -f 文件夹1/ 文件夹2/ 文件夹3/`删除多个
- `find`，高级查找
	- `find . -name *lin*`，其中 . 代表在当前目录找，-name 表示匹配文件名 / 文件夹名，\*lin\* 用通配符搜索含有lin的文件或是文件夹
	- `find . -iname *lin*`，其中 . 代表在当前目录找，-iname 表示匹配文件名 / 文件夹名（忽略大小写差异），\*lin\* 用通配符搜索含有lin的文件或是文件夹
	- `find / -name *.conf`，其中 / 代表根目录查找，*.conf代表搜索后缀会.conf的文件
	- `find /opt -name .oh-my-zsh`，其中 /opt 代表目录名，.oh-my-zsh 代表搜索的是隐藏文件 / 文件夹名字为 oh-my-zsh 的
	- `find /opt -name "myFileName" -print 2>/dev/null`，后面的 `-print 2>/dev/null` 表示把没有权限相关的提示结果去掉
	- `find /opt -type f -iname .oh-my-zsh`，其中 /opt 代表目录名，-type f 代表只找文件，.oh-my-zsh 代表搜索的是隐藏文件名字为 oh-my-zsh 的
	- `find /opt -type d -iname .oh-my-zsh`，其中 /opt 代表目录名，-type d 代表只找目录，.oh-my-zsh 代表搜索的是隐藏文件夹名字为 oh-my-zsh 的
	- `find . -name "lin*" -exec ls -l {} \;`，当前目录搜索lin开头的文件，然后用其搜索后的结果集，再执行ls -l的命令（这个命令可变，其他命令也可以），其中 -exec 和 {} \; 都是固定格式
	- `find / -name "*tower*" -exec rm {} \;`，找到文件并删除
	- `find / -name "*tower*" -exec mv {} /opt \;`，找到文件并移到 opt 目录
	- `find . -name "*" |xargs grep "youmeek"`，递归查找当前文件夹下所有文件内容中包含 youmeek 的文件
	- `find . -name "node_modules" |xargs rm -rf`，递归查找当前文件夹下所有 node_modules 文件夹进行删除
	- `find . -size 0 | xargs rm -f &`，删除当前目录下文件大小为0的文件
	- `find /opt -type f -size +800M  -print0 | xargs -0 du -h | sort -nr`，找出 /opt 目录下大于 800 M 的文件
	- `du -hm --max-depth=2 | sort -nr | head -12`，找出系统中占用容量最大的前 12 个目录
- `cat /etc/resolv.conf`，查看 DNS 设置
- `netstat -tlunp`，查看当前运行的服务，同时可以查看到：运行的程序已使用端口情况
- `env`，查看所有系统变量
- `export`，查看所有系统变量
- `echo`
	- `echo $JAVA_HOME`，查看指定系统变量的值，这里查看的是自己配置的 JAVA_HOME。
	- `echo "字符串内容"`，输出 "字符串内容"
	- `echo > aa.txt`，清空 aa.txt 文件内容（类似的还有：`: > aa.txt`，其中 : 是一个占位符, 不产生任何输出）
- `unset $JAVA_HOME`，删除指定的环境变量
- `ln -s /opt/data /opt/logs/data`，表示给 /opt/logs 目录下创建一个名为 data 的软链接，该软链接指向到 /opt/data
- `more` 查看文件内容，按空格显示下一屏，按回车向下移动一行。
- `grep`
	- `shell grep -H '安装' *.sh`，查找当前目录下所有 sh 类型文件中，文件内容包含 `安装` 的当前行内容
	- `grep 'test' java*`，显示当前目录下所有以 java 开头的文件中包含 test 的行
	- `grep 'test' spring.ini docker.sh`，显示当前目录下 spring.ini docker.sh 两个文件中匹配 test 的行
    - `grep -rH --include='*.xml' 'device' .` 寻找当前文件夹以及子文件夹下所有 xml 文件中包含有单词：device 的内容，返回结果第一行是文件名，第二行是内容。
        - `-H` 强制显示文件名
        - `--include='*.xml'` 仅匹配 XML 文件
        - `-r` 递归搜索子目录
    - `grep -B 100 -A 200 "测试句子" info.log | more` 寻找文件中某个句子，找就显示该句子前100行，和后200行的内容，把结果传给 more 展示
    - 更多参数
        - `-i` 搜索时忽略大小写
        - `-n` 显示行号
        - `-r` 递归搜索
        - `-E` 支持扩展正则
        - `V` 反向选择，不显示匹配行信息
        - `w` 只匹配整个单词，比如搜索 love，文件里面的 lover 是不会被匹配到的 
        - `x` 只匹配整个行
- `sed`
      - `sed -n -e '/pyth.*/p' aa.txt` 打印文件中匹配正则 pyth.* 规则的内容，p 是打印的意思（只有一个规则的时候 -e 是可以省略的，但是不建议）
      - `sed -n -e '/python/p' -e '/PYTHON/p' aa.txt` 打印文件中匹配 python 大写或小写的行内容，p 是打印的意思
      - `sed -n -r '/python|PYTHON/p' aa.txt` 打印文件中匹配 python 大写或小写的行内容，p 是打印的意思，这里用的是扩展表达式，不是正则表达式
      - `sed -i 's/python/java/g' aa.txt` 把 python 字眼改为 java
- `ps`
	- `ps –ef|grep java`，查看当前系统中有关 java 的所有进程
	- `ps -ef|grep --color java`，高亮显示当前系统中有关 java 的所有进程
    - `ps -e -o pid,stime,time,cmd --sort=start_time` 根据启动时间排序显示进程
      - `-e 显示所有进程`
      - `-o pid,stime,time,comm,cmd: 指定输出的格式，包括进程ID、启动时间、已运行时间、进程名、执行命令`
      - `--sort=start_time: 根据启动时间进行排序。`

- `kill`
	- `kill 1234`，结束 pid 为 1234 的进程
	- `kill -9 1234`，强制结束 pid 为 1234 的进程（慎重）
	- `killall java`，结束同一进程组内的所有为 java 进程
	- `ps -ef|grep hadoop|grep -v grep|cut -c 9-15|xargs kill -9`，结束包含关键字 hadoop 的所有进程
- `head`
	- `head -n 10 spring.ini`，查看当前文件的前 10 行内容
- `tail`
	- `tail -n 10 spring.ini`，查看当前文件的后 10 行内容
	- `tail -200f 文件名`，查看文件被更新的新内容尾 200 行，如果文件还有在新增可以动态查看到（一般用于查看日记文件）
- `while sleep 2; do clean; ls; done` 每隔2秒不断执行 ls 命令

## 用户、权限-相关命令

- linux 的权限分为 rwx。r 代表：可读，w 代表：可写，x 代表：可执行
- 这三个权限都可以转换成数值表示，r = 4，w = 2，x = 1，- = 0，所以总和是 7，也就是最大权限。第一个 7 是所属主（user）的权限，第二个 7 是所属组（group）的权限，最后一位 7 是非本群组用户（others）的权限。
- 下面根据实战来描述这个数字：

```
drwxr-xr-x 2 root root 4.0K Jun 22 00:35 test
因为 test 是目录，所以第一个字母是 d，代表 directory
接下来的 rwx 代表所属主拥有：r可读、w可写、x可执行，数值之和是：4+2+1=7
再接下来的 r-x 代表所属组拥有：r可读、x可执行，数值之和是：4+0+1=5
再接下来的 r-x 代表非本群组用户拥有：r可读、x可执行，数值之和是：4+0+1=5
所有总的权限赋值可以这样写：chmod -R 755 test
-------------------------------------------------------------------
-rw-r--r-- 1 root root    0 Jun 22 00:36 aa.txt
因为 aa.txt 是文件，所以第一个字母是 - 横杆
接下来的 rw- 代表所属主拥有：r可读、w可写，数值之和是：4+2=6
再接下来的 r-- 代表所属组拥有：r可读，数值之和是：4+0+0=4
再接下来的 r-- 代表非本群组用户拥有：r可读，数值之和是：4+0+0=4
所有总的权限赋值可以这样写：chmod 644 aa.txt
```

- 使用 pem 证书登录：`ssh -i /opt/mykey.pem root@192.168.0.70`
	- 证书权限不能太大，不然无法使用：`chmod 600 mykey.pem`
- `hostname`，查看当前登陆用户全名
- `cat /etc/group`，查看所有组
- `cat /etc/passwd`，查看所有用户
- `groups youmeek`，查看 youmeek 用户属于哪个组
- `useradd youmeek -g judasn`，添加用户并绑定到 judasn 组下
- `userdel -r youmeek`，删除名字为 youmeek 的用户
	- 参数：`-r`，表示删除用户的时候连同用户的家目录一起删除
- 修改普通用户 youmeek 的权限跟 root 权限一样：
	- 常用方法（原理是把该用户加到可以直接使用 sudo 的一个权限状态而已）：
		- 编辑配置文件：`vim /etc/sudoers`
		- 找到 98 行（预估），有一个：`root    ALL=(ALL)   ALL`，在这一行下面再增加一行，效果如下：

		``` nginx
		root    ALL=(ALL)   ALL
		youmeek    ALL=(ALL)   ALL
		```

	- 另一种方法：
		- 编辑系统用户的配置文件：`vim /etc/passwd`，找到 **root** 和 **youmeek** 各自开头的那一行，比如 root 是：`root:x:0:0:root:/root:/bin/zsh`，这个代表的含义为：*用户名:密码:UserId:GroupId:描述:家目录:登录使用的 shell*
		- 通过这两行对比，我们可以直接修改 youmeek 所在行的 UserId 值 和 GroupId 值，都改为 0。
- `groupadd judasn`，添加一个名为 judasn 的用户组
- `groupdel judasn`，删除一个名为 judasn 的用户组（前提：先删除组下面的所有用户）
- `usermod 用户名 -g 组名`，把用户修改到其他组下
- `passwd youmeek`，修改 youmeek 用户的密码（前提：只有 root 用户才有修改其他用户的权限，其他用户只能修改自己的）
- `chmod 777 文件名/目录`，给指定文件增加最高权限，系统中的所有人都可以进行读写。
- `chmod -R 777 目录` 表示递归目录下的所有文件夹，都赋予 777 权限
- `chown myUsername:myGroupName myFile` 表示修改文件所属用户、组
- `chown -R myUsername:myGroupName myFolder` 表示递归修改指定目录下的所有文件权限
- `su`：切换到 root 用户，终端目录还是原来的地方（常用）
	- `su -`：切换到 root 用户，其中 **-** 号另起一个终端并切换账号
	- `su 用户名`，切换指定用户帐号登陆，终端目录还是原来地方。
	- `su - 用户名`，切换到指定用户帐号登陆，其中 **-** 号另起一个终端并切换账号
- `exit`，注销当前用户（常用）
- `sudo 某个命令`，使用管理员权限使用命令，使用 sudo 回车之后需要输入当前登录账号的密码。（常用）
- `passwd`，修改当前用户密码（常用）
- 添加临时账号，并指定用户根目录，并只有可读权限方法
	- 添加账号并指定根目录（用户名 tempuser）：`useradd -d /data/logs -m tempuser`
	- 设置密码：`passwd tempuser` 回车设置密码
	- 删除用户（该用户必须退出 SSH 才能删除成功），也会同时删除组：`userdel tempuser`


## 磁盘管理

- `df -h`，自动以合适的磁盘容量单位查看磁盘大小和使用空间
	- `df -k`，以磁盘容量单位 K 为数值结果查看磁盘使用情况
	- `df -m`，以磁盘容量单位 M 为数值结果查看磁盘使用情况
- `du -sh /opt`，查看 opt 这个文件夹大小 （h 的意思 human-readable 用人类可读性较好方式显示，系统会自动调节单位，显示合适大小的单位）
- `du -sh ./*`，查看当前目录下所有文件夹大小（**常用**）（h 的意思 human-readable 用人类可读性较好方式显示，系统会自动调节单位，显示合适大小的单位）
- `du -sh /opt/setups/`，显示 /opt/setups/ 目录所占硬盘空间大小（s 表示 –summarize 仅显示总计，即当前目录的大小。h 表示 –human-readable 以 KB，MB，GB 为单位，提高信息的可读性）
- `mount /dev/sdb5 /newDir/`，把分区 sdb5 挂载在根目录下的一个名为 newDir 的空目录下，需要注意的是：这个目录最好为空，不然已有的那些文件将看不到，除非卸载挂载。
	- 挂载好之后，通过：`df -h`，查看挂载情况。
- `umount /newDir/`，卸载挂载，用目录名
	- 如果这样卸载不了可以使用：`umount -l /newDir/`
- `umount /dev/sdb5`，卸载挂载，用分区名

-------------------------------------------------------------------

## ECS 数据盘分区

- 参考：<https://help.aliyun.com/document_detail/25426.html>
- 先看已经挂载在服务器上的磁盘有多少：`fdisk -l`

```
Disk /dev/vda: 42.9 GB, 42949672960 bytes, 83886080 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x000c0010

   Device Boot      Start         End      Blocks   Id  System
/dev/vda1   *        2048    83886046    41941999+  83  Linux

Disk /dev/vdb: 21.5 GB, 21474836480 bytes, 41943040 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```

- 这里有 /dev/vda 和 /dev/vdb
- 如果发现没找到，则参考这篇文章进行挂载：[挂载数据盘](https://help.aliyun.com/document_detail/25446.html)
- 接着运行以下命令分区数据盘：
```
fdisk -u /dev/vdb

根据提示输入 n 创建一个新分区

接着根据提示输入 p 选择分区类型为主分区

接着输入分区编号：1

接着输入可用的扇区编号，这里直接回车采用默认值，或者自己输入 2048

接着输入最后一个扇区编号，这里直接回车采用默认值

最后输入 w 开始分区，并退出

整个流程如下：
Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p

Partition number (1-4, default 1): 1

First sector (2048-41943039, default 2048): 2048

Last sector, +sectors or +size{K,M,G} (2048-41943039, default 41943039):
Using default value 41943039
Partition 1 of type Linux and of size 20 GiB is set

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```

- 接着我们查看新分区情况：`fdisk -lu /dev/vdb`

```
Disk /dev/vdb: 21.5 GB, 21474836480 bytes, 41943040 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x3d24a4a9

   Device Boot      Start         End      Blocks   Id  System
/dev/vdb1            2048    41943039    20970496   83  Linux
```

- 接着为分区创建文件系统，CentOS 7 我们一般选择 ext4 文件系统：`mkfs -t ext4 /dev/vdb1`
- 接着配置 /etc/fstab 文件并挂载分区，让开启自动挂载分区

```
先备份
cp /etc/fstab /etc/fstab-20210115.bak

然后我们假设最终要挂载的一个新路径是：/mnt
这里我们用root用户可以直接使用以下命令修改配置文件，本质就是获取到 vdb1 的 UUID 自动补充成一个字符串写入到文件最底部
echo `blkid /dev/vdb1 | awk '{print $2}' | sed 's/\"//g'` /mnt ext4 defaults 0 0 >> /etc/fstab

然后挂载分区：
mount /dev/vdb1 /mnt

最后检查 /mnt 盘是不是变大了：df -h
```


-------------------------------------------------------------------

## ECS 系统盘数据迁移到数据盘

- 参考：<https://help.aliyun.com/knowledge_detail/41400.html>
- 先对系统盘做快照，出问题，方便回滚
- 先停止系统盘上的部署软件，比如 nginx，tomcat 等，我这里主要是迁移 Elasticsearch
- 先查看 Elasticsearch 未迁移之前的健康状态：

```
查看集群分布
curl -XGET 'http://192.168.0.18:9200/_cat/nodes?v'
ip           heap.percent ram.percent cpu load_1m load_5m load_15m node.role master name
192.168.0.19           37          98   0    0.05    0.06     0.05 mdi       -      elasticsearch-2
192.168.0.18           25          97   0    0.00    0.01     0.05 mdi       *      elasticsearch-1
192.168.0.20           22          96   0    0.00    0.01     0.05 mdi       -      elasticsearch-3

查看集群健康状态
curl -X GET 'http://192.168.0.18:9200/_cluster/health?pretty'
{
  "cluster_name" : "sacf",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 3,
  "number_of_data_nodes" : 3,
  "active_primary_shards" : 120,
  "active_shards" : 240,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}

查看索引清单健康状态
curl -X GET 'http://192.168.0.18:9200/_cluster/health?pretty&level=indices'

查看索引的分片的状态和位置（更加详细）
curl -X GET 'http://192.168.0.18:9200/_cluster/health?pretty&level=shards'
```

- 停止 Elasticsearch 命令：

```
切换用户：
su - sacf

jps -l
11825 org.elasticsearch.bootstrap.Elasticsearch
4394 sun.tools.jps.Jps

kill 11825

然后 exit 切换到 root 用户
```

- 对数据盘进行分区，具体方法参考本文上面资料。
- 假设我们要把 /opt 进行迁移
```
先把文件转移到数据库盘上
cp -arp /opt/* /mnt/

为了稳妥起见，可以再备份一次，创建一个临时目录
mkdir /home/temp
cp -arp /opt/* /home/temp/

删除旧文件
rm -rf /opt/*

卸载目录
umount /mnt
如果卸载报错：In some cases useful info about processes that use...
则查询谁在使用该目录后直接杀死进程
fuser -m -k /mnt/

执行以下命令，把数据盘挂载到 /opt 目录。
mount /dev/vdb1 /opt

然后修改 vim /etc/fstab，把上文填写的 /mnt 改为 /opt

然后用 df -h 查看新的磁盘分布情况

重新启动软件
切换用户：
su - sacf

后台运行：
cd /opt/elasticsearch-6.7.2 ; ./bin/elasticsearch -d -p 自定义pid值

发现没问题后删除临时备份
su - root
rm -rf /home/temp/

```


-------------------------------------------------------------------


## wget 下载文件

- 常规下载：`wget http://www.gitnavi.com/index.html`
- 自动断点下载：`wget -c http://www.gitnavi.com/index.html`
- 后台下载：`wget -b http://www.gitnavi.com/index.html`
- 伪装代理名称下载：`wget --user-agent="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16" http://www.gitnavi.com/index.html`
- 限速下载：`wget --limit-rate=300k http://www.gitnavi.com/index.html`
- 批量下载：`wget -i /opt/download.txt`，一个下载地址一行
- 后台批量下载：`wget -b -c -i /opt/download.txt`，一个下载地址一行


## 其他常用命令

- 编辑 hosts 文件：`vim /etc/hosts`，添加内容格式：`127.0.0.1 www.uptmr.com`
- RPM 文件操作命令：
	- 安装
		- `rpm -i example.rpm`，安装 example.rpm 包
		- `rpm -iv example.rpm`，安装 example.rpm 包并在安装过程中显示正在安装的文件信息
		- `rpm -ivh example.rpm`，安装 example.rpm 包并在安装过程中显示正在安装的文件信息及安装进度
	- 查询
		- `rpm -qa | grep jdk`，查看 jdk 是否被安装
		- `rpm -ql jdk`，查看 jdk 是否被安装
	- 卸载
		- `rpm -e jdk`，卸载 jdk（一般卸载的时候都要先用 rpm -qa 看下整个软件的全名）
- YUM 软件管理：
	- `yum install -y httpd`，安装 apache
	- `yum remove -y httpd`，卸载 apache
	- `yum info -y httpd`，查看 apache 版本信息
	- `yum list --showduplicates httpd`，查看可以安装的版本
	- `yum install httpd-查询到的版本号`，安装指定版本
	- 更多命令可以看：<http://man.linuxde.net/yum>
- 查看某个配置文件，排除掉里面以 # 开头的注释内容：
    - `grep '^[^#]' /etc/openvpn/server.conf`
- 查看某个配置文件，排除掉里面以 # 开头和 ; 开头的注释内容：
    - `grep '^[^#;]' /etc/openvpn/server.conf`
- 通过 yum 下载 rpm 安装包

```
- 安装该软件：yum install -y yum-plugin-downloadonly

- 以下载 openssh-server 为例：
- yum install openssh-server --downloadonly --downloaddir=/opt
- 在 /opt/ssh 目录下有如下内容：
    

-rw-r--r--. 1 root root 280524 Aug 13  2015 openssh-5.3p1-112.el6_7.x86_64.rpm
-rw-r--r--. 1 root root 448872 Aug 13  2015 openssh-clients-5.3p1-112.el6_7.x86_64.rpm
-rw-r--r--. 1 root root 331544 Aug 13  2015 openssh-server-5.3p1-112.el6_7.x86_64.rpm


- 安装下载的 rpm 文件：`sudo rpm -ivh *.rpm`
- 利用 yum 安装 rpm 文件，并自动满足依赖的 rpm 文件：`sudo yum localinstall *.rpm`
```




## 找回/恢复被删除文件

- 被删除的目录或文件，不能再重新进行创建，不然就无法再找回。即使你创建了一个同路径的目录，里面啥文件也没有，也是一种覆盖

```
安装依赖
yum -y install gcc-c++ e2fsprogs.x86_64 e2fsprogs-devel.x86_64

下载工具
wget https://nchc.dl.sourceforge.net/project/extundelete/extundelete/0.2.4/extundelete-0.2.4.tar.bz2

解压
tar jxvf extundelete-0.2.4.tar.bz2 

安装
cd  extundelete-0.2.4

./configure 

make && make install

验证安装结果
extundelete -v

假设你被删除的目录是：/opt/my-soft/abc 目录
这时候你要切换到原删除目录的上层目录，也就是 /opt/my-soft

输入
ls -id ./
结果格式：139372 ./

可以得到当前的 inode 值 139372

看下你这个被删除目录是属于哪个分区：df -h
一般如果没有自己动过分区，一般是：/dev/dba1

开始恢复
extundelete /dev/vda1 --inode 139372
WARNING: EXT3_FEATURE_INCOMPAT_RECOVER is set.
The partition should be unmounted to undelete any files without further data loss.
If the partition is not currently mounted, this message indicates 
it was improperly unmounted, and you should run fsck before continuing.
If you decide to continue, extundelete may overwrite some of the deleted
files and make recovering those files impossible.  You should unmount the
file system and check it with fsck before using extundelete.
Would you like to continue? (y/n) 

根据提示输入：y
可以看到你被删除的目录、文件

恢复文件
extundelete /dev/vda1 --restore-file wushan1.txt

恢复文件夹
extundelete  /dev/vda1  --restore-directory /opt/my-soft/abc
```



## 资料

- <http://wenku.baidu.com/view/1ad19bd226fff705cc170af3.html>
- <http://blog.csdn.net/nzing/article/details/9166057>
- <http://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/wget.html>
- <https://www.jianshu.com/p/180fb11a5b96>
