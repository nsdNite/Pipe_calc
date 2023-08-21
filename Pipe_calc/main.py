# Python 3
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk
from tkinter import messagebox
import math


# main calc function
def pipe_calc():
    m_entry.delete(0, END)
    mp_entry.delete(0, END)
    try:
        dia = float(dia_entry.get())
        th = float(th_entry.get())
        ln = float(ln_entry.get())
        den = float(den_entry.get())
        m = round((((math.pi * dia ** 2 / 4 * ln * den) -
                    (math.pi * (dia - 2 * th) ** 2 / 4 * ln * den)) / 1000000000), 2)
        mp = round((((math.pi * dia ** 2 / 4 * 1000 * den)
                     - (math.pi * (dia - 2 * th) ** 2 / 4 * 1000 * den)) / 1000000000), 2)
        results = (str(dia), str(th), str(ln), str(den), str(m))
        print(results)  # for check in prompt
        m_entry.insert(0, str(m))
        mp_entry.insert(0, str(mp))
        history_output = '|'.join(results)
        history.insert('end', f'{history_output}\n')
    except:
        messagebox.showwarning('Warning', 'Please check input!')


# history clear
def history_clear():
    history.delete('0.0', END)


# radiobuttons select density function
def sel():
    den_entry.delete(0, END)
    den_entry.insert(0, str(dnst.get()))


# history export
def history_export():
    file_path = filedialog.asksaveasfilename(filetypes=(("Comma separated (*.csv)", "*.csv"), ("All files", "*.*")))
    f = open(file_path, 'w', encoding='utf-8')
    text = history.get('1.0', END)
    f.write(text)
    f.close()


# main window
root = ThemedTk(theme='clam')
root.title('Round pipe calculator v1.1')
root.geometry('475x300+150+150')
root.resizable(False, False)

# frames
frameMain = ttk.Frame(root, height=50, width=30)
frameMain.place(x=12, y=5)

radioLabel = ttk.Label(text='Quick density:')
frameRadio = ttk.LabelFrame(root, labelwidget=radioLabel, height=40, width=20, padding=2)
frameRadio.place(x=320, y=3)

historyLabel = ttk.Label(text='History window:')
frameHistory = ttk.LabelFrame(root, labelwidget=historyLabel, height=50, width=40, padding=5)
frameHistory.place(x=10, y=155)

frameButtons = ttk.Frame(root, height=50, width=40)
frameButtons.place(x=350, y=175)

# window labels
labelingColumnOne = [
    'Diameter of pipe:',
    'Wall thickness:',
    'Length of pipe:',
    'Density of material:',
    'Mass result:',
    'Mass of 1 meter:'
]

labelingColumnThree = [
    ' mm',
    ' mm',
    ' mm',
    ' kg/m3',
    ' kg',
    ' kg'
]

rowLabelOne = 0
for i in labelingColumnOne:
    ttk.Label(frameMain, text=i, width=17).grid(row=rowLabelOne, column=0)
    rowLabelOne += 1

rowLabelThree = 0
for i in labelingColumnThree:
    ttk.Label(frameMain, text=i, anchor=W, width=10).grid(row=rowLabelThree, column=3)
    rowLabelThree += 1

# window entries
dia_entry = ttk.Entry(frameMain)
dia_entry.insert(0, '42.4')
dia_entry.grid(row=0, column=1)

th_entry = ttk.Entry(frameMain)
th_entry.insert(0, '6')
th_entry.grid(row=1, column=1)

ln_entry = ttk.Entry(frameMain)
ln_entry.insert(0, '500')
ln_entry.grid(row=2, column=1)

den_entry = ttk.Entry(frameMain)
den_entry.insert(0, '7850')
den_entry.grid(row=3, column=1)

m_entry = ttk.Entry(frameMain)
m_entry.insert(0, '[mass appears here]')
m_entry.grid(row=4, column=1)

mp_entry = ttk.Entry(frameMain)
mp_entry.insert(0, '[mass of 1 meter here]')
mp_entry.grid(row=5, column=1)

dnst = IntVar()
den_choice1 = ttk.Radiobutton(frameRadio, text='Steel 7850 kg/m3',
                              variable=dnst, value='7850', command=sel, width=18)
den_choice1.grid(row=0, column=4)
den_choice2 = ttk.Radiobutton(frameRadio, text='Alu 2700 kg/m3',
                              variable=dnst, value='2700', command=sel, width=18)
den_choice2.grid(row=1, column=4)
den_choice3 = ttk.Radiobutton(frameRadio, text='St. steel 7880 kg/m3',
                              variable=dnst, value='7880', command=sel, width=18)
den_choice3.grid(row=2, column=4)

# buttons
calc_but = ttk.Button(frameButtons, text='Calculate', command=pipe_calc, width=12)
calc_but.grid(row=3, column=4, rowspan=3)

history_clear = ttk.Button(frameButtons, text='Clear history', command=history_clear, width=12)
history_clear.grid(row=8, column=4)

history_export = ttk.Button(frameButtons, text='Export history', command=history_export, width=12)
history_export.grid(row=9, column=4)

# history
history = Text(frameHistory, height=5, width=35, padx=2, pady=0)
history.grid(row=8, columnspan=4)

root.mainloop()
