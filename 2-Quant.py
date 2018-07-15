##New, Improved File

def dbConnect():
    global cursor
    import pyodbc 
    cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                          "Server=localhost;"
                          "Database=Quant;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()
def Login(Username,Pass):
    global Email
    S=0
    dbConnect()
    P_C="exec dbo.SP_Verification 'SelectUser', null, ""?"", null, null"
    values=(Username)
    cursor.execute(P_C, (values))
    for row in cursor.execute(P_C, (values)):
        if Username==row[1] and Pass==row[2]:
            Email=row[0]
            S=1
    return S
def Register(Email,Username,Pass):
    import dbConnect
    from dbConnect import cursor
    P_C = "exec Quant.dbo.SP_Verification 'InsertUser', ""?"", ""?"", ""?"", '0'"
    values=(Email, Username, Pass)
    cursor.execute(P_C, values)
    cursor.commit()
    U=Username
    P=Pass
    Login(U,P)
def Verification(C):
    global U
    LoginList=['Login','L','login','l']
    RegisterList=['Register','register','r','R']
    if C in LoginList:
        print("Enter your Username and Password respectivley")
        U=input()
        P=input()
        S=Login(U,P)
    elif C in RegisterList:
        print("Enter your Email and the desired Username,Password respectivley")
        E=input()
        U=input()
        P=input()
        S=Register(E,U,P)
    return S
def VerLoop():
    print("Login or Register")
    choice=input()
    Session=0
    while Session!=1:
        Session=Verification(choice)
        if Session==1:
            break
        else:
            print("Wrong Username or Password!")
def Main():
    print("Stocks or Property?")
    C=input()
    while C!='Stocks':
        print(C,"Is An Invalid Choice!")
        C=input
        Main(C)
    print(C)
    return C

import numpy as np
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader as web
import datetime as dt

def Data():
    global symbol,windowc,df,Date,Open,High,Low,Close,Volume,open1,high1,low1,close1,open2,high2,low2,close2,limitmove
    print("Symbol?")
    symbol=input().upper()
    print("Window?") 
    windowc=int(input())
    start=dt.datetime(2000,1,1)
    end=dt.date.today()
    #company=web.DataReader(symbol,'quandl',start,end)
    #company.to_csv(symbol+'.csv')
    df=pd.read_csv(symbol+'.csv')#,parse_dates=True,index_col=0)
    Date=df['Date']
    Open=df['Open']
    High=df['High']
    Low=df['Low']
    Close=df['Close']
    Volume=df['Volume']
    #R
    open1=Open[1]
    high1=High[1]
    low1=Low[1]
    close1=Close[1]
    open2=Open[2]
    high2=High[2]
    low2=Low[2]
    close2=Close[2]
    limitmove=75

def movingaverage(closingvalues,window):
    weights=np.repeat(1.0,window)/window
    simplemovingaverages=np.convolve(closingvalues,weights,'valid')
    return simplemovingaverages

def emovingaverage(closingvalues,window):
    weights=np.exp(np.linspace(-1.,0.,window))
    weights/=weights.sum()
    a=np.convolve(closingvalues,weights)[:len(closingvalues)]
    a[:window]=a[window]
    return a

def SwingIndex(O1,O2,H1,H2,L1,L2,C1,C2,LM):
    global SwI
    def calc_R(H2,C1,L2,O1,LM):
        global R
        x=H2-C1
        y=L2-C1
        z=H2-L2
        if z<x>y:
            R=(H2-C1)-(.5*(L2-C1))+(.25*(C1-O1))
            return R
        elif x<y>z:
            R=(L2-C1)-(.5*(H2-C1))+(.25*(C1-O1))
            return R
        elif x<z>y:
            R=(H2-C1)+(.25*(C1-O1))
            return R
    def calc_K(H2,L2,C1):
        global K
        x=H2-C1
        y=L2-C1
        if x>y:
            K=x
            return K
        elif x<y:
            K=y
            return K
    L=LM
    R=calc_R(H2,C1,L2,O1,LM)
    K=calc_K(H2,L2,C2)
    SwI=50*((C2-C1+(.5*(C2-O2))+(.25*(C1-O1)))/R)*(K/L)
    return SwI

def TrueRange():
    global d,TR,TrueRanges,TRDates
    def TR(d,c,h,l,o,yc):
        x=h-l
        y=abs(h-yc)
        z=abs(l-yc)
        if y<=x>=z:
            TR=x
        elif x<=y>=z:
            TR=y
        elif x<=z>=y:
            TR=z
        return d,TR
    x=1
    TRDates=[]
    TrueRanges=[]
    while x<len(Date):
        TRDate,TrueRange=TR(Date[x]
                            ,Close[x]
                            ,High[x]
                            ,Low[x]
                            ,Open[x]
                            ,Close[x-1])
        TRDates.append(TRDate)
        TrueRanges.append(TrueRange)
        x+=1
        
def DMS():
    def TR(d,c,h,l,o,yc):
            x=h-l
            y=abs(h-yc)
            z=abs(l-yc)
            if y<=x>=z:
                TR=x
            elif x<=y>=z:
                TR=y
            elif x<=z>=y:
                TR=z
            return d,TR
    def DM(d,o,h,l,c,yo,yh,yl,yc):
        moveUp=h-yh
        moveDown=yl-l
        if 0<moveUp>moveDown:
            PDM=moveUp
        else:
            PDM=0
        if 0<moveDown>moveUp:
            NDM=moveDown
        else:
            NDM=0
        return d,PDM,NDM
    def calc_DIs():
        x=1
        TRDates=[]
        TrueRanges=[]
        PosDMs=[]
        NegDMs=[]
        while x<len(Date):
            TRDate,TrueRange=TR(Date[x]
                                ,Close[x]
                                ,High[x]
                                ,Low[x]
                                ,Open[x]
                                ,Close[x-1])
            TRDates.append(TRDate)
            TrueRanges.append(TrueRange)
            DMDate,PosDM,NegDM=DM(Date[x]
                                   ,Open[x]
                                   ,High[x]
                                   ,Low[x]
                                   ,Close[x]
                                   ,Open[x-1]
                                   ,High[x-1]
                                   ,Low[x-1]
                                   ,Close[x-1])
            PosDMs.append(PosDM)
            NegDMs.append(NegDM)
            x+=1
        expPosDM=emovingaverage(PosDMs,14)
        expNegDM=emovingaverage(NegDMs,14)
        ATR=emovingaverage(TrueRanges,14)
        xx=0
        PDIs=[]
        NDIs=[]
        while xx<len(ATR):
            PDI=100*(expPosDM[xx]/ATR[xx])
            PDIs.append(PDI)
            NDI=100*(expNegDM[xx]/ATR[xx])
            NDIs.append(NDI)
            xx+=1
        return PDIs,NDIs
    def ADX():
        global ADXv
        PositiveDI,NegativeDI=calc_DIs()
        xxx=0
        DXs=[]
        while xxx<len(Date[1:]):
            DX=100*((abs(PositiveDI[xxx]-NegativeDI[xxx])
                     /(PositiveDI[xxx]+NegativeDI[xxx])))
            DXs.append(DX)
            xxx+=1
        ADXv=emovingaverage(DXs,windowc)
    ADX()

def aroon(tf):
    global AroonDate,AroonUp,AroonDown
    AroonUp=[]
    AroonDown=[]
    AroonDate=[]
    AroonOscillator=[]
    x=tf
    while x<len(Date):
        Aroon_Up=((High[x-tf:x].tolist().index(max(High[x-tf:x])))/float(tf))*100
        Aroon_Down=((Low[x-tf:x].tolist().index(max(Low[x-tf:x])))/float(tf))*100
        Aroon_Osc=Aroon_Up-Aroon_Down
        AroonUp.append(Aroon_Up)
        AroonDown.append(Aroon_Down)
        AroonDate.append(Date[x])
        AroonOscillator.append(Aroon_Osc)
        #print(High[x],"|",Low[x])
        #print(Aroon_Up,"|",Aroon_Down,"\n----------------------")
        x+=1
    return AroonDate,AroonUp,AroonDown,AroonOscillator

def standard_deviation(tf):
    sd=[]
    sdDate=[]
    x=tf
    while x<len(Date):
        array2consider=Close[x-tf:]
        standev=array2consider.std()
        sd.append(standev)
        sdDate.append(Date[x])
        x+=1
    return sdDate,sd

def LastClose():
    global LastC
    x=0
    LastC=[]
    while x<len(Date):
        C=Close[0]
        LastC.append(C)
        x+=1
    print("\n\n-------------------------------------\nLast Closing price\nDate        | value\n"    
          ,Date[0]
          ,"|"
          ,LastC[0])

def DayRecentChange():
    print("\n\n-------------------------------------\nChange Between Last Day:\n")
    x=0
    xx=x+1
    MostRecentDailyChange=abs(Close[x]-Close[xx])
    PMostRecentDailyChange=abs(100-(100*(Close[x]/Close[xx])))
    if Close[x]>Close[xx]:
        print('+',PMostRecentDailyChange,'%')
        print('+',MostRecentDailyChange)
    elif Close[x]<Close[xx]:
        print('-',PMostRecentDailyChange,'%')
        print('-',MostRecentDailyChange) 
    else:
        print('0','%')
        print('0')

def visual():
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib import style
    from mpl_finance import candlestick_ohlc
    import matplotlib.animation as animation
    import matplotlib.ticker as mticker

    #fig = plt.figure(facecolor='#07000d')
    df=pd.read_csv(symbol+'.csv',parse_dates=True,index_col=0)
    df_ohlc=df['Close'].resample('10D').ohlc()
    df_volume=df['Volume'].resample('10D').sum()
    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date']=df_ohlc['Date'].map(mdates.date2num)
    df['50ma']=df['Close'].rolling(window=50,min_periods=0).mean()
    df['50ma'].plot(label='50MA(Short)',color='black')
    df['200ma']=df['Close'].rolling(window=200,min_periods=0).mean()
    df['200ma'].plot(label='200ma(Long)',color='darkred')
    df[windowc]=df['Close'].rolling(window=windowc,min_periods=0).mean()
    df[windowc].plot(label=windowc,color='darkred')
    ax1=plt.subplot2grid((9,1),(2,0),rowspan=5,colspan=1)
    ax2=plt.subplot2grid((9,1),(8,0),rowspan=1,colspan=1,sharex=ax1)
    ax3=plt.subplot2grid((9,1),(0,0),rowspan=1,colspan=1,sharex=ax1,title=symbol)
    ax1.plot(df.index,df['50ma'],color='black')
    ax1.plot(df.index,df['200ma'],color='blue')
    ax1.plot(df.index,df[windowc],color='red')
    ax1.plot(df.index,LastC,color='black')
    ax3.plot(df.index[1:],ADXv,color='black')
    candlestick_ohlc(ax1,df_ohlc.values,width=2,colorup='lightgreen')
    ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0,color='black')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.grid(True) 
    plt.show()




    
def MainOrder():
    def StocksOrder():
        Data()
        movingaverage(Close,windowc)
        emovingaverage(Close,windowc)
        SwingIndex(open1
                   ,open2
                   ,high1
                   ,high2
                   ,low1
                   ,low2
                   ,close1
                   ,close2
                   ,limitmove)
        TrueRange()
        print("\n\n-------------------------------------\nR:"
              ,R
              ,"| K:"
              ,K
              ,"\nSwI:"
              ,SwI
              )
        DMS()
        aroon(windowc)
        LastClose()
        DayRecentChange()
        visual()

    choice=input
    VerLoop()
    print("You have successfuly logged in as:",U)
    choice=Main()
    print(choice)
    if choice=='Stocks':
        StocksOrder()
    elif choice=='Property':
        PropertyOrder()
        
MainOrder()

