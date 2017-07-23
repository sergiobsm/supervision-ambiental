#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import * 
import RPi.GPIO as GPIO
import time
import smbus # comunicación i2c
import xlrd #leer datos de un archivo .xls
import xlutils #lmodificar datos de un archivo.xls
from xlrd import open_workbook 
from xlutils.copy import copy
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)
BUTTON_SIZE=50
NUM_BUTTON=10
MARGIN=1
WINDOW_H = MARGIN+((BUTTON_SIZE+MARGIN)*NUM_BUTTON)
WINDOW_W = (2*MARGIN)+BUTTON_SIZE

BLACK = '#000000'
BRIGHTRED = '#ff0000'
RED = '#9b0000'
WHITE= '#ffffff'
BLUE='#1D3F7F'
GREEN='#49B02A'
YELLOW='#F7EF00'
ORANGE='#ED9800'
HRED='#DB0021'
GRAY='#D5DFE5'
bus = smbus.SMBus(1)
dir=0x24
d=[0,0,0,0,0]
pulsos=0
pr=True
def eventoGIO(channel):
	global actualhora
	global pulsos	
	pulsos=pulsos+1
	inicio=0
	R=0.1
	print(R)
	while (inicio!=252):
		inicio=bus.read_byte(dir)	
		time.sleep(0.1)
	for i in range(5):
		d[i]=bus.read_byte(dir)
		print(d[i])
		d[i]=d[i]*1.0
		time.sleep(0.1)
	fila=int(sh.cell_value(rowx=0, colx=1))
	if cdi:
		fila=fila+1
	#Valor de la Humedad según el datasheet
	d[0]=32.653*(d[0]*5.0/250.0) -14.49
	
	#Nivel UV
	d[4]=d[4]*5.0/250.0
	if(d[4]<=0.2):
		d[4]= d[4]/0.2
	else:
		
		d[4]=(d[4]-0.1025)/0.0975

	#Valor de la resistencia
	R=-10.0+ 10.0*5.0 / (d[1]*5/250)
	#Valor de la temperatura conforme a la resistencia
	if((R<=163.81)and(R>97.1)):
		d[1]=(R-163.81)/ (-6.671)
	if((R<=97.1)and(R>59.42)): 
		d[1]=((R-97.1) / (-3.768))+10		
	if((R<=59.42)and(R>47.0)): 
		d[1]=((R-59.42)/ (-2.484))+20	
	if((R<=47.0)and(R>37.43)): 
		d[1]=((R-47.0) / (-1.914))+25	
	if((R<=37.43)and(R>24.19)):
		d[1]=((R-37.43)/ (-1.324))+30	
	if((R<=24.19)and(R>16.01)):
		d[1]=((R-24.19)/ (-0.818))+40	
	if((R<=16.01)and(R>10.83)) :
		d[1]=((R-16.01)/ (-0.518))+50									
	if (pulsos>=3):
		print((actualhora!=int(time.strftime("%H"))))
		if(actualhora!=int(time.strftime("%H"))) :
			actualhora=int(time.strftime("%H"))
			print(actualhora)
			for i in range(5):
				ws.write(fila,(actualhora*5)+1+i,d[i])
				wb.save('probar.xls')	
		
	temperatura=round(d[1],2)
	humedad=round(d[0],2)
	niveluv=int(d[4])
	ruido="MEDIO"
	nivelco="MEDIO"
	if(pulsos<=15):
		principal(temperatura,humedad,niveluv,ruido,nivelco,True)
	if((pulsos>15) and (pulsos<=30)):
		canvas2.delete(num)
		canvas3.delete(numl)
		termometro(temperatura,True)
		medidorHumedad(humedad)
	if((pulsos>30) and (pulsos<=45)):
		medidorUV(niveluv,True)
	if((pulsos>45) and (pulsos<=60)):
		canvas4.delete(poligono)
		canvas4.delete(texto3)
		medidordeRuido(200+pulsos,True)
		canvas5.delete(poligono5)
		canvas5.delete(texto4)
		medidordeCO(200-pulsos*1.2)
	if((pulsos>60) and (pulsos<=75)):
	    nmin= int(time.strftime("%M"))
	    rutas(nmin,True)
	if(pulsos>75):
		pulsos=0
GPIO.add_event_detect(17, GPIO.BOTH, callback=eventoGIO)  

def LuzUV():
 global tk
 global euv
 if euv:
	 tk.deiconify()
	 euv= False
 else:
	 tk.withdraw()
	 euv= True

def Coru():
 global euv
 if euv:
	 tk3.deiconify()
	 euv= False
 else:
	 tk3.withdraw()
	 euv= True

def temp():
 global tk2
 global euv

 if euv:
	 tk2.deiconify()
	 euv= False
 else:
	 tk2.withdraw()
	 euv= True

def termometro(tempe,lec):
 global num
 ovalo=canvas2.create_arc(10,500,110,400, start=140,extent=260, style=ARC, fill=WHITE)
 ovalo=canvas2.create_oval(20,490,100,410,fill=RED)
 caja=canvas2.create_rectangle(32,420,88,(-6*tempe+470),fill=RED,outline=RED)
 caja=canvas2.create_rectangle(32,(-6*tempe+470),88,30, fill=WHITE, outline=WHITE) 
 linea=canvas2.create_line(22,420,22,30, fill=BLACK)
 linea=canvas2.create_line(98,420,98,30, fill=BLACK)
 linea=canvas2.create_line(32,420,32,30, fill=BLACK)
 linea=canvas2.create_line(88,420,88,30, fill=BLACK)
 arco=canvas2.create_arc(22,1,98,60, start=0, extent=180, fill=WHITE, style=ARC)
 arco=canvas2.create_arc(32,12,88,60, start=0, extent=180, fill=WHITE, style=ARC)
 i=0
 tk2.geometry("%dx%d+%d+%d" % (670,590,ancho-335,alto-295))
 while(i<=5):
	linea=canvas2.create_line(22,410-60*i,52,410-60*i, fill=BLACK)
	num1=canvas2.create_text(12,410-60*i,text=format((i+1)*10))
	j=0	
	while (j<5):
		linea=canvas2.create_line(22,410-12*j-60*i,38,410-12*j-60*i, fill=BLACK)
		j=j+1
	i=i+1
 linea=canvas2.create_line(22,50,52,50, fill=BLACK)
 num1=canvas2.create_text(12,50,text="70")

 num=canvas2.create_text(200,250,text=format(tempe)+"°C",font="Arial 16")
 num1=canvas2.create_text(11,20,text="°C")
 l2=Label(tk2,text=time.strftime("%A %d/%m/%y  %H:%M"),bg=WHITE,font="Arial 12") 
 l2.grid(row=1, column=1, sticky=E,pady=10)
 if lec:
  tk2.deiconify()
  tk.withdraw()
  tkm.withdraw()
  tk3.withdraw()
  tk4.withdraw()
def medidorHumedad(humed):
 global canvas3
 global numl
 ovalo=canvas3.create_arc(10,500,110,400, start=140,extent=260, style=ARC, fill=WHITE)
 ovalo2=canvas3.create_oval(20,490,100,410,fill=BLUE)
 caja=canvas3.create_rectangle(32,420,88,(-4*humed+450),fill=BLUE,outline=BLUE)
 caja=canvas3.create_rectangle(32,(-4*humed+450),88,30, fill=WHITE, outline=WHITE) 
 linea=canvas3.create_line(22,420,22,30, fill=BLACK)
 linea=canvas3.create_line(98,420,98,30, fill=BLACK)
 linea=canvas3.create_line(32,420,32,30, fill=BLACK)
 linea=canvas3.create_line(88,420,88,30, fill=BLACK)
 arco=canvas3.create_arc(22,1,98,60, start=0, extent=180, fill=WHITE, style=ARC)
 arco=canvas3.create_arc(32,12,88,60, start=0, extent=180, fill=WHITE, style=ARC)
 i=0
 while(i<=8):
	linea=canvas3.create_line(22,410-40*i,52,410-40*i, fill=BLACK)
	num=canvas3.create_text(12,410-40*i,text=format((i+1)*10))
	j=0	
	while (j<2):
		linea=canvas3.create_line(22,410-20*j-40*i,38,410-20*j-40*i, fill=BLACK)
		j=j+1
	i=i+1
 linea=canvas3.create_line(22,50,52,50, fill=BLACK)
 num=canvas3.create_text(11,50,text="100")
 num=canvas3.create_text(11,20,text="%")
 numl=canvas3.create_text(200,250,text=format(humed)+"%",font="Arial 16")

def medidordeRuido(y,mr):
 global poligono
 global texto3
 tk3.geometry("%dx%d+%d+%d" % (500,400,ancho-250,alto-200))
 caja3=canvas4.create_rectangle(90,300,103,90, fill=WHITE, outline=BLACK) 
 poligono = canvas4.create_polygon(104, 300, 104, 90, 124, 90, fill=GRAY)

 poligono = canvas4.create_polygon(88,y,108,y,113,y+5,108,y+10,88,y+10, fill="lightblue", outline=BLUE, width=2)
 linea3=canvas4.create_line(104,300,125,300, fill=GRAY, width=3)
 linea3=canvas4.create_line(104,195,125,195, fill=GRAY, width=3)
 linea3=canvas4.create_line(104,90,132,90, fill=GRAY, width=3)
 texto3=canvas4.create_text(100,50,text="Nivel de Ruido",font="Arial 16")
 l3=Label(tk3,text=time.strftime("%A %d/%m/%y  %H:%M"),bg=WHITE,font="Arial 12")
 l3.grid(row=1, column=1, sticky=E) 
 if y<160:
	 imagalto=canvas4.create_image(104,330,anchor="center",image=imgalto)
	 texto3=canvas4.create_text(170,195,text="Alto",font="Arial 16")
 if y>=160 and y<230:
	 imagalto=canvas4.create_image(104,330,anchor="center",image=imgmedio)
	 texto3=canvas4.create_text(170,195,text="Medio",font="Arial 16")
 if y>=230:
	 imagalto=canvas4.create_image(104,330,anchor="center",image=imgbajo)
	 texto3=canvas4.create_text(170,195,text="Bajo",font="Arial 16")
 if mr:
  tk3.deiconify()
  tk2.withdraw()
  tk.withdraw()
  tk4.withdraw()
  tkm.withdraw()
def rutas(nmin,rin):
 global tk4
 tk4.geometry("%dx%d+%d+%d" % (570,460,ancho-285,alto-230))
 tar1=[0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60]
 tar2=[0,5,10,15,20,25,30,35,40,45,50,55,60]
 tar3=[0,10,20,30,40,50,60]
 tar4=[0,15,30,45,60]
 contador=[0,0,0,0]

 for e in tar1:
	 if nmin>e:
		 contador[0]=contador[0]+1
 for e in tar2:
	 if nmin>e:
		 contador[1]=contador[1]+1
 for e in tar3:
	 if nmin>e:
		 contador[2]=contador[2]+1
 for e in tar4:
	 if nmin>e:
		 contador[3]=contador[3]+1 
 Tfaltante=[(tar1[contador[0]]-nmin),(tar2[contador[1]]-nmin),(tar3[contador[2]]-nmin),(tar4[contador[3]]-nmin)]
 T1=Label(tk4,text=format(Tfaltante[0])+" Minutos", bg=WHITE, font="Arial 12")
 T2=Label(tk4,text=format(Tfaltante[1])+" Minutos", bg=WHITE, font="Arial 12")
 T3=Label(tk4,text=format(Tfaltante[2])+" Minutos", bg=WHITE, font="Arial 12")
 T4=Label(tk4,text=format(Tfaltante[3])+" Minutos", bg=WHITE, font="Arial 12")
 T5=Label(tk4,text=format(Tfaltante[2])+" Minutos", bg=WHITE, font="Arial 12")
 
 Estados=["","","",""]
 i=0
 for e in Tfaltante:
	 if e==0:
		 Estados[i]="Arrivando"
	 else:
		 Estados[i]="En espera"
	 i=i+1
 ET1=Label(tk4,text=Estados[0], bg=WHITE, font="Arial 12")
 ET2=Label(tk4,text=Estados[1], bg=WHITE, font="Arial 12")
 ET3=Label(tk4,text=Estados[2], bg=WHITE, font="Arial 12")
 ET4=Label(tk4,text=Estados[3], bg=WHITE, font="Arial 12")
 ET5=Label(tk4,text=Estados[2], bg=WHITE, font="Arial 12")		 

 T1.grid(row=2,column=1,padx=10,pady=10)
 T2.grid(row=3,column=1,padx=10,pady=10)
 T3.grid(row=4,column=1,padx=10,pady=10)
 T4.grid(row=5,column=1,padx=10,pady=10)
 T5.grid(row=6,column=1,padx=10,pady=10)

 ET1.grid(row=2,column=2,padx=10,pady=10)
 ET2.grid(row=3,column=2,padx=10,pady=10)
 ET3.grid(row=4,column=2,padx=10,pady=10)
 ET4.grid(row=5,column=2,padx=10,pady=10)
 ET5.grid(row=6,column=2,padx=10,pady=10)
 lk5=Label(tk4,text=time.strftime("%A %d/%m/%y  %H:%M"),bg=WHITE,font="Arial 12")
 lk5.grid(row=7, column=2, sticky=E,pady=10)
 if rin:
  tk4.deiconify()
  tk2.withdraw()
  tk.withdraw()
  tk3.withdraw()
  tkm.withdraw()
def medidorUV(nivel,mu):
 color=''
 for i in range(nivel):
	 if nivel<3 :
		color=GREEN
	 if nivel>=3 and nivel<6 :
		color=YELLOW
	 if nivel>=6 and nivel<8 :
		color=ORANGE
	 if nivel>=8 and nivel<10:
		color=HRED
	 if nivel> 10:
		color=HRED
	 canvas.itemconfig(10-i,fill=color)
 lk4=Label(tk,text=time.strftime("%A %d/%m/%y  %H:%M"),bg=WHITE,font="Arial 12")
 lk4.grid(row=1, column=1, sticky=E) 
 tk.geometry("%dx%d+%d+%d" % (690,580,ancho-345,alto-290))
 if mu:
	tk.deiconify()
	tk2.withdraw()
	tk3.withdraw()
	tk4.withdraw()
	tkm.withdraw()
def medidordeCO(y):
 global poligono5
 global texto4
 caja5=canvas5.create_rectangle(90,300,103,90, fill=WHITE, outline=BLACK) 
 poligono5=canvas5.create_polygon(104, 300, 104, 90, 124, 90, fill=GRAY)

 poligono5=canvas5.create_polygon(88,y,108,y,113,y+5,108,y+10,88,y+10, fill="lightblue", outline=BLUE, width=2)
 linea5=canvas5.create_line(104,300,125,300, fill=GRAY, width=3)
 linea5=canvas5.create_line(104,195,125,195, fill=GRAY, width=3)
 linea5=canvas5.create_line(104,90,132,90, fill=GRAY, width=3)
 texto5=canvas5.create_text(100,50,text="Nivel de CO2",font="Arial 16")
 if y<160:
	 texto4=canvas5.create_text(170,195,text="Alto",font="Arial 16")
 if y>=160 and y<230:
	 texto4=canvas5.create_text(170,195,text="Medio",font="Arial 16")
 if y>=230:
	 texto4=canvas5.create_text(170,195,text="Bajo",font="Arial 16")

def principal(temperatura,humedad,niveluv,ruido,nivelco,ciclo):
 LabelT= Label(tkm, text=format(temperatura) + " °C", bg=WHITE, font="Arial 12")
 LabelH= Label(tkm, text=format(humedad) + " %", bg=WHITE, font="Arial 12")
 if (niveluv<=3):
	 nuv="BAJO    "
 if ((niveluv>3) and (niveluv<=5)):
	 nuv="MEDIO   "
 if ((niveluv>5) and (niveluv<=6)):
	 nuv="ALTO    "
 if ((niveluv>6) and (niveluv<=9)):
	 nuv="MUY ALTO"
 if (niveluv>9):
	 nuv="MUY ALTO"
	 niveluv=10 	 
 LabelU= Label(tkm, text= nuv+" (" +format(niveluv)+")", bg=WHITE, font="Arial 12")
 LabelR= Label(tkm, text=ruido, bg=WHITE, font="Arial 12")
 LabelC= Label(tkm, text=nivelco, bg=WHITE, font="Arial 12")
 l1=Label(tkm,text=time.strftime("%A %d/%m/%y  %H:%M"),bg=WHITE,font="Arial 12")
 l1.grid(row=6, column=3, sticky=E,pady=10)
 LabelT.grid(row=1, column=2,sticky=W,padx=10,pady=10) 
 LabelH.grid(row=2, column=2,sticky=W,padx=10,pady=10) 
 LabelU.grid(row=3, column=2,sticky=W,padx=10,pady=10) 
 LabelR.grid(row=4, column=2,sticky=W,padx=10,pady=10) 
 LabelC.grid(row=5, column=2,sticky=W,padx=10,pady=10)

 if ciclo:
	tkm.deiconify()
	tk2.withdraw()
	tk3.withdraw()
	tk4.withdraw()
	tk.withdraw() 
 
def createDisplay():
 global tk 
 global tkm
 global canvas
 global euv
 global canvas2
 global canvas3
 global canvas4
 global canvas5
 global imgalto
 global imgmedio
 global imgbajo
 global tk2
 global tk3
 global tk4
 global ancho
 global alto
 global actualhora
 global ws
 global wb
 global sh
 global celda
 global cdi
 euv= True
 cdi=False
 tkm=Tk()
 tkm.title("ESTADO ACTUAL")
 tkm.config(bg=WHITE) 
 ancho=tkm.winfo_screenwidth()/2
 alto=tkm.winfo_screenheight()/2
 tkm.geometry("%dx%d+%d+%d" % (580,400,ancho-290,alto-200))
 actualhora=30
 rb = open_workbook('probar.xls',formatting_info=True)
 wb = copy(rb)
 sh = rb.sheet_by_index(0)
 ws = wb.get_sheet(0)
 celda=int(sh.cell_value(rowx=0, colx=1)) 
 if(sh.cell_value(rowx=celda, colx=0)!=time.strftime("%d/%m/%y")):
	ws.write(celda+1,0,time.strftime("%d/%m/%y"))
	ws.write(0,1,celda+1)	
	celda=celda+1	
	wb.save('probar.xls')
	cdi=True
	
 #Inicio Ventana rutas
 tk4=Toplevel(tkm)
 tk4.config(bg=WHITE) 
 tk4.title("RUTAS DEL PARADERO")
 nmin= int(time.strftime("%M"))

 panel=PanedWindow(tk4,bg=WHITE) 
 imgbus=PhotoImage(file="bus.gif")
 imagenbus=Label(tk4, image=imgbus,bg= WHITE)
 panel.add(imagenbus)
 TGE=Label(panel,text="RUTAS DEL PARADERO", bg=WHITE, font="Arial 14")
 panel.add(TGE,padx=10)
 RT=Label(tk4,text="RUTAS", bg=WHITE, font="Arial 12")
 R1=Label(tk4,text="Ruta 1 - Patios\nCOOMICRO", bg=WHITE, font="Arial 12")
 R2=Label(tk4,text="Ruta 2 - Zulia\nTrasan", bg=WHITE, font="Arial 12")
 R3=Label(tk4,text="Ruta 3 - Av. Américas\nCOOPETRAN", bg=WHITE, font="Arial 12")
 R4=Label(tk4,text="Ruta 4 - Motilones\nCOOMICRO", bg=WHITE, font="Arial 12")
 R5=Label(tk4,text="Ruta 5 - Guaimaral\nCOOMICRO", bg=WHITE, font="Arial 12")
 TT=Label(tk4,text="TIEMPO DE ARRIVO", bg=WHITE, font="Arial 12")
 
 ET=Label(tk4,text="ESTADO", bg=WHITE, font="Arial 12")
 tk4.withdraw()
 panel.grid(row=0,columnspan=3,padx=10,pady=10)
 RT.grid(row=1,column=0,padx=10,pady=10)
 TT.grid(row=1,column=1,padx=10,pady=10)
 ET.grid(row=1,column=2,padx=10,pady=10)
 R1.grid(row=2,column=0,padx=10,pady=10)
 R2.grid(row=3,column=0,padx=10,pady=10)
 R3.grid(row=4,column=0,padx=10,pady=10)
 R4.grid(row=5,column=0,padx=10,pady=10)
 R5.grid(row=6,column=0,padx=10,pady=10)
 rutas(nmin,False)
 
 btnUV=Button(tkm,text="Medidor UV", command=LuzUV, bg=WHITE)
 btnTH=Button(tkm,text="Temperatura-HUMEDAD", command=temp, bg=WHITE)
 btnRU=Button(tkm,text="Ruido - CO2", command=Coru, bg=WHITE)
 
 temperatura= 32
 ruido= "MEDIO"
 humedad=50
 niveluv=3
 nivelco="MEDIO"
 
 imgTemp=PhotoImage(file="temp.gif")
 imagenT=Label(tkm, image=imgTemp,bg= WHITE)
 
 imgHum=PhotoImage(file="humedad.gif")
 imagenH=Label(tkm, image=imgHum,bg= WHITE)
 
 imgCO=PhotoImage(file="CO2.gif")
 imagenCO=Label(tkm, image=imgCO,bg= WHITE)
 
 imgUV=PhotoImage(file="UV.gif")
 imagenUV=Label(tkm, image=imgUV,bg= WHITE)
 
 imgRU=PhotoImage(file="ruid.gif")
 imagenRU=Label(tkm, image=imgRU,bg= WHITE)
 
 TituloG=Label(tkm,text="ESTADO ACTUAL DE LA ESTACION",bg=WHITE, font="Arial 15")
 LabelTemp=Label(tkm, text="TEMPERATURA: ", bg=WHITE, font="Arial 12")
 LabelHum=Label(tkm, text="HUMEDAD: ", bg=WHITE, font="Arial 12")
 LabelUV=Label(tkm, text="NIVEL UV: ", bg=WHITE, font="Arial 12")
 LabelRuido=Label(tkm, text="NIVEL DE RUIDO: ", bg=WHITE, font="Arial 12")
 LabelCO=Label(tkm, text="NIVEL DE CO2: ", bg=WHITE, font="Arial 12") 

 
 TituloG.grid(row=0,columnspan=4,padx=10,pady=10)
 
 imagenT.grid(row=1, column=0,padx=10,pady=10)
 LabelTemp.grid(row=1, column=1,sticky=W,padx=10,pady=10)

 
 imagenH.grid(row=2, column=0,padx=10,pady=10)
 LabelHum.grid(row=2, column=1,sticky=W,padx=10,pady=10)

 
 imagenUV.grid(row=3, column=0,padx=10,pady=10)
 LabelUV.grid(row=3, column=1,sticky=W,padx=10,pady=10)

 
 imagenRU.grid(row=4, column=0,padx=10,pady=10)
 LabelRuido.grid(row=4, column=1,sticky=W,padx=10,pady=10)

 
 imagenCO.grid(row=5, column=0,padx=10,pady=10)
 LabelCO.grid(row=5, column=1,sticky=W,padx=10,pady=10)

 
 btnUV.grid(row=3,column=3,padx=10,pady=10)
 btnTH.grid(row=1, column=3, rowspan=2,padx=10,pady=10)
 btnRU.grid(row=4,column=3,rowspan=2,padx=10,pady=10)

 principal(temperatura,humedad,niveluv,ruido,nivelco,False)
 tkm.withdraw()
 
 #Inicio Ventana temperatura y humedad
 tk2=Toplevel(tkm)
 tk2.config(bg=WHITE)
 tk2.title("MEDIDOR DE TEMPERATURA Y HUMEDAD")
 canvas2=Canvas(tk2, width=280, height=500,bg=WHITE,highlightbackground=WHITE)
 termometro(temperatura,False)
 num=canvas2.create_text(200,210,text="TEMPERATURA",font="Arial 16")

 canvas2.grid(row=0,column=0,pady=20,padx=50)

 canvas3=Canvas(tk2, width=280, height=500,bg=WHITE,highlightbackground=WHITE)
 medidorHumedad(humedad)
 num=canvas3.create_text(200,210,text="HUMEDAD",font="Arial 16")

 canvas3.grid(row=0,column=1)

 tk2.withdraw()
 
 #Inicio Ventana Ruido y CO2
 
 tk3=Toplevel(tkm)
 tk3.config(bg=WHITE)
 tk3.title("MEDIDOR DE RUIDO Y CO2") 

 canvas4=Canvas(tk3, width=240, height=370,bg=WHITE,highlightbackground=WHITE)
 imgalto=PhotoImage(file="alto.gif")
 imgmedio=PhotoImage(file="medio.gif")
 imgbajo=PhotoImage(file="bajo.gif")
 medidordeRuido(280,False)
 
 canvas5=Canvas(tk3, width=240, height=370,bg=WHITE,highlightbackground=WHITE)
 imagalto=canvas5.create_image(104,330,anchor="center",image=imgCO)
 medidordeCO(200)
 


 canvas4.grid(row=0,column=0)
 canvas5.grid(row=0,column=1)

 tk3.withdraw()
 
 
 #Inicio Ventana UV#
 tk=Toplevel(tkm)
 tk.config(bg=WHITE) 
 tk.title("MEDIDOR DE INDICE UV")
 img = PhotoImage(file="indice.gif")
 imagen=Label(tk, image=img)
 imagen.grid(row=0,column=1,padx=10)

 
 canvas = Canvas(tk, width=WINDOW_W, height=WINDOW_H,background=BLACK)
 canvas.grid(row=0,column=0, padx=10, pady=15)
 
 light = []
 for i in range(0,NUM_BUTTON):
    x = MARGIN+((MARGIN+BUTTON_SIZE)*i)
    light.append(canvas.create_rectangle(MARGIN,x,BUTTON_SIZE+MARGIN,
           x+BUTTON_SIZE,fill=WHITE)) 

 medidorUV(niveluv,False)

 tk.withdraw()
 #Fin de la ventana UV#

 tkm.mainloop()


 
def main():
 createDisplay()


if __name__ == '__main__':
 main()


