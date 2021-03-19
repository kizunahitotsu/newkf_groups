import os

def lcut(str,chars):
    if(str.startswith(chars)==True):
        return str[len(chars):]
    else:
        return str
def rcut(str,chars):
    if(str.endswith(chars)==True):
        return str[:-len(chars)]
    else:
        return str

path_working=os.getcwd()
dirs=os.listdir(path_working)
if('main.bat' in dirs):
    #正常运行.bat时，工作目录与.bat相同，需要改变工作目录
    path=path_working+'/'
    path_py=path+'代码'
    os.chdir(path_py)
else:
    #单独运行.py时的工作目录
    path=rcut(path_working,'代码')
    #path_py=path_working

#读取apc结果
output=open('output.txt',mode='r',encoding='UTF-8')
output_lines=output.readlines()
output.close()

for line in output_lines:
    if(line=='Attribute Result:\n'):
        start_line_result=output_lines.index(line)+1
    if(line.startswith('Average Win Rate : ')==True):
        line_WinRate=output_lines.index(line)
        break

#记录apc结果
record_apc=open('记录apc.txt',mode='a+',encoding='UTF-8')
record_apc.writelines(output_lines[start_line_result:start_line_result+9])
record_apc.write(output_lines[line_WinRate]+'\n')
record_apc.close()

newkf=open(path+'newkf.in',mode='r',encoding='UTF-8')
newkf_lines=newkf.readlines()
newkf.close()
#按照LIN,MO,AI,MENG,WEI,YI,LIN的顺序换卡
names=['LIN','MO','AI','MENG','WEI','YI','LIN']
name=newkf_lines[2].split()[0]
temp=lcut(newkf_lines[2],name)
new_name=names[names.index(name)+1]
newkf_lines[2]=new_name+temp

newkf=open(path+'newkf.in',mode='w+',encoding='UTF-8')
newkf.writelines(newkf_lines)
newkf.close()
