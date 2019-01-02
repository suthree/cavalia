import requests
from contextlib import closing


class FileProgress(object):
    """
    文件 下载 进程

    """

    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/',
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
        _info = (f"[{self.title}] {self.status} {self.count/ self.chunk} {self.unit} "
                 f"{self.total} {self.total/self.chunk} {self.unit}")
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        self.status = status or self.status
        end_str = '\r'
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self._down_info(), end=end_str)


if __name__ == '__main__':
    print('*' * 100)
    file_url = input('请输入下载的链接:\n')
    file_name = file_url.split('/')[-1]
    with closing(requests.get(file_url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            print(f'文件大小{content_size/chunk_size}kb')
            progress = FileProgress(title=file_name, unit='KB', total=content_size, chunk=chunk_size, run_status='正在下载',
                                    fin_status='下载完成')
            with open(file_name, 'wb') as f:
                for data in response.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    progress.refresh(count=len(data))
