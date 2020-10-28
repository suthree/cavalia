# import fcntl
import multiprocessing
import os
import threading
import time
import requests


class Mythread(threading.Thread):
    def __init__(self, url, startpos, endpos, f):
        super(Mythread, self).__init__()
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = f

    def download(self):
        print(f'Start Thread: {self.getName()}')
        headers = {'Range': 'bytes=%s-%s' % (self.startpos, self.endpos)}
        res = requests.get(self.url, headers=headers, stream=True)
        self.fd.seek(self.startpos)
        self.fd.write(res.content)
        # 固定长度写入，需要更新 文件句柄位置
        # chunk_size = 1024
        # for data in res.iter_content(chunk_size=chunk_size):
        #     self.fd.write(data)
        print(f'Stop Thread: {self.getName()}')
        self.fd.close()

    def run(self):
        self.download()


def download_file_thread(file_url, file_dir):
    """
    多线程 下载 文件
    """
    file_name = file_url.split('/')[-1]  # url 文件名
    # file_dir, file_name = os.path.split(file_path)  # 存储文件名
    file_path = os.path.join(file_dir, file_name)
    # 文件存储路径
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    filesize = int(requests.head(file_url).headers['Content-Length'])
    chunk_size = 1024
    print(f'文件名： {file_name}  文件大小： {filesize/chunk_size} kb')
    max_threadnum = 3
    threading.BoundedSemaphore(max_threadnum)  # 允许线程个数
    step = filesize // max_threadnum  # 根据文件大小，和最大线程数，对文件进行分块
    start = 0
    end = -1
    mtd_list = []
    # 创建临时文件， 为后期 rb+ 模式做准备
    tempf = open(file_path, 'w')
    tempf.close()
    with open(file_path, 'rb+') as f:
        #获得文件句柄
        fileno = f.fileno()  #返回一个整型的文件描述符，可用于底层操作系统的 I/O 操作
        while end < filesize - 1:
            start = end + 1
            end = start + step - 1
            if end > filesize:
                end = filesize
            print(f'Start: {start}, end: {end}')
            dup = os.dup(fileno)  #复制文件句柄
            fd = os.fdopen(dup, 'rb+', -1)
            t = Mythread(file_url, start, end, fd)
            t.start()
            mtd_list.append(t)
        for i in mtd_list:
            i.join()
    f.close()


def bulk_write(file_path, content):
    with open(file_path, 'a+') as fo:
        # fcntl.flock(fo.fileno(), fcntl.LOCK_EX)  #加锁
        fo.write(content)


class FileProgress(object):
    """
    文件 下载 进程

    """

    def __init__(self,
                 title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='',
                 sep='/',
                 chunk=1.0):
        super().__init__()
        self.title = title
        self.total = total
        self.count = count
        self.chunk = chunk
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def _down_info(self):
        """
        文件名, 状态, 进度, 单位, 分割线, 总量, 单位
        :return:
        """
        _info = (
            f"[{self.title}] {self.status} {self.count/ self.chunk} {self.unit} "
            f"{self.total} {self.total/self.chunk} {self.unit}")
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        self.status = status or self.status
        end_str = '\r'
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        down_info = f'{self.title} {self.count / self.chunk} {self.unit}, {self.total} {self.total/self.chunk} {self.unit}'
        print(down_info, end=end_str)


def iter_download(file_url, file_dir):

    file_name = file_url.split('/')[-1]  # url 文件名
    # file_dir, file_name = os.path.split(file_path)  # 存储文件名
    file_path = os.path.join(file_dir, file_name)
    chunk_size = 1024
    res = requests.get(file_url, stream=True)
    file_size = int(res.headers.get('content-length'))
    # file_size = int(requests.head(file_url).headers['Content-Length'])
    with open(file_path, 'wb') as f:
        for chunk in res.iter_content(chunk_size=chunk_size):
            if not chunk:
                break
            f.write(chunk)
            f.flush()  # 刷新缓冲区


if __name__ == "__main__":
    # file_url = input('请输入下载的链接:\n')
    url = 'http://www.wendangxiazai.com/word/b-cfbdc77931b765ce050814a9-1.doc'
    # file_dir = '/d/Code/cavalia/spiders'
    file_path = os.path.dirname(__file__)
    file_dir = os.path.abspath(file_path)
    iter_download(url, file_dir)
