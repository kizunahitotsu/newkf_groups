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

#读取当前组和当前PC
pools=open('PC池子.txt',mode='r',encoding='UTF-8')
pools_lines=pools.readlines()
pools.close()

turn=int(lcut(pools_lines[0].rstrip(),'turn='))
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

#读取对各PC胜率以及总胜率
output=open('output.txt',mode='r',encoding='UTF-8')
output_lines=output.readlines()
output.close()

for line in output_lines:
    if(line.startswith('Average Win Rate : ')==True):
        line_rate=output_lines.index(line)
        break

#将总胜率填入 记录总bpc结果.txt
record_bpcs=open('记录总bpc结果.txt',mode='a+',encoding='UTF-8')
record_bpcs.write(now_PC+'\n')
record_bpcs.write(output_lines[line_rate])
record_bpcs.close()

#若now_PC为最新一轮的PC，且在settings.txt中开启了记录bpc，则将其记录至 记录bpc.txt
if(lcut(now_PC.split('_')[1],'turn')==str(turn)):
    settings=open(path+'settings.txt',mode='r',encoding='UTF-8')
    settings_lines=settings.readlines()
    settings.close()
    for line in settings_lines:
        if(line.startswith('recording_bpc=')==True):
            switch_bpc=lcut(line.rstrip(),'recording_bpc=')
            break
    if(switch_bpc=='ON'):
        #记录now_PC
        for i in range(start_line_group,end_line_group+1):
            if(pools_lines[i].startswith(now_PC)==True):
                index_PC=i
                break
        record_bpc=open('记录bpc.txt',mode='a+',encoding='UTF-8')
        for i in range(9):
            record_bpc.write(pools_lines[index_PC+i])
        #记录胜率
        for line in output_lines:
            if(line.rstrip()=='<enemy> := NPC <n> | PC <n> | PC <alias> | <NPCType> <Level> <PowerUp>'):
                start_line_rates=output_lines.index(line)+1
                break
        for i in range(start_line_rates,line_rate+1):
            record_bpc.write(output_lines[i])
        record_bpc.write('\n')
        record_bpc.close()

#读取当前组的PC名
now_PCs=[]
for i in range(start_line_group,end_line_group+1):
    if(pools_lines[i].startswith('WISH ')==True):
        now_PCs.append(pools_lines[i-1].split()[0])
#读取新PC名，并填入PC池子.txt
PC_index=now_PCs.index(now_PC)+1
if(PC_index==len(now_PCs)):
    PC_index=0
new_PC=now_PCs[PC_index]
pools_lines[2]='now_PC='+new_PC+'\n'
pools=open('PC池子.txt',mode='w+',encoding='UTF-8')
pools.writelines(pools_lines)
pools.close()
