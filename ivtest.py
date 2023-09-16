#!/usr/bin/env python

import vxi11
import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  

#连接
instr = vxi11.Instrument("192.168.21.145")

#设备信息
print(instr.ask("*IDN?"))#LANG IDN

#文件名称
fileName='iv_'+datetime.datetime.now().strftime('%m_%d_%H%M%S')+".txt"

#是否保存数据(电流 电压)到文件
ifSaveFile = 1 # 1保存 0不保存

#测量多次到缓存 or 直接测量
ifDirecMeasure = 0 # 1直接测量 0保存到缓存再读取

#开始和结束电压 步长
voltage_start = -20
voltage_end = 200
voltage_step = 5

#循环计数(不用设置)
count=0

#计算For循环次数
n=round((voltage_end-voltage_start)/voltage_step)+1

#坐标数据
datax = []#电压
datay = []#电流

#电压电流(不用设置)
cur=0
vol=0

#画图初始化
plt.ion()
figure, ax = plt.subplots()
lines, = ax.plot([], [],'ro')

#坐标自动范围
ax.set_autoscaley_on(True)

#图形显示网格
ax.grid()

#标题 轴标签
plt.title('I - V')
plt.xlabel('voltage / v')
plt.ylabel('current / A')
figure.canvas.draw()
plt.draw()

#instr.write("*RST")#重置
#instr.write(":ROUT:TERM REAR")#背部输出

#设置输出和测量对应
#instr.write(':SENS:FUNC CURR')
instr.write(':SOUR:FUNC VOLT')

#电压输出限制电流
instr.write(":SOUR:VOLT:ILIM 0.0001")

#设置量程 或 自动量程
instr.write(":SOUR:VOLT:RANG:AUTO ON")
#instr.write(":SOUR:VOLT:RANG 0.2")
instr.write(':SENS:CURR:RANG:AUTO ON')
#:SENSE:CURR:UNIT OHM

#trace 定义buff名称
buff='buff3'

#删除缓存
if not ifDirecMeasure:
    #instr.write(':TRACe:DELete "'+buff+'"')
    time.sleep(0.1)

#trace 创建缓存
if not ifDirecMeasure:
    instr.write(':TRACe:MAKE "'+buff+'", 100')
    time.sleep(0.1)

#print("fetch: ",instr.ask(':FETCh? "'+buff+'"'))#读取数据

#print("数据数量: ",instr.ask(':TRACe:ACTual? "'+buff+'"'))#buff中数据个数

#trace 缓存模式 每次可测量多个数据 和后面下标范围对应:若为此为4 则电流1-4，电压5-8
if not ifDirecMeasure:
    instr.write('COUNt 4')
    
#打开文件
if ifSaveFile:
    file = open(fileName, "w")
    
#循环
for i in range(0, n, 1):

    #计算需要设置的电压
    voltage=voltage_start+voltage_step*i
    
    #设置电压
    instr.write(":SOUR:VOLT "+str(voltage))
    
    #第一次循环设置电压 延迟打开输出
    if count==0:
        time.sleep(0.2)
        instr.write(":OUTPut:STATe ON")#:OUTPut:STATe ON
        time.sleep(1)
    count+=1
    
    #显示测量进度
    if (count*10 % (n))==0 and count <= n:
        print('> '+str(count * 100 // n)+'/'+str(100)+'   '+str(count)+' ..')
    time.sleep(3)  # sleep 1s
    
    #CURRent RESistance VOLTage
    #trace 测量电流放入buff 4次
    if not ifDirecMeasure:
        instr.ask(':MEASure:CURRent? "'+buff+'"')
    
    #trace 测量电压放入buff 4次
    if not ifDirecMeasure:
        instr.ask(':MEASure:VOLTage? "'+buff+'"')
    #time.sleep(1)
    
    #trace 缓存中数据个数
    if not ifDirecMeasure:
        numbers=instr.ask(':TRACe:ACTual? "'+buff+'"')#buff中几个数
    
    #trace 缓存中数据开始和结束的下标
    if not ifDirecMeasure:
        numberRange=instr.ask(':TRACe:ACTual:STARt? "'+buff+'" ; END? "'+buff+'"')
    
    if count==1 and not ifDirecMeasure:
        print(str(numbers)+'个数，'+"下标范围: "+str(numberRange))
    
    #trace 根据下标范围读取缓存
    if not ifDirecMeasure:
        curr_str=instr.ask(':TRAC:DATA? 1, 4, "'+buff+'"')#,READ, SOUR, REL
        print("curr: ",curr_str)
        currArr=curr_str.split(',')
        #time.sleep(0.5)
    
    #trace 根据下标范围读取缓存
    if not ifDirecMeasure:
        vol_str=instr.ask(':TRAC:DATA? 5, 8, "'+buff+'"')#,READ, SOUR, REL
        volArr=vol_str.split(',')
        print("vol: ",vol_str)
    
    #trace
    if not ifDirecMeasure:
        curr=(float(currArr[0])+float(currArr[1])+float(currArr[2])+float(currArr[3]))/4
        vol=(float(volArr[0])+float(volArr[1])+float(volArr[2])+float(volArr[3]))/4
    
    #直接进行测量
    if ifDirecMeasure:
        vol = instr.ask(':MEASure:VOLT?')
        curr = instr.ask(':MEASure:CURR?')
        time.sleep(0.5)
    
    #print("fetch: ",instr.ask(':FETCh? "'+buff+'"'))

    #转换成毫安
    curr_save = float(curr)*1# if voltage>0 else float(curr)*-1#
    vol_save = float(vol) *1#
    
    #写入文件保存
    if ifSaveFile:
        file.write(str(curr_save)+' '+str(vol_save))
        file.write("\n")
    
    #trace 清空缓存数据
    if not ifDirecMeasure:
        instr.write(':TRAC:CLE "'+buff+'"')
    
    #更新图表数据
    datax.append(vol_save)
    datay.append(curr_save)
    lines.set_xdata(datax)
    lines.set_ydata(datay)
    
    #调整坐标轴边界视图范围
    ax.relim()
    ax.autoscale_view()
    figure.canvas.draw()
    
    #每个点标签
    plt.text(float(vol), curr_save, '')  #str(count)
    #plt.ylim([0, max(10, max(curr_save * 1.1, 1))])  # 
    plt.draw()
    figure.canvas.flush_events()
    
    time.sleep(0.2)

time.sleep(0.1)
#trace 删除缓存空间
if not ifDirecMeasure:
    instr.write(':TRACe:DELete "'+buff+'"')

#关闭文件 关闭输出 
if ifSaveFile:
    file.close()

#关闭输出
instr.write(":OUTPut:STATe OFF")

#关闭画图
plt.ioff()
