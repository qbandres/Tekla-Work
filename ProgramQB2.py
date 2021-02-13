from scipy.optimize import fsolve
import plotly.graph_objects as go
import numpy as np
import math
import pandas as pd
from datetime import date, timedelta


class Equation:
    def __init__(self, Wt, t):
        self.Wt = Wt
        self.t = t

    def calc1(self):
        def equ(pa):
            a, b, c = pa
            return (b ** 2 - a * c, -2 * a * self.t ** 3 + 3 * b * self.t ** 2 + 6 * c * self.t - 6 * self.Wt,
                    -2 * a * self.t ** 2 + 2 * b * self.t + c)

        a, b, c = fsolve(equ, (1, 1, 1))
        x = np.arange(1, self.t + 1)
        y = -a * x ** 2 + b * x + c
        return y


class splitdate:
    def __init__(self, fi, ff, Wt, pwa, pwb, pwc, pta, ptb, ptc):
        self.Wt = Wt
        self.pwa = pwa
        self.pwb = pwb
        self.pwc = pwc
        self.pta = pta
        self.ptb = ptb
        self.ptc = ptc
        self.ft = [fi + timedelta(days=d) for d in range((ff - fi).days + 1)] #CREAMOS LA LISTA DE FECHSA
        self.dft = pd.DataFrame({'Fecha': self.ft})
        self.dft.set_index('Fecha', inplace=True)
        self.t=(ff - fi).days + 1
    def calc1(self):
        #particionar las fechas de ejecución de los quiebres
        fta = self.ft[:int(self.t * self.pta)]
        ftb = self.ft[int(self.t * (1-self.ptc-self.ptb)):int(self.t * (1-self.ptc))]
        ftc = self.ft[int(self.t * (1-self.ptc)):]                   #se extrae la parte de la lista de pucnh
        ta = len(fta)
        tb = len(ftb)
        tc = len(ftc)

        # Distribucion de pesos
        Wa = self.Wt * self.pwa
        Wb = self.Wt * self.pwb
        Wc = self.Wt * self.pwc

        return fta, ftb, ftc, Wa, Wb, Wc, ta, tb, tc


class convdf:
    def __init__(self, ft, y, name):
        self.ft = ft
        self.y = y
        self.name = name

    def act(self):
        df = pd.DataFrame({'Fecha': self.ft, self.name: self.y})
        df.set_index('Fecha', inplace=True)
        return df

class Calular:
    def __init__(self, W, fi, ff):
        self.W = W
        self.fi = fi
        self.ff = ff
        self.t=(ff - fi).days + 1

    def met1(self):
        fta1, ftb1, ftc1, Wa1, Wb1, Wc1, ta1, tb1, tc1 = splitdate(self.fi, self.ff, self.W, 0.6, 0.3, 0.1, 0.6, 0.3, 0.1).calc1()
        ya1 = Equation(Wa1, ta1).calc1()
        yb1 = Equation(Wb1, tb1).calc1()
        yc1 = Equation(Wc1, tc1).calc1()

        var_a1 = (Wa1 - ya1.sum()) / len(ya1)
        self.ya1 = ya1 + var_a1
        var_b1 = (Wb1 - yb1.sum()) / len(yb1)
        self.yb1 = yb1 + var_b1
        var_c1 = (Wc1 - yc1.sum()) / len(yc1)
        self.yc1 = yc1 + var_c1

        dfa1 = convdf(fta1, self.ya1, 'Montaje').act()
        dfb1 = convdf(ftb1, self.yb1, 'Torque').act()
        dfc1 = convdf(ftc1, self.yc1, 'Punch').act()

        datos_f1 = pd.concat([dfa1, dfb1, dfc1], axis=1)
        datos_f1 = datos_f1.fillna(0)

        return datos_f1





###     FASEALL FASES CREATED

df_fase1=Calular(1632.350,date(2019, 10, 31),date(2021, 6, 30)).met1()
df_fase2=Calular(3703.991,date(2019, 10, 31),date(2021, 8, 8)).met1()
df_fase3=Calular(551.989,date(2019, 12, 1),date(2021, 6, 30)).met1()
df_fase4=Calular(381.594,date(2021, 4, 3),date(2021, 8, 8)).met1()
df_fase5=Calular(585.098,date(2021, 1, 23),date(2021, 9, 4)).met1()
df_fase6=Calular(453.079,date(2021, 6, 30),date(2021, 11, 28)).met1()
df_fase7=Calular(134.123,date(2021, 2, 18),date(2021, 4, 3)).met1()
df_fase8=Calular(109.371,date(2021, 11, 28),date(2022, 1, 3)).met1()
df_fase9=Calular(250.840,date(2021, 8, 8),date(2021, 10, 27)).met1()
df_fase10=Calular(209.864,date(2022, 1, 3),date(2022, 3, 4)).met1()
df_fase11=Calular(496.915,date(2021, 9, 4),date(2022, 2, 11)).met1()
df_fase12=Calular(54.467,date(2022, 2, 11),date(2022, 3, 4)).met1()

fi=date(2019,10,30)
ff=date(2022,8,8)
t=(ff-fi).days


ft = [fi + timedelta(days=d) for d in range((ff - fi).days + 1)]  # CREAMOS LA LISTA DE FECHSA
dft = pd.DataFrame({'Fecha': ft})
dft.set_index('Fecha', inplace=True)

df_total=pd.concat([dft,df_fase1,df_fase2,df_fase3,df_fase4,df_fase5,df_fase6,df_fase7,df_fase8,df_fase9,df_fase10,df_fase11,df_fase12],axis=1)
df_total=df_total.fillna(0)
df_total["total"] = df_total.sum(axis=1)
df_total['acum']= df_total['total'].cumsum()

from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=2, cols=1)

fig.append_trace(go.Scatter(
    x=df_total.index,
    y=df_total.total,
    name='Montaje diario'
), row=1, col=1)

fig.append_trace(go.Scatter(
    x=df_total.index,
    y=df_total.acum,
    name='Montaje Acumulado'
), row=2, col=1)


fig.update_layout(title_text="Stacked Subplots")
fig.show()


















