"""
Torrent文件处理工具箱
功能包含：种子文件修复、重复文件清理、下载状态检测、云格式转换等
"""
import os
import shutil
import zipfile
import time
from pathlib import Path
from typing import List, Dict, Set, Generator

from torrentool.api import Torrent
from torrentool.exceptions import BencodeDecodingError
from torrent_download_files_check import DownLoadCheck
import loggerTemplate as logger
import mysqlTemplate as dbtool

# --------------------------
# 常量配置区
# --------------------------
TORRENT_ERROR_DIR = "errorbak"  # 种子错误备份目录
HALF_PREFIX = "HALF-"  # 未完成文件前缀
LOG_BASE_PATH = Path("D:/temp/0555")  # 日志基础路径

BLOCKED_FILES = [
    '【01axg.xyz】.jpg',
    '02AXG.XYZ.png',
    '03axg.XYZ.png',
    '8axg.xyz.png',
    'duplicatedirtyData.txt'
]

DOWNLOADER_SUFFIXES = {
    'xunlei': '.bt.xltd',
    'fdm': '.fdmdownload',
    'btcomet': '.bc!'
}


# --------------------------
# 工具函数
# --------------------------
def safe_path_join(base: Path, *parts: str) -> Path:
    """安全路径拼接"""
    try:
        return base.joinpath(*parts).resolve()
    except Exception as e:
        logger.error(f"路径拼接错误: {base}/{parts} -> {str(e)}")
        return base


def backup_error_file(src_path: Path) -> None:
    """错误文件备份"""
    try:
        backup_dir = src_path.parent / TORRENT_ERROR_DIR
        backup_dir.mkdir(exist_ok=True)

        dst_path = backup_dir / src_path.name
        if not dst_path.exists():
            shutil.copy(src_path, dst_path)
            logger.info(f"已备份错误文件: {src_path} -> {dst_path}")
    except Exception as e:
        logger.error(f"备份失败: {src_path} -> {str(e)}")


# --------------------------
# 核心功能实现
# --------------------------
class TorrentProcessor:
    """种子文件处理核心类"""

    def __init__(self, work_dir: Path):
        self.work_dir = work_dir.resolve()
        self.download_checker = DownLoadCheck()

    def _walk_files(self, pattern: str = "*") -> Generator[Path, None, None]:
        """文件遍历生成器"""
        for entry in self.work_dir.rglob(pattern):
            if entry.is_file():
                yield entry

    def clean_blocked_files(self) -> None:
        """清理临时文件"""
        for filepath in self._walk_files():
            if filepath.name in BLOCKED_FILES:
                try:
                    filepath.unlink()
                    logger.info(f"已删除临时文件: {filepath}")
                except Exception as e:
                    logger.error(f"删除失败: {filepath} -> {str(e)}")

    def find_duplicates(self, prefix: str) -> List[Path]:
        """查找重复文件"""
        return [
            filepath for filepath in self._walk_files()
            if filepath.name.startswith(prefix)
        ]

    def load_torrent(self, torr_path: Path) -> Torrent:
        """加载种子文件（自动修复）"""
        try:
            # 第一次尝试加载
            return Torrent.from_file(str(torr_path))
        except (BencodeDecodingError, IndexError):
            logger.warning(f"种子加载失败，尝试修复: {torr_path}")
            return self._fix_and_reload(torr_path)

    def _fix_and_reload(self, torr_path: Path, retry: int = 3) -> Torrent:
        """修复并重新加载种子"""
        for attempt in range(retry):
            try:
                # 修复文件末尾异常字符
                with torr_path.open('rb+') as f:
                    content = f.read()
                    if content.endswith(b'\r\n'):
                        f.seek(-2, os.SEEK_END)
                        f.truncate()

                # 二次加载尝试
                return Torrent.from_file(str(torr_path))

            except Exception as e:
                logger.error(f"修复失败({attempt + 1}/{retry}): {torr_path} -> {str(e)}")
                time.sleep(0.5)

        backup_error_file(torr_path)
        raise RuntimeError(f"种子修复失败: {torr_path}")

    def filter_downloaded(self, torr_path: Path, target_dir: Path) -> Dict[str, str]:
        """过滤已下载文件"""
        torrent = self.load_torrent(torr_path)
        status_report = {}

        for fileinfo in torrent.get_files():
            source_path = safe_path_join(self.work_dir, fileinfo.path)
            dest_path = safe_path_join(target_dir, fileinfo.path)

            if self.download_checker.is_completed(source_path):
                try:
                    shutil.move(str(source_path), str(dest_path))
                    status_report[fileinfo.path] = "MOVED"
                except Exception as e:
                    status_report[fileinfo.path] = f"ERROR: {str(e)}"
            else:
                status_report[fileinfo.path] = "INCOMPLETE"

        return status_report

    def clear_downloader_files(self, downloader: str = "xunlei") -> int:
        """清理下载器临时文件"""
        suffix = DOWNLOADER_SUFFIXES.get(downloader.lower(), '')
        if not suffix:
            raise ValueError(f"不支持的下载器类型: {downloader}")

        count = 0
        for filepath in self._walk_files(f"*{suffix}"):
            try:
                filepath.unlink()
                count += 1
            except Exception as e:
                logger.error(f"删除失败: {filepath} -> {str(e)}")
        return count


# --------------------------
# 数据库操作模块
# --------------------------
class TorrentDBAccess:
    """种子数据库操作"""

    def __init__(self, db_config: dict):
        self.conn = dbtool.connect(**db_config)

    def find_by_hash(self, hash_list: List[str]) -> List[dict]:
        """根据hash值查询种子"""
        placeholders = ','.join(['%s'] * len(hash_list))
        query = f"""
            SELECT hash, name, size, create_time 
            FROM torrents 
            WHERE hash IN ({placeholders})
        """
        return dbtool.query(self.conn, query, hash_list)

    def search_torrents(self, keywords: List[str]) -> List[dict]:
        """根据关键词搜索种子"""
        query = "SELECT * FROM torrents WHERE "
        conditions = []
        params = []

        for kw in keywords:
            conditions.append("name LIKE %s")
            params.append(f"%{kw}%")

        return dbtool.query(self.conn, query + " OR ".join(conditions), params)


# --------------------------
# 主程序入口
# --------------------------
if __name__ == "__main__":
    # 初始化日志系统
    logger.init_logger(str(LOG_BASE_PATH / "torrent_tool.log"))

    # 示例使用流程
    processor = TorrentProcessor(Path("D:/torrents/working"))

    # 清理临时文件
    processor.clean_blocked_files()

    # 处理种子文件
    for torr_file in processor._walk_files("*.torrent"):
        try:
            report = processor.filter_downloaded(
                torr_file,
                Path("G:/down/processed")
            )
            logger.info(f"处理完成: {torr_file.name} -> 移动{len(report)}个文件")
        except Exception as e:
            logger.error(f"处理失败: {torr_file} -> {str(e)}")

    # 清理迅雷临时文件
    cleared_count = processor.clear_downloader_files("xunlei")
    logger.info(f"已清理{cleared_count}个迅雷临时文件")
