#!/usr/bin/env python
# -*- coding: utf-8 -*-


from config import *;
import os,time,codecs;

def print_log(msg):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime());
    log_dir = 'logs/';#当前工作目录下创建日志目录
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir);

        #以下部分主要判断当前日志文件是否已过期(即已是新的一天)
        log_file = log_dir + 'log.txt';
        if(os.path.exists(log_file)):
            last_modified_time = time.localtime(os.stat(log_file).st_mtime);
            last_modified_date = time.strftime('%d', last_modified_time);
            now_date = time.strftime('%d', time.localtime()) ;
            if(now_date != last_modified_date):#最后修改文件的日期与当前不一致时，将原日志文件进行转移，保证当前日志文件只包含当天的日志
                now_date_text = time.strftime('%Y-%m-%d', time.localtime());
                new_file_path = log_dir + now_date_text + '-log.txt';
                os.rename(log_file,new_file_path);

        #记录日志
        fo = codecs.open(log_file, 'a','utf-8');
        content = now + ' ' + str(msg) + '\n';
        fo.write(content.decode('utf-8'));
        fo.close();
    except Exception,err:
        print now,'write log file error:' + str(err);
    print now,msg;
