from tkinter import *
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
from matplotlib.figure import Figure

#LECTURA Y CAMBIO DE NOMBRES A LAS COLUMNAS

root=Tk()
root.title('GESTION DE RESULTADOS PROYECTO QB2')
root.configure(bg="#BDBDBD")
root.geometry('900x755')  #Definir el tamaño de celda
root.resizable(width=0, height=0)

# Definir Colores
d_color={'fondobg':'#BDBDBD','buttonbg':'gray','framebg':'gray60','labelbg':'#BDBDBD'}
# DEFINIR PONDERACIONES
d_pon = {'TR': 0.05, 'PA': 0.1, 'MO': 0.45, 'NI': 0.2, 'PI': 0.1, 'PU': 0.1}


#Creando pestañas
nb=ttk.Notebook(root)
nb.pack(fill='both',expand='yes')  #expandir las pestañas
s = ttk.Style()
s.configure('TLabelframe', background='#BDBDBD')
General=ttk.Frame(nb,style='TLabelframe')
Detalle=ttk.Frame(nb,style='TLabelframe')
Regre=ttk.Frame(nb,style='TLabelframe')
nb.add(General,text='General')
nb.add(Detalle,text='Detalle')
nb.add(Regre,text='Proyección')





################################General##################################################################################
def importar():
    global df, matrix, pint_dtr, pint_dpa, pint_dmo, pint_dni, pint_dpi, pint_dpu, pint_dtrdmo, d_color

    import_file_path = filedialog.askopenfilename()
    df = pd.read_excel(import_file_path,sheet_name='Reporte', skiprows = 7)
    df = df[['ID Tekla', 'ESP', 'Barcode', 'Peso Total (Kg)', 'Ratio', 'Traslado', 'Pre armado', 'Montaje',
             'Nivelacion, soldadura &Torque', 'Touch up', 'Punch list', 'Protocolo Torque']]

    df.rename(columns={'ID Tekla': 'ID', 'Peso Total (Kg)': 'WEIGHT', 'Traslado': 'DTR', 'Pre armado': 'DPA',
                       'Montaje': 'DMO', 'Nivelacion, soldadura &Torque': 'DNI', 'Touch up': 'DPI',
                       'Punch list': 'DPU'},
              inplace=True)
    df = df[df.Ratio.notnull()]  # LIMPIAMOS DATOS QUE ESTEN NULOS EN EL RATIO
    df = df[df.WEIGHT.notnull()]  # LIMPIAMOS LOS DATOS QUE ESTEN NULOS EN EL PESO

    ####DEFINIMOS LAS COLUMNAS EN DATOS DE FECHAS EN MATRIX####
    df['DTR'] = pd.to_datetime(df['DTR'])
    df['DPA'] = pd.to_datetime(df['DPA'])
    df['DMO'] = pd.to_datetime(df['DMO'])
    df['DNI'] = pd.to_datetime(df['DNI'])
    df['DPI'] = pd.to_datetime(df['DPI'])
    df['DPU'] = pd.to_datetime(df['DPU'])

    ##CALCULO DE PESOS TOTALES DE SEGUN PONDERACION

    df['TOTAL_WTR'] = df.WEIGHT * d_pon['TR']
    df['TOTAL_WPA'] = df.WEIGHT * d_pon['PA']
    df['TOTAL_WMO'] = df.WEIGHT * d_pon['MO']
    df['TOTAL_WNI'] = df.WEIGHT * d_pon['NI']
    df['TOTAL_WPI'] = df.WEIGHT * d_pon['PI']
    df['TOTAL_WPU'] = df.WEIGHT * d_pon['PU']

    # CALCULO DE HH EARNED TOTALES SEGUN PONDERACION
    df['TOTAL_ETR'] = df.WEIGHT * d_pon['TR'] * df.Ratio / 1000
    df['TOTAL_EPA'] = df.WEIGHT * d_pon['PA'] * df.Ratio / 1000
    df['TOTAL_EMO'] = df.WEIGHT * d_pon['MO'] * df.Ratio / 1000
    df['TOTAL_ENI'] = df.WEIGHT * d_pon['NI'] * df.Ratio / 1000
    df['TOTAL_EPI'] = df.WEIGHT * d_pon['PI'] * df.Ratio / 1000
    df['TOTAL_EPU'] = df.WEIGHT * d_pon['PU'] * df.Ratio / 1000

    # CALCULO DE PESO SEGUN AVANCE
    df['WTR'] = np.where(df['DTR'].isnull(), 0, df.WEIGHT * d_pon['TR'])
    df['WPA'] = np.where(df['DPA'].isnull(), 0, df.WEIGHT * d_pon['PA'])
    df['WMO'] = np.where(df['DMO'].isnull(), 0, df.WEIGHT * d_pon['MO'])
    df['WNI'] = np.where(df['DNI'].isnull(), 0, df.WEIGHT * d_pon['NI'])
    df['WPI'] = np.where(df['DPI'].isnull(), 0, df.WEIGHT * d_pon['PI'])
    df['WPU'] = np.where(df['DPU'].isnull(), 0, df.WEIGHT * d_pon['PU'])

    # CALCULO DE HH EARNED SEGUN AVANCE
    df['ETR'] = np.where(df['DTR'].isnull(), 0, df.WEIGHT * d_pon['TR'] * df.Ratio / 1000)
    df['EPA'] = np.where(df['DPA'].isnull(), 0, df.WEIGHT * d_pon['PA'] * df.Ratio / 1000)
    df['EMO'] = np.where(df['DMO'].isnull(), 0, df.WEIGHT * d_pon['MO'] * df.Ratio / 1000)
    df['ENI'] = np.where(df['DNI'].isnull(), 0, df.WEIGHT * d_pon['NI'] * df.Ratio / 1000)
    df['EPI'] = np.where(df['DPI'].isnull(), 0, df.WEIGHT * d_pon['PI'] * df.Ratio / 1000)
    df['EPU'] = np.where(df['DPU'].isnull(), 0, df.WEIGHT * d_pon['PU'] * df.Ratio / 1000)

    df['WBRUTO'] = np.where(df['DMO'].isnull(), 0, df.WEIGHT)

    ##########################SEPARAMOS LOS PESOS POR AVANCE DE CADA ETAPA
    df_dtr = df[["ESP", "ID", "WEIGHT", "Ratio", "DTR", "WTR", "ETR"]]
    df_dtr = df_dtr.dropna(subset=['DTR'])  # Elimina llas filas vacias de DTR
    df_dtr["Etapa"] = "1-Traslado"
    df_dtr = df_dtr.rename(columns={'WTR': 'WPOND', "DTR": 'Fecha', 'ETR': 'HGan'})

    df_dpa = df[["ESP", "ID", "WEIGHT", "Ratio", "DPA", "WPA", "EPA"]]
    df_dpa = df_dpa.dropna(subset=['DPA'])
    df_dpa["Etapa"] = "2-Ensamble"
    df_dpa = df_dpa.rename(columns={'WPA': 'WPOND', "DPA": 'Fecha', 'EPA': 'HGan'})

    df_dmo = df[["ESP", "ID", "WEIGHT", "Ratio", "DMO", "WMO", "EMO"]]
    df_dmo = df_dmo.dropna(subset=['DMO'])
    df_dmo["Etapa"] = "3-Montaje"
    df_dmo = df_dmo.rename(columns={'WMO': 'WPOND', "DMO": 'Fecha', 'EMO': 'HGan'})

    df_dni = df[["ESP", "ID", "WEIGHT", "Ratio", "DNI", "WNI", "ENI"]]
    df_dni = df_dni.dropna(subset=['DNI'])
    df_dni["Etapa"] = "4-Alineamiento"
    df_dni = df_dni.rename(columns={'WNI': 'WPOND', "DNI": 'Fecha', 'ENI': 'HGan'})

    df_dpi = df[["ESP", "ID", "WEIGHT", "Ratio", "DPI", "WPI", "EPI"]]
    df_dpi = df_dpi.dropna(subset=['DPI'])
    df_dpi["Etapa"] = "5-Touch Up"
    df_dpi = df_dpi.rename(columns={'WPI': 'WPOND', "DPI": 'Fecha', 'EPI': 'HGan'})

    df_dpu = df[["ESP", "ID", "WEIGHT", "Ratio", "DPU", "WPU", "EPU"]]
    df_dpu = df_dpu.dropna(subset=['DPU'])
    df_dpu["Etapa"] = "6-Punch List"
    df_dpu = df_dpu.rename(columns={'WPU': 'WPOND', "DPU": 'Fecha', 'EPU': 'HGan'})

    ##CONCATENAR VERTICAL DE LAS COLUMNAS DE RESUMEN

    matrix = pd.concat(
        [df_dtr.round(1), df_dpa.round(1), df_dmo.round(1), df_dni.round(1), df_dpi.round(1), df_dpu.round(1)], axis=0)

    d_color = {'1-Traslado': 'green', '2-Ensamble': 'gray', '3-Montaje': '#00aae4', '4-Alineamiento': '#FF0000',
               '5-Touch Up': '#9E19CF', '6-Punch List': '#D4CE4D'}

    # Asignar valores a una columna según diccionario
    matrix['color'] = matrix['Etapa'].map(d_color)

    ##CREAMOS LAS CARPETAS PARA TEKLA
    pint_dtr = df[['ID', 'DTR']].dropna()
    pint_dtr['USER_FIELD_1'] = 'DTR'
    pint_dtr = pint_dtr[['ID', 'USER_FIELD_1']]

    pint_dpa = df[['ID', 'DPA']].dropna()
    pint_dpa['USER_FIELD_1'] = 'DPA'
    pint_dpa = pint_dpa[['ID', 'USER_FIELD_1']]

    pint_dmo = df[['ID', 'DMO']].dropna()
    pint_dmo['USER_FIELD_1'] = 'DMO'
    pint_dmo = pint_dmo[['ID', 'USER_FIELD_1']]

    pint_dni = df[['ID', 'DNI']].dropna()
    pint_dni['USER_FIELD_1'] = 'DNI'
    pint_dni = pint_dni[['ID', 'USER_FIELD_1']]

    pint_dpi = df[['ID', 'DPI']].dropna()
    pint_dpi['USER_FIELD_1'] = 'DPI'
    pint_dpi = pint_dpi[['ID', 'USER_FIELD_1']]

    pint_dpu = df[['ID', 'DPU']].dropna()
    pint_dpu['USER_FIELD_1'] = 'DPU'
    pint_dpu = pint_dpu[['ID', 'USER_FIELD_1']]

    pint_dtrdmo = df[['ID', 'DTR', 'DMO']]
    pint_dtrdmo = pint_dtrdmo.dropna(subset=['DTR', 'ID'])  # FILTRAR LOS VACIOS DE DTR Y ID

    pint_dtrdmo.DMO = pint_dtrdmo.DMO.isnull()
    pint_dtrdmo = pint_dtrdmo[pint_dtrdmo.DMO == True]
    pint_dtrdmo['USER_FIELD_1'] = 'SALD'
    pint_dtrdmo = pint_dtrdmo[['ID', 'USER_FIELD_1']]

    #########################infromacion general########################                                                INFORMACION GENERAL
    sum_proy=round(df["WEIGHT"].sum()/1000,0)
    wpond_proy=round((df["WTR"].sum()+df["WPA"].sum()+df["WMO"].sum()+df["WNI"].sum()+df["WPI"].sum()+df["WPU"].sum())/1000,0)
    wbrut_proy=round((df["WBRUTO"].sum())/1000,0)
    porcwpon_proy=round(wpond_proy/sum_proy*100,2)
    porcbbrut_proy=round(wbrut_proy/sum_proy*100,2)

    labelinf0 = Label(General,text=sum_proy,bg='gray60').place(x=55,y=42)
    labelinf1 = Label(General, text=wpond_proy, bg='gray60').place(x=55, y=64)
    labelinf2 = Label(General, text=wbrut_proy, bg='gray60').place(x=55, y=86)
    labelinf3 = Label(General, text=porcwpon_proy, bg='gray60').place(x=190, y=64)
    labelinf4 = Label(General, text=porcbbrut_proy, bg='gray60').place(x=190, y=86)


    ##################################################################infodiaria###################                     #SELECCION POR MONTAJE DIARIO
    infdia=matrix.groupby(['Fecha'])
    pondia=infdia['WPOND'].sum()/1000
    matrixtemp=matrix[matrix.Etapa=='3-Montaje']
    matrixtemp['WBRUTO']=matrixtemp['WPOND'].div(d_pon['MO']*1000)
    infodiab=matrixtemp.groupby(['Fecha'])
    brutdia=infodiab['WBRUTO'].sum()

    label2=pd.concat([pondia,brutdia],axis=1)
    label2['FECHA'] = label2.index
    label2=label2[['FECHA','WPOND','WBRUTO']]
    label2['FECHA'] = label2["FECHA"].dt.strftime("%m/%d/%y")


    label2['WPACUM'] = label2.WPOND.cumsum()
    label2['WBACUM'] = label2.WBRUTO.cumsum()
    label2=label2.fillna(method='ffill')
    label2=label2.round(2)


    tree = ttk.Treeview(General)
    tree.pack()
    tree['column'] = list(label2.columns)
    tree['show'] = 'headings'
    #loop trhu column
    for column in tree['column']:
        tree.heading(column,text=column)

    df_rows=label2.to_numpy().tolist()
    for row in df_rows:
        tree.insert("","end",values=row)
    tree.place(x=7,y=162)

    tree.column("#1", width=89, minwidth=89, stretch=tk.NO)
    tree.column("#2", width=65, minwidth=65,stretch=tk.NO)
    tree.column("#3", width=68, minwidth=68, stretch=tk.NO)
    tree.column("#4", width=79, minwidth=79, stretch=tk.NO)
    tree.column("#5", width=79, minwidth=79, stretch=tk.NO)


    ######################################frame 3#################                                                      #SELECCION POR ESP

    espinfo=df.groupby(['ESP'])
    espresum=espinfo['WEIGHT'].sum()/1000
    esppon=matrix.groupby(['ESP'])
    esppond=esppon['WPOND'].sum()/1000
    matrixesp = matrixtemp.groupby(['ESP'])
    espbruto = matrixesp['WBRUTO'].sum()

    label3=pd.concat([espresum,esppond,espbruto],axis=1,ignore_index=True)

    label3['ESP_N'] = label3.index
    label3.reset_index(drop=True, inplace=True)
    np_array=label3.to_numpy()
    label3=pd.DataFrame(data=np_array,columns=['TOTAL','WPOND','WBRUTO','ESP'])

    label3=label3[['ESP','TOTAL','WPOND','WBRUTO']]



    label3['WPOND%']=label3.WPOND/label3.TOTAL*100
    label3['WBRUTO%'] = label3.WBRUTO / label3.TOTAL * 100

    label3=label3.fillna(0)
    label3=label3.round(2)



    tree2 = ttk.Treeview(General)
    tree2.pack()
    tree2['column'] = list(label3.columns)
    tree2['show'] = 'headings'
    #loop trhu column
    for column in tree2['column']:
        tree2.heading(column,text=column)

    df_rows=label3.to_numpy().tolist()
    for row in df_rows:
        tree2.insert("","end",values=row)
    tree2.place(x=7,y=440)

    tree2.column("#1", width=75, minwidth=75, stretch=tk.NO)
    tree2.column("#2", width=55, minwidth=55,stretch=tk.NO)
    tree2.column("#3", width=55, minwidth=55, stretch=tk.NO)
    tree2.column("#4", width=55, minwidth=55, stretch=tk.NO)
    tree2.column("#5", width=70, minwidth=70, stretch=tk.NO)
    tree2.column("#6", width=70, minwidth=70, stretch=tk.NO)





    #sns.lineplot(data=label2, x='FECHA', y='WPACUM', ax=ax)


    myPlot.cla()
    myPlot.plot(label2.FECHA,label2.WPACUM)
    myPlot.plot(label2.FECHA, label2.WBACUM)
    canvas.draw()

    myPlot1.cla()
    myPlot1.bar(label3.ESP, label3.WBRUTO, width=0.4,label='WBruto')
    myPlot1.bar(label3.ESP,label3.WPOND,width=0.2,label='WPond')
    canvas1.draw()





    ####################CONFIG SCROLLBAR

    desl1 = ttk.Scrollbar(General, orient="vertical", command=tree.yview)
    desl1.place(x=372, y=163, height=225)
    tree.configure(yscrollcommand=desl1.set)

    desl2 = ttk.Scrollbar(General, orient="vertical", command=tree2.yview)
    desl2.place(x=372, y=441, height=225)
    tree2.configure(yscrollcommand=desl2.set)






###################################################################DETALLE##############################################

def pbi():                                                                                                              #FUNCION EXPORTAR PARA PBI
    global df
    global matrix

    export_file= filedialog.askdirectory()
    df.to_csv(export_file+'/base.csv',index=False)
    matrix.to_csv(export_file + '/base_powerbi.csv', header=True, index=False)

def pintadog():                                                                                                         #FUNCION EXPORTAR PARA PINTAR
    global df,matrix,pint_dtr,pint_dpa,pint_dmo,pint_dni,pint_dpi,pint_dpu,pint_dtrdmo

    export_file= filedialog.askdirectory()
    # Exportar para tekla
    pint_dtr.to_csv(export_file+'/dtr_tekla.csv', index=False)
    pint_dpa.to_csv(export_file+'/dpa_tekla.csv', index=False)
    pint_dmo.to_csv(export_file+'/dmo_tekla.csv', index=False)
    pint_dni.to_csv(export_file+'/dni_tekla.csv', index=False)
    pint_dpi.to_csv(export_file+'/dpi.csv', index=False)
    pint_dpu.to_csv(export_file+'/dpu.csv', index=False)
    pint_dtrdmo.to_csv(export_file+'/pint_dtr_dmo.csv', index=False)









frame1_1=Frame(General,width=250,height=110,bg=d_color['framebg'],relief='sunken',bd=2).place(x=5,y=10)
frame1_2=Frame(General,width=310,height=90,bg=d_color['framebg'],relief='sunken',bd=2).place(x=572,y=18)
frame1_3=Frame(General,width=386,height=229,bg=d_color['framebg'],relief='sunken',bd=2).place(x=5,y=161)
frame1_4=Frame(General,width=386,height=229,bg=d_color['framebg'],relief='sunken',bd=2).place(x=5,y=439)


etiq1_1=Label(General,text='RESUMEN GENERAL DEL PROYECTO',  padx=10,pady=9,bg='gray60').place(x=7,y=12)


button_importg=Button(General,text='IMPORTAR',width=13,height=5,bg='steelblue4',command=importar).place(x=574,y=20)
button_pbig=Button(General,text='EXP. POWER BI',width=13,height=5,bg=d_color['buttonbg'],command=pbi).place(x=677,y=20)
button_pintg=Button(General,text='EXP. TEKLA',width=13,height=5,bg=d_color['buttonbg'],command=pintadog).place(x=780,y=20)

labelinfa0 = Label(General, text='  Total:', bg='gray60').place(x=15, y=42)
labelinfa1 = Label(General, text=' Pond:', bg='gray60').place(x=15, y=64)
labelinfa2 = Label(General, text='   Brut:', bg='gray60').place(x=15, y=86)
labelinfa3 = Label(General, text=' Pond% :', bg='gray60').place(x=130, y=64)
labelinfa4 = Label(General, text='   Brut% :', bg='gray60').place(x=130, y=86)

etiq1_6=Label(General,text='Resumen por Fecha',  padx=10,pady=5,bg=d_color['fondobg']).place(x=1,y=132)
etiq1_7=Label(General,text='Resumen por ESP',  padx=10,pady=5,bg=d_color['fondobg']).place(x=1,y=410)

'''
f = plt.Figure(figsize=(5, 3), dpi=100)
ax = f.subplots()
canvas = FigureCanvasTkAgg(f, General)
canvas.get_tk_widget().place(x=410, y=120)
'''


fig=Figure(figsize=(5,3),dpi=93)
myPlot=fig.add_subplot(111)
myPlot.set_facecolor('#BDBDBD')
fig.patch.set_facecolor('#BDBDBD')

canvas=FigureCanvasTkAgg(fig,master=General)
canvas.get_tk_widget().place(x=410,y=115)


fig1=Figure(figsize=(5,3),dpi=93)
myPlot1=fig1.add_subplot(111)
myPlot1.set_facecolor('#BDBDBD')
fig1.patch.set_facecolor('#BDBDBD')

canvas1=FigureCanvasTkAgg(fig1,master=General)
canvas1.get_tk_widget().place(x=410,y=400)















######################################################detalle###########################################################VENTANA DETALLE


def filtrar():
    global df, matrix

    fechain = pd.to_datetime(efechai.get())
    fechaout=pd.to_datetime(efechaf.get())

    ################################################INFI GENERAL                                                           #FILTRAR GENERAL

    animat=matrix

    animat['filtro'] = np.where((qui1.get() == 1) & (animat['Etapa'] == "1-Traslado"),"positivo",'')     #APLICA FILTRO FECHA
    filtro1=animat[animat['filtro']=='positivo']
    animat['filtro'] = np.where((qui2.get() == 1) & (animat['Etapa'] == "2-Ensamble"), "positivo", '')
    filtro2=animat[animat['filtro']=='positivo']
    animat['filtro'] = np.where((qui3.get() == 1) & (animat['Etapa'] == "3-Montaje"), "positivo", '')
    filtro3=animat[animat['filtro']=='positivo']
    animat['filtro'] = np.where((qui4.get() == 1) & (animat['Etapa'] == "4-Alineamiento"), "positivo", '')
    filtro4=animat[animat['filtro']=='positivo']
    animat['filtro'] = np.where((qui4.get() == 1) & (animat['Etapa'] == "5-Touch Up"), "positivo", '')
    filtro5=animat[animat['filtro']=='positivo']
    animat['filtro'] = np.where((qui4.get() == 1) & (animat['Etapa'] == "6-Punch List"), "positivo", '')
    filtro6=animat[animat['filtro']=='positivo']

    animatrix = pd.concat([filtro1,filtro2,filtro3,filtro4,filtro5,filtro6], axis=0)



    animatrix2 = animatrix[(animatrix['Fecha'] >= fechain) & (animatrix['Fecha'] <= fechaout)]

    dfmat=df

    dfmat['filtro1'] = np.where((qui1.get() == 1), dfmat['TOTAL_WTR'],0)     #APLICA FILTRO FECHA
    dfmat['filtro2'] = np.where((qui2.get() == 1), dfmat['TOTAL_WPA'],0)
    dfmat['filtro3'] = np.where((qui3.get() == 1), dfmat['TOTAL_WMO'],0)
    dfmat['filtro4'] = np.where((qui4.get() == 1), dfmat['TOTAL_WNI'],0)
    dfmat['filtro5'] = np.where((qui5.get() == 1), dfmat['TOTAL_WPI'],0)
    dfmat['filtro6'] = np.where((qui6.get() == 1), dfmat['TOTAL_WPU'],0)

    sum_proyf=(dfmat['filtro1'].sum()+dfmat['filtro2'].sum()+dfmat['filtro3'].sum()+dfmat['filtro4'].sum()+
               dfmat['filtro5'].sum()+dfmat['filtro6'].sum())/1000

    wpond_proyf=round((animatrix['WPOND'].sum())/1000,0)
    porcwpon_proyf=round(wpond_proyf/sum_proyf*100,2)

    labelinf20 = Label(Detalle,text=round(sum_proyf,0),bg='gray60').place(x=55,y=42)
    labelinf21 = Label(Detalle, text=wpond_proyf, bg='gray60').place(x=55, y=64)
    labelinf23 = Label(Detalle, text=porcwpon_proyf, bg='gray60').place(x=190, y=64)


    ################################FILTRAR################################                                             #SELECCION MONTAJE DIARIO

    infdia=animatrix2.groupby(['Fecha'])
    pondia=infdia['WPOND'].sum()/1000
    matrixtemp=animatrix2[animatrix2.Etapa=='3-Montaje']
    matrixtemp['WBRUTO']=matrixtemp['WPOND'].div(d_pon['MO']*1000)
    infodiab=matrixtemp.groupby(['Fecha'])
    brutdia=infodiab['WBRUTO'].sum()

    label2=pd.concat([pondia,brutdia],axis=1)
    label2['FECHA'] = label2.index
    label2=label2[['FECHA','WPOND','WBRUTO']]
    label2['FECHA'] = label2["FECHA"].dt.strftime("%m/%d/%y")


    label2['WPACUM'] = label2.WPOND.cumsum()
    label2['WBACUM'] = label2.WBRUTO.cumsum()
    label2=label2.fillna(method='ffill')
    label2=label2.round(2)

    tree = ttk.Treeview(Detalle)
    tree.place(x=7, y=300)
    tree['column'] = list(label2.columns)
    tree['show'] = 'headings'
    #loop trhu column
    for column in tree['column']:
        tree.heading(column,text=column)

    df_rows=label2.to_numpy().tolist()
    for row in df_rows:
        tree.insert("","end",values=row)
    tree.place(x=7,y=162)

    tree.column("#1", width=89, minwidth=89, stretch=tk.NO)
    tree.column("#2", width=65, minwidth=65,stretch=tk.NO)
    tree.column("#3", width=68, minwidth=68, stretch=tk.NO)
    tree.column("#4", width=79, minwidth=79, stretch=tk.NO)
    tree.column("#5", width=79, minwidth=79, stretch=tk.NO)

    ######################################frame 3#################                                                      #SELECCION POR ESP

    espinfo=df.groupby(['ESP'])
    espresum=espinfo['WEIGHT'].sum()/1000
    esppon=animatrix2.groupby(['ESP'])
    esppond=esppon['WPOND'].sum()/1000
    matrixesp = matrixtemp.groupby(['ESP'])
    espbruto = matrixesp['WBRUTO'].sum()

    label3=pd.concat([espresum,esppond,espbruto],axis=1,ignore_index=True)

    label3['ESP_N'] = label3.index
    label3.reset_index(drop=True, inplace=True)
    np_array=label3.to_numpy()
    label3=pd.DataFrame(data=np_array,columns=['TOTAL','WPOND','WBRUTO','ESP'])

    label3=label3[['ESP','TOTAL','WPOND','WBRUTO']]



    label3['WPOND%']=label3.WPOND/label3.TOTAL*100
    label3['WBRUTO%'] = label3.WBRUTO / label3.TOTAL * 100

    label3=label3.fillna(0)
    label3=label3.round(2)

    tree2 = ttk.Treeview(Detalle)
    tree2.place(x=7, y=300)
    tree2['column'] = list(label3.columns)
    tree2['show'] = 'headings'
    #loop trhu column
    for column in tree2['column']:
        tree2.heading(column,text=column)

    df_rows=label3.to_numpy().tolist()
    for row in df_rows:
        tree2.insert("","end",values=row)
    tree2.place(x=7,y=440)

    tree2.column("#1", width=75, minwidth=75, stretch=tk.NO)
    tree2.column("#2", width=55, minwidth=55,stretch=tk.NO)
    tree2.column("#3", width=55, minwidth=55, stretch=tk.NO)
    tree2.column("#4", width=55, minwidth=55, stretch=tk.NO)
    tree2.column("#5", width=70, minwidth=70, stretch=tk.NO)
    tree2.column("#6", width=70, minwidth=70, stretch=tk.NO)

    labela=label2
    labelb=label3

    ##label resultados
    labelinfaa = Label(Detalle, text=round(pondia.sum(),2), bg='#BDBDBD').place(x=87, y=392)
    labelinfab = Label(Detalle, text=round(brutdia.sum(),2), bg='#BDBDBD').place(x=155, y=392)

    labelinfae = Label(Detalle, text=round(espresum.sum(),2), bg='#BDBDBD').place(x=80, y=670)
    labelinfaf = Label(Detalle, text=round(esppond.sum(),2), bg='#BDBDBD').place(x=138, y=670)
    labelinfag = Label(Detalle, text=round(espbruto.sum(),2), bg='#BDBDBD').place(x=192, y=670)

    desl1 = ttk.Scrollbar(Detalle, orient="vertical", command=tree.yview)
    desl1.place(x=372, y=163, height=225)
    tree.configure(yscrollcommand=desl1.set)

    desl2 = ttk.Scrollbar(Detalle, orient="vertical", command=tree2.yview)
    desl2.place(x=372, y=441, height=225)
    tree2.configure(yscrollcommand=desl2.set)

    #graficos                                                                                                           #graficso 2
    myPlot3.cla()
    myPlot3.plot(labela.FECHA,labela.WPACUM)
    myPlot3.plot(labela.FECHA, labela.WBACUM)
    canvas3.draw()

    myPlot4.cla()
    myPlot4.bar(labelb.ESP, labelb.WBRUTO, width=0.4,label='WBruto')
    myPlot4.bar(labelb.ESP,labelb.WPOND,width=0.2,label='WPond')
    canvas4.draw()









etiq2_3=Label(Detalle,text='Ingrese Fechas  (yyyy/mm/dd)',  padx=10,pady=9,bg=d_color['fondobg']).place(x=280,y=12)                  #Button Filtrar
etiq2_4=Label(Detalle,text='Inicio',  padx=10,pady=9,bg=d_color['fondobg']).place(x=280,y=40)
etiq2_5=Label(Detalle,text='Final',  padx=10,pady=9,bg=d_color['fondobg']).place(x=280,y=70)


efechai=Entry(Detalle)
efechai.place(x=330,y=50)
efechaf=Entry(Detalle)
efechaf.place(x=330,y=80)



frame2_1=Frame(Detalle,width=250,height=110,bg=d_color['framebg'],relief='sunken',bd=2).place(x=5,y=10)                 #RESUMEN GENERAL

frame2_2=Frame(Detalle,width=386,height=229,bg=d_color['framebg'],relief='sunken',bd=2).place(x=5,y=161)
frame2_3=Frame(Detalle,width=386,height=229,bg=d_color['framebg'],relief='sunken',bd=2).place(x=5,y=439)




etiq2_1=Label(Detalle,text='RESUMEN GENERAL DEL PROYECTO',  padx=10,pady=9,bg='gray60').place(x=7,y=12)
labelinfa02 = Label(Detalle, text='  Total:', bg='gray60').place(x=15, y=42)
labelinfa12 = Label(Detalle, text=' Pond:', bg='gray60').place(x=15, y=64)
labelinfa32 = Label(Detalle, text=' Pond% :', bg='gray60').place(x=130, y=64)

etiq2_6=Label(Detalle,text='Resumen por Fecha',  padx=10,pady=5,bg=d_color['fondobg']).place(x=1,y=132)
etiq2_7=Label(Detalle,text='Resumen por ESP',  padx=10,pady=5,bg=d_color['fondobg']).place(x=1,y=410)

##label para resultados

labelinfac = Label(Detalle, text='  Total:', bg=d_color['fondobg']).place(x=17, y=392)
labelinfad = Label(Detalle, text='  Total:', bg=d_color['fondobg']).place(x=17, y=670)
#labelinfah = Label(Detalle, text='  Total:', bg='gray60').place(x=244, y=670)
#labelinfai = Label(Detalle, text='  Total:', bg='gray60').place(x=312, y=670)




#etiq2_2=Label(Detalle,text='Selecciona los quiebres',  padx=10,pady=9,bg=d_color['labelbg']).place(x=600,y=12)           #CheckBook Quiebres
qui1=IntVar()
qui2=IntVar()
qui3=IntVar()
qui4=IntVar()
qui5=IntVar()
qui6=IntVar()
chekqu1=Checkbutton(Detalle,text='Traslado',variable=qui1,bg=d_color['fondobg'])
chekqu1.place(x=650,y=15)
chekqu2=Checkbutton(Detalle,text='Pre-Armado',variable=qui2,bg=d_color['fondobg'])
chekqu2.place(x=650,y=40)
chekqu3=Checkbutton(Detalle,text='Montaje',variable=qui3,bg=d_color['fondobg'])
chekqu3.place(x=650,y=65)
chekqu4=Checkbutton(Detalle,text='Nivelación',variable=qui4,bg=d_color['fondobg'])
chekqu4.place(x=780,y=15)
chekqu5=Checkbutton(Detalle,text='Touch-Up',variable=qui5,bg=d_color['fondobg'])
chekqu5.place(x=780,y=40)
chekqu6=Checkbutton(Detalle,text='Punch-Lis',variable=qui6,bg=d_color['fondobg'])
chekqu6.place(x=780,y=65)

presFilt=Button(Detalle,text='Filtrar',width=13,height=5,bg='steelblue4',command=filtrar).place(x=500,y=15)

fig3 = Figure(figsize=(5, 3), dpi=93)
myPlot3 = fig3.add_subplot(111)
myPlot3.set_facecolor('#BDBDBD')
fig3.patch.set_facecolor('#BDBDBD')

canvas3 = FigureCanvasTkAgg(fig3, master=Detalle)
canvas3.get_tk_widget().place(x=410, y=115)


fig4 = Figure(figsize=(5, 3), dpi=93)
myPlot4 = fig4.add_subplot(111)
myPlot4.set_facecolor('#BDBDBD')
fig4.patch.set_facecolor('#BDBDBD')

canvas4 = FigureCanvasTkAgg(fig4, master=Detalle)
canvas4.get_tk_widget().place(x=410, y=400)



root.mainloop()