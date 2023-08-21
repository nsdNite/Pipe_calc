# Python 3
# Production info packer for MDEM to be free from nupas macro
# dtat01, 2022

import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
import shutil

'''
TO-DO
1) Користувач вказує директорії секції на диску z:-на будь-якому диску, йде перевірка cam та pi директорій
2) Пакер створює в C:/temp директорію проекту: - done
    2.1) перевірити, може є така директорія? - done
    2.2) створити, якщо немає - done
    2.3) назва директорії береться в коріння вказаної секції - done
        2.3.1) опція для інтерфейсу - по чек-боксу можна налаштувати номер проекту - done, вказуємо завжди (номер може відрізнятись)
3) Пакер маніпулює файлами з мережевого диску (спочатку спробуємо копіювати) - done
    3.1) пакер знаходить в указаній секції директорії pi, cam. - done
        з дирекоторії cam копіює/переміщає pdf та dwg; - done
        з директорії pi копіює/переміщає dwg; - done
        з pi копіює та переіменовує репорти - partlist, cog, nesting list, bar list, тощо. - done
    3.2) теж саме, але для креслень в директорії dxfout - додається dxfout у шлях перед проектом. - done
    3.3) якщо немає креслень чи папки з pi пусті - попередети через меседж бокс. - done, зроблено повідомлення про успіх
    3.4) опція для інтерфейсу - по чек боксу можна налаштувати переміщення чи копіювання - to be done
    3.5) опція для інтерйейсу - в полях задавати проект та номер секції, без вказання папки. - to be done

3) Створювати всередені директорії проекта у с:/temp/project директорії наступного дерева: 
    XXXXXX_SSS(SSSS)_PROD_INFO - номер проекту хай вводиться в entry - DONE
        - Revision files A01 (може це налаштувати якось?) - complete_package
             - Plates - сюди dwg з PI
             - Profiles - сюди pdf та dwg з CAM
             - Reports - сюди переіменовані репорти з PI
        - Документ Revision_management_section_SSS(SSSS)_Rev.A01 (копіюємо його з постійного місця або забиваємо:)) - не треба
'''


# Створеняя директорій та піддерикторій продакшену у темпах.
def pack_start():
    global plates_d, profiles_d, formed_d, reports_d, prj_no, sec_name, dwg_dir, prod_dir, temp_path, complete_p  # !Винести деяки поза функцій.
    # Створення папок у темп
    prj_no = prj_entry.get()  # читає ввод користувача в проект номер
    temp_path = os.path.join('C:/temp/', prj_no)  # будуємо шлях до проекту = може просто f'C:/temp/{prj_no}'?
    if not os.path.exists(temp_path):  # якщо такого шляху нема, то створюється директорія проекту
        os.mkdir(temp_path)
    cur_path = e_path.get()  # читаємо ввод папки
    sec_name = os.path.basename(cur_path)  # знаходимо номер секції
    prod_name = f'{prj_no}_{sec_name}_PROD_INFO'  # ім'я директорії пакету продакшену
    dwg_name = f'{prj_no}_{sec_name}_DRAWINGS'  # ім'я директорії креслень
    prod_dir = os.path.join(temp_path, prod_name)  # будуємо шлях для папки продакшену
    dwg_dir = os.path.join(temp_path, dwg_name)
    # шляхи до директорій всередені пакету:
    complete_p = os.path.join(prod_dir, 'Complete_package')
    plates_d = os.path.join(complete_p, 'Plates/Cutting_data')
    profiles_d = os.path.join(complete_p, 'Profiles/Single_profile_sketches')
    formed_d = os.path.join(complete_p, 'Profiles/Formed_profiles_templates')
    reports_d = os.path.join(complete_p, 'Reports')
    while os.path.exists(
            prod_dir):  # якщо є старий продакшен, виводимо попередження і додаємо OLD_ перед назвою старого продакшена
        try:
            old_prod_dir = os.path.join(temp_path, f'OLD_{prj_no}_{sec_name}_PROD_INFO')
            if not os.path.exists(old_prod_dir):
                messagebox.showwarning('Увага!',
                                       f'У C:/temp/{prj_no} знайден пакет креслень для цієї секції.'
                                       f'\nТепер його назва буде: {old_prod_dir}')
                os.rename(prod_dir, old_prod_dir)
            else:
                messagebox.showwarning('Увага!',
                                       f'У вас вже є застарілий пакет продакшену у C:/temp/{prj_no}'
                                       f'\nНаведіть трохи порядку:)'
                                       f'\nПродакшен не зібрано!!')
                break
        except:
            break
    else:
        os.mkdir(prod_dir)
        os.makedirs(complete_p)
        os.makedirs(plates_d)
        os.makedirs(profiles_d)
        os.mkdir(formed_d)
        os.makedirs(reports_d)
        copy_PI()


# Копіювання продакшену та креслень
def copy_PI():
    cur_path = e_path.get()
    prof_path = os.path.join(cur_path, 'cam')
    plat_path = os.path.join(cur_path, 'pi')
    for folder, subfolders, files in os.walk(plat_path):
        for file in files:
            path = os.path.join(folder, file)  # повний шлях до файлу
            if file.startswith('FP'):
                shutil.copy2(path, os.path.join(formed_d, file))
            elif file.endswith('.dxf'):
                shutil.copy2(path, os.path.join(plates_d, file))
            elif file.endswith('.list') or file.endswith('.csv') or file.endswith('.xlsx'):
                shutil.copy2(path, os.path.join(reports_d, file))
            else:
                pass
    for folder, subfolders, files in os.walk(prof_path):
        for file in files:
            path = os.path.join(folder, file)
            if file.endswith('.pdf') or file.endswith('.dwg'):
                shutil.copy2(path, os.path.join(profiles_d, file))
            else:
                pass
    #видаляємо пусті директорії
    dirs=[
        plates_d,
        profiles_d,
        formed_d,
        reports_d,
         ]
    for i in dirs:
        path = i
        if not os.listdir(path):
            os.rmdir(i)
    rename_reports()


# окрема функція по репортам
def rename_reports():
    cog_report = os.path.join(reports_d, f'{prj_no}_{sec_name}_centre_of_gravity.csv')
    nestprof = os.path.join(reports_d, f'{prj_no}_{sec_name}_profile_nesting_list.txt')
    nestbar = os.path.join(reports_d, f'{prj_no}_{sec_name}_profile_bar_list.txt')
    partlist = os.path.join(reports_d, f'{prj_no}_{sec_name}_partlist.xlsx')
    weight_report = os.path.join(reports_d, f'{prj_no}_{sec_name}_block-weight.txt')
    bom_report=os.path.join(reports_d, f'{prj_no}_{sec_name}_BOM.csv')
    for folder, subfolders, files in os.walk(reports_d):
        for file in files:
            path = os.path.join(folder, file)
            if file.startswith('rep-cog'):
                os.rename(path, cog_report)
            elif file.startswith('nestprof'):
                os.rename(path, nestprof)
            elif file.startswith('nestbar'):
                os.rename(path, nestbar)
            elif file.endswith('.xlsx'):
                os.rename(path, partlist)
            elif file.startswith('rep-block'):
                os.rename(path, weight_report)
            elif file.startswith('rep-bom'):
                os.rename(path, bom_report)
            else:
                pass
    messagebox.showinfo('Шикарно!', f'Пакет продакшену зібрано у {prod_dir}!')
    drawings()


def drawings():
    cur_path = e_path.get()
    temp_path_one = os.path.split(cur_path)[0]
    temp_path_two = os.path.split(temp_path_one)[0]
    drw_path = temp_path_two + f'\dxfout\\{prj_no}\\{sec_name}\\sheet'  # всі строки до цього-спроба добратись до dxfout
    while os.path.exists(dwg_dir):
        try:
            old_dwg_dir = os.path.join(temp_path, f'OLD_{prj_no}_{sec_name}_DRAWINGS')
            if not os.path.exists(old_dwg_dir):
                messagebox.showwarning('Увага!',
                                       f'У C:/temp/{prj_no} знайден пакет креслень для цієї секції.'
                                       f'\nТепер його назва буде: {old_dwg_dir}')
                os.rename(dwg_dir, old_dwg_dir)
            else:
                messagebox.showwarning('Увага!',
                                       f'У вас вже є застарілий пакет креслень у C:/temp/{prj_no}'
                                       f'\nНаведіть трохи порядку:)'
                                       f'\nКреслення не зібрано!!')
                break
        except:
            break
    else:
        os.mkdir(dwg_dir)
    for folder, subfolders, files in os.walk(drw_path):
        for file in files:
            path = os.path.join(folder, file)
            if file.endswith('.dwg') or file.endswith('.pdf') or file.endswith('.plt'):
                shutil.copy2(path, os.path.join(dwg_dir, file))
    if not os.listdir(dwg_dir):
        os.rmdir(dwg_dir)
    else:
        messagebox.showinfo('Шикарно!', f'Креслення зібрано у {dwg_dir}!')


# Переміщення продакшену та креслень - у наступних версіях
def move_PI():
    pass


# Функція для вибору директорії
def choose_dir():
    global check_cam, check_pi
    dir_path = filedialog.askdirectory()
    check_pi_path = os.path.join(dir_path, 'pi')
    check_cam_path = os.path.join(dir_path, 'cam')
    print(f'{check_cam_path}\n{check_pi_path}')
    check_cam = True
    check_pi = True
    if not os.path.exists(check_cam_path):
        check_cam = False
    else:
        pass
    if not os.path.exists(check_pi_path):
        check_pi = False
    else:
        pass
    if (check_pi, check_cam) == (False, False):
        messagebox.showerror('Помилка!',
                             'Не знайдено директорій продакшену. Перевірте, будь ласка, вказану директорію.')
    else:
        e_path.delete(0, END)
        e_path.insert(0, dir_path)


root = ThemedTk(theme='arc')
root.geometry('400x135+500+300')
root.resizable(False, False)
root.title('Universal Production Packager v.1.0')

frame_folder = ttk.Frame(root)
frame_folder.pack(pady=5, padx=10, fill=X)

frame_project = ttk.Frame(root)
frame_project.pack(pady=8, padx=10, fill=X)

btn_dialog = ttk.Button(frame_folder, text="Вибрати директорію секції", command=choose_dir)
btn_dialog.pack(side=LEFT, padx=0)

e_path = ttk.Entry(frame_folder)
e_path.pack(side=LEFT, expand=True, fill=X, ipady=2)

prj_label = ttk.Label(frame_project, text='Вкажіть номер проекту:')
prj_label.pack(side=LEFT, padx=5)

prj_entry = ttk.Entry(frame_project)
prj_entry.pack(side=LEFT, expand=True, fill=X, ipady=3)

btn_start = ttk.Button(root, text="Start", command=pack_start)
btn_start.pack(fill=X, padx=10)

root.mainloop()
