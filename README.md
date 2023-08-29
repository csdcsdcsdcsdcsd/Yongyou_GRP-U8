## 用友GRP-U8 info.log存在信息泄露
直接访问log日志，泄露敏感信息
```
fofa:body="U8Accid" || title="GRP-U8" || body="用友优普信息技术有限公司"
```
```
Usage:
  python3 GRP-U8_loginfo.py -u http://www.example.com 单个url测试
  python3 GRP-U8_loginfo.py -f url.txt 批量检测
```
![](https://github.com/csdcsdcsdcsdcsd/Yongyou_GRP-U8_POC/blob/main/YongYou_GRP-U8.png)

会在当前目录生成存在漏洞的vuln.txt文件
