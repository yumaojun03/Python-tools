# -*- coding: gbk -*-
from __future__ import print_function

__author__ = u'�ƴ�'
__contributor__ = u'��ï��'

import sys
reload(sys)
sys.setdefaultencoding('gbk')

import sys, os
from subprocess import Popen, PIPE
import configparser
import requests
import datetime
import time

remote_addr = 'www.baidu.com'
config_name = 'config.txt'
result_name = 'result.txt'


class TestConnectTool(object):
    """
    �����û����Ա������絽�����ƻ���������������
    """

    def __init__(self):
        self.count = 0
        self.remote_addr = None
        self.request_path = None
        self.script_dir_path = None
        self.f_result = None
        self.config()

    def config(self):
        """
        ͨ�������ļ����ù��ߵ����в���
        """
        script_dir_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir_path, config_name)
        cf = configparser.ConfigParser()
        cf.read(config_path)
        result_path = os.path.join(script_dir_path, result_name)
        self.remote_addr = cf.get('CHECK_INFO', 'Remote_Addr')
        self.request_path = cf.get('CHECK_INFO', 'Request_Path')
        self.script_dir_path = script_dir_path
        self.f_result = open(result_path, 'w')

    def http_download_file(self, url, directory):
        """
        ����ͨ��HTTP�����ļ�������

        Args:
            url: ��Ҫ�����ļ���url
            directory: �����ļ���ŵ�Ŀ¼
        Returns:
            file_size: <float> �ļ���С����λKB
        """
        local_filename = url.split('/')[-1]
        with open(self.script_dir_path + '/' + local_filename, 'wb') as f:
            start = time.clock()
            r = requests.get(url, stream=True)
            total_length = int(r.headers.get('content-length'))
            dl = 0
            if total_length is None:
                raise ValueError(u"no content-length header get, next to do...")
            else:
                for chunk in r.iter_content(4096):
                    dl += len(chunk)
                    f.write(chunk)
                    bytes_ps = dl//(time.clock() - start)
                    done = int(50 * dl / total_length)
                    if done > self.count:
                        msg = "[%s%s] %.2f KB/s" % ('=' * done, ' ' * (50-done), bytes_ps/1024)
                        wipe = '\b'*(len(msg))
                        print(wipe+msg, end='')
                        sys.stdout.flush()
                    self.count = done
                print('')
        return total_length/1024/1024.00

    def ping(self):
        """
        Ping ����
        """
        print(u'===> ping���ԣ�<===')
        p1 = Popen("ping %s" % remote_addr, stdout=PIPE, stderr=PIPE)

        while p1.poll() is None:
            output = p1.stdout.readline().strip()
            if output:
                print(output.decode('gbk'))
                print(output, file=self.f_result)

        print(u'')
        print(u'', file=self.f_result)

    def trace_route(self):
        """
        Trace Route ����
        """
        print(u'===> tracert���ԣ�<===')
        p2 = Popen("tracert %s" % remote_addr,   stdout=PIPE, stderr=PIPE)
        while p2.poll() is None:
            output = p2.stdout.readline().strip()
            if output:
                print(output.decode('gbk'))
                print(output, file=self.f_result)

        print(u'')
        print(u'', file=self.f_result)

    def download(self):
        """
        �ļ����ز���
        """
        print(u'===> �ļ����ز��ԣ�<===')
        '''��ȡ����·�� '''
        dl_url = 'http://{0}/{1}'.format(self.remote_addr, self.request_path)

        starttime = datetime.datetime.now()
        file_size = self.http_download_file(dl_url, self.script_dir_path)
        endtime = datetime.datetime.now()
        delta = endtime - starttime
        time_elaps = delta.total_seconds()

        dl_speed = file_size/time_elaps

        print(u'\n\n=== �ļ����ز��ԣ�', file=self.f_result)
        print(u'����·����%s' % dl_url)
        print(u'����·����%s' % dl_url, file=self.f_result)
        print(u'�ļ���С��%.2f MB' % file_size)
        print(u'�ļ���С��%.2f MB' % file_size, file=self.f_result)
        print(u'���غ�ʱ��%.2f ��' % time_elaps)
        print(u'���غ�ʱ��%.2f ��' % time_elaps, file=self.f_result)
        print(u'�����ٶȣ�%.2f MB/S' % dl_speed)
        print(u'�����ٶȣ�%.2f MB/S' % dl_speed, file=self.f_result)

    def write_result(self):
        """
        �����Ժ�Ľ��������ļ���
        """
        self.f_result.flush()
        self.f_result.close()
        print(u'=== �������')

    def __call__(self):
        print('%s -- %s' % (self.remote_addr, self.request_path))
        self.ping()
        # self.trace_route()
        self.download()
        self.write_result()


if __name__ == '__main__':
    tool = TestConnectTool()
    tool()















