from tkinter import *
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import ttk
import numpy as np
from tkcalendar import*
import plotly.graph_objects as go
import plotly.offline as po


#LECTURA Y CAMBIO DE NOMBRES A LAS COLUMNAS

root=Tk()
root.title('GESTION DE RESULTADOS PROYECTO QB2')
root.configure(bg="#BDBDBD")
root.geometry('740x755')  #Definir el tamaño de celda
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
General=ttk.Frame(nb, style='TLabelframe')
Regre=ttk.Frame(nb,style='TLabelframe')
nb.add(General, text='General')
nb.add(Regre,text='Proyección')





################################General##################################################################################
def importar():

    global df, matrix, d_color,datafiltro,df_dtr, df_dpa,df_dmo, df_dni,df_dpi,df_dpu

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

    datafiltro = df

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
    df_dtr = df[["ESP", "ID",'Barcode', "WEIGHT", "Ratio", "DTR", "WTR", "ETR"]]
    df_dtr = df_dtr.dropna(subset=['DTR'])  # Elimina llas filas vacias de DTR
    df_dtr["Etapa"] = "1-Traslado"
    df_dtr = df_dtr.rename(columns={'WTR': 'WPOND', "DTR": 'Fecha', 'ETR': 'HGan'})

    df_dpa = df[["ESP", "ID",'Barcode', "WEIGHT", "Ratio", "DPA", "WPA", "EPA"]]
    df_dpa = df_dpa.dropna(subset=['DPA'])
    df_dpa["Etapa"] = "2-Ensamble"
    df_dpa = df_dpa.rename(columns={'WPA': 'WPOND', "DPA": 'Fecha', 'EPA': 'HGan'})

    df_dmo = df[["ESP", "ID",'Barcode', "WEIGHT", "Ratio", "DMO", "WMO", "EMO"]]
    df_dmo = df_dmo.dropna(subset=['DMO'])
    df_dmo["Etapa"] = "3-Montaje"
    df_dmo = df_dmo.rename(columns={'WMO': 'WPOND', "DMO": 'Fecha', 'EMO': 'HGan'})

    df_dni = df[["ESP", "ID",'Barcode', "WEIGHT", "Ratio", "DNI", "WNI", "ENI"]]
    df_dni = df_dni.dropna(subset=['DNI'])
    df_dni["Etapa"] = "4-Alineamiento"
    df_dni = df_dni.rename(columns={'WNI': 'WPOND', "DNI": 'Fecha', 'ENI': 'HGan'})

    df_dpi = df[["ESP", "ID",'Barcode', "WEIGHT", "Ratio", "DPI", "WPI", "EPI"]]
    df_dpi = df_dpi.dropna(subset=['DPI'])
    df_dpi["Etapa"] = "5-Touch Up"
    df_dpi = df_dpi.rename(columns={'WPI': 'WPOND', "DPI": 'Fecha', 'EPI': 'HGan'})

    df_dpu = df[["ESP", "ID",'Barcode', "WEIGHT", "Ratio", "DPU", "WPU", "EPU"]]
    df_dpu = df_dpu.dropna(subset=['DPU'])
    df_dpu["Etapa"] = "6-Punch List"
    df_dpu = df_dpu.rename(columns={'WPU': 'WPOND', "DPU": 'Fecha', 'EPU': 'HGan'})

    ##CONCATENAR VERTICAL DE LAS COLUMNAS DE RESUMEN

    matrix = pd.concat(
        [df_dtr.round(1), df_dpa.round(1), df_dmo.round(1), df_dni.round(1), df_dpi.round(1), df_dpu.round(1)], axis=0)

    matrix['WBRUTO'] = np.where(matrix.Etapa!='3-Montaje', 0, matrix.WEIGHT)

    np_array=matrix.to_numpy()

    matrix=pd.DataFrame(data=np_array,columns=['ESP','ID','Barcode','WEIGHT','Ratio','Fecha','WPOND','HGan','Etapa','WBRUTO'])
    matrix["Fecha"] = pd.to_datetime(matrix.Fecha).dt.date


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

    ################################################################DETALLE##############################################

def pbi1():                                                                                                              #FUNCION EXPORTAR PARA PBI
    global df, matrix

    dfpbi=df[['ID','Barcode','WEIGHT','DTR','DPA','DMO','DNI','DPI','DPU','WTR','WPA','WMO','WNI','WPI','WPU']]

    export_file= filedialog.askdirectory()
    dfpbi.to_csv(export_file+'/Matriz.csv',index=False)
    matrix.to_csv(export_file + '/QB_PBI.csv', header=True, index=False)

######################################################detalle###########################################################VENTANA DETALLE


def filtrar():

    global animatrix2, info1, info2, info3, Nsemana

    efechai = pd.to_datetime(fechai.get())
    efechaf=pd.to_datetime(fechaf.get())

    ################################################INFI GENERAL                                                           #FILTRAR GENERAL

    animat=matrix

    animat['filtro'] = np.where((qui1.get() == 1) & (animat['Etapa'] == "1-Traslado"),"positivo",'')                    #APLICA FILTRO DE QUIEBRE
    filtro1=animat[animat['filtro']=='positivo']
    animat['filtro'] = np.where((qui2.get() == 1) & (animat['Etapa'] == "2-Ensamble"), "positivo", '')
    filtro2=animat[animat['filtro']=='positivo']
    animat['filtro'] = np.where((qui3.get() == 1) & (animat['Etapa'] == "3-Montaje"), "positivo", '')
    filtro3=animat[animat['filtro']=='positivo']
    animat['filtro'] = np.where((qui4.get() == 1) & (animat['Etapa'] == "4-Alineamiento"), "positivo", '')
    filtro4=animat[animat['filtro']=='positivo']
    animat['filtro'] = np.where((qui5.get() == 1) & (animat['Etapa'] == "5-Touch Up"), "positivo", '')
    filtro5=animat[animat['filtro']=='positivo']
    animat['filtro'] = np.where((qui6.get() == 1) & (animat['Etapa'] == "6-Punch List"), "positivo", '')
    filtro6=animat[animat['filtro']=='positivo']

    animatrix2 = pd.concat([filtro1,filtro2,filtro3,filtro4,filtro5,filtro6], axis=0)

    animatrix2 = animatrix2[(animatrix2['Fecha'] >= efechai ) & (animatrix2['Fecha'] <= efechaf)]                          #SELECCION MONTAJE DIARIO

    animatrix=animatrix2[['Fecha','WPOND','WBRUTO']]
    info1=animatrix.groupby(['Fecha']).sum()/1000         #crea el label2
    info1['WPACUM']=info1['WPOND'].cumsum()
    info1['WBACUM'] = info1['WBRUTO'].cumsum()
    info1.reset_index(inplace=True)

    info1=info1.round(2)
    info1.fillna(0, inplace=True)

    tree = ttk.Treeview(General)
    tree.place(x=7, y=300)
    tree['column'] = list(info1.columns)
    tree['show'] = 'headings'
    #loop trhu column
    for column in tree['column']:
        tree.heading(column,text=column)

    df_rows=info1.to_numpy().tolist()
    for row in df_rows:
        tree.insert("","end",values=row)
    tree.place(x=7,y=162)

    tree.column("#1", width=89, minwidth=89, stretch=tk.NO)
    tree.column("#2", width=65, minwidth=65,stretch=tk.NO)
    tree.column("#3", width=68, minwidth=68, stretch=tk.NO)
    tree.column("#4", width=79, minwidth=79, stretch=tk.NO)
    tree.column("#5", width=79, minwidth=79, stretch=tk.NO)

    ######################################frame 3#################                                                      #SELECCION POR ESP

    animatrix1 = animatrix2[['ESP', 'WPOND', 'WBRUTO']]
    labelp=animatrix1.groupby(['ESP']).sum()/1000
    labelp.reset_index(inplace=True)

    espinfo=df[['ESP','WEIGHT']]
    espresum=espinfo.groupby(['ESP']).sum()/1000

    labelp.set_index('ESP', inplace = True)

    info2=pd.concat([espresum,labelp],axis=1)      #creas el label3
    info2.rename(columns={'WEIGHT': 'Total'},inplace=True)


    info2['Pond%']=info2.WPOND/info2.Total*100
    info2['Bruto%'] = info2.WBRUTO / info2.Total * 100
    info2.reset_index(inplace=True)
    info2=info2.round(2)
    info2.fillna(0,inplace=True)

    tree2 = ttk.Treeview(General)
    tree2.place(x=7, y=300)
    tree2['column'] = list(info2.columns)
    tree2['show'] = 'headings'
    #loop trhu column
    for column in tree2['column']:
        tree2.heading(column,text=column)

    df_rows1=info2.to_numpy().tolist()
    for row in df_rows1:
        tree2.insert("","end",values=row)
    tree2.place(x=7,y=440)

    tree2.column("#1", width=75, minwidth=75, stretch=tk.NO)
    tree2.column("#2", width=55, minwidth=55,stretch=tk.NO)
    tree2.column("#3", width=55, minwidth=55, stretch=tk.NO)
    tree2.column("#4", width=55, minwidth=55, stretch=tk.NO)
    tree2.column("#5", width=70, minwidth=70, stretch=tk.NO)
    tree2.column("#6", width=70, minwidth=70, stretch=tk.NO)

    ##label resultados
    labelinfaa = Label(General, text=round(info1['WPOND'].sum(), 2), bg='#BDBDBD').place(x=87, y=392)
    labelinfab = Label(General, text=round(info1['WBRUTO'].sum(), 2), bg='#BDBDBD').place(x=155, y=392)

    labelinfae = Label(General, text=round(info2['Total'].sum(), 2), bg='#BDBDBD').place(x=80, y=670)
    labelinfaf = Label(General, text=round(info2['WPOND'].sum(), 2), bg='#BDBDBD').place(x=138, y=670)
    labelinfag = Label(General, text=round(info2['WBRUTO'].sum(), 2), bg='#BDBDBD').place(x=192, y=670)
    #####################SEMANA

    #####CREAR DF NRO SEMANA#######
    s = pd.date_range(start='2019-04-12', periods=1200, freq='D')
    Nsemana = pd.DataFrame(s, columns=['Fecha'])
    Nsemana['SEMANA'] = Nsemana.index
    Nsemana["Fecha"] = pd.to_datetime(Nsemana.Fecha).dt.date
    Nsemana.set_index('Fecha', inplace=True)
    Nsemana['Semana'] = Nsemana.SEMANA // 7 + 1
    del Nsemana['SEMANA']

    animatrix0=info1[['Fecha','WPOND','WBRUTO']]
    animatrix0.set_index('Fecha', inplace = True)

    filtro_sem=pd.concat([Nsemana,animatrix0],axis=1)   #Juntamos la nueva matriz con la del montaje diario


    info3=filtro_sem.groupby(['Semana']).sum()        #Agrupamod por Semana
    info3=info3[(info3['WPOND'] != 0) | (info3['WBRUTO'] != 0)]  #Limpiamos la matriz de los ceros
    info3.reset_index(inplace=True)
    info3=info3.round(2)


    tree3 = ttk.Treeview(General)
    tree3.pack()
    tree3['column'] = list(info3.columns)
    tree3['show'] = 'headings'
    # loop trhu column
    for column in tree3['column']:
        tree3.heading(column, text=column)

    df_rows3 = info3.to_numpy().tolist()
    for row in df_rows3:
        tree3.insert("", "end", values=row)
    tree3.place(x=494, y=440)

    tree3.column("#1", width=75, minwidth=75, stretch=tk.NO)
    tree3.column("#2", width=70, minwidth=70, stretch=tk.NO)
    tree3.column("#3", width=70, minwidth=70, stretch=tk.NO)

    desl1 = ttk.Scrollbar(General, orient="vertical", command=tree.yview)
    desl1.place(x=389, y=163, height=225)
    tree.configure(yscrollcommand=desl1.set)

    desl2 = ttk.Scrollbar(General, orient="vertical", command=tree2.yview)
    desl2.place(x=381, y=441, height=225)
    tree2.configure(yscrollcommand=desl2.set)

    desl3 = ttk.Scrollbar(General, orient="vertical", command=tree3.yview)
    desl3.place(x=710, y=441, height=225)
    tree3.configure(yscrollcommand=desl3.set)



def reporte():                                                                                                              #FUNCION EXPORTAR PARA PBI
    global animatrix2,info1,info2,info3, Nsemana

    yminfo1=info1[['Fecha','WPOND','WBRUTO']]
    yminfo1['Year_month'] = pd.to_datetime(yminfo1['Fecha']).dt.to_period('M')  # get month an year

    filtro_mes=yminfo1.groupby(['Year_month']).sum()
    filtro_mes.reset_index(inplace=True)

    export_file= filedialog.askdirectory()                              #Buscamos el directorio para gruafar

    #Creamos una excel y le indicamos la ruta
    writer = pd.ExcelWriter(export_file + '/' + 'Reporte.xlsx')

    # Write each dataframe to a different worksheet.
    animatrix2.to_excel(writer, sheet_name='General',index=True)
    info1.to_excel(writer, sheet_name='Dia',index=False)
    filtro_mes.to_excel(writer, sheet_name='Mes',index=False)
    info3.to_excel(writer, sheet_name='Semana')
    info2.to_excel(writer, sheet_name='ESP')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

def pintadog2():                                                                                                         #FUNCION EXPORTAR PARA PINTAR
    global animatrix2

    pintado=animatrix2[['ID','Etapa']]

    pint_dtr = pintado[pintado.Etapa == '1-Traslado']
    pint_dtr['USER_FIELD_1'] = 'dtr_'+euser.get()
    del pint_dtr['Etapa']


    pint_dpa = pintado[pintado.Etapa == '2-Ensamble']
    pint_dpa['USER_FIELD_1'] = 'dpa_' + euser.get()
    del pint_dpa['Etapa']

    pint_dmo = pintado[pintado.Etapa == '3-Montaje']
    pint_dmo['USER_FIELD_1'] = 'dmo_' + euser.get()
    del pint_dmo['Etapa']

    pint_dni = pintado[pintado.Etapa == '4-Alineamiento']
    pint_dni['USER_FIELD_1'] = 'dtr_' + euser.get()
    del pint_dni['Etapa']

    pint_dpi = pintado[pintado.Etapa == '5-Touch Up']
    pint_dpi['USER_FIELD_1'] = 'dpi_' + euser.get()
    del pint_dpi['Etapa']

    pint_dpu = pintado[pintado.Etapa == '6-Punch List']
    pint_dpu['USER_FIELD_1'] = 'dpu_' + euser.get()
    del pint_dpu['Etapa']

    export_file= filedialog.askdirectory()

    # Exportar para tekla
    pint_dtr.to_csv(export_file+'/dtr_tekla.csv', index=False)
    pint_dpa.to_csv(export_file+'/dpa_tekla.csv', index=False)
    pint_dmo.to_csv(export_file+'/dmo_tekla.csv', index=False)
    pint_dni.to_csv(export_file+'/dni_tekla.csv', index=False)
    pint_dpi.to_csv(export_file+'/dpi_tekla.csv', index=False)
    pint_dpu.to_csv(export_file+'/dpu_tekla.csv', index=False)


def graficos():
    global animatrix2, info1, info2, info3

    if combo.get()=="Montaje Diario":

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=info1.Fecha, y=info1.WPOND,
                                 mode='lines+markers',
                                 name='lines+markers'))
        fig.add_trace(go.Scatter(x=info1.Fecha, y=info1.WBRUTO,
                                 mode='lines+markers',
                                 name='lines+markers'))

        fig.show()


    elif combo.get()=="Montaje Semanal":

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=info3.Semana, y=info3.WPOND,
                                 mode='lines+markers',
                                 name='lines+markers'))
        fig.add_trace(go.Scatter(x=info3.Semana, y=info3.WBRUTO,
                                 mode='lines+markers',
                                 name='lines+markers'))

        fig.show()

    elif combo.get()=='Montaje Diario Acumulado':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=info1.Fecha, y=info1.WPACUM,
                                 mode='lines+markers',
                                 name='lines+markers'))
        fig.add_trace(go.Scatter(x=info1.Fecha, y=info1.WBACUM,
                                 mode='lines+markers',
                                 name='lines+markers'))
        fig.show()



    elif combo.get() == "Montaje por ESP":
        fig = go.Figure(data=[
            go.Bar(name='Montaje Ponderado', x=info2.ESP, y=info2.WPOND),
            go.Bar(name='Montaje Bruto', x=info2.ESP, y=info2.WBRUTO),
            go.Bar(name='Total', x=info2.ESP, y=info2.Total)
        ])
        # Change the bar mode
        fig.update_layout(barmode='group', xaxis_tickangle=-45)
        fig.show()

    elif combo.get()=='Por Quiebre':

        import plotly.express as px
        fig = px.area(animatrix2, x="Fecha", y="WPOND", color="Etapa")
        fig.show()


########################################################################################################################button importar
frameresumen=Frame(General, width=250, height=116, bg=d_color['framebg'], relief='sunken', bd=2).place(x=5, y=10)
etiq1_1=Label(General, text='RESUMEN GENERAL DEL PROYECTO', padx=10, pady=9, bg='gray60').place(x=7, y=12)


labelinfa0 = Label(General, text='  Total:', bg='gray60').place(x=15, y=42)
labelinfa1 = Label(General, text=' Pond:', bg='gray60').place(x=15, y=64)
labelinfa2 = Label(General, text='   Brut:', bg='gray60').place(x=15, y=86)
labelinfa3 = Label(General, text=' Pond% :', bg='gray60').place(x=130, y=64)
labelinfa4 = Label(General, text='   Brut% :', bg='gray60').place(x=130, y=86)


button_importg=Button(General, text='IMPORTAR', width=18, height=7, bg='steelblue4', command=importar).place(x=260, y=9)
button_importg2=Button(General, text='FILTRAR', width=13, height=7, bg='steelblue4', command=filtrar).place(x=428, y=10)
button_pbig2=Button(General, text='REPORTE', width=13, height=3, bg=d_color['buttonbg'], command=reporte).place(x=532, y=10)
button_pbig=Button(General, text='POWER BI', width=12, height=3, bg=d_color['buttonbg'], command=pbi1).place(x=634, y=10)
button_grafico=Button(General, text='VER GRAFICO', width=12, height=3, bg=d_color['buttonbg'], command=graficos).place(x=634, y=200)


button_pintg2=Button(General, text='EXP. TEKLA', width=27, height=3, bg=d_color['buttonbg'], command=pintadog2).place(x=531, y=68)

def on_click(event):
    euser.config(state=NORMAL)
    euser.delete(0,END)

euser=Entry(General, width=30)
euser.insert(0,'USER_FIELD')
euser.config(state=DISABLED)
euser.bind('<Button-1>',on_click)
euser.place(x=532,y=132)


#etiq2_3=Label(General, text='Ingrese Fechas', padx=10, pady=9, bg=d_color['fondobg']).place(x=430, y=312)                    #Button Filtrar
etiq2_4=Label(General, text='Inicio', padx=10, pady=9, bg=d_color['fondobg']).place(x=405, y=340)
etiq2_5=Label(General, text='Final', padx=10, pady=9, bg=d_color['fondobg']).place(x=405, y=370)

fechai=DateEntry(General, width=20, bg='blue', date_pattern='yyyy/MM/dd', year=2019, month=10, day=1)
fechai.place(x=455,y=350)

fechaf=DateEntry(General, width=20, bg='blue', date_pattern='yyyy/MM/dd', year=2021, month=2, day=28)
fechaf.place(x=455,y=380)
                                                                                                                     #RESUMEN GENERAL
frame2_2=Frame(General, width=395, height=229, bg=d_color['framebg'], relief='sunken', bd=2).place(x=5, y=161)
frame2_3=Frame(General, width=395, height=229, bg=d_color['framebg'], relief='sunken', bd=2).place(x=5, y=439)
frame2_4=Frame(General, width=236, height=229, bg=d_color['framebg'], relief='sunken', bd=2).place(x=493, y=439)


etiq2_6=Label(General, text='Resumen por Fecha', padx=10, pady=5, bg=d_color['fondobg']).place(x=0, y=132)
etiq2_7=Label(General, text='Resumen por ESP', padx=10, pady=5, bg=d_color['fondobg']).place(x=0, y=410)
etiq2_8=Label(General, text='Resumen por Semana', padx=10, pady=5, bg=d_color['fondobg']).place(x=410, y=410)

##label para resultados

labelinfac = Label(General, text='  Total:', bg=d_color['fondobg']).place(x=17, y=392)
labelinfad = Label(General, text='  Total:', bg=d_color['fondobg']).place(x=17, y=670)

qui1=IntVar(value=1)
qui2=IntVar(value=1)
qui3=IntVar(value=1)
qui4=IntVar(value=1)
qui5=IntVar(value=1)
qui6=IntVar(value=1)
chekqu1=Checkbutton(General, text='Traslado', variable=qui1, bg=d_color['fondobg'])
chekqu1.place(x=412,y=170)
chekqu2=Checkbutton(General, text='Pre-Armado', variable=qui2, bg=d_color['fondobg'])
chekqu2.place(x=412,y=195)
chekqu3=Checkbutton(General, text='Montaje', variable=qui3, bg=d_color['fondobg'])
chekqu3.place(x=412,y=220)
chekqu4=Checkbutton(General, text='Nivelación', variable=qui4, bg=d_color['fondobg'])
chekqu4.place(x=412,y=245)
chekqu5=Checkbutton(General, text='Touch-Up', variable=qui5, bg=d_color['fondobg'])
chekqu5.place(x=412,y=270)
chekqu6=Checkbutton(General, text='Punch-Lis', variable=qui6, bg=d_color['fondobg'])
chekqu6.place(x=412,y=295)

###combo box
combo = ttk.Combobox(General, state="readonly")
combo.place(x=570,y=280)
combo["values"] = ["Montaje Diario", "Montaje Semanal", "Montaje por ESP",'Montaje Diario Acumulado','Por Quiebre']
combo.current(0)


root.mainloop()