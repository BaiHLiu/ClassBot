# ClassBot
A simple assistant for class clerk.

### 目前状态：为了不耽误其他功能快速上线，临时改为public，大家遇到不对劲的地方直接改好并pr即可。

### ⚠️本项目仅供其他班长测试学习，其中包含巨多错误和不足。

## 目录结构说明
```
.
├── adminManager  [管理员配置模块]
│   ├── __init__.py
│   ├── adminConf.py
│   └── admin_list.txt
├── changZheng  [示例插件-长征路截图收集]
│   ├── CZ_dbconn.py
│   ├── __init__.py
│   ├── compress.py
│   ├── compressed
│   ├── images
│   ├── ocrplus.py
│   └── plugin_main.py
├── conf  [配置文件]
│   ├── botConf_default.json  [默认配置文件]
│   ├── qqbot.sql  [mysql结构]
│   └── requirements.txt  [python依赖列表]
├── globalAPI  [全局接口]
│   ├── CB_logger.py  [日志模块]
│   ├── __init__.py
│   ├── dbconn.py  [全局数据库连接]
│   ├── goapi.py  [go-cq接口]
│   ├── inputFilter.py  [简单输入过滤]
│   └── register.py  [用户注册模块]
├── main.py  [Flask主程序]
└── router.py  [消息路由]
```

## 使用和配置
 1.修改./conf/botConf_default.json 为./conf/botConf.json
 2.导入qqbot.sql，相关配置写入./conf/botConf.json
 3.启动go-cqhttp，注意修改Flask http参数和go-cq api参数。

## 功能开发注意
** 当然这只是本菜鸡为了快速上功能而约定的，如果有不合适的地方请调整后pr即可。 **

以下内容以新增"classAlert"功能为例。

 1.每个插件独占一个目录，如此处应使"classAlert"目录与main.py同级。插件的入口文件名为"plugin_main.py"。

 2.建议plugin_main.py内使用

```python
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
#添加当前目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#添加上级目录
```

 3.调用全局接口示例

```python
import adminManager.adminConf as adminConf
import globalAPI.dbconn as globalDB
import globalAPI.goapi as goapi
import globalAPI.inputFilter as inputFilter
```

4.调用本插件目录内的模块示例

```python
import compress
import CZ_dbconn as dbconn
import ocrplus
```

**5.插件任何文件操作必须使用绝对路径**

建议使用

```python
cwd = os.path.dirname(os.path.realpath(__file__))
```

来获取某插件本身的存储路径，而**不是工作路径**。

6.建议插件内每个文件都加前缀。例如"CZ_plugin_main"代表"长走长征路"插件的main文件。但时间仓促，代码中并未添加该前缀，后续设计插件时请注意。

7.所有插件使用一个数据库，数据表必须加前缀。如"CA_submit"、"XB_user"。建议用户信息表，使用公共的"userinfo"，其他插件不宜再增加用户信息表。
