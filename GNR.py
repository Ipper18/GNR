import os
import time
import webbrowser
import tkinter as tk
from tkinter import messagebox
import plotly
import plotly.graph_objects as go
import pandas as pd

excel_file = 'minuty.xlsx'
html_file = 'ruch.html'

def generate_plots():
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

    godz = []
    h = 1
    for i in range(len(a)):
        h = (a[i]) / 60
        godz.append(round(h, 2))

    hours = [str(hour).zfill(2) for hour in godz]  # Tworzenie listy godzin w formacie HH:00

    fig.add_trace(go.Scatter(x=hours, y=b, name="Ruch w ciągu dnia"))
    fig.add_trace(go.Scatter(x=hours[int(highest_index):int(highest_index) + 60], y=d, name='Godzina największego ruchu'))

    fig.update_layout(
        title="Wyznaczanie godziny największego ruchu",
        xaxis_title="Czas [godziny]",
        yaxis_title="Intensywność"
    )

    plotly.offline.plot(fig, filename=html_file)

    print("Wyniki programu zapisane w pliku HTML")

    # Dodanie informacji o godzinie największego ruchu i średnim ruchu do końcowego pliku HTML
    with open(html_file, "a") as file:
        start_time = hours[int(highest_index)]
        end_time = hours[int(highest_index) + 59]
        average_traffic = srednia
        file.write(f"<p>Godzina najwiekszego ruchu: {start_time} - {end_time}</p>")
        file.write(f"<p>Sredni ruch w ciagu calego dnia: {average_traffic}</p>")

def show_menu():
    window = tk.Tk()
    window.title("Menu")
    window.geometry("300x300")

    def show_description():
        messagebox.showinfo("Opis", "Ten program generuje wykres Godzin Największego Ruchu wraz z zaznaczoną godziną w ciągu dnia z największym ruchem na podstawie danych z pliku 'minuty.xlsx'.\n\n Plik ten należy stworzyć tak, aby w pierwszej kolumnie znajdowały się minuty, a w drugiej ruch w ciągu jednej minuty oraz w trzeciej kolumnie intensywność i dodajemy tam długość w minutach poszczególnej rozmowy.\n\n ")

    def open_plots():
        if os.path.isfile(html_file):
            webbrowser.open(html_file)
        else:
            messagebox.showinfo("Brak wykresu", "Wykres jeszcze nie został stworzony. Kliknij 'Stwórz wykres'.")



    description_button = tk.Button(window, text="Opis programu", command=show_description)
    description_button.pack(pady=10, anchor="center")

    generate_button = tk.Button(window, text="Stwórz i wyświetl wykresy", command=generate_plots)
    generate_button.pack(pady=10, anchor="center")

    plots_button = tk.Button(window, text="Wyświetl wykresy", command=open_plots)
    plots_button.pack(pady=10, anchor="center")

    window.mainloop()

show_menu()
