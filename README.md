# [scrapy-spider-mm131](https://github.com/cuevven/scrapy-spider-mm131)

最近在学 python 爬虫，所以写了个脚本抓取 mm131.net 练练手。

## :star: 特性

- 使用了爬虫框架 scrapy
- user-agent 使用了fake-useragent
- 使用 python 3.7

## :open_file_folder: 目录介绍

```
scrapymm131 项目主目录
├── scrapymm131 爬虫主目录
│   └── spiders 爬虫脚本目录
├── CHANGELOG.md 变更日志
└── TODO.md 计划功能
```

## :rocket: 使用者指南

确保已经安装了 scrapy 库及相关依赖

```bash
$ pip install scrapy
```

确保已经安装了 fake-useragent

```bash
$ pip install fake-useragent
```

将脚本 clone 到本地，进入到脚本目录启动爬虫

```bash
$ scrapy crawl mm131
```

## :gear: 更新日志
[CHANGELOG.md](./CHANGELOG.md)

## :airplane: 计划列表
[TODO.md](./TODO.md)

## 相关链接

- [scrapy](https://github.com/scrapy/scrapy)
- [fake-useragent](https://github.com/hellysmile/fake-useragent)
- [教会我怎么写爬虫，思路基本来源于此](http://www.scrapyd.cn)
