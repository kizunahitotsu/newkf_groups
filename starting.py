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

path=os.getcwd()
path_py=path+'/代码/'
dirs=os.listdir(path)

settings=open('settings.txt',mode='r',encoding='UTF-8')
settings_lines=settings.readlines()
settings.close()

while('\n' in settings_lines):
    settings_lines.remove('\n')

#检测字符串形式的整数是否在范围内（闭区间）
def check_range(str,min,max):
    if(str.isnumeric()==False):
        return 1
    elif(int(str) not in range(min,max+1)):
        return 1
    else:
        return 0
#检测字符串是否为ON/OFF
def check_switch(str):
    switchs=['ON','OFF']
    if(str in switchs):
        return 0
    else:
        return 1
#检测以空格分隔的一组整数是否在范围内（闭区间）
def check_ranges(str,number,mins,maxs):
    to_return=0
    strs=str.split()
    if(len(strs)!=number):
        to_return+=1
    else:
        for i in range(number):
            if(strs[i].isnumeric()==False):
                to_return+=1
            elif(int(strs[i]) not in range(mins[i],maxs[i]+1)):
                to_return+=1
    return to_return
#检测光环
def check_AURAFILTER(str):
    to_return=0
    list=['SHI','XIN','FENG','BI','MO','DUN','XUE','SHANG','SHEN','CI','REN','FEI','BO','JU','HONG','JUE']
    strs=str.split('_')
    for a in strs:
        if(a not in list):
            to_return+=1
    return to_return
#检查出错时生成空的main.bat
def error_bat():
    bat=open('main.bat',mode='w+',encoding='ANSI')
    bat.close()

start_line_global=-1
start_line_diedai=-1
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

check=0
if(group==0):
    check+=1
    print('PC组数为0，',end='')
elif(start_lines[-1]+6!=len(settings_lines)):
    check+=1
    print('行数',end='')
else:
    check+=check_range(lcut(settings_lines[start_line_global+1].rstrip(),'THREADS '),1,64)
    check+=check_range(lcut(settings_lines[start_line_global+2].rstrip(),'TESTS '),1,100000)
    check+=check_range(lcut(settings_lines[start_line_global+3].rstrip(),'SEEDMAX '),1,100000000)
    check+=check_AURAFILTER(lcut(settings_lines[start_line_global+4].rstrip(),'AURAFILTER '))
    check+=check_range(lcut(settings_lines[start_line_global+5].rstrip(),'DEFENDER '),0,2)
    check+=check_range(lcut(settings_lines[start_line_global+6].rstrip(),'VERBOSE '),0,1)
    check+=check_range(lcut(settings_lines[start_line_diedai+1].rstrip(),'turns='),1,100000000)
    check+=check_switch(lcut(settings_lines[start_line_diedai+2].rstrip(),'recording_bpc='))
    check+=check_switch(lcut(settings_lines[start_line_diedai+3].rstrip(),'recording_pools='))
    for i in range(group):
        check+=check_range(lcut(settings_lines[start_lines[i]+1].rstrip(),'guanghuan='),0,210)
        check+=check_ranges(lcut(settings_lines[start_lines[i]+2].rstrip(),'level='),3,[0,2,1],[700,4,8])
        check+=check_ranges(lcut(settings_lines[start_lines[i]+3].rstrip(),'WISH '),7,[0,0,0,0,0,0,0],[10,10,10,10,10,10,10])
        check+=check_ranges(lcut(settings_lines[start_lines[i]+4].rstrip(),'level_GEAR='),6,[1,50,50,50,50,0],[300,150,150,150,150,1])
        check+=check_range(lcut(settings_lines[start_lines[i]+5].rstrip(),'pool_size='),1,100000000)

if(check>0):
    print('填写有误，请检查settings.txt！')
    input()
    error_bat()
elif('newkf.in' not in dirs):
    print('当前目录没有找到newkf.in，请确认路径！')
    input()
    error_bat()
else:
    #检查settings.txt无误，且路径正确后
    #将对应设置填入newkf.in
    newkf=open('newkf.in',mode='r',encoding='UTF-8')
    newkf_lines=newkf.readlines()
    newkf.close()
    while('\n' in newkf_lines):
        newkf_lines.remove('\n')
    
    THREADS=settings_lines[start_line_global+1]
    TESTS=settings_lines[start_line_global+2]
    SEEDMAX=settings_lines[start_line_global+3]
    AURAFILTER=settings_lines[start_line_global+4]
    DEFENDER=settings_lines[start_line_global+5]
    VERBOSE=settings_lines[start_line_global+6]
    turns=int(lcut(settings_lines[start_line_diedai+1].rstrip(),'turns='))
    #switch_bpc=lcut(settings_lines[start_line_diedai+2].rstrip(),'recording_bpc=')
    #switch_pools=lcut(settings_lines[start_line_diedai+3].rstrip(),'recording_pools=')
    guanghuans=[]
    levels=[]
    WISHES=[]
    levels_GEAR=[]
    #pools_size=[]
    for i in range(group):
        guanghuans.append(lcut(settings_lines[start_lines[i]+1],'guanghuan='))
        levels.append(lcut(settings_lines[start_lines[i]+2],'level='))
        WISHES.append(settings_lines[start_lines[i]+3])
        levels_GEAR.append(lcut(settings_lines[start_lines[i]+4],'level_GEAR='))
        #pools_size.append(int(lcut(settings_lines[start_lines[i]+5].rstrip(),'pool_size=')))
    
    for line in newkf_lines:
        if(line.rstrip()=='PC'):
            line_PC=newkf_lines.index(line)
        if(line.rstrip()=='ENDPC'):
            line_ENDPC=newkf_lines.index(line) #line_GEAR=line_ENDPC+1
        if(line.rstrip()=='ENDGEAR'):
            line_ENDGEAR=newkf_lines.index(line)
            break
    
    newkf_lines[line_ENDGEAR+1]=THREADS
    newkf_lines[line_ENDGEAR+2]=TESTS
    newkf_lines[line_ENDGEAR+5]=SEEDMAX
    newkf_lines[line_ENDGEAR+6]=AURAFILTER
    newkf_lines[line_ENDGEAR+7]=DEFENDER
    newkf_lines[line_ENDGEAR+8]=VERBOSE
    newkf_lines.insert(line_ENDGEAR+1,'\n')

    for i in range(line_ENDPC+2,line_ENDGEAR):
        temp=newkf_lines[i].split()[0]
        newkf_lines[i]=temp+' '+levels_GEAR[0]

    newkf_lines.insert(line_ENDGEAR,'\n')
    newkf_lines.insert(line_ENDPC+2,'\n')
    newkf_lines.insert(line_ENDPC+1,'\n')

    for i in range(line_PC+1,line_ENDPC):
        newkf_lines[i]=''

    #填入PC池子
    pools=open(path_py+'PC池子.txt',mode='r',encoding='UTF-8')
    pools_lines=pools.readlines()
    pools.close()
    
    pools=open(path_py+'PC池子.txt',mode='w+',encoding='UTF-8')
    pools_lines[1]='now_group='+groups[0]+'\n'
    pools.writelines(pools_lines)
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
        newkf_lines.insert(line_PC+1,PC)
    newkf_lines.insert(line_PC+1,'\n')
    newkf_lines.insert(line_PC,'\n')

    #重置待算的PC
    for i in range(9):
        newkf_lines[i]=''
    newkf_lines.insert(0,guanghuans[0]+'\nLIN '+levels[0]+WISHES[0]+'1 1 1 1 1 1\nNONE\nNONE\nNONE\nNONE\n0\n\n')
    
    newkf=open('newkf.in',mode='w+',encoding='UTF-8')
    newkf.writelines(newkf_lines)
    newkf.close()

    #生成main1.bat
    #一行行写
    bat=open('main.bat',mode='w+',encoding='ANSI')
    bat.write('@echo off\n')
    bat.write('for /l %%k in (1,1,'+str(turns)+') do (\n')
    bat.write('for /l %%j in (1,1,'+str(group)+') do (\n')
    bat.write('for /l %%i in (1,1,6) do (\n')
    bat.write('newkf_64.exe < '+path_py+'input_apc.txt > '+path_py+'output.txt\n')
    bat.write('start /wait /b '+path_py+'记录并换卡.py\n')
    bat.write(')\n')
    bat.write('start /wait /b '+path_py+'加入池子并换组.py\n')
    bat.write(')\n')
    bat.write('for /l %%i in (1,1,'+str(group)+') do (\n')
    bat.write('start /wait /b '+path_py+'bpc部分.py\n')
    bat.write('call main2.bat\n')
    bat.write(')\n')
    bat.write('start /wait /b '+path_py+'整理池子.py\n')
    bat.write(')\n')
    bat.close()
