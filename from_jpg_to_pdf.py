##### -------------------------------------------------------------------------
##### from jpg to pdf
##### version: 2.0
##### author: Filippo
##### -------------------------------------------------------------------------

import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# VARIABLE
images = list()  # global  # it'll became a tuple
valid_extensions = ['png', 'jpg', 'jpeg', 'gif', 'ico', 'tiff', 'bmp', 'pdn']

# FUNCTIONS
def create_thumbs(x):  # create thumb image for application using PIL
    img = Image.open(x)
    img = img.resize((96, 96), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img

def create_pdf():
    global images
    images_conv = []
    # convert images in a PIL format
    for el in images:
        el_1 = Image.open(el)
        el_2 = el_1.convert('RGB')
        images_conv.append(el_2)
    # get user name destination of the file
    name_file = filedialog.asksaveasfile(defaultextension='pdf',
                                         initialdir=r'C:\Users\{0}\Desktop'
                                         .format(os.getlogin())
                                         )
    # check if file destination exist
    if name_file is not None:
        try:  # try the save as pdf command of PIL
            if len(images_conv) == 1:  # if only one image
                images_conv[0].save(name_file.name)
            else:  # fi multiple images
                images_conv[0].save(name_file.name, save_all=True,
                                    append_images=images_conv[1:])

            messagebox.showinfo(title='Info', message='Operacao kaba diritu')

            root.destroy()  # close the application
            
        except Exception as e:
            messagebox.showerror(title='Error', message=e)


# CLASSES 
# class tkinter
class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        
        self.set_option()
        self.create_menu()
        self.create_label()
    
    def set_option(self):
        self.master.title('Create PDF from image')
        self.master.geometry('700x200+300+150')
        self.master.resizable(0,0)

    def create_menu(self):  # create the menubar widget
        self.menubar = tk.Menu(self.master)
        
        self.menubar.add_command(label='Open',
                                 command=lambda: self.show_images()
                                 )
        self.menubar.add_command(label='Convert',
                                 command= lambda: create_pdf(),
                                 state=('disabled')
                                 )
        self.menubar.add_command(label='Help',
                                 command=lambda: os.startfile('user guide.pdf')
                                 )

        self.master.config(menu=self.menubar)

    def create_label(self):

        self.body = tk.Frame(self.master)
        self.body.pack(fill='both', expand=1, anchor='nw')

        # create temporary lbel for strart the application
        self.central_label = tk.Label(self.body,
                                      text='+\nClick to select images',
                                      font=('Helvetica', 18, 'bold'),
                                      foreground='gray', background='white',
                                      justify='center')
        self.central_label.pack(expand=1, fill='both', pady=5, padx=5)

        self.central_label.bind('<Button>', lambda a: self.show_images())
        
    def create_body(self):
        # create a canva and aa scrollable frame inside of it
        self.canva = tk.Canvas(self.body, background='white')
        self.canva.pack(expand=1, fill='both', anchor='nw')
        # frame is packed as interior canva's window
        self.inner_frame = tk.Frame(self.canva, background='white')
        self.interior_wd = self.canva.create_window(5, 5,
                                                    window=self.inner_frame,
                                                    anchor='nw')
        
    def scroll_and_option(self):
        # creaate the scroller and set configuration
        self.scroll = ttk.Scrollbar(self.body, orient='horizontal',
                                        command=self.canva.xview)
        self.scroll.pack(expand=0, fill='x')

        self.canva.configure(xscrollcommand=self.scroll.set)

        self.canva.xview_moveto(0)

        # track changes to the canvas and frame width and sync them,
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (self.inner_frame.winfo_reqwidth(),
                    self.inner_frame.winfo_reqheight())
            self.canva.config(scrollregion="0 0 %s %s" % size)
            if self.inner_frame.winfo_reqheight() != self.canva.winfo_height():
                # update the canvas's height to fit the inner frame
                self.canva.config(height=self.inner_frame.winfo_reqheight())

        self.inner_frame.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.inner_frame.winfo_reqheight() != self.canva.winfo_height():
                # update the inner frame's height to fill the canvas
                self.canva.itemconfigure(self.interior_wd,
                                         height=self.canva.winfo_height())

        self.canva.bind('<Configure>', _configure_canvas)
        
    def show_images(self, event=None):
        global images
        # disable the menucommand to avoid multiple widget creation
        self.menubar.entryconfig('Open', state='disabled')
        # get images from the user
        open_images = filedialog.askopenfilenames(
            multiple=True,
            initialdir=r'C:\Users\{0}\Documents'.format(os.getlogin())
            )
        # check if the user selected images
        validation = 0
        for el in open_images:
            if el[-3:] not in valid_extensions:
                messagebox.showerror(title='Error',
                                     message='Not only images selected')
                validation += 1
        # check if user selected something
        if open_images != '' and validation == 0:
            images = open_images  # copy selected images to the global variable
            # destroy the temporary label
            self.central_label.destroy()
            # create the canvas and populate it
            self.create_body()
            self.populate()
            # add conversion button
            ttk.Button(self.master, text='Convert',
                       command= lambda: create_pdf()
                       ).pack(pady=2)
            # enable conversion button on the menubar
            self.menubar.entryconfig('Convert', state='normal')

    def populate(self):
        global images
        
        count_column = 0
        
        for img in images:
            thumb_img = create_thumbs(img)  # create thumbs
            # get the only name of the file ndo not the all path
            name_img = img.split('/')[-1][:-4]
            # add two label one with the thumb image and one with the name
            img_label = ttk.Label(self.inner_frame, image=thumb_img)
            img_label.image = thumb_img
            img_label.grid(row=0, column=count_column, pady=2, padx=5)
            
            text_label = ttk.Label(self.inner_frame, text=name_img).grid(
                row=1, column=count_column, padx=5, pady=2)
            
            count_column += 1

        if count_column > 6:  # if images are more of 6 add the scrollbar
            self.scroll_and_option()
        else:
            self.canva.config(height=100)  # reset the size of the canvas


# APPLICATION
if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
