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
    path_py=path_working

#读取当前组
pools=open('PC池子.txt',mode='r',encoding='UTF-8')
pools_lines=pools.readlines()
pools.close()
now_group=lcut(pools_lines[1].rstrip(),'now_group=')

#确定当前组所包含的行
index=0
start_line_group=-1
while(index<len(pools_lines)):
    if(rcut(lcut(pools_lines[index].rstrip(),'group_'),':')==now_group):
        start_line_group=index+1
    if(pools_lines[index].startswith('group_')==True):
        end_line_group=index-1
        if(end_line_group>start_line_group and start_line_group>-1): #start_line_group已确定，且找到下一组
            break
    if(index==len(pools_lines)-1): #最后一组
        end_line_group=index
        break
    index+=1

PC_number=0
for i in range(start_line_group,end_line_group+1):
    if(pools_lines[i].startswith('WISH ')==True):
        PC_number+=1

#生成main2.bat
#一行行写
bat=open(path+'main2.bat',mode='w+',encoding='ANSI')
bat.write('@echo off\n')
bat.write('for /l %%i in (1,1,'+str(PC_number)+') do (\n')
bat.write('start /wait /b '+path_py+'/准备bpc.py\n')
bat.write('newkf_64.exe < '+path_py+'/input_bpc.txt > '+path_py+'/output.txt\n')
bat.write('start /wait /b '+path_py+'/导出bpc结果.py\n')
bat.write(')\n')
bat.write('start /wait /b '+path_py+'/淘汰并记录.py\n')
bat.close()
