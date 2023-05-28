import time
import plotly
import plotly.graph_objects as go
import pandas as pd
import datetime



excel_file = 'minuty.xlsx'

print("Odczytywanie pliku")
df = pd.read_excel(excel_file)

print("Obliczanie średniej intensywności ruchu")
srednia = df['intensywnosc'].mean()

a = df['minuta']
b = df['ruch']

for i in range(len(b)):
    b[i] = b[i] * srednia

print("Obliczanie godziny największego ruchu")
highest = 0
highest_index = 0

for i in range(0, len(b) - 59):
    current = 0   
    for j in range(0, 59):
        current = current + b[i+j]    
    if current > highest:
        highest = current        
        highest_index = i

c = []
d = []

for i in range(int(highest_index), int(highest_index) + 60, 1):
    c.append(a[i])
    d.append(b[i])

print("Tworzenie wykresu")
fig = go.Figure()

def convert_to_time(number):
    hours = int(number)
    minutes = int((number - hours) * 60)
    time_obj = datetime.time(hours, minutes)
    return time_obj.strftime("%H:%M")

godz = []
h=1
for i in range(len(a)):
    h = (a[i])/60 
    godz.append(round(h,2))
    print(h)

#zmieniona = [convert_to_time(number) for number in godz]

hours = [str(hour).zfill(2) for hour in godz]  # Tworzenie listy godzin w formacie HH:00

fig.add_trace(go.Scatter(x=hours, y=b, name="Ruch w ciągu dnia"))
fig.add_trace(go.Scatter(x=hours[int(highest_index):int(highest_index) + 60], y=d, name='Godzina największego ruchu'))

fig.update_layout(
    title="Wyznaczanie godziny największego ruchu",
    xaxis_title="Czas [godziny]",
    yaxis_title="Intensywność"
)

plotly.offline.plot(fig, filename="ruch.html")

print("Wyniki programu zapisane w pliku HTML")
time.sleep(10)
