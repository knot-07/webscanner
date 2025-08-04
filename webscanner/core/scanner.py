import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from .requester import Requester
from .utils import normalize_url, print_result, load_wordlist

class Scanner:
    def __init__(self, target, wordlist_path, threads=5, extensions=None, output=None):
        self.target = normalize_url(target)
        self.wordlist = load_wordlist(wordlist_path)
        self.threads = threads
        self.extensions = extensions or []
        self.output = output
        self.requester = Requester()
        self.valid_paths = []

    def generate_paths(self):
        """生成所有待扫描的路径"""
        paths = set()
        for word in self.wordlist:
            # 添加原始路径
            paths.add(word)
            # 添加带扩展名的路径
            for ext in self.extensions:
                paths.add(f"{word}.{ext}")
        return sorted(paths)

    def scan_path(self, path):
        """扫描单个路径"""
        url = f"{self.target}{path}"
        result = self.requester.get(url)
        if result["success"] and result["status"] not in [404, 400]:
            return result
        return None

    def run(self):
        """启动扫描"""
        print(f"开始扫描目标: {self.target}")
        print(f"使用字典: {len(self.wordlist)} 个基础路径")
        print(f"线程数: {self.threads} | 扩展: {','.join(self.extensions) or '无'}")
        print("="*50)

        start_time = time.time()
        paths = self.generate_paths()

        # 多线程扫描
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            # 创建任务列表
            futures = {executor.submit(self.scan_path, path): path for path in paths}
            
            # 处理完成的任务
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.valid_paths.append(result)
                    print_result(result["status"], result["url"], result["size"])

        # 保存结果到文件
        if self.output:
            with open(self.output, 'w', encoding='utf-8') as f:
                for item in self.valid_paths:
                    f.write(f"{item['status']} {item['url']} ({item['size']} bytes)\n")

        end_time = time.time()
        print("="*50)
        print(f"扫描完成 | 耗时: {end_time - start_time:.2f}秒")
        print(f"发现有效路径: {len(self.valid_paths)} 个")
        if self.output:
            print(f"结果已保存到: {self.output}")