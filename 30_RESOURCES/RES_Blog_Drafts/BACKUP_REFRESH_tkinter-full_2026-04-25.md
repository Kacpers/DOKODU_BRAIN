---
backup: python/automatyzacja/tkinter-gui
id: cmls1woqk0025w3hswe4d34un
original_title: Tworzenie interfejsów graficznych w Pythonie - wprowadzenie do Tkinter
---

Interfejsy graficzne są nieodłącznym elementem współczesnego oprogramowania. Tkinter, będący standardową biblioteką dla Pythona, umożliwia tworzenie aplikacji okienkowych w prosty sposób. W tym artykule dowiesz się, jak zacząć swoją przygodę z Tkinterem, poznasz podstawowe komponenty tej biblioteki oraz zobaczysz przykłady ich wykorzystania. Dzięki tej wiedzy będziesz w stanie tworzyć własne aplikacje z przyjaznym użytkownikowi interfejsem.


## Jak zacząć z Tkinterem?

Tkinter jest częścią standardowej biblioteki Pythona, co oznacza, że nie musisz instalować dodatkowych pakietów, aby z niego korzystać. Wystarczy, że zaimportujesz go w swoim skrypcie. Aby to zrobić:

```python
import tkinter as tk
```

Podstawowe komponenty Tkinter

Tkinter oferuje szeroki wachlarz komponentów (tzw. widgetów), które pomagają w konstrukcji interfejsów graficznych. Poniżej przedstawiam kilka podstawowych elementów, które można wykorzystać do budowy prostych aplikacji.

### Okno główne

Na początku należy stworzyć główne okno aplikacji:

```python
root = tk.Tk()
root.title("Moja aplikacja")
root.geometry("400x300")
```

### Etykiety (Label)

Etykiety służą do wyświetlania tekstu lub obrazków w oknie aplikacji.

```python
label = tk.Label(root, text="Witaj w aplikacji!")
label.pack()
```

### Przycisk (Button)

Przyciski umożliwiają użytkownikom wykonywanie akcji poprzez kliknięcie.

```python
def on_click():
    print("Przycisk został kliknięty")

button = tk.Button(root, text="Kliknij mnie", command=on_click)
button.pack()
```

### Pole wejściowe (Entry)

Pole wejściowe pozwala użytkownikom na wprowadzanie tekstu.

```python
entry = tk.Entry(root)
entry.pack()

def show_input():
    print(f"Wprowadzono: {entry.get()}")

button_show = tk.Button(root, text="Pokaż tekst", command=show_input)
button_show.pack()
```

### Pole wyboru (Checkbutton)

Pola wyboru umożliwiają zaznaczenie lub odznaczenie opcji.

```python
var = tk.IntVar()
checkbutton = tk.Checkbutton(root, text="Wyrażam zgodę", variable=var)
checkbutton.pack()
```

Układ elementów w Tkinter

Elementy można układać w oknie za pomocą metod takich jak `pack`, `grid` i `place`. Metoda `pack` dodaje elementy jeden pod drugim, `grid` umożliwia układ w formie siatki, a `place` pozwala precyzyjnie określić pozycję komponentu.

### Układ za pomocą grid

```python
label_grid = tk.Label(root, text="Etykieta w siatce")
label_grid.grid(row=0, column=0)

button_grid = tk.Button(root, text="Przycisk w siatce")
button_grid.grid(row=1, column=1)
```

## Uruchomienie aplikacji

Aby nasza aplikacja zaczęła działać, musimy wywołać pętlę główną Tkintera:

```python
root.mainloop()
```


Życzę powodzenia w tworzeniu własnych projektów z wykorzystaniem Tkintera!