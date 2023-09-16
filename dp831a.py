#!/usr/bin/env python

import vxi11
import time
import datetime
import matplotlib.pyplot as plt  
from matplotlib.animation import FuncAnimation

#文件名称
fileName='data_'+datetime.datetime.now().strftime('%m_%d_%H%M%S')+".txt"

#是否保存数据(电流 电压)到文件
ifSaveFile = 1 # 1保存 0不保存

#连接
instr = vxi11.Instrument("192.168.24.72")

#设备信息
#print(instr.ask("*IDN?"))#LANG IDN

#开始和结束电压 步长
voltage_start = 1.0  
voltage_step = 0.2
voltage_end = 2.0

#循环计数(不设置)
count=0

#计数For循环次数
n=round((voltage_end-voltage_start)/voltage_step)+1

#坐标数据
datax = []
datay = []

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
plt.xlabel('vol / v')  
plt.ylabel('cur / mA')

#:MEASure:ALL[:DC]?
#:MEASure:CURRent[:DC]?
#:MEASure:POWEr[:DC]?
#:MEASure[:VOLTage][:DC]?

#选择
#print(instr.ask(":MEAS:ALL? CH1"))

#设置重置
#print(instr.write("*RST"))

#选择通道CH1
instr.write(":INST:NSEL 1")

#限流保护
instr.write(":CURR:PROT 5")
instr.write(":CURR:PROT:STAT ON")

#设置电流
instr.write(":CURR 0.1")

#打开文件
if ifSaveFile:
    file = open(fileName, "w") 
    
#循环
for i in range(0, n, 1):

    #计算需要设置的电压
    voltage=voltage_start+voltage_step*i
    
    #设置电压
    instr.write(":VOLT "+str(voltage))
    
    #第一次循环设置电压 延迟打开输出
    if count==0:
        time.sleep(0.2)
        instr.write(":OUTP CH1,ON")
    count +=1
    
    #显示测量进度
    if (count*10 % (n))==0 and count <= n:
        print('> '+str(count * 100 // n)+'/'+str(100)+'   '+str(count)+' ..')
    time.sleep(1)  # sleep 1s
    
    #获取实时电流和电压值
    curr_str=instr.ask(":MEAS:CURR:DC? CH1")
    vol_str=instr.ask(":MEAS:VOLT:DC? CH1")
    
    #转换成毫安
    current = float(curr_str) *1000  #
    voltage = float(vol_str) *1  #
    
    #写入文件保存
    if ifSaveFile:
        file.write(str(current)+' '+str(voltage))
        file.write("\n")
    
    #更新图表数据
    datax.append(voltage)
    datay.append(current)
    
    lines.set_xdata(datax)
    lines.set_ydata(datay)
    
    #调整坐标轴边界 视图范围
    ax.relim()
    ax.autoscale_view()
    figure.canvas.draw()
    
    #每个点注释
    plt.text(float(vol), current, '')  #str(count)
    #plt.ylim([0, max(10, max(current * 1.1, 1))])  #
    
    #画图和更新
    plt.draw()
    figure.canvas.flush_events()

    time.sleep(0.2)
    
#关闭文件
if ifSaveFile:
    file.close()

#关闭仪器输出
instr.write(":OUTP CH1,OFF")

#关闭画图
plt.ioff()