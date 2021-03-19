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

newkf=open(path+'newkf.in',mode='r',encoding='UTF-8')
newkf_lines=newkf.readlines()
newkf.close()

#读取当前组和当前PC
pools=open('PC池子.txt',mode='r',encoding='UTF-8')
pools_lines=pools.readlines()
pools.close()

now_group=lcut(pools_lines[1].rstrip(),'now_group=')
now_PC=lcut(pools_lines[2].rstrip(),'now_PC=')

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

#找到now_PC，并在PC列表里去掉now_PC，PC列表由PC池子.txt里去掉多余的内容构成
PCs=[]
for line in pools_lines:
    PCs.append(line)
PC=''
for i in range(start_line_group,end_line_group+1):
    if(pools_lines[i].startswith(now_PC)==True):
        for j in range(9):
            if(j==0):
                PC+=now_PC.split('_')[0]+lcut(pools_lines[i+j],now_PC) #去掉别名
            else:
                PC+=pools_lines[i+j]
            PCs[i+j]=''
        break

for line in PCs:
    if(line.startswith('group_')==True):
        PCs.remove(line)
PCs=PCs[3:]

#将PCs填入newkf.in
for line in newkf_lines:
    if(line.rstrip()=='PC'):
        line_PC=newkf_lines.index(line)
    if(line.rstrip()=='ENDPC'):
        line_ENDPC=newkf_lines.index(line)
        break
for i in range(line_PC+1,line_ENDPC):
    newkf_lines[i]=''

PCs.reverse()
for line in PCs:
    newkf_lines.insert(line_PC+1,line)

#将PC填入newkf.in
for i in range(11):
    newkf_lines[i]=''
newkf_lines.insert(0,PC)

#读取光环并填入newkf.in
settings=open(path+'settings.txt',mode='r',encoding='UTF-8')
settings_lines=settings.readlines()
settings.close()

for line in settings_lines:
    if(rcut(lcut(line.rstrip(),'group_'),' settings:')==now_group):
        guanghuan=lcut(settings_lines[settings_lines.index(line)+1],'guanghuan=')
        break
newkf_lines.insert(0,guanghuan+'\n')

newkf=open(path+'newkf.in',mode='w+',encoding='UTF-8')
newkf.writelines(newkf_lines)
newkf.close()
