from ctypes import *
from tkinter import *
from math import tan,pi,cos,sin,pow

class MinairoSensorPerimetre(Canvas):
    def dimensions(self, W, H):
        self._Width = W
        self._Height = H
        self.FondoEscala = 400
        self.openAngle = 10
        MinairoSensorPerimetre.config(self,width=self._Width,height=H+10, bg='black')
        self.SensorSharp = [0,0,0,0]
        self.Nsensors = 4
        self.i=0
        self.Gap=30
        self.SenRad = self._Width//30
        self.Xa=self.Gap
        self.Ya=self.Gap
        self.Xb=self._Width-self.Gap
        self.Yb=self.Gap
        self.Xc=self.Gap
        self.Yc=self._Height
        self.Xd=self._Width-self.Gap
        self.Yd=self._Height
        self.Xo=self._Width//2
        self.Yo=self._Height
        self.DeltaH=(self.Yc-self.Ya)//5
        self.DeltaW=(self.Xo-self.Xc)//5
        self.DeltaXp=(self.Yc-self.Ya)/tan(3.1415/3)
        self.DeltaYp=tan(3.1415/3)*(self.Xd-self.Xo)
        self.DeltaRx=self.DeltaW*cos(3.1415/3)
        self.DeltaRy=self.DeltaW*sin(3.1415/3)
        if (self.DeltaYp<(self.Yd-self.Yb)):
            self.x2=self.Xb
            self.x1=self.Xa
            self.y2=self.Yd-self.DeltaYp
            self.y1=self.y2
            self.EscalableX=(self.Xo-self.Xc-self.DeltaRx)
            self.EscalableY=(self.DeltaYp-self.DeltaRy)
        else:
            self.x2=self.Xo+self.DeltaXp
            self.x1=self.Xo-self.DeltaXp
            self.y2=self.Yb
            self.y1=self.y2
            self.EscalableX=(self.DeltaXp-self.DeltaRx)
            self.EscalableY=(self.Yo-self.Ya-self.DeltaRy)



    def update(self,valor):
        color=['green','green','green','green']
        self.delete(ALL)
        self.create_line(self.Xa,self.Ya,self.Xc,self.Yc, fill='darkgreen' )
        self.create_line(self.Xb,self.Yb,self.Xd,self.Yd, fill='darkgreen' )
        self.create_line(self.Xa,self.Ya,self.Xb,self.Yb, fill='darkgreen' )
        self.create_line(self.Xc,self.Yc,self.Xd,self.Yd, fill='darkgreen' )

        self.create_line(self.Xo,self.Yo,self.x2,self.y2,fill='darkgreen')
        self.create_line(self.Xo,self.Yo,self.x1,self.y1,fill='darkgreen')
        for i in range(5):
            self.create_arc(self.Xo-self.DeltaW*(i+1),self.Yo-self.DeltaH*(i+1),self.Xo+self.DeltaW*(i+1),self.Yo+self.DeltaH*(i+1), start=0,extent=180,outline='darkgreen')
        self.create_arc(self.Xo-self.DeltaW,self.Yo-self.DeltaH,self.Xo+self.DeltaW,self.Yo+self.DeltaH, start=0,extent=180,outline='darkgreen',fill='darkgreen')
        modulX0 = (valor[0]*(self.Xo-self.DeltaW-self.Xc))//400
        modulX1 = (valor[1]*self.EscalableX)//400
        modulY1 = (valor[1]*self.EscalableY)//400
        modulX2 = (valor[2]*self.EscalableX)//400
        modulY2 = (valor[2]*self.EscalableY)//400
        modulX3 = (valor[3]*(self.Xo-self.DeltaW-self.Xc))//400
        x0=self.Xo+self.DeltaW+modulX0
        x1=self.Xo+self.DeltaRx+modulX1
        y1=self.Yo-self.DeltaRy-modulY1
        x2=self.Xo-self.DeltaRx-modulX2
        y2=self.Yo-self.DeltaRy-modulY2
        x3=self.Xo-self.DeltaW-modulX3
        for i in range(4):
            if valor[i]<100:
                color[i]='red'
            elif valor[i]<200:
                color[i]='orange'
            elif valor[i]<300:
                color[i]='yellow'
            else:
                color[i]='green1'
        self.create_oval(x0-self.SenRad,self.Yc-self.SenRad,x0+self.SenRad,self.Yc+self.SenRad,outline='darkgreen',fill=color[0])
        self.create_oval(x1-self.SenRad,y1-self.SenRad,x1+self.SenRad,y1+self.SenRad,outline='darkgreen',fill=color[1])
        self.create_oval(x2-self.SenRad,y2-self.SenRad,x2+self.SenRad,y2+self.SenRad,outline='darkgreen',fill=color[2])
        self.create_oval(x3-self.SenRad,self.Yc-self.SenRad,x3+self.SenRad,self.Yc+self.SenRad,outline='darkgreen',fill=color[3])
        self.create_text(self.Xd+15,self.Yd-8,text=valor[0],fill='darkgreen',font=('Helvetica 8'))
        self.create_text(self.x2+15,self.y2-10,text=valor[1],fill='darkgreen',font=('Helvetica 8'))
        self.create_text(self.x1-15,self.y1-10,text=valor[2],fill='darkgreen',font=('Helvetica 8'))
        self.create_text(self.Xc-15,self.Yc-8,text=valor[3],fill='darkgreen',font=('Helvetica 8'))

class MinairoSensorLine(Canvas):
    def dimensions(self, W, H):
        self.LEDheight = 20
        self.columnWidth = W//8
        self.columnHeight = H-self.LEDheight
        self._Width = 8*self.columnWidth
        self._Height = H
        self.convFactor = self.columnHeight//2500
        MinairoSensorLine.config(self,width=self._Width,height=self._Height, bg='black')
        self.threshold = 2400
        self.scaledThreshold = (self.threshold*self.columnHeight)//2500
        self.SensorLine_Analog = [self._Height/2,self._Height/3,self._Height/4,self._Height/5,self._Height/4,self._Height/3,self._Height/2,self._Height]
        self.SensorsAnalog=list()
        self.Nsensors = 8
        self.i=0
        
        for i in range(self.Nsensors):
            w=self.create_rectangle(self.columnWidth*i,self.columnHeight-self.SensorLine_Analog[i],self.columnWidth*(i+1),self.columnHeight, fill='green')
            self.SensorsAnalog.append(w)
        self.create_line(0,self.columnHeight-(self.scaledThreshold), self._Width, self.columnHeight-(self.scaledThreshold), width=2, fill='darkgreen')
        for i in range(self.Nsensors):
            if self.SensorLine_Analog[i] > self.scaledThreshold:
                w=self.create_rectangle(self.columnWidth*i,self.columnHeight,self.columnWidth*(i+1),self.columnHeight+self.LEDheight, fill='green1')
            else:
                w=self.create_rectangle(self.columnWidth*i,self.columnHeight,self.columnWidth*(i+1),self.columnHeight+self.LEDheight, fill='darkgreen')
            self.SensorsAnalog.append(w)

    
    def update(self,valors):
        for i in range(self.Nsensors):
            self.SensorLine_Analog[i] = (valors[i]*self.columnHeight)//2500
        self.delete(ALL)
        self.SensorsAnalog.clear    
        for i in range(self.Nsensors):
            w=self.create_rectangle(self.columnWidth*i,self.columnHeight-self.SensorLine_Analog[i],self.columnWidth*(i+1),self.columnHeight, fill='green')
            self.SensorsAnalog.append(w)
        self.create_line(0,self.columnHeight-(self.scaledThreshold), self._Width, self.columnHeight-(self.scaledThreshold), width=2, fill='darkgreen')
        for i in range(self.Nsensors):
            if self.SensorLine_Analog[i] > self.scaledThreshold:
                w=self.create_rectangle(self.columnWidth*i,self.columnHeight,self.columnWidth*(i+1),self.columnHeight+self.LEDheight, fill='green1')
            else:
                w=self.create_rectangle(self.columnWidth*i,self.columnHeight,self.columnWidth*(i+1),self.columnHeight+self.LEDheight, fill='darkgreen')
            self.SensorsAnalog.append(w)

class MinairoSonar(Canvas):
    def dimensions(self, W):
        self._Width = W
        self._Height = W
        MinairoSonar.config(self,width=self._Width,height=self._Height, bg='black')
        self.FondoEscala = 400
        self.SonarPoints = 360
        self.Sonar=[0 for _ in range( self.SonarPoints)]
        for i in range(360):
            self.Sonar[i]=2
        self.i=0
        self.Gap=20
        #self.SenRad = self._Width//100
        self.SenRad = 1
        self.Xa=self.Gap
        self.Ya=self.Gap
        self.Xb=self._Width-self.Gap
        self.Yb=self.Gap
        self.Xc=self.Gap
        self.Yc=self._Height-self.Gap
        self.Xd=self._Width-self.Gap
        self.Yd=self._Height-self.Gap
        self.Xo=self._Width//2
        self.Yo=self._Height//2
        self.Divisions = 8
        self.DeltaH=(self.Yo-self.Ya)//self.Divisions
        self.DeltaW=(self.Xo-self.Xc)//self.Divisions
        self.Escalable=(self.Xo-self.DeltaW-self.Xc)//2
        column, row = 2, 360
        self.Trigonom = [[0 for _ in range(column)] for _ in range(row)]
        for i in range(360):
            self.Trigonom[i][0]=sin((3.14156/180)*i)*self.Escalable
            self.Trigonom[i][1]=cos((3.14156/180)*i)*self.Escalable
        #print(self.Trigonom)
 
    def update(self):
        color=['green','green','green','green']
        self.delete(ALL)
        self.create_line(self.Xa,self.Ya,self.Xc,self.Yc, fill='darkgreen' )
        self.create_line(self.Xb,self.Yb,self.Xd,self.Yd, fill='darkgreen' )
        self.create_line(self.Xa,self.Ya,self.Xb,self.Yb, fill='darkgreen' )
        self.create_line(self.Xc,self.Yc,self.Xd,self.Yd, fill='darkgreen' )

        self.create_line(self.Xa,self.Ya,self.Xd,self.Yd,fill='darkgreen')
        self.create_line(self.Xb,self.Yb,self.Xc,self.Yc,fill='darkgreen')
        self.create_line(self.Gap,self.Yo,self._Width-self.Gap,self.Yo,fill='darkgreen')
        self.create_line(self.Xo,self.Gap,self.Xo,self._Height-self.Gap,fill='darkgreen')


        for i in range(self.Divisions):
            self.create_oval(self.Xo-self.DeltaW*(i+1),self.Yo-self.DeltaH*(i+1),self.Xo+self.DeltaW*(i+1),self.Yo+self.DeltaH*(i+1),outline='darkgreen')
        #self.create_oval(self.Xo-self.DeltaW,self.Yo-self.DeltaH,self.Xo+self.DeltaW,self.Yo+self.DeltaH,outline='darkgreen',fill='darkgreen')

        self.create_text(self.Xo,self.Gap//2,justify='center',text="0",fill='darkgreen',font=('Helvetica 8'))
        self.create_text(self.Xo,self._Height-self.Gap//2,justify='center',text="180",fill='darkgreen',font=('Helvetica 8'))
        self.create_text(self._Width-self.Gap//2,self.Yo,justify='center',text="90",fill='darkgreen',font=('Helvetica 8'))
        self.create_text(self.Gap//2,self.Yo,justify='center',text="270",fill='darkgreen',font=('Helvetica 8'))
        
    def clear(self):
        for i in range(360):
            self.Sonar[i]=-1
        self.update()
        

    def plot(self,valor,angle):
        self.Sonar[angle]=valor
        xa=self.Sonar[angle]*round( self.Trigonom[angle][0])
        ya=self.Sonar[angle]*round(self.Trigonom[angle][1])
        if self.Sonar[angle]<2 and self.Sonar[angle]>0:
            self.create_oval(self.Xo+xa-self.SenRad,self.Yo-ya-self.SenRad,self.Xo+xa+self.SenRad,self.Yo-ya+self.SenRad,outline='green1',fill='green1')

    def plotAll(self):
        for i in range(360):
            xa=self.Sonar[i]*round( self.Trigonom[i][0])
            ya=self.Sonar[i]*round(self.Trigonom[i][1])
            if self.Sonar[i]<2 and self.Sonar[i]>0:
                self.create_oval(self.Xo+xa-self.SenRad,self.Yo-ya-self.SenRad,self.Xo+xa+self.SenRad,self.Yo-ya+self.SenRad,outline='green1',fill='green1')
        