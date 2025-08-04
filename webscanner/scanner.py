import argparse
from core.scanner import Scanner
from colorama import init

def main():
    # 初始化colorama（支持Windows彩色输出）
    init(autoreset=True)
    
    # 命令行参数解析
    parser = argparse.ArgumentParser(description="Web路径扫描工具")
    parser.add_argument("target", help="目标URL (例如: http://example.com)")
    parser.add_argument("-w", "--wordlist", default="dictionaries/common.txt", 
                      help="字典文件路径 (默认: dictionaries/common.txt)")
    parser.add_argument("-t", "--threads", type=int, default=5, 
                      help="线程数量 (默认: 5)")
    parser.add_argument("-e", "--extensions", 
                      help="文件扩展名 (例如: php,html,asp)")
    parser.add_argument("-o", "--output", 
                      help="结果输出文件路径")
    
    args = parser.parse_args()
    
    # 处理扩展参数
    extensions = args.extensions.split(',') if args.extensions else []
    
    # 初始化并启动扫描器
    scanner = Scanner(
        target=args.target,
        wordlist_path=args.wordlist,
        threads=args.threads,
        extensions=extensions,
        output=args.output
    )
    scanner.run()

if __name__ == "__main__":
    main()