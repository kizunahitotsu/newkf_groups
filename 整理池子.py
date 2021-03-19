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

#读取所有组以及settings
settings=open(path+'settings.txt',mode='r',encoding='UTF-8')
settings_lines=settings.readlines()
settings.close()

start_lines=[]
groups=[]
for line in settings_lines:
    if(line.rstrip()=='global settings:'):
        start_line_global=settings_lines.index(line)
    if(line.rstrip()=='diedai settings:'):
        start_line_diedai=settings_lines.index(line)
    if(rcut(line.rstrip(),' settings:').startswith('group_')==True):
        start_lines.append(settings_lines.index(line))
        groups.append(rcut(lcut(line.rstrip(),'group_'),' settings:'))
group=len(groups)

TESTS=settings_lines[start_line_global+2]
switch_bpc=lcut(settings_lines[start_line_diedai+2].rstrip(),'recording_bpc=')
switch_pools=lcut(settings_lines[start_line_diedai+3].rstrip(),'recording_pools=')
guanghuans=[]
levels=[]
WISHES=[]
levels_GEAR=[]
for i in range(group):
    guanghuans.append(lcut(settings_lines[start_lines[i]+1],'guanghuan='))
    levels.append(lcut(settings_lines[start_lines[i]+2],'level='))
    WISHES.append(settings_lines[start_lines[i]+3])
    levels_GEAR.append(lcut(settings_lines[start_lines[i]+4],'level_GEAR='))

#将记录PC池子及胜率.txt内的PC导入PC池子.txt
record_rates=open('记录PC池子及胜率.txt',mode='r',encoding='UTF-8')
record_rates_lines=record_rates.readlines()
record_rates.close()
turn=int(lcut(record_rates_lines[0].rstrip(),'turn='))

#前3行
pools=open('PC池子.txt',mode='w+',encoding='UTF-8')
pools.write('turn='+str(turn)+'\n')
pools.write('now_group='+groups[0]+'\n')
pools.write('now_PC='+'\n\n')
#找到每组所在行
start_lines_PC=[]
for i in range(group):
    for line in record_rates_lines:
        if(rcut(lcut(line.rstrip(),'group_'),':')==groups[i]):
            start_lines_PC.append(record_rates_lines.index(line))
            break
#导入每组PC
for i in range(group):
    index=start_lines_PC[i]
    while(True):
        if(record_rates_lines[index].startswith('//')==True):
            break
        elif(record_rates_lines[index]=='\n' and record_rates_lines[index-1]=='\n'):
            break
        else: #若该行不以//开头且不是连续2行空行则写入
            pools.write(record_rates_lines[index])
            index+=1
pools.close()

#将newkf.in初始化
newkf=open(path+'newkf.in',mode='r',encoding='UTF-8')
newkf_lines=newkf.readlines()
newkf.close()

for line in newkf_lines:
    if(line.rstrip()=='PC'):
        line_PC=newkf_lines.index(line)
    if(line.rstrip()=='ENDPC'):
        line_ENDPC=newkf_lines.index(line)
    if(line.rstrip()=='ENDGEAR'):
        line_ENDGEAR=newkf_lines.index(line)
        break
#重置TESTS
newkf_lines[line_ENDGEAR+3]=TESTS
#填入PC池子
for i in range(line_PC+2,line_ENDPC):
    newkf_lines[i]=''

pools=open('PC池子.txt',mode='r',encoding='UTF-8')
pools_lines=pools.readlines()
pools.close()

PCs=[]
index=0
while(index<len(pools_lines)):
    if(pools_lines[index].startswith('WISH ')==True):
        PC_temp=''
        for i in range(9):
            PC_temp+=pools_lines[index-1+i]
        PCs.append(PC_temp)
    index+=1
PCs.reverse()
for PC in PCs:
    newkf_lines.insert(line_PC+2,PC)

#重置待算的PC
for i in range(11):
    newkf_lines[i]=''
newkf_lines.insert(0,guanghuans[0]+'\nLIN '+levels[0]+WISHES[0]+'1 1 1 1 1 1\nNONE\nNONE\nNONE\nNONE\n0\n\n')

newkf=open(path+'newkf.in',mode='w+',encoding='UTF-8')
newkf.writelines(newkf_lines)
newkf.close()

#若开启记录bpc，则将记录bpc.txt移动到/记录 下
if(switch_bpc=='ON'):
    os.rename(path_py+'/记录bpc.txt',path+'记录/记录bpc_turn'+str(turn)+'.txt')
    record_bpc=open('记录bpc.txt',mode='w+',encoding='UTF-8')
    record_bpc.close()

#若开启记录池子，则将记录PC池子和胜率.txt移动到/记录 下
if(switch_pools=='ON'):
    os.rename(path_py+'/记录PC池子及胜率.txt',path+'记录/记录PC池子及胜率_turn'+str(turn)+'.txt')

#将记录PC池子及胜率.txt初始化
record_rates=open('记录PC池子及胜率.txt',mode='w+',encoding='UTF-8')
record_rates.write('turn='+str(turn+1)+'\n\n') #为下一轮迭代做准备
record_rates.close()

print('已完成第',turn,'轮迭代！')
