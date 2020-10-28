# Importing required modeules
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog
import os
import tkinter.messagebox
from tkinter import font,ttk
# --------------------------------------------------------------------------------------
# Global Variables Space
file_name = None
PROGRAM_NAME = "MarcoEditor"
# --------------------------------------------------------------------------------------

root = tk.Tk()
# Main Code
root.title("MarcoEditor")
root.wm_iconbitmap('icon.png')
root.geometry("850x450")
root.minsize(250, 300)
# --------------------------------------------------------------------------------------
# Imorting icons and images
new_icon = ImageTk.PhotoImage(Image.open("menu_icons/new.png"))
save_icon = ImageTk.PhotoImage(Image.open("menu_icons/save.png"))
open_icon = ImageTk.PhotoImage(Image.open("menu_icons/open.png"))
saveas_icon = ImageTk.PhotoImage(Image.open("menu_icons/saveas.png"))
exit_icon = ImageTk.PhotoImage(Image.open("menu_icons/exit.png"))
cut_icon = ImageTk.PhotoImage(Image.open("menu_icons/cut.png"))
copy_icon = ImageTk.PhotoImage(Image.open("menu_icons/copy.png"))
paste_icon = ImageTk.PhotoImage(Image.open("menu_icons/paste.png"))
undo_icon = ImageTk.PhotoImage(Image.open("menu_icons/undo.png"))
redo_icon = ImageTk.PhotoImage(Image.open("menu_icons/redo.png"))


# --------------------------------------------------------------------------------------

# Defining Functions
def cut():
    content_text.event_generate("<<Cut>>")
    return 'break'


def copy():
    content_text.event_generate("<<Copy>>")
    return 'break'


def paste():
    content_text.event_generate("<<Paste>>")
    return 'break'


def undo():
    content_text.event_generate("<<Undo>>")
    return 'break'


def redo(event=None):
    content_text.event_generate("<<Redo>>")
    return 'break'


def selectall(event=None):
    content_text.tag_add('sel', '1.0', 'end')
    return 'break'


def find_text(event=None):
    search_toplevel = tk.Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    tk.Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = tk.Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = tk.IntVar()
    tk.Checkbutton(search_toplevel, text="Ignore Case", variable=ignore_case_value).grid(row=1, column=1, sticky='e',
                                                                                         padx=2, pady=2)
    tk.Button(search_toplevel, text="Find ALL", underline=0,
              command=lambda: search_output(search_entry_widget.get(), ignore_case_value.get(), content_text,
                                            search_toplevel, search_entry_widget)).grid(row=0, column=2,
                                                                                        sticky='e' + 'w', padx=2,
                                                                                        pady=2)

    def close_search_window():
        content_text.tag_remove('match', '1.0', tk.END)
        search_toplevel.destroy()

    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return 'break'


def search_output(needle, if_ignore_case, content_text, search_toplevel, search_box):
    content_text.tag_remove('match', '1.0', tk.END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos, nocase=if_ignore_case, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config('match', foreground='red', background='yellow')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))


def new_file(event=None):
    root.title("Untitled-MacroEditor")
    global file_name
    file_name = None
    content_text.delete(1.0, tk.END)


def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                         filetypes=[("AllFiles", "*.*"), ("Text Document", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        content_text.delete(1.0, tk.END)
        root.title("{}-{}".format(os.path.basename(file_name), PROGRAM_NAME))
        with open(file_name) as file:
            content_text.insert(1.0, file.read())


def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass


def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("AllFiles", "*.*"), ("Text Document", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{}-{}'.format(os.path.basename(file_name), PROGRAM_NAME))
    return 'break'

def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return 'break'


def help_box(event=None):
    tkinter.messagebox.showinfo("Help","Use the White Space to write your content and use the menu options to perform operations on your content.")

def about_box(event=None):
    tkinter.messagebox.showinfo("About","Developed by YASH DABHADE . COPYRIGHTS 2020")

def exit_box(event=None):
    if tk.messagebox.askokcancel("Really Quit?","DO YOU WANT TO EXIT ?"):
        root.destroy()


def get_line_numbers():
    output=""
    if show_line_number.get():
        row,col=content_text.index('end').split('.')
        for i in range(1,int(row)):
            output+=str(i)+'\n'
    return output

def update_line_numbers(event=None):
    line_numbers=get_line_numbers()
    linenumber_bar.config(state='normal')
    linenumber_bar.delete('1.0','end')
    linenumber_bar.insert('1.0',line_numbers)
    linenumber_bar.config(state='disabled')

def show_cursor_info_fun():
    if show_cursor_info.get():
        cursor_info_bar.pack(expand=tk.NO,fill=None,side=tk.RIGHT,anchor='se')
    else:
        cursor_info_bar.pack_forget()

def update_cursorinfo_bar(event=None):
    row,col=content_text.index(tk.INSERT).split('.')
    line_num,col_num=str(int(row)),str(int(col)+1)
    infotext="Line: {0} | Column: {1}".format(line_num,col_num)
    cursor_info_bar.config(text=infotext)

def on_content_changed(event=None):
    update_line_numbers()
    update_cursorinfo_bar()




def highlight_line(interval=100):
    content_text.tag_remove("active_line",1.0,"end")
    content_text.tag_add('active_line','insert linestart','insert lineend+1c')
    content_text.after(interval,toogle_highlight)

def undo_highlight():
    content_text.tag_remove("active_line",1.0,'end')


def toogle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()

def changetheme(event=None):
    selected_theme=theme_choice.get()
    fg_bg_colors=color_schemes.get(selected_theme)
    fgc,bgc=fg_bg_colors.split('.')
    content_text.config(fg=fgc,bg=bgc)

# --------------------------------------------------------------------------------------

# Making Menu Bar
menu_bar = tk.Menu(root)
# --------------------------------------------------------------------------------------

# Making File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)

file_menu.add_command(underline=0, label="New", accelerator='Ctrl+N', compound='left', image=new_icon,command=new_file)
file_menu.add_separator()
file_menu.add_command(label="Open", accelerator='Ctrl+O', compound='left', image=open_icon,command=open_file)
file_menu.add_command(label="Save", accelerator='Ctrl+S', compound='left', image=save_icon,command=save)
file_menu.add_command(label="SaveAs", accelerator='Shift+Ctrl+S', compound='left', image=saveas_icon,command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator='Alt+F4', compound='left', image=exit_icon,command=exit_box)
# Cascading File menu in the menu Bar
menu_bar.add_cascade(label="File", menu=file_menu)
# --------------------------------------------------------------------------------------
# making Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)

edit_menu.add_command(label="Undo", accelerator='Ctrl+Z', compound='left', image=undo_icon, command=undo)
edit_menu.add_separator()
edit_menu.add_command(label="Redo", accelerator='Ctrl+Y', compound='left', image=redo_icon, command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", accelerator='Ctrl+X', compound='left', image=cut_icon, command=cut)
edit_menu.add_command(label="Copy", accelerator='Ctrl+C', compound='left', image=copy_icon, command=copy)
edit_menu.add_command(label="Paste", accelerator='Ctrl+V', compound='left', image=paste_icon, command=paste)
edit_menu.add_command(label="Find", accelerator='Ctrl+F', underline=0, command=find_text)
edit_menu.add_command(label="SelectAll", accelerator='Ctrl+A', underline=7, command=selectall)
# Cascading Edit Menu in the Menu Bar
menu_bar.add_cascade(label="Edit", menu=edit_menu)
# --------------------------------------------------------------------------------------
# making View Menu
view_menu = tk.Menu(menu_bar, tearoff=0)
# TODO -Add View Menu Items
show_line_number = tk.IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label="Show Line Numbers", variable=show_line_number)
show_cursor_info = tk.IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label="Show Cursor Location At bottom", variable=show_cursor_info,command=show_cursor_info_fun)
to_highlight_line = tk.BooleanVar()
view_menu.add_checkbutton(label="Highlight Current Line", onvalue=1, offvalue=0, variable=to_highlight_line,command=toogle_highlight)
# Making Themes Menu is View menu
# --------------------------------------------------------------------------------------
themes_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Themes", menu=themes_menu)
# Defining color scheme

"""
color scheme is defined with dictionary elements like -
        theme_name : foreground_color.background_color
"""
color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Dark': '#c4c4c4.#2d2d2d',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
    'Monokai':'#d3b774.#474747',
    'Night Blue':'#ededed.#6b9dc2'
}
theme_choice = tk.StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(label=k, variable=theme_choice,command=changetheme)
# Cascading VIew Menu in the Menu Bar
menu_bar.add_cascade(label="View", menu=view_menu)

# --------------------------------------------------------------------------------------

# making Help Menu
about_menu = tk.Menu(menu_bar, tearoff=0)

about_menu.add_command(label="About",command=about_box)
about_menu.add_command(label="Help",command=help_box)
# Cascading VIew Menu in the Menu Bar
menu_bar.add_cascade(label="About", menu=about_menu)
# --------------------------------------------------------------------------------------

# Adding Menu_bar in root
root.config(menu=menu_bar)
# --------------------------------------------------------------------------------------

# Making Shortcut Bar
shorcut_bar = tk.Frame(root, height=25, background='light sea green')
shorcut_bar.pack(expand='no', fill='x')
#Creating Shortcut Buttons
icons=('new_file','open_file','save','cut','copy','paste','undo','redo','find_text')
for i,icon in enumerate(icons):
    tool_bar_icon=tk.PhotoImage(file='icons/{}.png'.format(icon))
    cmd=eval(icon)
    tool_bar=tk.Button(shorcut_bar,image=tool_bar_icon,command=cmd)
    tool_bar.image=tool_bar_icon
    tool_bar.pack(side="left")

#-------------------------------------------------------------------------------------------------------
#Making Customize Bar
customize_bar=tk.Frame(root,height=40,background='lightcyan')
customize_bar.pack(expand='no',fill='x')

#MAking font box_______
font_tuple=tk.font.families()
font_family=tk.StringVar()
font_box=ttk.Combobox(customize_bar,width=30,textvariable=font_family,state='readonly')
font_box['values']=font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0,column=0,ipady=10,padx=10)

#Making Size Box
size_var=tk.IntVar()
font_size=ttk.Combobox(customize_bar,width=10,textvariable=size_var,state='readonly')
font_size['values']=tuple(range(2,120,2))
font_size.current(7)
font_size.grid(row=0,column=2,ipady=10,padx=10)

#Making Bold Button
bold_icon=ImageTk.PhotoImage(Image.open('icons2/bold.png'))
bold_btn=ttk.Button(customize_bar,image=bold_icon)
bold_btn.grid(row=0,column=5,padx=2,pady=5)

#MAking Italic Button
italic_icon=ImageTk.PhotoImage(Image.open('icons2/italic.png'))
italic_btn=ttk.Button(customize_bar,image=italic_icon)
italic_btn.grid(row=0,column=6,padx=2,pady=5)

#MAking UnderLine Button
underline_icon=ImageTk.PhotoImage(Image.open('icons2/underline.png'))
underline_btn=ttk.Button(customize_bar,image=underline_icon)
underline_btn.grid(row=0,column=7,padx=2,pady=5)

#MAking color button
color_icon=ImageTk.PhotoImage(Image.open('icons2/color.png'))
color_btn=ttk.Button(customize_bar,image=color_icon)
color_btn.grid(row=0,column=8,padx=22,pady=5)

#MAking align left
alignleft_icon=ImageTk.PhotoImage(Image.open('icons2/alignleft.png'))
alignleft_btn=ttk.Button(customize_bar,image=alignleft_icon)
alignleft_btn.grid(row=0,column=10,padx=5,pady=5)

#MAking align center
aligncenter_icon=ImageTk.PhotoImage(Image.open('icons2/aligncenter.png'))
aligncenter_btn=ttk.Button(customize_bar,image=aligncenter_icon)
aligncenter_btn.grid(row=0,column=11,padx=5,pady=5)

#MAking align right
alignright_icon=ImageTk.PhotoImage(Image.open('icons2/alignright.png'))
alignright_btn=ttk.Button(customize_bar,image=alignright_icon)
alignright_btn.grid(row=0,column=12,padx=5,pady=5)



# --------------------------------------------------------------------------------------



# MakingLineNumberBar
linenumber_bar = tk.Text(root, width=4, padx=3, takefocus=0, border=0, background='lightblue', state='disabled',
                         wrap='none')
linenumber_bar.pack(side='left', fill='y')
# --------------------------------------------------------------------------------------



# Adding Text area
content_text = tk.Text(root, wrap='word', undo=1,insertbackground="red")
content_text.pack(expand='yes', fill='both')

#Configure font family and fot size
current_font_family='Arial'
current_font_size=12
def change_font(root):
    global current_font_size
    global current_font_family
    current_font_size=font_size.get()
    current_font_family=font_family.get()
    content_text.configure(font=(current_font_family,current_font_size))
content_text.configure(font=(current_font_family,current_font_size))
font_box.bind("<<ComboboxSelected>>",change_font)
font_size.bind("<<ComboboxSelected>>",change_font)

# content_text.configure(font=("Arial",12))

# --------------------------------------------------------------------------------------
# Adding ScrollBar
scroll_bar = tk.Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side="right", fill='y')
# --------------------------------------------------------------------------------------


#Adding cursor Info Bar
cursor_info_bar=tk.Label(content_text,text="Line: 1 || Column: 1")
cursor_info_bar.pack(expand=tk.NO,fill=None,side=tk.RIGHT,anchor='se')
# --------------------------------------------------------------------------------------

# Handling Shortcuts
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Control-A>', selectall)
content_text.bind('<Control-a>', selectall)
content_text.bind('<Control-F>', find_text)
content_text.bind('<Control-f>', find_text)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)
content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Any-KeyPress>',on_content_changed)
content_text.bind('<Alt-F4>',exit_box)
#Deffining active line
content_text.tag_configure('active_line', background='lightgrey')
# --------------------------------------------------------------------------------------

new_file()
root.protocol('WM_DELETE_WINDOW', exit_box)

# main Loop
root.mainloop()
