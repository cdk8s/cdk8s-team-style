
### **1. 安装 screen**
```bash
# Debian/Ubuntu 系统
sudo apt install screen

# CentOS/RHEL 系统
sudo yum install screen
```

---

### **2. 基本操作**
#### **启动新会话**
```bash
screen                 # 创建匿名会话
screen -S session_name # 创建命名会话（推荐）
screen -U -S session_name # 使用 UTF-8 编码
```

#### **暂时离开会话（Detach）**
- 快捷键：`Ctrl + A` → `D`  
  会话将在后台运行，进程不会中断。

#### **查看所有会话**
```bash
screen -ls
# 输出示例：12345.session_name (Detached)
```

#### **恢复会话（Attach）**
```bash
screen -r session_name   # 通过名称恢复
screen -r 12345         # 通过 ID 恢复
```

#### **强制恢复被占用的会话**
```bash
screen -rd session_name  # 先 Detach 其他连接，再恢复
```

#### **关闭会话**
- 在会话中直接输入 `exit` 或 `Ctrl + D`

---

### **3. 会话内操作**
#### **窗口管理**
| 快捷键          | 功能                     |
|----------------|--------------------------|
| `Ctrl + A` → `c` | 创建新窗口               |
| `Ctrl + A` → `n` | 切换到下一个窗口         |
| `Ctrl + A` → `p` | 切换到上一个窗口         |
| `Ctrl + A` → `0-9` | 跳转到第 0-9 号窗口     |
| `Ctrl + A` → `w` | 显示窗口列表             |
| `Ctrl + A` → `k` | 杀死当前窗口             |
| `Ctrl + A` → `"` | 可视化选择窗口           |

#### **分屏操作**
| 快捷键          | 功能                     |
|----------------|--------------------------|
| `Ctrl + A` → `S` | 水平分割屏幕（上下布局） |
| `Ctrl + A` → `|` | 垂直分割屏幕（左右布局） |
| `Ctrl + A` → `Tab` | 在分屏区域间切换         |
| `Ctrl + A` → `Q` | 关闭除当前区域外的所有分屏 |
| `Ctrl + A` → `X` | 关闭当前分屏区域         |

#### **其他常用命令**
| 快捷键          | 功能                     |
|----------------|--------------------------|
| `Ctrl + A` → `d` | 脱离当前会话（同 Detach） |
| `Ctrl + A` → `[` | 进入滚动模式（用方向键滚动，按 `Esc` 退出） |
| `Ctrl + A` → `?` | 查看帮助                 |

---

### **4. 高级用法**
#### **会话共享（多人协作）**
```bash
screen -S shared_session  # 用户A创建会话
screen -x shared_session  # 用户B加入同一会话
# 两人可实时看到操作
```

#### **启动时运行命令**
```bash
screen -S session_name bash -c 'your_command; exec sh'
```

#### **日志记录**
```bash
screen -L -S session_name  # 自动保存日志到 ~/screenlog.0
```

#### **配置文件（~/.screenrc）**
自定义设置示例：
```bash
# 显示状态栏
hardstatus alwayslastline
hardstatus string '%{= kG}[ %{G}%H %{g}][ %{= kC}%?%-Lw%?%{r}(%{W}%n*%f%t%?(%u)%?%{r})%{w}%?%+Lw%?%?%= %{g}][%{B}%Y-%m-%d %{W}%c %{g}]'

# 设置滚动缓冲区大小
defscrollback 5000
```

---

### **5. 常见问题**
- **问题**：恢复会话时报错 `There is no screen to be resumed`  
  **解决**：确认会话名或 ID 是否正确，使用 `screen -ls` 检查。

- **问题**：恢复时报错 `Attached but dead`  
  **解决**：强行创建新会话恢复：
  ```bash
  screen -D -r session_name
  ```

- **问题**：`Ctrl + A` 快捷键冲突  
  **解决**：将前缀键改为其他组合（如 `Ctrl + B`），在 `~/.screenrc` 中添加：
  ```bash
  escape ^Bb  # 使用 Ctrl + B 作为前缀
  ```

---

通过 `screen`，你可以在断开 SSH 后保持任务运行，并随时恢复工作进度。掌握基本快捷键后，效率将大幅提升！