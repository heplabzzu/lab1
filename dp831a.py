#!/usr/bin/env python

import vxi11
import time
import datetime
import matplotlib.pyplot as plt  
from matplotlib.animation import FuncAnimation

#�ļ�����
fileName='data_'+datetime.datetime.now().strftime('%m_%d_%H%M%S')+".txt"

#�Ƿ񱣴�����(���� ��ѹ)���ļ�
ifSaveFile = 1 # 1���� 0������

#����
instr = vxi11.Instrument("192.168.24.72")

#�豸��Ϣ
#print(instr.ask("*IDN?"))#LANG IDN

#��ʼ�ͽ�����ѹ ����
voltage_start = 1.0  
voltage_step = 0.2
voltage_end = 2.0

#ѭ������(������)
count=0

#����Forѭ������
n=round((voltage_end-voltage_start)/voltage_step)+1

#��������
datax = []
datay = []

#��ͼ��ʼ��
plt.ion()
figure, ax = plt.subplots()
lines, = ax.plot([], [],'ro')

#�����Զ���Χ
ax.set_autoscaley_on(True)

#ͼ����ʾ����
ax.grid()

#���� ���ǩ
plt.title('I - V')
plt.xlabel('vol / v')  
plt.ylabel('cur / mA')

#:MEASure:ALL[:DC]?
#:MEASure:CURRent[:DC]?
#:MEASure:POWEr[:DC]?
#:MEASure[:VOLTage][:DC]?

#ѡ��
#print(instr.ask(":MEAS:ALL? CH1"))

#��������
#print(instr.write("*RST"))

#ѡ��ͨ��CH1
instr.write(":INST:NSEL 1")

#��������
instr.write(":CURR:PROT 5")
instr.write(":CURR:PROT:STAT ON")

#���õ���
instr.write(":CURR 0.1")

#���ļ�
if ifSaveFile:
    file = open(fileName, "w") 
    
#ѭ��
for i in range(0, n, 1):

    #������Ҫ���õĵ�ѹ
    voltage=voltage_start+voltage_step*i
    
    #���õ�ѹ
    instr.write(":VOLT "+str(voltage))
    
    #��һ��ѭ�����õ�ѹ �ӳٴ����
    if count==0:
        time.sleep(0.2)
        instr.write(":OUTP CH1,ON")
    count +=1
    
    #��ʾ��������
    if (count*10 % (n))==0 and count <= n:
        print('> '+str(count * 100 // n)+'/'+str(100)+'   '+str(count)+' ..')
    time.sleep(1)  # sleep 1s
    
    #��ȡʵʱ�����͵�ѹֵ
    curr_str=instr.ask(":MEAS:CURR:DC? CH1")
    vol_str=instr.ask(":MEAS:VOLT:DC? CH1")
    
    #ת���ɺ���
    current = float(curr_str) *1000  #
    voltage = float(vol_str) *1  #
    
    #д���ļ�����
    if ifSaveFile:
        file.write(str(current)+' '+str(voltage))
        file.write("\n")
    
    #����ͼ������
    datax.append(voltage)
    datay.append(current)
    
    lines.set_xdata(datax)
    lines.set_ydata(datay)
    
    #����������߽� ��ͼ��Χ
    ax.relim()
    ax.autoscale_view()
    figure.canvas.draw()
    
    #ÿ����ע��
    plt.text(float(vol), current, '')  #str(count)
    #plt.ylim([0, max(10, max(current * 1.1, 1))])  #
    
    #��ͼ�͸���
    plt.draw()
    figure.canvas.flush_events()

    time.sleep(0.2)
    
#�ر��ļ�
if ifSaveFile:
    file.close()

#�ر��������
instr.write(":OUTP CH1,OFF")

#�رջ�ͼ
plt.ioff()