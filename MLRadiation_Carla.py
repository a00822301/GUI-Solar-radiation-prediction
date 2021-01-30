import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn import linear_model
from sklearn import svm
from pytz import timezone
import pytz
sns.set()



train_data = pd.read_csv('SolarPrediction.csv')
train_data = train_data.sort_values(['UNIXTime'], ascending = [True])
train_data.head()



TZhawaii= timezone('Pacific/Honolulu')
train_data.index =  pd.to_datetime(train_data['UNIXTime'], unit='s')
train_data.index = train_data.index.tz_localize(pytz.utc).tz_convert(TZhawaii)

train_data['MonthOfYear'] = train_data.index.strftime('%m').astype(int)
train_data['DayOfYear'] = train_data.index.strftime('%j').astype(int)
train_data['WeekOfYear'] = train_data.index.strftime('%U').astype(int)
train_data['HourOfDay(h)'] = train_data.index.hour
train_data['MinuteOfDay(m)'] = train_data.index.minute
train_data['SecondOfDay(s)'] = train_data.index.second

train_data.drop(['Data','Time','TimeSunRise','TimeSunSet'], inplace=True, axis=1)
train_data


train_data_temp = (train_data['Temperature'] - 32)/1.8
train_data['Temperature'] = train_data_temp

train_data_pres = train_data['Pressure'] * 3386.39
train_data['Pressure'] = train_data_pres

train_data_vel = train_data['Speed'] * 0.44704
train_data['Speed'] = train_data_vel
train_data


train_data['Radiation'].describe()


group_month=train_data.groupby('MonthOfYear').mean().reset_index()
group_week=train_data.groupby('WeekOfYear').mean().reset_index()
group_day=train_data.groupby('DayOfYear').mean().reset_index()
group_hour=train_data.groupby('HourOfDay(h)').mean().reset_index()


X = train_data.iloc[:,np.r_[2:7,10]] # Independent variables: Temperature, Pressure, Humidity, Wind direction, speed and HourOfDay
y = train_data.iloc[:,1] # Dependent variable: Radiation


X.head(-5)
y.head()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 25)


regresor= LinearRegression()
reg = regresor.fit(X_train, y_train)
regresor_pred = regresor.predict(X_test)

slope_T = reg.coef_[0]
intercept = reg.intercept_

train_data.iloc[0]



rf_reg = RandomForestRegressor()
rf_reg.fit(X_train, y_train)
randomforest_pred= rf_reg.predict(X_test)



dtree = DecisionTreeRegressor(max_depth=8, min_samples_leaf=0.13, random_state=3)
dtree.fit(X_train, y_train)
pred_train_tree= dtree.predict(X_test)



train_data.iloc[100]

modelos = ["SVR","SGDRegressor","BayesianRidge", "LassoLars", "ARDRegression",
                   "PassiveAggressiveRegressor","TheilSenRegressor","LinearRegression",
                   "RandomForestRegressor","DecisionTreeRegressor"]
classifiers = [
    svm.SVR(),
    linear_model.SGDRegressor(),
    linear_model.BayesianRidge(),
    linear_model.LassoLars(),
    linear_model.ARDRegression(),
    linear_model.PassiveAggressiveRegressor(),
    linear_model.TheilSenRegressor(),
    linear_model.LinearRegression(),
    RandomForestRegressor(),
    DecisionTreeRegressor(max_depth=8, min_samples_leaf=0.13, random_state=3)]


"""
Created on Fri Nov 27 16:36:22 2020    
@author: Carla López
Now that we have our models up  and running, we will create a GUI 
that allows the user to import their own data
"""

import tkinter as tk
from tkinter import ttk

#SE DEFNIE EL ESPACIO 
class ScrolledFrame(tk.Frame):
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill= tk.Y, side=tk.RIGHT, expand=False)


        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vscrollbar.config(command=self.canvas.yview)
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.contenedor = tk.Frame(self.canvas)
        self.contenedor_id = self.canvas.create_window(0, 0,
                                                       window=self.contenedor,
                                                       anchor=tk.NW)
        self.contenedor.bind('<Configure>', self._configure_contenedor)
        self.canvas.bind('<Configure>', self._configure_canvas)


    def _configure_contenedor(self, event):
        size = (self.contenedor.winfo_reqwidth(), self.contenedor.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 {} {}".format(*size))
        if self.contenedor.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.contenedor.winfo_reqwidth())


    def _configure_canvas(self, event):
        if self.contenedor.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.contenedor_id, width=self.canvas.winfo_width())

#SE CREA LA APLICACION
class Aplicacion:
    def __init__(self, root):
        self.master = root

        self.frame_conf = tk.Frame(root)
        self.frame_conf.pack()
        
        label  = tk.Label(self.frame_conf,
                          text = 'Ingresa los datos del día')
        label.grid(row = 0, column = 0, columnspan = 3, sticky ='nsew', padx=10, pady=10)

       
        tk.Label(self.frame_conf,
                          text = 'Temperatura [°C]').grid(row = 1, column = 0, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        self.temp  = tk.Entry(self.frame_conf)
        self.temp.grid(row = 1, column = 1, columnspan = 1, sticky =tk.W+tk.E+tk.N+tk.S, padx=10)
        
        tk.Label(self.frame_conf,
                          text = 'Presion atmosférica [Pa]').grid(row = 2, column = 0, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        self.pressure  = tk.Entry(self.frame_conf)
        self.pressure.grid(row = 2, column = 1, columnspan = 1, sticky =tk.W+tk.E+tk.N+tk.S, padx=10)
        
        tk.Label(self.frame_conf,
                          text = 'Humedad [%]').grid(row = 3, column = 0, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        self.humidity  = tk.Entry(self.frame_conf)
        self.humidity.grid(row = 3, column = 1, columnspan = 1, sticky =tk.W+tk.E+tk.N+tk.S, padx=10)
        
        tk.Label(self.frame_conf,
                          text = 'Dirección del viento [°]').grid(row = 1, column = 2, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        self.winddir  = tk.Entry(self.frame_conf)
        self.winddir.grid(row = 1, column = 3, columnspan = 1, sticky =tk.W+tk.E+tk.N+tk.S, padx=10)
        
        tk.Label(self.frame_conf,
                          text = 'Velocidad del viento [m/s]').grid(row = 2, column = 2, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        self.windvel  = tk.Entry(self.frame_conf)
        self.windvel.grid(row = 2, column = 3, columnspan = 1, sticky =tk.W+tk.E+tk.N+tk.S, padx=10)
        
        tk.Label(self.frame_conf,
                          text = 'Hora del día [0-23]').grid(row = 3, column = 2, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        self.hour  = tk.Entry(self.frame_conf)
        self.hour.grid(row = 3, column = 3, columnspan = 1, sticky =tk.W+tk.E+tk.N+tk.S, padx=10)
       
        #ESCOGEMOS EL MODELO A UTILIZAR
        self.options = tk.StringVar()
        self.options.set("Escoge uno") # default value
        
        tk.Label(self.frame_conf,  text='Modelo a usar', width=15 ).grid(row=4,column=0) 
       
        self.om1 =tk.OptionMenu(self.frame_conf, self.options, *modelos)
        self.om1.grid(row=4,column=1,columnspan = 2) 
        
        boton = tk.Button(self.frame_conf, text = 'Guardar', command = self.save_data)
        boton.grid(row = 4, column = 3, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        
        boton = tk.Button(self.frame_conf, text = 'Resultados', command = self.next_win)
        boton.grid(row = 5, column = 3, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        
        
        self.lbl_info  = tk.Label(root)
        self.lbl_info.pack(padx=10, anchor = 'w')

        self.frame_botones = ScrolledFrame(root)
        self.frame_botones.pack(fill = 'x')
        
        #Guardamos los datos de las entries en variables globales.
    def save_data(self):
        global data
        global modelo
        global radiation
    
        data = [float(self.temp.get()),float(self.pressure.get()), float(self.humidity.get()), 
                float(self.winddir.get()), float(self.windvel.get()), float(self.hour.get())]
        
        modelo=modelos.index(self.options.get())
        
        # MANDAMOS A LLAMAR LA FUNCIÓN
        global clf
        clf = classifiers[modelo]
        clf.fit(X_train, y_train)
        radiation = clf.predict([data])

    def next_win(self):     
       
        label  = tk.Label(self.frame_conf,
                          text = 'La radiación predicha por el modelo '+ self.options.get()+
                          ', a las '+str(self.hour.get())+' es '+str(round(radiation[0], 2))+ ' [W/m^2].')
        label.grid(row = 5, column = 0, columnspan = 3, sticky ='nsew', padx=10, pady=0)
        
        tk.Label(self.frame_conf,  text='Panel a usar', width=15 ).grid(row=6,column=0) 
        
        global paneles
        paneles = ['LG335N1C-A5', 'LG33ON1C-A5', 'LG325N1C-A5']
        
        self.panels = tk.StringVar()
        self.panels.set("Escoge uno") 
        
        self.om2 =tk.OptionMenu(self.frame_conf, self.panels, *paneles)
        self.om2.grid(row=6,column=1,columnspan = 1) 
        
        boton = tk.Button(self.frame_conf, text = 'Producción fotovoltaica', command = self.energy_win)
        boton.grid(row = 6, column = 2, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        
    def energy_win(self):
        
        i=paneles.index(self.panels.get())
        panels=[[9.83,34.1,10.49,41.0,1000,-0.27,45,25,800],[9.80,33.7,10.45,40.9,1000,-0.27,45,25,800],
                [9.77,33.3,10.41,40.8,1000,-0.27,45,25,800]]
        Impp=panels[i][0]
        Vmpp=panels[i][1]
        Isc=panels[i][2]
        Voc=panels[i][3]
        Gstc=panels[i][4]
        beta=panels[i][5]
        Tnoct=panels[i][6]
        Tstc=panels[i][7]
        Gnoct=panels[i][8]
        FF=Impp*Vmpp/(Isc*Voc)
        
        global total
        total=0
        datas = data[:-1]
        
        for t in range(12,38):
            t=t/2
            d=np.concatenate((datas,[t]))
            G = clf.predict([d])
            I=Isc/Gstc*G
            V=Voc+beta*(Tnoct-Tstc)/Gnoct*G
            E=FF*I*V/1000*0.5 #Energia producida en media hora en kWh
            total=total+E 
        
        label  = tk.Label(self.frame_conf,
                          text = 'La producción fotovolataica para el panel '+ self.panels.get()+
                          ' en todo el día es '+str(round(total[0],2))+ ' [kWh].')
        label.grid(row = 7, column = 0, columnspan = 4, sticky ='nsew', padx=10, pady=0)
        
        boton = tk.Button(self.frame_conf, text = 'Análisis energético', command = self.panels_win)
        boton.grid(row = 8, column = 1, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        
        
    def panels_win(self):
        
        label  = tk.Label(self.frame_conf,
                          text = 'Escoge los artículos que quieras agregar')
        label.grid(row = 9, column = 0, columnspan = 3, sticky ='nsew', padx=10, pady=0)
        
        self.v = tk.StringVar() 
        values = {"Aire acondicionado" : "1", 
                  "Ventiladores" : "2", "Refrigeración de alimentos" : "3", 
                  "Aparatos de cocina" : "4", "Luz" : "5", 
                  "Entretenimiento" : "6", "Lavandería" : "7"}
        
        opcionesac = ["Comfort Central (2 tons)",
                    "Comfort Central (3 tons)",
                    "Comfort Central (4 tons)",
                    "Room Units (8 hrs, 1 Ton, EER 6)",
                    "Room Units (8 hrs, 1 Ton, EER 8)",
                    "Room Units (8 hrs, 3/4 Ton, EER 6)",
                    "Room Units (8 hrs, 3/4 ton, EER 8)"]
        
        opcionesvent = ["Whole House","Circulating","Ceiling"]

        opcionesrefri = ["Refrigerator( Manual 12 cu. ft.)","Ref-Freezer (Manual 12-14 cu. ft.)",
                         "Ref-Freezer (Frost-free 14-17 cu. ft.)","Ref-Freezer (Frost free 17-20 cu. ft.)",
                         "Freezer (Manual 14.5-17.5 cu. ft.)","Freezer (Frost- Free  14.5- 17.5 cu. ft.)"]

        opcionescocina = ["Baby Food/Bottle Warmer","Broiler/Rotisserie","Coffee Maker",
                          "Dishwasher","Egg Cooker","Frying Pan",
                          "Microwave Oven", "Range with Oven", "Roaster",
                          "Sandwich Grill", "Slow Cooker", "Toaster", "Trash Compactor", "Waffle Iron"]
        opcionesluz =["4-5 Room","6-8 Room","Outdoors, 1 Spotlight, All Night"]

        opcionesentr = ["Radio","Radio/Record Player","Television (color solid state)"]
        
        opcioneslav = ["Dryer","Iron","Washing Machine"]

        
        self.options1 = tk.StringVar()
        self.options1.set("Escoge uno")
        self.options2 = tk.StringVar()
        self.options2.set("Escoge uno")
        self.options3 = tk.StringVar()
        self.options3.set("Escoge uno")
        self.options4 = tk.StringVar()
        self.options4.set("Escoge uno")
        self.options5 = tk.StringVar()
        self.options5.set("Escoge uno")
        self.options6 = tk.StringVar()
        self.options6.set("Escoge uno")
        self.options7 = tk.StringVar()
        self.options7.set("Escoge uno")
            
        for (text, value) in values.items(): 
            tk.Label(self.frame_conf, text = text).grid(row=9+int(value),column=0, padx=0, pady=0)  
            
            
        tk.OptionMenu(self.frame_conf, self.options1,
                           *opcionesac).grid(row=10,column=1, columnspan = 2)
        boton = tk.Button(self.frame_conf, text = 'Añadir', command = self.but1)
        boton.grid(row = 10, column = 3, columnspan = 1, sticky ='nsew', padx=10, pady=10) 
          
        tk.OptionMenu(self.frame_conf, self.options2,
                           *opcionesvent).grid(row=11,column=1, columnspan = 2)
        boton = tk.Button(self.frame_conf, text = 'Añadir', command = self.but2)
        boton.grid(row = 11, column = 3, columnspan = 1, sticky ='nsew', padx=10, pady=10) 
        
        tk.OptionMenu(self.frame_conf, self.options3,
                           *opcionesrefri).grid(row=12,column=1, columnspan = 2)
        boton = tk.Button(self.frame_conf, text = 'Añadir', command = self.but3)
        boton.grid(row = 12, column = 3, columnspan = 1, sticky ='nsew', padx=10, pady=10) 
        
        tk.OptionMenu(self.frame_conf, self.options4,
                           *opcionescocina).grid(row=13,column=1, columnspan = 2) 
        boton = tk.Button(self.frame_conf, text = 'Añadir', command = self.but4)
        boton.grid(row = 13, column = 3, columnspan = 1, sticky ='nsew', padx=10, pady=10) 
        
        tk.OptionMenu(self.frame_conf, self.options5,
                           *opcionesluz).grid(row=14,column=1, columnspan = 2)
        boton = tk.Button(self.frame_conf, text = 'Añadir', command = self.but5)
        boton.grid(row = 14, column = 3, columnspan = 1, sticky ='nsew', padx=10, pady=10) 
        
        tk.OptionMenu(self.frame_conf, self.options6,
                           *opcionesentr).grid(row=15,column=1, columnspan = 2) 
        boton = tk.Button(self.frame_conf, text = 'Añadir', command = self.but6)
        boton.grid(row = 15, column = 3, columnspan = 1, sticky ='nsew', padx=10, pady=10) 
        
        tk.OptionMenu(self.frame_conf, self.options7,
                           *opcioneslav).grid(row=16,column=1, columnspan = 2)
        boton = tk.Button(self.frame_conf, text = 'Añadir', command = self.but7)
        boton.grid(row = 16, column = 3, columnspan = 1, sticky ='nsew', padx=10, pady=10) 
        
        tk.Label(self.frame_conf, text = "Los artículos escogidos son:").grid(row=1,column=4, padx=0, pady=0)  
        for n in range(12):
            tk.Label(self.frame_conf, 
                     text = " _________________________________________ ").grid(row=2+n,column=4, rowspan = 1,padx=10, pady=10) 

        
        
        boton = tk.Button(self.frame_conf, text = 'Borrar artículos', command = self.borrar)
        boton.grid(row = 15, column = 4, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        
        
        boton = tk.Button(self.frame_conf, text = 'Evaluar', command = self.evaluate)
        boton.grid(row = 16, column = 4, columnspan = 1, sticky ='nsew', padx=10, pady=10)
        
        self.count = tk.IntVar()
        self.count = 0

        global arti
        arti = []
        self.totenergy = tk.DoubleVar()
        self.totenergy = 0
        
        tk.Label(self.frame_conf, text = "Rendimiento del panel").grid(row=1,column=5,padx=0, pady=0) 
        self.bar = ttk.Progressbar(self.frame_conf, length = 400, mode='determinate',orient=tk.VERTICAL)
        self.bar.grid(row = 2, rowspan=10, column = 5)
        
        tk.Label(self.frame_conf, text = 'La potencia generada').grid(row=12,column=5,padx=0, pady=0) 
        tk.Label(self.frame_conf, text = ' por el panel es '+str(round(total[0],2))+' [kWh].').grid(row=13,column=5,padx=0, pady=0) 
        tk.Label(self.frame_conf, text = 'La potencia consumida por los').grid(row=14,column=5,padx=0, pady=0) 
        tk.Label(self.frame_conf, text = 'artículos seleccionados es ').grid(row=15,column=5,padx=0, pady=0) 
        tk.Label(self.frame_conf, text = str(round(self.totenergy,2))+' [kWh].').grid(row=16,column=5,padx=0, pady=0) 
             
        self.articles = ['Comfort Central (2 tons)', 'Comfort Central (3 tons)',
                    'Comfort Central (4 tons)',
                    'Room Units (8 hrs, 1 Ton, EER 6)',
                    'Room Units (8 hrs, 1 Ton, EER 8)',
                    'Room Units (8 hrs, 3/4 Ton, EER 6)',
                    'Room Units (8 hrs, 3/4 ton, EER 8)',
                    'Whole House','Circulating','Ceiling',
                    'Refrigerator( Manual 12 cu. ft.)',
                    'Ref-Freezer (Manual 12-14 cu. ft.)',
                    'Ref-Freezer (Frost-free 14-17 cu. ft.)',
                    'Ref-Freezer (Frost free 17-20 cu. ft.)',
                    'Freezer (Manual 14.5-17.5 cu. ft.)',
                    'Freezer (Frost- Free  14.5- 17.5 cu. ft.)',
                    'Baby Food/Bottle Warmer','Broiler/Rotisserie',
                    'Coffee Maker','Dishwasher','Egg Cooker','Frying Pan','Microwave Oven',
                    'Range with Oven','Roaster',
                    'Sandwich Grill','Slow Cooker', 'Toaster','Trash Compactor','Waffle Iron','4-5 Room',
                    '6-8 Room','Outdoors, Spotlight, All Night',
                    'Dryer','Iron','Washing Machine','Radio',
                    'Radio/Record Player','Television (color solid state)']

        self.kwh = [48.33333333, 70, 91.66666667, 4.714666667, 3.536,
                           16.50133333, 12.376, 1, 0.133333333, 0.4, 2.6,
                           4.166666667, 5.666666667, 6.833333333, 4.5, 
                           6.266666667, 0.066666667, 0.233333333, 0.3, 1,
                           0.033333333, 0.266666667, 0.533333333, 1.933333333, 
                           0.166666667, 0.1, 0.4, 0.1, 0.133333333, 0.066666667,
                           1.666666667, 2, 1.5, 2.5, 0.166666667, 0.3, 0.233333333, 0.3,0.9]
        
        self.frame_conf.mainloop()

    def but1(self):
        self.count += 1
        tk.Label(self.frame_conf, text = self.options1.get()).grid(row = 1+self.count, column = 4)
        arti.append(self.options1.get())
    def but2(self):
        self.count += 1
        tk.Label(self.frame_conf, text = self.options2.get()).grid(row = 1+self.count, column = 4)
        arti.append(self.options2.get())
    def but3(self):
        self.count += 1
        tk.Label(self.frame_conf, text = self.options3.get()).grid(row = 1+self.count, column = 4)
        arti.append(self.options3.get())
    def but4(self):
        self.count += 1
        tk.Label(self.frame_conf, text = self.options4.get()).grid(row = 1+self.count, column = 4)
        arti.append(self.options4.get())
    def but5(self):
        self.count += 1
        tk.Label(self.frame_conf, text = self.options5.get()).grid(row = 1+self.count, column = 4)
        arti.append(self.options5.get())
    def but6(self):
        self.count += 1
        tk.Label(self.frame_conf, text = self.options6.get()).grid(row = 1+self.count, column = 4)
        arti.append(self.options6.get())
    def but7(self):
        self.count += 1
        tk.Label(self.frame_conf, text = self.options7.get()).grid(row = 1+self.count, column = 4)
        arti.append(self.options7.get())
        
        
    def borrar(self):
        self.count = 0
        for n in range(12):
            tk.Label(self.frame_conf, 
                     text = " _________________________________________ ").grid(row=2+n,column=4, rowspan = 1,padx=10, pady=10) 
        arti.clear()
        self.totenergy=0
        self.bar['value'] = self.totenergy
        tk.Label(self.frame_conf, text = '                0 [kWh].                 ').grid(row=16,column=5,padx=0, pady=0) 
        
    def evaluate(self):
        print(arti)
        self.totenergy = 0
        for n in range(len(arti)) :
            energy  = self.kwh[self.articles.index(arti[n])]
            self.totenergy = self.totenergy + energy
        
        self.bar['value'] = self.totenergy/total[0]*100
            
        tk.Label(self.frame_conf, text = 'La potencia consumida por los').grid(row=14,column=5,padx=0, pady=0) 
        tk.Label(self.frame_conf, text = 'artículos seleccionados es').grid(row=15,column=5,padx=0, pady=0) 
        tk.Label(self.frame_conf, text = str(round(self.totenergy,2))+' [kWh].').grid(row=16,column=5,padx=0, pady=0) 
         
            
            
        
def main(): 
    root = tk.Tk()
    Aplicacion(root)
    root.title("Produccion fotovoltaica")
    root.mainloop()

if __name__ == '__main__':
    main()

