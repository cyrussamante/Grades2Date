from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile
from ctypes import windll
import os

root = Tk()
root.iconbitmap(default="icon.ico")
root.geometry("1000x800")
root.minsize(1000,800)
root.maxsize(1000,800)
windll.shcore.SetProcessDpiAwareness(1)

# Clear Window and all Widgets
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Task Not Available Function
def task_not_available():
    messagebox.showerror("Task Not Available", "Sorry! This task is still in development is currently not available.")

# Closing Confirmation
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Main Menu Class
class main_menu:
    def __init__(self, master):
        root.title("Grades2Date | Calculate the Future!")
        # Menu Frame
        self.menu_frame = Frame(master)
        self.menu_frame.pack()

        # Title & Subtitle Label
        self.title_label = Label(self.menu_frame, text="Grades 2 Date", font="Helvetica 55 bold")
        self.title_label.grid(row=0, column=0, pady=(100,0))
        self.subtitle_label = Label(self.menu_frame, text="Calculate the Future!", font="Helvetica 20")
        self.subtitle_label.grid(row=1, column=0, pady=(0,100))

        # Menu Buttons
        self.calc_btn = Button(self.menu_frame, text="Calculate", font="Helvetica 20", padx=34, command=lambda:[clear_window(),gpa_page(root)])
        self.calc_btn.grid(row=2, column=0, pady=(0,20))
        #self.import_btn = Button(self.menu_frame, text="Import Data", font="Helvetica 20", command=lambda:[task_not_available(),self.import_data()], padx=19)
        self.import_btn = Button(self.menu_frame, text="Import Data", font="Helvetica 20", command=lambda:[self.import_data()], padx=19)
        self.import_btn.grid(row=3, column=0, pady=(0,20))
        self.exit_btn = Button(self.menu_frame, text="Close Program", font="Helvetica 20", command=on_closing)
        self.exit_btn.grid(row=4, column=0, pady=(0,20))

        # Version Label
        self.version_num_label = Label(master, text="Version 1.0.1", font="Helvetica 18")
        self.version_num_label.pack(side=LEFT, anchor=SW, padx=(5,0))

    # Import Data Function
    def import_data(self):
        files = [('Text Document', '*.txt')]
        root.datalocation = filedialog.askopenfilename(initialdir="~/Downloads", title="Select a File", filetypes= files)
        if root.datalocation == "":
            return
        clear_window()
        imported_gpa(root, root.datalocation)
        return root.datalocation

# Calculator Page Class
class gpa_page:
    def __init__(self, master):
        root.title("Untitled - Grades2Date")

        #Initialization of Entry Boxes
        self.course_entries = []
        self.grade_entries = []
        self.unit_entries = []

        # Calculator Frame
        self.calc_frame = Frame(master)
        self.calc_frame.pack(side=LEFT, anchor=NW, padx=(0,0), pady=(80,0))

        # Button Frame
        self.btn_frame=Frame(master)
        self.btn_frame.pack(ipadx=100)

        # Results Frame
        self.result_frame=LabelFrame(master, borderwidth=5)
        self.result_frame.pack(pady=(50,0), ipadx=20, padx=(3,0))

        # Main Menu Button
        self.menu_frame=Frame(master, bg="orange")
        self.menu_frame.pack(side=RIGHT, anchor=SE, padx=(0,5), pady=(0,5))
        self.main_menu_btn = Button(self.menu_frame, text="Main Menu", font="Helvetica 18", command=lambda:[clear_window(),main_menu(root)])
        self.main_menu_btn.pack()

        # Header Labels
        self.course_label = Label(self.calc_frame, text="Course Name", font="Helvetica 20 bold")
        self.course_label.grid(row=0, column=0)
        self.grade_label = Label(self.calc_frame, text="Grade", font="Helvetica 20 bold")
        self.grade_label.grid(row=0, column=1)
        self.units_label = Label(self.calc_frame, text="# of Units", font="Helvetica 20 bold")
        self.units_label.grid(row=0, column=2)

        # Entry Box Frame
        self.entry_frame = Frame(self.calc_frame, borderwidth=0, highlightthickness=0)
        self.entry_frame.grid(row=1, column=0, columnspan=3, padx=(40,0), pady=(20,0), ipady=120)

        # Entry Canvas
        self.entry_canvas = Canvas(self.entry_frame, borderwidth=0, highlightthickness=0)
        self.entry_canvas.pack(side=LEFT, fill=BOTH, expand=1, ipadx=100)

        # Entry Scrollbar & Canvas Setup
        self.scrollbar = Scrollbar(self.entry_frame, orient=VERTICAL, command=self.entry_canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.entry_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.entry_canvas.bind("<Configure>", lambda e: self.entry_canvas.configure(scrollregion=self.entry_canvas.bbox("all")))

        # Inner Frame for Entry Boxes
        self.inner_frame = Frame(self.entry_canvas, borderwidth=0, highlightthickness=0)
        self.entry_canvas.create_window((0,0), window=self.inner_frame, anchor="nw")
        
        
        # Entry Creation Loop
        def entry_creation():
            for x in range(10):
                self.course_entry = Entry(self.inner_frame, font="Helvetica 18", justify="center", width=14)
                self.course_entry.grid(row=x, column=0, padx=(0,54), pady=(0,20))
                self.grade_entry = Entry(self.inner_frame, font="Helvetica 18", justify="center", width=10)
                self.grade_entry.grid(row=x, column=1, padx=(0,55), pady=(0,20))
                self.unit_entry = Entry(self.inner_frame, font="Helvetica 18", justify="center", width=10)
                self.unit_entry.grid(row=x, column=2, pady=(0,20))
                self.course_entries.append(self.course_entry)
                self.grade_entries.append(self.grade_entry)
                self.unit_entries.append(self.unit_entry)
        entry_creation()

        # Calculate Button
        self.calculate_btn = Button(self.btn_frame, text="Calculate", font="Helvetica 18", command=self.calculate, width=5, padx=100)
        self.calculate_btn.grid(row=0, column=0, padx=(40,0), pady=(150,10), columnspan=2)

        # Add Rows Button
        self.add_rows_btn = Button(self.btn_frame, text="Add Rows", font="Helvetica 18", command=self.add_rows, width=5, padx=28)
        self.add_rows_btn.grid(row=1, column=0, padx=(40,0))

        # Clear Rows Button
        self.clear_rows_btn = Button(self.btn_frame, text="Clear Rows", font="Helvetica 18", command=self.clear_rows, width=5, padx=28)
        self.clear_rows_btn.grid(row=1, column=1, padx=(10,0))

        # Export Data Button
        self.export_btn = Button(self.btn_frame, text="Export Data", font="Helvetica 18", command=self.save_data, width=5, padx=100)
        self.export_btn.grid(row=2, column=0, padx=(40,0), pady=(10,0), columnspan=2)

        # Results Labels
        self.gpa_label = Label(self.result_frame, text="Overall GPA: ", font="Helvetica 18", width=18)
        self.gpa_label.pack(pady=(60,5), anchor=CENTER)
        self.units_label = Label(self.result_frame, text="Total Units: ", font="Helvetica 18", width=18)
        self.units_label.pack(pady=(5,60))

    # Clear Rows Function
    def clear_rows(self):
        for entry in self.grade_entries:
            entry.delete(0, END)
        for entry in self.unit_entries:
            entry.delete(0, END)
        for entry in self.course_entries:
            entry.delete(0, END)

    # Add Rows Function
    def add_rows(self):
        self.num_rows = self.inner_frame.grid_size()[1]
        self.course_entry = Entry(self.inner_frame, font="Helvetica 18", justify="center", width=14)
        self.course_entry.grid(row=self.num_rows + 1, column=0, padx=(0,54), pady=(0,20))
        self.grade_entry = Entry(self.inner_frame, font="Helvetica 18",justify="center", width=10)
        self.grade_entry.grid(row=self.num_rows + 1, column=1, padx=(0,55), pady=(0,20))
        self.unit_entry = Entry(self.inner_frame, font="Helvetica 18", justify="center", width=10)
        self.unit_entry.grid(row=self.num_rows + 1, column=2)
        self.entry_canvas.configure(scrollregion=self.entry_canvas.bbox("all"))
        self.grade_entries.append(self.grade_entry)
        self.unit_entries.append(self.unit_entry)
        self.course_entries.append(self.course_entry)

    #GPA Calculate Function
    def calculate(self):
        self.grades = []
        self.unit = []
        self.total = 0
        self.unit_total = 0

        for entry in self.grade_entries:
            try:
                self.current_grade = float(entry.get())
                self.grades.append(self.current_grade)
            except ValueError:
                pass
        for entry in self.unit_entries:
            self.grade_weighting = entry.get()
            try:
                self.grade_weighting = float(self.grade_weighting)
                self.unit.append(self.grade_weighting)
            except ValueError:
                pass
        i = 0
        while i < len(self.grades):
            self.unit_total += self.unit[i]
            self.total += self.grades[i] * self.unit[i]
            i += 1
        try:
            self.average = self.total / self.unit_total
            self.gpa_label.configure(text="Overall GPA: " + str(round(self.average, 3)))
            self.units_label.configure(text="Total Units: " + str(self.unit_total))
        except ZeroDivisionError:
            pass
        except ValueError:
            self.gpa_label.configure(text="Overall GPA: ERROR")
            self.units_label.configure(text="Total Units: ERROR")
        if self.grades == [] and self.unit == []:
            self.gpa_label.configure(text="Overall GPA: ")
            self.units_label.configure(text="Total Units: ")

    def save_data(self):
        files = [('Text Document', '*.txt')]
        file = asksaveasfile(mode = 'w', filetypes = files, defaultextension = files)
        if file == None:
            return
        file_name = os.path.basename(file.name)
        root.title(file_name[:-4] + " - Grades2Date")
        self.file = open(file.name, "w")
        self.file.write("=====Courses=====\n")
        for entry in self.course_entries:
            self.course = entry.get()
            self.file.write(self.course + "--\n")
        self.file.write("=====Grades=====\n")
        for entry in self.grade_entries:
            self.grade = entry.get()
            self.file.write(self.grade + "--\n")
        self.file.write("=====Units=====\n")
        for entry in self.unit_entries:
            self.numunit = entry.get()
            self.file.write(self.numunit + "--\n")
        self.file.close()

    # Exit Confirmation
    root.protocol("WM_DELETE_WINDOW", on_closing)

# GPA page w/ imported data
class imported_gpa(gpa_page):
    def __init__(self, master, import_info):
        super(imported_gpa, self).__init__(master)
        print("imported info " + import_info)
        file_name = os.path.basename(import_info)
        root.title(file_name[:-4] + " - Grades2Date")
        file = open(import_info, "r")
        data = file.read()
        data_info_list = data.split("\n")
        courses_list = []
        grade_list = []
        unit_list = []
        for i in range(len(data_info_list)):
            if data_info_list[i] == "=====Grades=====":
                break
            if data_info_list[i] == "=====Courses=====":
                continue
            else:
                courses_list.append(data_info_list[i][:-2])
        
        for j in range(len(courses_list) + 1, len(data_info_list)):
            if data_info_list[j] == "=====Units=====":
                break
            if data_info_list[j] == "=====Grades=====":
                continue
            else:
                grade_list.append(data_info_list[j][:-2])
        
        for k in range(2*len(courses_list) + 2, len(data_info_list)):
            if data_info_list[k] == "":
                break
            if data_info_list[k] == "=====Units=====":
                continue
            else:
                unit_list.append(data_info_list[k][:-2])
        print(courses_list)
        print(grade_list)
        print(unit_list)
        file.close()
        def gpa_import():
            num_rows = 10
            if len(courses_list) > 10:
                num_rows = len(courses_list)
            for x in range(num_rows-1):
                self.course_entry = Entry(self.inner_frame, font="Helvetica 18", justify="center", width=14)
                self.course_entry.grid(row=x, column=0, padx=(0,54), pady=(0,20))
                self.course_entry.insert(0, courses_list[x])
                self.grade_entry = Entry(self.inner_frame, font="Helvetica 18", justify="center", width=10)
                self.grade_entry.grid(row=x, column=1, padx=(0,55), pady=(0,20))
                self.grade_entry.insert(0, grade_list[x])
                self.unit_entry = Entry(self.inner_frame, font="Helvetica 18", justify="center", width=10)
                self.unit_entry.grid(row=x, column=2, pady=(0,20))
                self.unit_entry.insert(0,unit_list[x])
                self.course_entries.append(self.course_entry)
                self.grade_entries.append(self.grade_entry)
                self.unit_entries.append(self.unit_entry)
        gpa_import()
        
homepage = main_menu(root)
root.mainloop()