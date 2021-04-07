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

def youxiaoshuzi(xiaoshu,weishu):
    a=round(xiaoshu,weishu)
    a_str=str(a)
    while(len(a_str.split('.')[1])<weishu):
        a_str+='0'
    return a_str

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

#读取pool_size
pools_sizes=[]
for i in range(group):
    pools_sizes.append(int(lcut(settings_lines[start_lines[i]+5].rstrip(),'pool_size=')))
pool_size=pools_sizes[groups.index(now_group)]

#读取PC及其对应的胜率
record_bpcs=open('记录总bpc结果.txt',mode='r',encoding='UTF-8')
record_bpcs_lines=record_bpcs.readlines()
record_bpcs.close()

PCs=[]
rates=[]
#用于排序的列表
rank_PCs=[]
rank_rates=[]
for line in record_bpcs_lines:
    if(line.startswith('Average Win Rate : ')==False):
        PCs.append(line.rstrip())
    else:
        rates.append(round(float(rcut(lcut(line.rstrip(),'Average Win Rate : '),'%')),5))
        rank_rates.append(round(float(rcut(lcut(line.rstrip(),'Average Win Rate : '),'%')),5))
#排序
rank_rates.sort(reverse=True)
for rate in rank_rates:
    rate_index=rates.index(rate)
    rank_PCs.append(PCs[rate_index])
    rates[rate_index]=-1 #选中过的rate不会再被选中，防止出现多个PC胜率恰好相等而返回其中1个的情况
#淘汰，取前pool_size个
taotai_PCs=rank_PCs[:pool_size]

#导入记录PC池子及胜率.txt
record_rates=open('记录PC池子及胜率.txt',mode='a+',encoding='UTF-8')
record_rates.write('group_'+now_group+':\n')
for PC_name in rank_PCs:
    PC=''
    for i in range(start_line_group,end_line_group+1):
        if(pools_lines[i].startswith(PC_name)==True):
            line_PC=i
            break
    for i in range(9):
        if(PC_name in taotai_PCs):
            PC+=pools_lines[line_PC+i]
        else:
            PC+='//'+pools_lines[line_PC+i]
    record_rates.write(PC)

record_rates.write('\n')
for i in range(len(rank_PCs)):
    record_rates.write(rank_PCs[i]+' Average Win Rate : '+youxiaoshuzi(rank_rates[i],5)+'%\n')
record_rates.write('\n')

#清空记录总bpc结果.txt
record_bpcs=open('记录总bpc结果.txt',mode='w+',encoding='UTF-8')
record_bpcs.close()

#换为新组，若为最后一组则换回第1组
group_index=groups.index(now_group)+1
if(group_index==group):
    group_index=0
new_group=groups[group_index]
pools_lines[1]='now_group='+new_group+'\n'
#更换新的now_PC
for line in pools_lines:
    if(rcut(lcut(line.rstrip(),'group_'),':')==new_group):
        line_new_group=pools_lines.index(line)
        break
new_PC=pools_lines[line_new_group+1].split()[0]
pools_lines[2]='now_PC='+new_PC+'\n'

pools=open('PC池子.txt',mode='w+',encoding='UTF-8')
pools.writelines(pools_lines)
pools.close()
