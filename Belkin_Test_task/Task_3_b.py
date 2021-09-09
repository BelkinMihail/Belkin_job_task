import plotly.graph_objs as go
import sqlite3
import np

obtainable =[]
order = []

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
cursor.execute("""SELECT * from sofa left join vendor on vendor.Артикул = sofa.Артикул""")
rows = cursor.fetchall()
for row in rows:
    if row[2] != 'в пути':#все статусы кроме 'в пути'
        if row[2] != 'доступно':#если статус: 'доступен'
                obtainable.append([row[5],row[1]])# добавляем цену без скидки и артикул
        else:                                   # если статус 'под заказ'
                order.append([row[5],row[1]])  # добавляем цену без скидки и артикул

def custom_key(sofa): return sofa[0]# ключ для сортировки по 0-ому элементу


#obtainable = list(map(list, {tuple(x) for x in obtainable}))

obtainable.sort(key=custom_key)#сортируем в порядке возрастания
order.sort()#сортируем в порядке возрастания

obtainable=np.unique(obtainable,axis=0)# убираем дубликаты
order=np.unique(order,axis=0)# убираем дубликаты

#--------------------------------------------------------
#график распределения цены
#выводим цены доступных в отдельный список
Line_obtainable_list = []
for i in obtainable:
    Line_obtainable_list.append(i[0])
Line_obtainable_list=np.unique(Line_obtainable_list,axis=0)# убираем дубликаты
#выводим цены под заказ в отдельный список
Line_order_list = []
for i in order:
    Line_order_list.append(i[0])
Line_order_list=np.unique(Line_order_list,axis=0)# убираем дубликаты

fig = go.Figure()
fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, xanchor="center"),
                  title="Графики распределения цены без скидки для «доступных» диванов и «под заказ»",
                  yaxis_title="цена(рублей)",
                  margin=dict(l=0, r=0, t=30, b=0))
fig.add_trace(go.Scatter(y=Line_obtainable_list,mode='lines+markers', hovertemplate=" %{y} рублей",name='доступные'))#создаем линию графика с доступными
fig.add_trace(go.Scatter(y=Line_order_list, mode='lines+markers', hovertemplate=" %{y} рублей",name='под заказ'))#создаем линию графика с под заказ
fig.show()
#--------------------------------------------------------
#столбчатый график топ 10
sofa=[]
for row in rows:
    sofa.append([row[5],row[1]])# добавляем цену без скидки и артикул

def custom_key(sof): return sof[0]
sofa.sort(key=custom_key)#сортируем в порядке возрастания
sofa=np.unique(sofa,axis=0)# убираем дубликаты

column_list=[]
n = len(sofa)//2 # середина списка
# заполняем список 10-ю близжайшими к середине значенями
column_list.append(sofa[n - 4])
column_list.append(sofa[n - 3])
column_list.append(sofa[n - 2])
column_list.append(sofa[n - 1])
column_list.append(sofa[n])
column_list.append(sofa[n + 1])
column_list.append(sofa[n + 2])
column_list.append(sofa[n + 3])
column_list.append(sofa[n + 4])
column_list.append(sofa[n + 5])

x=[]
y=[]
for i in column_list:
    #y.append("цена: " + str(i[0])+ "рублей")
    y.append(i[0])
    x.append("Артикул:" + str(i[1]))


fig = go.Figure()
fig.update_yaxes(range=[44500, 46500], zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')
fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, xanchor="center"),
                  title="ТОП-10 артикулов по средней цене без скидки",
                  yaxis_title="цена(рублей)",
                  margin=dict(l=0, r=0, t=30, b=0))
fig.add_trace(go.Bar( x=x , y = y))
fig.show()
#--------------------------------------------------------
#круговая диаграмма
circle_obtainable =[]
circle_order =[]
for row in rows:
    if row[2] != 'в пути':#все статусы кроме 'в пути'
        if row[2] != 'доступно':#если статус: 'доступен'
                circle_obtainable.append(row[0])
        else:                                   # если статус 'под заказ'
                circle_order.append(row[0])


obt_sum = len(circle_obtainable)
ord_sum = len(circle_order)

fig = go.Figure()
fig.add_trace(go.Pie(values=[obt_sum, ord_sum], labels=['доступеные', 'под заказ']))

fig.show()