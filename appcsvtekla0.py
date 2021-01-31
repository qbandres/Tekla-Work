from tkinter import *
from tkinter import filedialog
import pandas as pd
from pandastable import Table, TableModel
from glob import glob  ##para juntar los cvs


root=Tk()
root.title('GESTION DE ARCHIVOS TEKLA')
root.configure(bg="gray69")
root.geometry('344x200')  #Definir el tamaño de celda


def getCSV():
    global df

    import_file_path = filedialog.askopenfilename()
    df = pd.read_csv(import_file_path, skiprows = 2,
                     names = ['ID', 'PIECEMARK', 'BARCODE', 'ESP', 'PROFILE', 'DESCRIPTION', 'QUANTITY', 'WEIGHT'])
    return print(df)


def exportXLS():
    global df

    export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
    df.to_excel(export_file_path, header=True)

def exportCSV():
    global df

    df['USER_FIELD_1'] = e.get()
    df1 = df[['ID', 'USER_FIELD_1']]
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df1.to_csv(export_file_path, index=False, header=True)

def visualizar():
    global df
    frame = Toplevel()
    pt = Table(frame,dataframe=df)
    pt.show()

def ver():
    global df
    frame1 = Toplevel()
    df['USER_FIELD_1'] = e.get()
    df1 = df[['ID', 'USER_FIELD_1']]
    pt = Table(frame1,dataframe=df1)
    pt.show()

def jointexcel():
    global df

    import_file_path = filedialog.askopenfilename(multiple=True)
    matrix = pd.concat((pd.read_excel(file).assign(filename=file) for file in import_file_path), ignore_index=True, )
    del matrix['filename']

    matrix = matrix.rename(columns={'Unnamed: 0': 'Item'})
    matrix.Item=matrix.index+1



    export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
    matrix.to_excel(export_file_path, header=True,index=False)

def jointcsv():
    global df

    import_file_path = filedialog.askopenfilename(multiple=True)
    matrix = pd.concat((pd.read_csv(file).assign(filename=file) for file in import_file_path), ignore_index=True, )
    del matrix['filename']
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    matrix.to_csv(export_file_path, header=True,index=False)



mylabel=Label(root,text="APP PARA IMPORTAR ARCHIVO TEKLA --MODIFICAR-- ",bg="gray69")
mylabel.place(x=5,y=15)

e=Entry(root,width=20)
e.place(x=5,y=110)
elabel=Label(root,text="NOMBRE USER_FILE_1",bg="gray69")
elabel.place(x=5,y=88)


mybuttoni=Button(root,text="IMPORTAR",padx=20,pady=10,fg="blue",bg="gray",command=getCSV)
mybuttoni.place(x=5,y=40)

mybuttone=Button(root,text=" EXP. EXCEL",padx=20,pady=10,fg="blue",bg="gray",command=exportXLS)
mybuttone.place(x=115,y=40)

mybuttonelook=Button(root,text=" EXP. ATT. ",padx=22,pady=10,fg="blue",bg="gray",command=exportCSV)
mybuttonelook.place(x=230,y=40)

mybuttoneve=Button(root,text=" VER EXCEL ",padx=18,pady=6,fg="blue",bg="gray",command=visualizar)
mybuttoneve.place(x=230,y=92)

mybuttonevc=Button(root,text=" VER CSV",padx=26,pady=6,fg="blue",bg="gray",command=ver)
mybuttonevc.place(x=230,y=138)


jointex=Button(root,text=" Juntar .xlsx",padx=20,pady=6,fg="blue",bg="gray",command=jointexcel)
jointex.place(x=5,y=138)

jointc=Button(root,text=" Juntar .csv",padx=20,pady=6,fg="blue",bg="gray",command=jointcsv)
jointc.place(x=120,y=138)

root.mainloop()