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

record_apc=open('记录apc.txt',mode='r',encoding='UTF-8')
record_apc_lines=record_apc.readlines()
record_apc.close()

#胜率最高的PC的序号
rates=[]
for line in record_apc_lines:
    if(line.startswith('Average Win Rate : ')==True):
        rate=round(float(rcut(lcut(line.rstrip(),'Average Win Rate : '),'%')),5)
        rates.append(rate)
PC_index=rates.index(max(rates))
#读取胜率最高的PC
names=['LIN','MO','AI','MENG','WEI','YI']
for line in record_apc_lines:
    if(len(line.split())>0):
        if(line.split()[0]==names[PC_index]):
            start_line_PC=record_apc_lines.index(line)
            PC=''
            for i in range(9):
                PC+=record_apc_lines[start_line_PC+i]
            break

pools=open('PC池子.txt',mode='r',encoding='UTF-8')
pools_lines=pools.readlines()
pools.close()

#读取当前所在组，并将该PC加入当前所在组的位置
turn=int(lcut(pools_lines[0].rstrip(),'turn='))
now_group=lcut(pools_lines[1].rstrip(),'now_group=')
PC=names[PC_index]+'_turn'+str(turn+1)+'_'+now_group+lcut(PC,names[PC_index]) #给PC加入turn和now_group的别名
line_now_group=-1
for line in pools_lines:
    if(rcut(lcut(line.rstrip(),'group_'),':')==now_group):
        line_now_group=pools_lines.index(line)
        break
pools_lines.insert(line_now_group+1,PC)

#读取所有组
settings=open(path+'settings.txt',mode='r',encoding='UTF-8')
settings_lines=settings.readlines()
settings.close()

start_lines=[]
groups=[]
for line in settings_lines:
    if(rcut(line.rstrip(),' settings:').startswith('group_')==True):
        start_lines.append(settings_lines.index(line))
        groups.append(rcut(lcut(line.rstrip(),'group_'),' settings:'))
group=len(groups)
#新组，若为最后一组则换回第1组
group_index=groups.index(now_group)+1
if(group_index==group):
    group_index=0
new_group=groups[group_index]
pools_lines[1]='now_group='+new_group+'\n'

#将新组的信息导入newkf.in
newkf=open(path+'newkf.in',mode='r',encoding='UTF-8')
newkf_lines=newkf.readlines()
newkf.close()

guanghuans=[]
levels=[]
WISHES=[]
levels_GEAR=[]
#pools_sizes=[]
for i in range(group):
    guanghuans.append(lcut(settings_lines[start_lines[i]+1],'guanghuan='))
    levels.append(lcut(settings_lines[start_lines[i]+2],'level='))
    WISHES.append(settings_lines[start_lines[i]+3])
    levels_GEAR.append(lcut(settings_lines[start_lines[i]+4],'level_GEAR='))
    #pools_sizes.append(int(lcut(settings_lines[start_lines[i]+5].rstrip(),'pool_size=')))

for line in newkf_lines:
    if(line.rstrip()=='GEAR'):
        line_GEAR=newkf_lines.index(line)
    if(line.rstrip()=='ENDGEAR'):
        line_ENDGEAR=newkf_lines.index(line)
        break
for i in range(line_GEAR+2,line_ENDGEAR-1):
    temp=newkf_lines[i].split()[0]
    newkf_lines[i]=temp+' '+levels_GEAR[group_index]

newkf_lines[0]=guanghuans[group_index]
newkf_lines[2]='LIN '+levels[group_index]
newkf_lines[3]=WISHES[group_index]

#若完成了最后1组，则准备进行bpc
if(group_index==0):
    #设置TESTS
    newkf_lines[line_ENDGEAR+3]='TESTS 10000\n'
    #临时记录PC名为第1组第1个PC
    pools_lines[2]='now_PC='+pools_lines[5].split()[0]+'\n'
    #更新turn
    pools_lines[0]='turn='+str(turn+1)+'\n'

pools=open('PC池子.txt',mode='w+',encoding='UTF-8')
pools.writelines(pools_lines)
pools.close()

newkf=open(path+'newkf.in',mode='w+',encoding='UTF-8')
newkf.writelines(newkf_lines)
newkf.close()

#清空记录apc.txt
record_apc=open('记录apc.txt',mode='w+',encoding='UTF-8')
record_apc.close()
