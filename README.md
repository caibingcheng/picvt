## PICVT

用于静态博客的图床转换工具

## 使用
例如:
```Shell
python3 ./picvt.py -D ../blog/content/posts/ -F imgtu -T github -t **** --repo resources --branch main --path images
```
更多参数参考`python3 ./picvt.py -h`:
```Shell
usage: picvt.py [-h] [-u USER] [-p PASSWORD] [-t TOKEN]
                [-f FORMAT [FORMAT ...]] [-r RETRY] [--repo REPO]
                [--branch BRANCH] [--path PATH] -D DIR -F {imgtu,github} -T
                {imgtu,github}

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  target user
  -p PASSWORD, --password PASSWORD
                        target password
  -t TOKEN, --token TOKEN
                        target token
  -f FORMAT [FORMAT ...], --format FORMAT [FORMAT ...]
                        file format
  -r RETRY, --retry RETRY
                        retry times
  --repo REPO           repo name
  --branch BRANCH       branch name
  --path PATH           content path
  -D DIR, --dir DIR     target dir
  -F {imgtu,github}, --from {imgtu,github}
                        from
  -T {imgtu,github}, --to {imgtu,github}
                        to
```

## 已支持的图床

- github
```
python3 ./picvt.py -D ../blog/content/posts/ -F imgtu -T github -t **** --repo resources --branch main --path images
```

- imgtu (download)
```
python3 ./picvt.py -D ../blog/content/posts/ -F imgtu -T github -t **** --repo resources --branch main --path images
```

- local (upload)
```
python3 ./picvt.py -D ../blog/content/ -F github -T local --path /home/xxx/projects/blog/content/statics/
```


## 添加支持

在`platforms`中添加`platforms/picvt_xxxx.py`, 比如`platforms/picvt_github.py`. 然后在`platforms/picvt_config.json`中添加关于此platform的配置.

### 主要处理文件`platforms/picvt_xxxx.py`

需要实现一个名为Porcess的类, 继承自PICVT, 如:
```Python
class Process(PICVT):
    pass
```

#### extract
需要实现一个名为`extract`的方法, 如:
```Python
def extract(self, content):
    return None
```
`extract`将用于原图床的链接提取, 输入是一段`string`, 比如一篇`markdown`的原始数据, 实现者需要从中提取出待转换的图床链接, 并使用一个`list`返回.

#### download
需要实现一个名为`download`的方法, 如:
```Python
def download(self, url):
    return False, None
```
`download`将用于原图床图片的下载, 并且需要将下载文件保存在本地磁盘, 其输入是原图床图片的链接, 输出是下载成功的状态以及保存的本地文件地址, 如果下载失败, 则本地文件地址为`None`.
父类`PICVT`中提供了`download`的实现, 但是不适用于所有平台, 所以特殊平台需要自己实现`download`方法.

#### upload
需要实现一个名为`upload`的方法, 如:
```Python
def upload(self, path, params):
    return False, None
```
`upload`将用于新图床的上传, 输入参数为本地需要上传的文件的路径, 以及与图床登录相关的参数, 包括但不限于用户名/密码/token. 该方法将返回上传成功与否的状态, 以及新图床的外链, 如果上传失败, 则外链应该为`None`.

