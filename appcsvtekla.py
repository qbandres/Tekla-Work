from tkinter import *
from tkinter import filedialog
import pandas as pd
from pandastable import Table, TableModel
import os


root=Tk()
root.title('GESTION DE ARCHIVOS TEKLA')
root.configure(bg="gray69")
root.geometry('344x300')  #Definir el tamaño de celda
root.resizable(width=0, height=0)


def getCSV():
    global df

    import_file_path = filedialog.askopenfilename()
    df = pd.read_csv(import_file_path, skiprows = 2,
                     names = ['ID', 'PIECEMARK', 'BARCODE', 'ESP', 'PROFILE', 'DESCRIPTION', 'QUANTITY', 'WEIGHT'])


def export():
    global df
    if tipo_1.get()==1:
        if user.get()==1:
            df['USER_FIELD_1'] = e.get()
            df1 = df[['ID', 'USER_FIELD_1']]
            export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
            df1.to_csv(export_file_path, index=False, header=True)
            del df['USER_FIELD_1']
        elif user.get()==2:
            df['USER_FIELD_3'] = e.get()
            df1 = df[['ID', 'USER_FIELD_3']]
            export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
            df1.to_csv(export_file_path, index=False, header=True)
            del df['USER_FIELD_3']

    elif tipo_1.get()==2:
        if user.get()==1:
            df['USER_FIELD_1'] = e.get()
            df['Item']=df.index+1
            df=df[['Item','ID', 'PIECEMARK', 'BARCODE', 'ESP', 'PROFILE', 'DESCRIPTION', 'QUANTITY', 'WEIGHT','USER_FIELD_1']]
            export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
            df.to_excel(export_file_path, header=True,index=False)
            del df['USER_FIELD_1']
            del df['Item']
        elif user.get()==2:
            df['USER_FIELD_3'] = e.get()
            df['Item']=df.index+1
            df=df[['Item','ID', 'PIECEMARK', 'BARCODE', 'ESP', 'PROFILE', 'DESCRIPTION', 'QUANTITY', 'WEIGHT','USER_FIELD_3']]
            export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
            df.to_excel(export_file_path, header=True,index=False)
            del df['USER_FIELD_3']
            del df['Item']

def exportCSV():
    global df

    df['USER_FIELD_1'] = e.get()
    df1 = df[['ID', 'USER_FIELD_1']]
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df1.to_csv(export_file_path, index=False, header=True)

def visualizar():
    global df
    if tipo_1.get()==1:
        if user.get()==1:
            df['USER_FIELD_1'] = e.get()
            df1 = df[['ID', 'USER_FIELD_1']]
            frame1 = Toplevel()
            pt = Table(frame1, dataframe=df1)
            pt.show()
            del df['USER_FIELD_1']
        elif user.get()==2:
            df['USER_FIELD_3'] = e.get()
            df1 = df[['ID', 'USER_FIELD_3']]
            frame1 = Toplevel()
            pt = Table(frame1, dataframe=df1)
            pt.show()
            del df['USER_FIELD_3']

    elif tipo_1.get()==2:
        if user.get()==1:
            df['USER_FIELD_1'] = e.get()
            df['Item']=df.index+1
            df2=df[['Item','ID', 'PIECEMARK', 'BARCODE', 'ESP', 'PROFILE', 'DESCRIPTION', 'QUANTITY', 'WEIGHT','USER_FIELD_1']]
            frame1 = Toplevel()
            pt = Table(frame1, dataframe=df2)
            pt.show()
            del df['USER_FIELD_1']
            del df['Item']
        elif user.get()==2:
            df['USER_FIELD_3'] = e.get()
            df['Item']=df.index+1
            df3=df[['Item','ID', 'PIECEMARK', 'BARCODE', 'ESP', 'PROFILE', 'DESCRIPTION', 'QUANTITY', 'WEIGHT','USER_FIELD_3']]
            frame1 = Toplevel()
            pt = Table(frame1, dataframe=df3)
            pt.show()
            del df['USER_FIELD_3']
            del df['Item']





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



def getCSV2():
    global data

    import_file_path2 = filedialog.askopenfilename()
    data = pd.read_csv(import_file_path2)
    tmep=os.path.basename(import_file_path2)
    label2_2=Label(frame_2,text=tmep,bg="gray70",font=("bold", 8))
    label2_2.place(x=210,y=75)

def visualizar2():
    global data
    frame2 = Toplevel()
    pt = Table(frame2,dataframe=data)
    pt.show()

def modificar():
    global data
    if change.get()==1:
        data['USER_FIELD_1']=e2.get()
        print(data)
        export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
        data.to_csv(export_file_path, header=True, index=False)
        del data['USER_FIELD_1']

    elif change.get()==2:
        data['USER_FIELD_3'] = e2.get()
        print(data)
        export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
        data.to_csv(export_file_path, header=True, index=False)
        del data['USER_FIELD_3']

def getCSV3():
    global matrixcsv
    global  matrixxlsx

    if tipo_3.get()==1:
        import_file_path3 = filedialog.askopenfilename(multiple=True)
        matrixcsv = pd.concat((pd.read_csv(file).assign(filename=file) for file in import_file_path3), ignore_index=True, )
        del matrixcsv['filename']

    elif tipo_3.get()==2:
        import_file_path4 = filedialog.askopenfilename(multiple=True)
        matrixxlsx = pd.concat((pd.read_excel(file).assign(filename=file) for file in import_file_path4),
                           ignore_index=True, )
        del matrixxlsx['filename']

        matrixxlsx = matrixxlsx.rename(columns={'Unnamed: 0': 'Item'})
        matrixxlsx.Item = matrixxlsx.index + 1


def visualizar3():
    global matrixcsv
    global matrixxlsx
    if tipo_3.get()==1:
        frame31 = Toplevel()
        pt = Table(frame31, dataframe=matrixcsv)
        pt.show()

    elif tipo_3.get()==2:
        frame32 = Toplevel()
        pt = Table(frame32, dataframe=matrixxlsx)
        pt.show()

def export3():
    global matrixcsv
    global matrixxlsx
    if tipo_3.get() == 1:
        export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
        matrixcsv.to_csv(export_file_path, header=True, index=False)

    elif tipo_3.get() == 2:
        export_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
        matrixxlsx.to_excel(export_file_path, header=True, index=False)



frame_1=Frame(root,bg="gray70",width=340,height=120,relief='sunken',bd=2)
frame_1.pack(side=TOP)
frame_2=Frame(root,bg='gray70',width=340,height=100,relief='sunken',bd=2)
frame_2.pack()
frame_3=Frame(root,bg='gray70',width=340,height=100,relief='sunken',bd=2)
frame_3.pack(side=BOTTOM)



mylabel1=Label(frame_1,text="CONVERTIR EL ARCHIVO DE TEKLA || Modificar.csv ||",bg="gray70",font=("bold", 8))
mylabel1.place(x=2,y=1)

mybuttoni=Button(frame_1,text="IMPORTAR",padx=20,pady=30,fg="blue",bg="gray50",command=getCSV)
mybuttoni.place(x=2,y=30)

tipo_1 = IntVar() # Como StrinVar pero en entero

frame_1_1=Frame(frame_1,relief='sunken',bd=1.5,bg='gray65',width=60,height=55).place(x=275,y=1)
Radiobutton(frame_1_1, text=".csv ", variable=tipo_1,value=1,bg='gray65').place(x=283,y=6)
Radiobutton(frame_1_1, text=".xlsx", variable=tipo_1,value=2,bg='gray65').place(x=283,y=31)
tipo_1.set('1')


frame_1_2=Frame(frame_1,relief='sunken',bd=1.5,bg='gray65',width=60,height=55).place(x=275,y=60)
user = IntVar() # Como StrinVar pero en entero
Radiobutton(frame_1_2, text=".UF1 ", variable=user,value=1,bg='gray65').place(x=283,y=67)
Radiobutton(frame_1_2, text=".UF3", variable=user,value=2,bg='gray65').place(x=283,y=90)
user.set('1')

def on_click(event):
    e.config(state=NORMAL)
    e.delete(0,END)

e=Entry(frame_1,width=20)
e.insert(0,'USER_FIELD_')
e.config(state=DISABLED)
e.bind('<Button-1>',on_click)
e.place(x=115,y=30)

mybuttoneve=Button(frame_1,text=" Visualizar ",padx=42,pady=2,fg="blue",bg="gray",command=visualizar)
mybuttoneve.place(x=115,y=56)

mybuttone=Button(root,text=" Exportar",padx=46,pady=2,fg="blue",bg="gray",command=export)
mybuttone.place(x=119,y=88)

#################################################################################################

mylabel2=Label(frame_2,text="MODIFICAR DATOS DE USER_FIELD (.CSV)",bg="gray70",font=("bold", 8))
mylabel2.place(x=2,y=1)

def on_click(event):
    e2.config(state=NORMAL)
    e2.delete(0,END)

e2=Entry(frame_2,width=25)
e2.insert(0,'NEW NAME USER_FIELD')
e2.config(state=DISABLED)
e2.bind('<Button-1>',on_click)
e2.place(x=5,y=70)

frame_2_2=Frame(frame_2,relief='sunken',bd=1.5,bg='gray65',width=60,height=55).place(x=275,y=25)
change = IntVar() # Como StrinVar pero en entero
Radiobutton(frame_2_2, text="UF1 ", variable=change,value=1,bg='gray65').place(x=283,y=150)
Radiobutton(frame_2_2, text="UF3", variable=change,value=2,bg='gray65').place(x=283,y=175)
change.set('1')

mybuttoni2=Button(frame_2,text="IMPORTAR",padx=10,pady=8,fg="blue",bg="gray",command=getCSV2)
mybuttoni2.place(x=5,y=25)

mybuttoneve2=Button(frame_2,text=" VISUALIZAR ",padx=10,pady=8,fg="blue",bg="gray",command=visualizar2)
mybuttoneve2.place(x=93,y=25)

mybuttoneve2=Button(frame_2,text=" MODIF. ",padx=12,pady=8,fg="blue",bg="gray",command=modificar)
mybuttoneve2.place(x=192,y=25)

###############################################################################################################

mylabel3=Label(frame_3,text="UNIR ARCHIVOS SIMILARES",bg="gray70",font=("bold", 8))
mylabel3.place(x=2,y=1)

mybuttoni3=Button(frame_3,text="IMPORTAR",padx=10,pady=8,fg="blue",bg="gray",command=getCSV3)
mybuttoni3.place(x=5,y=25)

mybuttoneve3=Button(frame_3,text=" VISUALIZAR ",padx=10,pady=8,fg="blue",bg="gray",command=visualizar3)
mybuttoneve3.place(x=93,y=25)


tipo_3 = IntVar() # Como StrinVar pero en entero

frame_3_3=Frame(frame_3,relief='sunken',bd=1.5,bg='gray65',width=60,height=55).place(x=275,y=10)
Radiobutton(frame_3_3, text=".csv ", variable=tipo_3,value=1,bg='gray65').place(x=283,y=236)
Radiobutton(frame_3_3, text=".xlsx", variable=tipo_3,value=2,bg='gray65').place(x=283,y=261)
tipo_3.set('1')

mybuttoneve2=Button(frame_3,text=" EXPORT ",padx=12,pady=8,fg="blue",bg="gray",command=export3)
mybuttoneve2.place(x=192,y=25)

root.mainloop()