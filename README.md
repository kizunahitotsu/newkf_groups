# newkf分组迭代
1.确保已安装python，并且默认用python启动.py文件
2.将main的所有文件放入与计算器相同目录，然后将 代码 分支的所有文件放入 /代码 下（注意备份，若出错可以将各txt还原）
3.新建 记录 文件夹，使得存在 /记录 路径
4.正确填写settings.txt，其中：
global settings为计算器的设置，按照计算器的要求填写即可
diedai settings为迭代设置，其中turns为要迭代的轮数，recording_bpc和recording_pools为是否要记录bpc/PC池子，若开启则记录至 /记录 下
group setting为对单组PC进行设置，其中group_后面为组名，组名理论上可以是不含空格和'\','_'之类的东西的任意字符串，暂时没测试过中文会不会有乱码
pool_size为该组PC池子大小，若PC数量不足则会填充，超过则会淘汰其中胜率最低的
settings.txt对空行和行末空格不作要求，但整体有较为严格的检查，若出错请仔细检查有无填错
不需要管newkf.in，该填的都填入settings.txt即可
5.检查 /代码 下的 PC池子.txt，如有手动设置组或手动设置PC，需保证每组的组名和PC名对应，每组下至少有一个PC，且空行较为严格，格式要求见示例
6.运行迭代.bat
7.迭代运行过程中会生成main.bat和main2.bat，请不要单独运行它们
8.如有出错，在群里反馈（
