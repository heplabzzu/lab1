import vxi11
import time
import datetime
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#############        ���� start       ##########

#����
instr = vxi11.Instrument("192.168.24.6")

rangeMin = -2 #bin��෶Χ 0
rangeMax = 5 #bin�Ҳ෶Χ 0.07
bins = 150 #bin������

#���ֻ����źŸ߶�
calculusOrHeight= 'cal' #cal(�������) hei(�źŸ߶�)

#�ź�������俪ʼ�ͽ��� calģʽ����Ҫ����
signalStart = 450
signalEnd = 630

#ȡ�����ʱ��(����)
delayTime=300  #microSecond

#Ҫ��ȡ��������
dataNumber=2000

#�������ݵ��ļ�����
fileName='rpc_'+calculusOrHeight+'_'+datetime.datetime.now().strftime('%m_%d_%H%M%S')+".txt"

#�Ƿ񱣴����ݵ��ļ�
ifSaveFile = 1 # 1���� 0������


#############        ���� end       ##########


#�豸��Ϣ
#print(instr.ask("*IDN?"))#
#�Զ�����
#instr.write(":AUToscale")#auto

#basePos=instr.ask(":TIMebase:HREFerence:POSition?")
#print(":TIMebase:HREFerence:POSition? ",basePos)

#print(":TIMebase:DELay:SCALe? ",instr.ask(":TIMebase:DELay:SCALe?"))

#print(":TIMebase:MAIN:OFFSet? ",instr.ask(":TIMebase:MAIN:OFFSet?"))#λ��
#instr.write(":TIMebase:MAIN:OFFSet 0")#0.000000005

#print(":TIMebase:MAIN:SCALe? ",instr.ask(":TIMebase:MAIN:SCALe?"))#ʱ��
#instr.write(":TIMebase:MAIN:SCALe 0.0000002")

#print("TIMebase:DELay OFFSet? ",instr.ask(":TIMebase:DELay:OFFSet?"))
#############         CHANnel        ##########
#ͨ������
#cHANnel1Dis = instr.ask(":CHANnel1:DISPlay?")#
#print(":CHANnel1:DISPlay? ",cHANnel1Dis)
#instr.write(":CHANnel2:DISPlay ON")#1 ON 0 OFF

#��ֱƫ��
#instr.write(":CHANnel2:OFFSet 0.01")#

#��ֱscale����
#instr.write(":CHANnel1:SCALe 0.01")#Ĭ��΢���ر� ֻ��1-2-5 ����
#instr.write(":CHANnel2:VERNier OFF")#

#############         TRIGger        ##########
#����ģʽ
#sWEep = instr.ask(":TRIGger:SWEep?")#
#print(":TRIGger:SWEep? ",sWEep)
#instr.write(":TRIGger:SWEep AUTO")#AUTO|NORMal|SINGle

#
#sWEep = instr.ask(":TRIGger:EDGE:SOURce?")#
#print(":TRIGger:EDGE:SOURce? ",sWEep)
#instr.write(":TRIGger:EDGE:SOURce CHANnel1")#

#����Դ
#instr.write(":TRIGger:SHOLd:DSRC CHANnel1")#
#������ƽ
#dLEVel = instr.ask(":TRIGger:SHOLd:DLEVel?")#
#print(":TRIGger:SHOLd:DLEVel? ",dLEVel)
instr.write(":TRIGger:SHOLd:DLEVel 0.013")#


############         pulsh        ##########

#instr.write(":SOURce:PULSe:DCYCle 50")#

#<��������>,<Ƶ��>,<����>,<ƫ��>,<��ʼ��λ>
#dLEVel = instr.ask(":SOURce1:APPLy?")#

#[<freq>[,<amp>[,<offset>[,<phase>]]]]
#instr.write(":SOURce1:APPLy:PULSe 50,0.1,0,0")#

#instr.write(":SOURce1:OUTPut1 ON")#

#############         waveform        ##########

#whichSource = instr.ask(":WAVeform:SOURce?")#
#print(":WAVeform:SOURce? ",whichSource)
#instr.write(":WAVeform:SOURce CHAN1")#����ͨ��

#waveMode = instr.ask(":WAVeform:MODE?")#
#print(":WAVeform:MODE? ",waveMode)
#instr.write(":WAVeform:MODE CHAN1")# NORMal|MAXimum|RAW

#�������ݸ�ʽ
#print(":WAVeform:FORMat? ",instr.ask(":WAVeform:FORMat?"))#
instr.write(":WAVeform:FORMat ASCii")# WORD|BYTE|ASCii

#instr.write(":WAVeform:POINts NORMal")# NORMal RAW MAXimum
#print(":WAVeform:POINts? ",instr.ask(":WAVeform:POINts?"))#

#instr.write(":WAVeform:POINts NORMal")# NORMal RAW MAXimum
#print(":WAVeform:POINts? ",instr.ask(":WAVeform:POINts?"))#


#xINCrement=instr.ask(":WAVeform:XINCrement?")#��������ʵ�ʼ��
#print(":WAVeform:POINts? ",xINCrement)

#xORigin=instr.ask(":WAVeform:XORigin?")#��ʼʱ��
#print(":WAVeform:XORigin? ",xORigin)

#yINCrement=instr.ask(":WAVeform:YINCrement?")#
#print(":WAVeform:YINCrement? ",yINCrement)

#yORigin=instr.ask(":WAVeform:YORigin?")#
#print(":WAVeform:YORigin? ",yORigin)

pREamble=instr.ask(":WAVeform:PREamble?")#�����������в���
print(":WAVeform:PREamble? ",pREamble)

#wave=instr.ask(":WAVeform:DATA?")

#bin����
HIST_BINS = np.linspace(rangeMin, rangeMax, bins)

#�洢�ź�ֵ
data = []

#�����ݱ��ֱ��ͼ����
n, _ = np.histogram(data, HIST_BINS)

def process_wave(s):  
    # ʹ��������ʽƥ���һ�� '+' �� '-' ����ǰ����ַ�
    pattern = r"[+-]"  
    match = re.search(pattern, s)
    if match:
        #ɾ����һ������ʼ(+��-)֮ǰ���ַ�
        s = s[match.start():]
        #ȥ�����һ������
        s = s[:-1]
        #print(s)
    arr=list(map(float, s.split(',')))#���ָ����ַ����������
    return arr

def process_signal(wave,start,end):
    #���㱾��
    background1 = sum(wave[(start-200):(start-100)])/100#���һ��������
    background2 = sum(wave[(start-300):(start-200)])/100#���һ��������
    background = min(background1,background2)
        
    sumSig = sum(wave[start:end])
    #print("���� ",background*(end-start))
    #�ź�������ͺ��ȥ����
    return sumSig-background*(end-start)
    
   
#y������ʾ�����Χ�������Զ��ı�
yMaxLimit=10

#ͳ��ȡ�����������ݻ��ظ�
runCout = 0

#ͳ����Ч�ź���
signalCout = 0

#�ϴν��
preSignal=0

#��ͼ
fig, ax = plt.subplots()

#ֱ��ͼ lw�����޸ĵ���bin��Ե����ɫ(ec)��ֵΪ��������
_, _, bar_container = ax.hist(data, HIST_BINS, lw=0,
                              ec="yellow", fc="blue", alpha=0.5)

#��ʼ����ͼ�ε�y��Χ
ax.set_ylim(top = yMaxLimit)  # set safe limit to ensure that all data is visible.
plt.ylim(auto=True)

#���ļ�
if ifSaveFile:
    file = open(fileName, "w")

#�ر��ļ�
def closeFile():
    if ifSaveFile and file:
        #time.sleep(2)
        file.close()
        
def prepare_animation(bar_container):

    def animate(frame_number):
        global runCout
        global signalCout
        global signalStart
        global signalEnd
        global preSignal
        
        #���д���ͳ��
        runCout += 1
        
        #ʾ����ȡ��
        wave=instr.ask(":WAVeform:DATA?")
        
        #����ȡ���ַ�����ɲ�������
        waveform = process_wave(wave)
        
        if calculusOrHeight== 'cal':
        
            #���ź����������͵õ��źŴ�С
            sig = process_signal(waveform,signalStart,signalEnd)
        else:
            #�źŸ߶�
            sig = max(waveform)
        
        if signalCout < dataNumber and abs(preSignal - sig) > 1e-7:
        
            #���ź�ֵ�����ź�����
            data.append(sig)
            
            #ͳ����Ч�ź���
            signalCout +=1
            
            #������д���ļ���Ҫ���ƴ�����������ܶ�д
            if ifSaveFile:
                file.write(str("{:.8f}".format(sig)))
                file.write("\n")

                #���һ��ȡ����ɹر��ļ�
                if signalCout >= dataNumber:
                    closeFile()
                    
            #��ʾ��������
            if (signalCout*10 % (dataNumber))==0 and signalCout <= dataNumber:
                progress1 = str(signalCout * 100 // dataNumber)+'/'+str(100)
                mean = np.mean(data)
                median = np.median(data)
                print('> '+ progress1 +'   '+ str(signalCout) + '  Mean: ' + "{:.8f}".format(mean) + '  Median: ' + "{:.8f}".format(median) +' ..')
                ax.legend([progress1,str(signalCout)])
                fig.canvas.flush_events()
            #ȡ����ɣ��˳�����
            if signalCout == dataNumber:
                anim.event_source.stop()
            
            
        preSignal = sig
        
        #����ֱ��ͼ��
        his, _ = np.histogram(data, HIST_BINS)
        
        #���ʵʱֱ��ͼ����bin
        maxNumber = 0
        
        global yMaxLimit
        for count, rect in zip(his, bar_container.patches):
            if count > maxNumber:
                #�����bin
                maxNumber = count
            #����bin�߶�
            rect.set_height(count)
            
        #�޸�y�������Χ
        if (maxNumber//10+2) > (yMaxLimit//10):
            yMaxLimit += 10
            #�޸ķ�Χ
            ax.set_ylim(top=yMaxLimit)
            #�޸ĺ����ͼ��
            plt.draw()
            plt.pause(0.01)
        

        
        return bar_container.patches
    return animate
    
#�رմ���ҲҪ�ر��ļ�
def on_close(event):  
    closeFile()

#�����رմ����¼�
fig.canvas.mpl_connect('close_event', on_close)

#��̬����ֱ��ͼ
anim = animation.FuncAnimation(fig, prepare_animation(bar_container), 100000000,
                              repeat=False, blit=True, interval=delayTime)
#��ʾ
plt.show()

