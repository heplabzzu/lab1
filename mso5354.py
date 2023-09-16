import vxi11
import time
import datetime
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#############        参数 start       ##########

#连接
instr = vxi11.Instrument("192.168.24.6")

rangeMin = -2 #bin左侧范围 0
rangeMax = 5 #bin右侧范围 0.07
bins = 150 #bin的数量

#积分或者信号高度
calculusOrHeight= 'cal' #cal(区间求和) hei(信号高度)

#信号求和区间开始和结束 cal模式下需要设置
signalStart = 450
signalEnd = 630

#取数间隔时间(毫秒)
delayTime=300  #microSecond

#要获取的数据量
dataNumber=2000

#保存数据的文件名称
fileName='rpc_'+calculusOrHeight+'_'+datetime.datetime.now().strftime('%m_%d_%H%M%S')+".txt"

#是否保存数据到文件
ifSaveFile = 1 # 1保存 0不保存


#############        参数 end       ##########


#设备信息
#print(instr.ask("*IDN?"))#
#自动调整
#instr.write(":AUToscale")#auto

#basePos=instr.ask(":TIMebase:HREFerence:POSition?")
#print(":TIMebase:HREFerence:POSition? ",basePos)

#print(":TIMebase:DELay:SCALe? ",instr.ask(":TIMebase:DELay:SCALe?"))

#print(":TIMebase:MAIN:OFFSet? ",instr.ask(":TIMebase:MAIN:OFFSet?"))#位移
#instr.write(":TIMebase:MAIN:OFFSet 0")#0.000000005

#print(":TIMebase:MAIN:SCALe? ",instr.ask(":TIMebase:MAIN:SCALe?"))#时基
#instr.write(":TIMebase:MAIN:SCALe 0.0000002")

#print("TIMebase:DELay OFFSet? ",instr.ask(":TIMebase:DELay:OFFSet?"))
#############         CHANnel        ##########
#通道开关
#cHANnel1Dis = instr.ask(":CHANnel1:DISPlay?")#
#print(":CHANnel1:DISPlay? ",cHANnel1Dis)
#instr.write(":CHANnel2:DISPlay ON")#1 ON 0 OFF

#垂直偏移
#instr.write(":CHANnel2:OFFSet 0.01")#

#垂直scale调整
#instr.write(":CHANnel1:SCALe 0.01")#默认微调关闭 只能1-2-5 步进
#instr.write(":CHANnel2:VERNier OFF")#

#############         TRIGger        ##########
#触发模式
#sWEep = instr.ask(":TRIGger:SWEep?")#
#print(":TRIGger:SWEep? ",sWEep)
#instr.write(":TRIGger:SWEep AUTO")#AUTO|NORMal|SINGle

#
#sWEep = instr.ask(":TRIGger:EDGE:SOURce?")#
#print(":TRIGger:EDGE:SOURce? ",sWEep)
#instr.write(":TRIGger:EDGE:SOURce CHANnel1")#

#触发源
#instr.write(":TRIGger:SHOLd:DSRC CHANnel1")#
#触发电平
#dLEVel = instr.ask(":TRIGger:SHOLd:DLEVel?")#
#print(":TRIGger:SHOLd:DLEVel? ",dLEVel)
instr.write(":TRIGger:SHOLd:DLEVel 0.013")#


############         pulsh        ##########

#instr.write(":SOURce:PULSe:DCYCle 50")#

#<波形名称>,<频率>,<幅度>,<偏移>,<起始相位>
#dLEVel = instr.ask(":SOURce1:APPLy?")#

#[<freq>[,<amp>[,<offset>[,<phase>]]]]
#instr.write(":SOURce1:APPLy:PULSe 50,0.1,0,0")#

#instr.write(":SOURce1:OUTPut1 ON")#

#############         waveform        ##########

#whichSource = instr.ask(":WAVeform:SOURce?")#
#print(":WAVeform:SOURce? ",whichSource)
#instr.write(":WAVeform:SOURce CHAN1")#设置通道

#waveMode = instr.ask(":WAVeform:MODE?")#
#print(":WAVeform:MODE? ",waveMode)
#instr.write(":WAVeform:MODE CHAN1")# NORMal|MAXimum|RAW

#返回数据格式
#print(":WAVeform:FORMat? ",instr.ask(":WAVeform:FORMat?"))#
instr.write(":WAVeform:FORMat ASCii")# WORD|BYTE|ASCii

#instr.write(":WAVeform:POINts NORMal")# NORMal RAW MAXimum
#print(":WAVeform:POINts? ",instr.ask(":WAVeform:POINts?"))#

#instr.write(":WAVeform:POINts NORMal")# NORMal RAW MAXimum
#print(":WAVeform:POINts? ",instr.ask(":WAVeform:POINts?"))#


#xINCrement=instr.ask(":WAVeform:XINCrement?")#相邻两点实际间隔
#print(":WAVeform:POINts? ",xINCrement)

#xORigin=instr.ask(":WAVeform:XORigin?")#起始时间
#print(":WAVeform:XORigin? ",xORigin)

#yINCrement=instr.ask(":WAVeform:YINCrement?")#
#print(":WAVeform:YINCrement? ",yINCrement)

#yORigin=instr.ask(":WAVeform:YORigin?")#
#print(":WAVeform:YORigin? ",yORigin)

pREamble=instr.ask(":WAVeform:PREamble?")#返回上面所有参数
print(":WAVeform:PREamble? ",pREamble)

#wave=instr.ask(":WAVeform:DATA?")

#bin处理
HIST_BINS = np.linspace(rangeMin, rangeMax, bins)

#存储信号值
data = []

#把数据变成直方图数据
n, _ = np.histogram(data, HIST_BINS)

def process_wave(s):  
    # 使用正则表达式匹配第一个 '+' 或 '-' 符号前面的字符
    pattern = r"[+-]"  
    match = re.search(pattern, s)
    if match:
        #删除第一个数开始(+或-)之前的字符
        s = s[match.start():]
        #去掉最后一个逗号
        s = s[:-1]
        #print(s)
    arr=list(map(float, s.split(',')))#将分割后的字符串变成数字
    return arr

def process_signal(wave,start,end):
    #计算本底
    background1 = sum(wave[(start-200):(start-100)])/100#最后一个不包含
    background2 = sum(wave[(start-300):(start-200)])/100#最后一个不包含
    background = min(background1,background2)
        
    sumSig = sum(wave[start:end])
    #print("本底 ",background*(end-start))
    #信号区间求和后减去本底
    return sumSig-background*(end-start)
    
   
#y坐标显示的最大范围，后面自动改变
yMaxLimit=10

#统计取数次数，数据会重复
runCout = 0

#统计有效信号数
signalCout = 0

#上次结果
preSignal=0

#画图
fig, ax = plt.subplots()

#直方图 lw可以修改单个bin边缘的颜色(ec)，值为多少像素
_, _, bar_container = ax.hist(data, HIST_BINS, lw=0,
                              ec="yellow", fc="blue", alpha=0.5)

#初始设置图形的y范围
ax.set_ylim(top = yMaxLimit)  # set safe limit to ensure that all data is visible.
plt.ylim(auto=True)

#打开文件
if ifSaveFile:
    file = open(fileName, "w")

#关闭文件
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
        
        #运行次数统计
        runCout += 1
        
        #示波器取数
        wave=instr.ask(":WAVeform:DATA?")
        
        #将获取的字符串变成波形数组
        waveform = process_wave(wave)
        
        if calculusOrHeight== 'cal':
        
            #对信号区间积分求和得到信号大小
            sig = process_signal(waveform,signalStart,signalEnd)
        else:
            #信号高度
            sig = max(waveform)
        
        if signalCout < dataNumber and abs(preSignal - sig) > 1e-7:
        
            #将信号值放入信号数组
            data.append(sig)
            
            #统计有效信号数
            signalCout +=1
            
            #将数据写入文件，要控制次数，否则可能多写
            if ifSaveFile:
                file.write(str("{:.8f}".format(sig)))
                file.write("\n")

                #最后一次取数完成关闭文件
                if signalCout >= dataNumber:
                    closeFile()
                    
            #显示测量进度
            if (signalCout*10 % (dataNumber))==0 and signalCout <= dataNumber:
                progress1 = str(signalCout * 100 // dataNumber)+'/'+str(100)
                mean = np.mean(data)
                median = np.median(data)
                print('> '+ progress1 +'   '+ str(signalCout) + '  Mean: ' + "{:.8f}".format(mean) + '  Median: ' + "{:.8f}".format(median) +' ..')
                ax.legend([progress1,str(signalCout)])
                fig.canvas.flush_events()
            #取数完成，退出程序
            if signalCout == dataNumber:
                anim.event_source.stop()
            
            
        preSignal = sig
        
        #数据直方图化
        his, _ = np.histogram(data, HIST_BINS)
        
        #存放实时直方图最大的bin
        maxNumber = 0
        
        global yMaxLimit
        for count, rect in zip(his, bar_container.patches):
            if count > maxNumber:
                #找最大bin
                maxNumber = count
            #设置bin高度
            rect.set_height(count)
            
        #修改y坐标最大范围
        if (maxNumber//10+2) > (yMaxLimit//10):
            yMaxLimit += 10
            #修改范围
            ax.set_ylim(top=yMaxLimit)
            #修改后更新图表
            plt.draw()
            plt.pause(0.01)
        

        
        return bar_container.patches
    return animate
    
#关闭窗口也要关闭文件
def on_close(event):  
    closeFile()

#监听关闭窗口事件
fig.canvas.mpl_connect('close_event', on_close)

#动态更新直方图
anim = animation.FuncAnimation(fig, prepare_animation(bar_container), 100000000,
                              repeat=False, blit=True, interval=delayTime)
#显示
plt.show()

