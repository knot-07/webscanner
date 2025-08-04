import os
import re
from colorama import Fore, Style

def normalize_url(url):
    """标准化URL标准化处理"""
    if not url.startswith(('http://', 'https://')):
        url = f'http://{url}'
    if not url.endswith('/'):
        url += '/'
    return url

def print_result(status, url, size):
    """格式化输出结果"""
    status_color = {
        200: Fore.GREEN,
        301: Fore.BLUE,
        302: Fore.CYAN,
        403: Fore.YELLOW,
        404: Fore.RED
    }.get(status, Fore.WHITE)
    
    print(f"{status_color}[{status}] {Style.RESET_ALL}{url} ({size} bytes)")

def load_wordlist(path):
    """加载字典文件"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"字典文件不存在: {path}")
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]