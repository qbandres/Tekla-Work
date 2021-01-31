import numpy as np
import pandas as pd

#LECTURA Y CAMBIO DE NOMBRES A LAS COLUMNAS
df=pd.read_excel(r'C:\Users\qband\Documents\QBANDRES\WORK\QB2\CONSTRUCCION\REPORTE\Master210124.xlsx',
                 sheet_name='Reporte',skiprows=7)
df=df[['ID Tekla','ESP','Barcode','Peso Total (Kg)','Ratio','Traslado','Pre armado','Montaje',
       'Nivelacion, soldadura &Torque','Touch up','Punch list','Protocolo Torque']]

df.rename(columns={'ID Tekla': 'ID', 'Peso Total (Kg)': 'WEIGHT', 'Traslado': 'DTR','Pre armado': 'DPA',
                   'Montaje': 'DMO','Nivelacion, soldadura &Torque': 'DNI','Touch up':'DPI','Punch list':'DPU'},
          inplace=True)

#DEFINIR PONDERACIONES
d_pon={'TR':0.05,'PA':0.1,'MO':0.45,'NI':0.2,'PI':0.1,'PU':0.1}

df = df[df.Ratio.notnull()]     #LIMPIAMOS DATOS QUE ESTEN NULOS EN EL RATIO
df = df[df.WEIGHT.notnull()]    #LIMPIAMOS LOS DATOS QUE ESTEN NULOS EN EL PESO

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
df_dtr=df[["ESP", "ID", "WEIGHT", "Ratio", "DTR", "WTR", "ETR"]]
df_dtr=df_dtr.dropna(subset=['DTR']) #Elimina llas filas vacias de DTR
df_dtr["Etapa"]= "1-Traslado"
df_dtr=df_dtr.rename(columns={'WTR': 'WPOND', "DTR": 'Fecha', 'ETR': 'HGan'})

df_dpa=df[["ESP", "ID", "WEIGHT", "Ratio", "DPA", "WPA", "EPA"]]
df_dpa=df_dpa.dropna(subset=['DPA'])
df_dpa["Etapa"]= "2-Ensamble"
df_dpa=df_dpa.rename(columns={'WPA': 'WPOND', "DPA": 'Fecha', 'EPA': 'HGan'})

df_dmo=df[["ESP", "ID", "WEIGHT", "Ratio", "DMO", "WMO", "EMO"]]
df_dmo=df_dmo.dropna(subset=['DMO'])
df_dmo["Etapa"]= "3-Montaje"
df_dmo=df_dmo.rename(columns={'WMO': 'WPOND', "DMO": 'Fecha', 'EMO': 'HGan'})

df_dni=df[["ESP", "ID","WEIGHT", "Ratio", "DNI", "WNI", "ENI"]]
df_dni=df_dni.dropna(subset=['DNI'])
df_dni["Etapa"]= "4-Alineamiento"
df_dni=df_dni.rename(columns={'WNI': 'WPOND', "DNI": 'Fecha', 'ENI': 'HGan'})

df_dpi=df[["ESP", "ID","WEIGHT", "Ratio", "DPI", "WPI", "EPI"]]
df_dpi=df_dpi.dropna(subset=['DPI'])
df_dpi["Etapa"]= "5-Touch Up"
df_dpi=df_dpi.rename(columns={'WPI': 'WPOND', "DPI": 'Fecha', 'EPI': 'HGan'})

df_dpu=df[["ESP", "ID", "WEIGHT", "Ratio", "DPU", "WPU", "EPU"]]
df_dpu=df_dpu.dropna(subset=['DPU'])
df_dpu["Etapa"]= "6-Punch List"
df_dpu=df_dpu.rename(columns={'WPU': 'WPOND', "DPU": 'Fecha', 'EPU': 'HGan'})

##CONCATENAR VERTICAL DE LAS COLUMNAS DE RESUMEN

matrix = pd.concat([df_dtr.round(1), df_dpa.round(1), df_dmo.round(1), df_dni.round(1), df_dpi.round(1), df_dpu.round(1)], axis=0)
#matrix_br=matrix[matrix['Etapa']=='3-Montaje']

d_color={'1-Traslado':'green','2-Ensamble':'gray','3-Montaje':'#00aae4','4-Alineamiento':'#FF0000',
         '5-Touch Up':'#9E19CF','6-Punch List':'#D4CE4D'}

#Asignar valores a una columna según diccionario
matrix['color']=matrix['Etapa'].map(d_color)

##CREAMOS LAS CARPETAS PARA TEKLA
pint_dtr=df[['ID','DTR']].dropna()
pint_dtr['USER_FIELD_1']='DTR'
pint_dtr=pint_dtr[['ID','USER_FIELD_1']]

pint_dpa=df[['ID','DPA']].dropna()
pint_dpa['USER_FIELD_1']='DPA'
pint_dpa=pint_dpa[['ID','USER_FIELD_1']]

pint_dmo=df[['ID','DMO']].dropna()
pint_dmo['USER_FIELD_1']='DMO'
pint_dmo=pint_dmo[['ID','USER_FIELD_1']]

pint_dni=df[['ID','DNI']].dropna()
pint_dni['USER_FIELD_1']='DNI'
pint_dni=pint_dni[['ID','USER_FIELD_1']]

pint_dpi=df[['ID','DPI']].dropna()
pint_dpi['USER_FIELD_1']='DPI'
pint_dpi=pint_dpi[['ID','USER_FIELD_1']]

pint_dpu=df[['ID','DPU']].dropna()
pint_dpu['USER_FIELD_1']='DPU'
pint_dpu=pint_dpu[['ID','USER_FIELD_1']]

pint_dtrdmo=df[['ID','DTR','DMO']]
pint_dtrdmo=pint_dtrdmo.dropna(subset=['DTR','ID'])  #FILTRAR LOS VACIOS DE DTR Y ID

pint_dtrdmo.DMO=pint_dtrdmo.DMO.isnull()
pint_dtrdmo=pint_dtrdmo[pint_dtrdmo.DMO==True]
pint_dtrdmo['USER_FIELD_1']='SALD'
pint_dtrdmo=pint_dtrdmo[['ID','USER_FIELD_1']]


df.to_csv('base.csv')
matrix.to_csv('base_powerbi.csv')

#Exportar para tekla
pint_dtr.to_csv(r'C:\Users\qband\Desktop\Report_Tekla\dtr_tekla.csv',index=False)
pint_dpa.to_csv(r'C:\Users\qband\Desktop\Report_Tekla\dpa_tekla.csv',index=False)
pint_dmo.to_csv(r'C:\Users\qband\Desktop\Report_Tekla\dmo_tekla.csv',index=False)
pint_dni.to_csv(r'C:\Users\qband\Desktop\Report_Tekla\dni_tekla.csv',index=False)
pint_dpi.to_csv(r'C:\Users\qband\Desktop\Report_Tekla\dpi_tekla.csv',index=False)
pint_dpu.to_csv(r'C:\Users\qband\Desktop\Report_Tekla\dpu_tekla.csv',index=False)
pint_dtrdmo.to_csv(r'C:\Users\qband\Desktop\Report_Tekla\dtrdtmo_tekla.csv',index=False)