#!/usr/bin/env python

import vxi11
import time
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  

#����
instr = vxi11.Instrument("192.168.21.145")

#�豸��Ϣ
print(instr.ask("*IDN?"))#LANG IDN

#�ļ�����
fileName='iv_'+datetime.datetime.now().strftime('%m_%d_%H%M%S')+".txt"

#�Ƿ񱣴�����(���� ��ѹ)���ļ�
ifSaveFile = 1 # 1���� 0������

#������ε����� or ֱ�Ӳ���
ifDirecMeasure = 0 # 1ֱ�Ӳ��� 0���浽�����ٶ�ȡ

#��ʼ�ͽ�����ѹ ����
voltage_start = -20
voltage_end = 200
voltage_step = 5

#ѭ������(��������)
count=0

#����Forѭ������
n=round((voltage_end-voltage_start)/voltage_step)+1

#��������
datax = []#��ѹ
datay = []#����

#��ѹ����(��������)
cur=0
vol=0

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
plt.xlabel('voltage / v')
plt.ylabel('current / A')
figure.canvas.draw()
plt.draw()

#instr.write("*RST")#����
#instr.write(":ROUT:TERM REAR")#�������

#��������Ͳ�����Ӧ
#instr.write(':SENS:FUNC CURR')
instr.write(':SOUR:FUNC VOLT')

#��ѹ������Ƶ���
instr.write(":SOUR:VOLT:ILIM 0.0001")

#�������� �� �Զ�����
instr.write(":SOUR:VOLT:RANG:AUTO ON")
#instr.write(":SOUR:VOLT:RANG 0.2")
instr.write(':SENS:CURR:RANG:AUTO ON')
#:SENSE:CURR:UNIT OHM

#trace ����buff����
buff='buff3'

#ɾ������
if not ifDirecMeasure:
    #instr.write(':TRACe:DELete "'+buff+'"')
    time.sleep(0.1)

#trace ��������
if not ifDirecMeasure:
    instr.write(':TRACe:MAKE "'+buff+'", 100')
    time.sleep(0.1)

#print("fetch: ",instr.ask(':FETCh? "'+buff+'"'))#��ȡ����

#print("��������: ",instr.ask(':TRACe:ACTual? "'+buff+'"'))#buff�����ݸ���

#trace ����ģʽ ÿ�οɲ���������� �ͺ����±귶Χ��Ӧ:��Ϊ��Ϊ4 �����1-4����ѹ5-8
if not ifDirecMeasure:
    instr.write('COUNt 4')
    
#���ļ�
if ifSaveFile:
    file = open(fileName, "w")
    
#ѭ��
for i in range(0, n, 1):

    #������Ҫ���õĵ�ѹ
    voltage=voltage_start+voltage_step*i
    
    #���õ�ѹ
    instr.write(":SOUR:VOLT "+str(voltage))
    
    #��һ��ѭ�����õ�ѹ �ӳٴ����
    if count==0:
        time.sleep(0.2)
        instr.write(":OUTPut:STATe ON")#:OUTPut:STATe ON
        time.sleep(1)
    count+=1
    
    #��ʾ��������
    if (count*10 % (n))==0 and count <= n:
        print('> '+str(count * 100 // n)+'/'+str(100)+'   '+str(count)+' ..')
    time.sleep(3)  # sleep 1s
    
    #CURRent RESistance VOLTage
    #trace ������������buff 4��
    if not ifDirecMeasure:
        instr.ask(':MEASure:CURRent? "'+buff+'"')
    
    #trace ������ѹ����buff 4��
    if not ifDirecMeasure:
        instr.ask(':MEASure:VOLTage? "'+buff+'"')
    #time.sleep(1)
    
    #trace ���������ݸ���
    if not ifDirecMeasure:
        numbers=instr.ask(':TRACe:ACTual? "'+buff+'"')#buff�м�����
    
    #trace ���������ݿ�ʼ�ͽ������±�
    if not ifDirecMeasure:
        numberRange=instr.ask(':TRACe:ACTual:STARt? "'+buff+'" ; END? "'+buff+'"')
    
    if count==1 and not ifDirecMeasure:
        print(str(numbers)+'������'+"�±귶Χ: "+str(numberRange))
    
    #trace �����±귶Χ��ȡ����
    if not ifDirecMeasure:
        curr_str=instr.ask(':TRAC:DATA? 1, 4, "'+buff+'"')#,READ, SOUR, REL
        print("curr: ",curr_str)
        currArr=curr_str.split(',')
        #time.sleep(0.5)
    
    #trace �����±귶Χ��ȡ����
    if not ifDirecMeasure:
        vol_str=instr.ask(':TRAC:DATA? 5, 8, "'+buff+'"')#,READ, SOUR, REL
        volArr=vol_str.split(',')
        print("vol: ",vol_str)
    
    #trace
    if not ifDirecMeasure:
        curr=(float(currArr[0])+float(currArr[1])+float(currArr[2])+float(currArr[3]))/4
        vol=(float(volArr[0])+float(volArr[1])+float(volArr[2])+float(volArr[3]))/4
    
    #ֱ�ӽ��в���
    if ifDirecMeasure:
        vol = instr.ask(':MEASure:VOLT?')
        curr = instr.ask(':MEASure:CURR?')
        time.sleep(0.5)
    
    #print("fetch: ",instr.ask(':FETCh? "'+buff+'"'))

    #ת���ɺ���
    curr_save = float(curr)*1# if voltage>0 else float(curr)*-1#
    vol_save = float(vol) *1#
    
    #д���ļ�����
    if ifSaveFile:
        file.write(str(curr_save)+' '+str(vol_save))
        file.write("\n")
    
    #trace ��ջ�������
    if not ifDirecMeasure:
        instr.write(':TRAC:CLE "'+buff+'"')
    
    #����ͼ������
    datax.append(vol_save)
    datay.append(curr_save)
    lines.set_xdata(datax)
    lines.set_ydata(datay)
    
    #����������߽���ͼ��Χ
    ax.relim()
    ax.autoscale_view()
    figure.canvas.draw()
    
    #ÿ�����ǩ
    plt.text(float(vol), curr_save, '')  #str(count)
    #plt.ylim([0, max(10, max(curr_save * 1.1, 1))])  # 
    plt.draw()
    figure.canvas.flush_events()
    
    time.sleep(0.2)

time.sleep(0.1)
#trace ɾ������ռ�
if not ifDirecMeasure:
    instr.write(':TRACe:DELete "'+buff+'"')

#�ر��ļ� �ر���� 
if ifSaveFile:
    file.close()

#�ر����
instr.write(":OUTPut:STATe OFF")

#�رջ�ͼ
plt.ioff()
