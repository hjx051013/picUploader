import re
import os
import sys
import datetime
import platform
import imghdr
import shutil
import tinify
import urllib
import sqlite3
from hashlib import md5
import validators
import getopt
import configparser
from QiniuYun import Qiniu
from UpYun import Upai

md_loc = ''  # md地址
need_zip = False
os_name = ''
need_cache = False
today = datetime.date.today()
yyyymmdd = today.strftime('%Y%m%d')  # 创建时间变量，用于图片起名
total, success, failure, ignore = 0, 0, 0, 0
cloud_cfg = None
need_back = False

def upload_file(upload_file_name):
    '''
    根据给定的图片名上传图片，并返回图片地址和一些上传信息
    '''
    global success, failure

    # 上传到云存储后的图片名:上传日期-MD文件名/image序号.png or jpg
    key = yyyymmdd + "_" + os.path.splitext(os.path.basename(sys.argv[1]))[0] + "/image" + ('{0}'.format(success + 1)) + \
          os.path.splitext(upload_file_name)[1]
    try:
        upload_url = cloud_cfg.upload_file(upload_file_name, key, False)
        if upload_url:
            success = success + 1
            return upload_url
        failure = failure + 1
    except Exception as e:
        print("异常：", e)
    return None


def transfer_online_img(old_link):
    '''
    根据给定的图片链接上传图片到云存储，并返回图片地址和一些上传信息
    '''
    global success, ignore, failure
    if validators.url(old_link) is not True:
        ignore = ignore + 1
        print('invalid url, ignore')
        return None

    # maybe a url
    # already from qiniu
    if old_link.find(cloud_cfg.domain) != -1:
        ignore = ignore + 1
        print('already in target cloud, ignore')
        return None

    # omit the query string section like:?arg1=val1&arg2=val2 in the url
    if old_link.find('?') != -1:
        old_link = old_link[: old_link.index('?')]

    # 上传到云存储后的图片名:上传日期-MD文件名/image序号
    key = yyyymmdd + "_" + os.path.splitext(os.path.basename(sys.argv[1]))[0] + "/image" + ('{0}'.format(success + 1))
    try:
        upload_url = cloud_cfg.upload_file(old_link, key, True)
        if upload_url:
            success = success + 1
            return upload_url
        failure = failure + 1
    except Exception as e:
        print("异常：", e)

    return None


def cached_img_url(img_loc_path):
    '''
    根据给定的本地图片绝对路径，转换成一个网上路径。
    如果本地缓存中有，则直接读取并返回，如果没有，则上传后返回。
    '''
    conn = sqlite3.connect(md_loc + './img_hash_cache.db')
    cursor = conn.cursor()
    try:
        cursor.execute(''' 
            CREATE TABLE if not exists img_cache_table (
                img_hash TEXT,
                real_p TEXT,
                img_url TEXT
            )
            ''')
    except Exception as e:
        pass
    img_hash = md5(open(img_loc_path, 'rb').read()).hexdigest()  # 图片的hash值，用来确定图片的唯一性，避免多次上传，浪费流量
    cursor.execute("SELECT img_url FROM img_cache_table WHERE img_hash='%s'" % img_hash)  # 根据图片的hash值来找缓存下来的图片网址
    select_res = [row for row in cursor]
    img_url = (
        select_res[0][0] if select_res and len(select_res) > 0 and select_res[0] and len(select_res[0]) > 0 else None)

    remote_exists = False
    if img_url:
        try:
            remote_exists = urllib.request.urlopen(img_url).code == 200
        except Exception as e:
            print('#warning: 网址不存在 ：', img_url)
            cursor.execute("DELETE FROM img_cache_table WHERE img_hash='%s'" % img_hash)
            remote_exists = False
    if remote_exists:
        print("已缓存")
    if not img_url or not remote_exists:  # 如果没有查到图片的网址，或者网址失效
        print('上传图片 ：', img_loc_path)
        img_url = upload_file(img_loc_path)  # 接取上传后的图片信息
        if not img_url:  # 如果图片地址为空，则说明上传失败
            print('#warning: 上传失败')
            conn.close()
            return None
        else:
            if not remote_exists:
                cursor.execute('INSERT INTO img_cache_table VALUES(?,?,?)',
                               (img_hash, img_loc_path, img_url))  # 如果上传成功，则直接缓存下来
            else:
                cursor.execute("UPDATE img_cache_table SET img_url='%s', u_info='%s' WHERE img_hash='%s'" % (
                img_url, img_hash))
            conn.commit()
    conn.close()

    return img_url


def zip_pic(loc_p):
    o_img = loc_p + '.ori'  # 原始未压缩的图片
    try:
        if not os.path.isfile(o_img) or not imghdr.what(o_img):  # 如果没有的话，那就需要进行压缩处理
            print('压缩图片 ：', loc_p)
            s_img = tinify.from_file(loc_p)
            s_img.to_file(loc_p + '.z')
            os.rename(loc_p, loc_p + '.ori')
            os.rename(loc_p + '.z', loc_p)
    except Exception as e:
        print('#warning: tinypng压缩出问题了，图片未压缩。')


def upload_pic_proc(md_file, match):
    if not re.match('((http(s?))|(ftp))://.*', match):  # 判断是不是已经是一个图片的网址
        loc_p = match
        if not os.path.exists(loc_p) or not os.path.isfile(loc_p):
            # 如果文件不存在，则可能这是用的一个相对路径，需要转成绝对路径
            # Windows中 md_file的本地路径为反斜杠\\, match的相对路径为 "MD标题\图片文件名"
            loc_p = (md_file[:md_file.rfind('\\') + 1] + match) if os_name == 'Windows' else (
                        md_file[:md_file.rfind('/') + 1] + match)
        if os.path.exists(loc_p) and os.path.isfile(loc_p) and imghdr.what(loc_p):
            if need_zip:
                zip_pic(loc_p)
            if need_cache:
                file_url = cached_img_url(loc_p)  # 获取上传后的图片地址
            else:
                print('上传图片 ：', loc_p)
                file_url = upload_file(loc_p)
                if file_url is None:
                    print("上传失败")
            return file_url
        else:
            print('#warning: 文件不存在或者不是图片文件 ：', loc_p)
            return None
    else:
        print('markdown文件中的图片用的是网址 ：', match)
        file_url = transfer_online_img(match)  # 获取上传后的图片地址
        return file_url


def md_img_find(md_file):
    '''
    将给定的markdown文件里的图片本地路径转换成网上路径
    '''
    if need_back:
        bak_md = '%s.bak' % md_file
        shutil.copyfile(md_file, bak_md)  # 在执行改动之前备份原MD文件，可手动删除
        print('origin markdown file backup in: %s' % bak_md)
    post = None  # 用来存放markdown文件内容
    global total, success, failure, ignore
    with open(md_file, 'r', encoding='utf-8') as f:  # 使用utf-8 编码打开 by chalkit
        post = f.read()
        matches = re.compile('!\\[.*?\\]\\((.*?)\\)|<img.*?src=[\'\"](.*?)[\'\"].*?>').findall(post)  # 匹配md文件中的图片
        if matches is None or len(matches) == 0:
            print("%s no matches" % md_file)
            return
        for sub_match in matches:  # 正则里有个或，所以有分组，需要单独遍历去修改
            for match in sub_match:  # 遍历去修改每个图片
                if match is None or len(match) == 0:
                    continue
                total = total + 1
                print("match pic : ", match)
                file_url = upload_pic_proc(md_file, match)
                if file_url:
                    post = post.replace(match, file_url)  # 替换md文件中的地址
                else:
                    ignore += 1
        if post:
            open(md_file, 'w', encoding='utf-8').write(post)  # 如果有内容的话，就直接覆盖写入当前的markdown文件
            # 仍然注意用uft-8编码打开
    print('Complete!')
    print(' total   :%d' % total)
    print(' success :%d' % success)
    print(' failure :%d' % failure)
    print(' ignore  :%d' % ignore)


def find_md(folder):
    '''
    在给定的目录下寻找md文件
    '''
    if len(folder) > 3 and folder[folder.rfind('.') + 1:] == 'md':
        md_img_find(folder)  # 判断是否是一个md文件，如果是的话，直接开始转换
    elif os.path.isdir(folder):
        files = os.listdir(folder)
        # 读取目录下的文件
        for file in files:
            curp = folder + '/' + file
            if os.path.isdir(curp):
                find_md(curp)  # 递归读取
            elif file[file.rfind('.') + 1:] == 'md':
                md_img_find(curp)


def get_config(cfg_file_path):
    global cloud_cfg
    if os.path.exists(cfg_file_path) and os.path.isfile(cfg_file_path):
        config = configparser.ConfigParser()
        config.read(cfg_file_path, encoding="utf-8")
        try:
            option = config.get('common', 'option')
            if option == "upai":
                servicename = config.get(option, "servicename")
                operatorname = config.get(option, "operatorname")
                password = config.get(option, "password")
                domain = config.get(option, "domain")
                cloud_cfg = Upai(servicename, operatorname, password, domain)
            elif option == "qiniu":
                ak = config.get(option, "accesskey")
                sk = config.get(option, "secretkey")
                bucketname = config.get(option, "bucketname")
                domain = config.get(option, "domain")
                cloud_cfg = Qiniu(ak, sk, bucketname, domain)
            else:
                print("目前不支持除又拍、七牛以外的云存储服务")
                sys.exit(0)
            if need_zip:
                tinify.key = config.get('common', 'tinypngkey')  # 设置tinipng的key
        except configparser.NoOptionError as e:
            print("配置出错: ", e)
            sys.exit(0)
    else:
        print("配置文件路径出错")
        sys.exit(0)


def usage():
    print('''
usage: 
    python %s file [-c|--config configfile] [-z|--zip] [--cache] [-b|--back]
    python %s -R|--Recursive directory [-c|--config configfile] [-z|--zip] [-b|--back]
    python %s -h|--help
    ''' % (sys.argv[0], sys.argv[0], sys.argv[0]))


if __name__ == '__main__':
    dir_path = ''
    file_path = ''
    config_file = ''
    os_name = platform.system()
    find_err = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hR:c:zb', ["help", "Recursive=", "config=", "zip", "cache", "back"])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit(0)
            elif opt in ("-R", "--Recursive"):
                dir_path = arg
            elif opt in ("-c", "--config"):
                config_file = arg
            elif opt in ("-z", "--zip"):
                need_zip = True
            elif opt == "--cache":
                need_cache = True
            elif opt in ("-b", "--back"):
                need_back = True
            else:
                usage()
                exit(1)
        if args is not None and (len(args) != 0):
            if len(args) == 1:
                file_path = args[0]
            else:
                find_err = True
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    if (file_path and dir_path) or (not file_path and not dir_path) or find_err:
        # 两个都设置或者两个都没设置或者已经发现错误，出错
        usage()
        sys.exit(1)
    if file_path:
        c_p = file_path
        md_loc = c_p[:c_p.rfind('/') + 1]
    else:
        c_p = dir_path
        if c_p[-1] == '/':
            md_loc = c_p
        else:
            md_loc = c_p + '/'
    if not config_file:
        if os_name == 'Windows':
            print("please input config file path in Windows")
            exit(1)
        else:
            config_file = os.getenv("HOME") + "/.mdPicTransfer.cfg"
    if not os.path.exists(c_p):
        print("指定路径不存在")
        sys.exit(1)
    if not os.path.exists(config_file) or not os.path.isfile(config_file):
        print("配置文件路径出错")
        sys.exit(1)
    get_config(config_file)
    find_md(c_p)

