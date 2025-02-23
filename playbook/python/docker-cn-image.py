# 脚本和镜像来源：https://www.coderjia.cn/archives/dba3f94c-a021-468a-8ac6-e840f85867ea

import re
import requests
import concurrent.futures
import time
import threading
from urllib3.exceptions import InsecureRequestWarning

# 禁用SSL证书警告
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

print_lock = threading.Lock()


def load_mirrors_from_md(file_path):
    """
    从Markdown文件读取有效镜像列表
    格式要求：第一列为`包裹的镜像地址，第二列为状态（支持：正常/新增）
    """
    valid_status = {"正常", "新增"}
    pattern = r"`([\w\.\-]+)`.*?\|.*?(\S+)\s*\|"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 跳过表头前两行
            for _ in range(2): next(f)

            return [
                re.search(pattern, line).group(1)
                for line in f
                if re.search(pattern, line)
                   and re.search(pattern, line).group(2) in valid_status
            ]
    except Exception as e:
        print(f"\033[31mError reading markdown file: {str(e)}\033[0m")
        return []


def test_mirror(mirror):
    url = f"https://{mirror}"
    success = 0
    total_time = 0.0
    attempts = 3
    log_buffer = []  # 日志缓存器

    # 初始化日志
    log_buffer.append(f"\n\033[1m▶ Testing {url}\033[0m")

    for i in range(attempts):
        attempt_log = ""
        try:
            start_time = time.time()
            response = requests.head(
                f"{url}/v2/",
                timeout=5,
                verify=False
            )
            elapsed = time.time() - start_time

            if response.status_code in (200, 401):
                success += 1
                total_time += elapsed
                status_desc = f"\033[32m{response.status_code} OK\033[0m"
            else:
                status_desc = f"\033[33m{response.status_code} Error\033[0m"

            attempt_log = f"  Attempt {i + 1}: {status_desc} ({elapsed:.2f}s)"

        except Exception as e:
            elapsed = time.time() - start_time if 'start_time' in locals() else 0
            error_msg = str(e).split(":")[0]
            attempt_log = f"  Attempt {i + 1}: \033[31mFailed ({error_msg})\033[0m"

        finally:
            log_buffer.append(attempt_log)
            time.sleep(1)

    # 计算统计指标
    success_rate = success / attempts
    avg_time = total_time / success if success > 0 else float('inf')

    # 添加结果摘要
    status_icon = "\033[32m✓\033[0m" if success_rate > 0.5 else "\033[31m✗\033[0m"
    log_buffer.append(
        f"{status_icon} 最终结果: "
        f"成功率 {success_rate * 100:.1f}% | "
        f"平均响应 {avg_time:.2f}s"
    )

    # 原子化输出完整日志
    with print_lock:
        print("\n".join(log_buffer))

    return {
        "url": url,
        "success_rate": success_rate,
        "avg_time": avg_time
    }


if __name__ == "__main__":
    # 从当前目录读取 mirrors.md 文件
    MIRROR_FILE = "mirrors.md"
    mirror_list = load_mirrors_from_md(MIRROR_FILE)

    if not mirror_list:
        print("\033[31m未找到有效镜像地址，请检查markdown文件格式！\033[0m")
        exit(1)

    print(f"\033[1m成功加载 {len(mirror_list)} 个有效镜像\033[0m")

    print("\033[1m\n开始测试镜像加速器...\033[0m")
    start_time = time.time()

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(test_mirror, mirror): mirror for mirror in mirror_list}

        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            results.append(data)
            with print_lock:
                status_color = "\033[32m✓\033[0m" if data["success_rate"] > 0.5 else "\033[31m✗\033[0m"
                print(f"{status_color} {data['url']}: "
                      f"成功率 {data['success_rate'] * 100:.1f}% | "
                      f"平均响应 {data['avg_time']:.2f}s")

    # 排序逻辑：成功率 > 响应时间
    sorted_results = sorted(results,
                            key=lambda x: (-x['success_rate'], x['avg_time']))

    print("\n\033[1m测试结果排序（最佳到最差）：\033[0m")
    for idx, res in enumerate(sorted_results, 1):
        color_code = "\033[32m" if res["success_rate"] > 0.7 else "\033[33m" if res[
                                                                                    "success_rate"] > 0.3 else "\033[31m"
        print(f"{idx:2d}. {color_code}{res['url']}\033[0m "
              f"(成功率: {res['success_rate'] * 100:.1f}%, "
              f"响应: {res['avg_time']:.2f}s)")

    # 原有排序输出保持不变...
    print(f"\n总测试时间: {time.time() - start_time:.1f}秒")

    # 新增有效镜像列表输出 ------------------------------------------
    print("\n\033[1m可用镜像列表（过滤零成功率镜像）：\033[0m")
    valid_mirrors = [
        res["url"]
        for res in sorted_results
        if res["success_rate"] > 0
    ]

    # 控制台彩色输出
    for idx, url in enumerate(valid_mirrors, 1):
        print(f"{idx:2d}. \033[34m{url}\033[0m")

    # 同时生成纯文本文件（只是换行）
    # with open("valid_mirrors.txt", "w") as f:
    #     f.write("\n".join(valid_mirrors))

    # 同时生成纯文本文件（用双引号包裹，最后有逗号）
    with open('valid_mirrors.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(
            f'"{item}"' + (',' if i < len(valid_mirrors) - 1 else '')
            for i, item in enumerate(valid_mirrors)
        ))

    print(f"\n\033[36m已生成 {len(valid_mirrors)} 个有效镜像到 valid_mirrors.txt\033[0m")
