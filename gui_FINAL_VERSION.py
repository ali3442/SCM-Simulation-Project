from tkinter import *
from PIL import Image, ImageTk
from main_project_FINAL_VERSION import LoginLogic

page = Tk()
page.geometry("650x400")
page.title("Log In Page")

img = Image.open(r"C:\Users\alika\OneDrive\Desktop\Collage\mini_project\backgroundIMG.jpg")
img = img.resize((650, 400))
bg = ImageTk.PhotoImage(img)
background_label = Label(page, image=bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

label = Label(page, text="LOG IN", font="Jokerman 40 bold", fg="white", bg="black")
label.grid(row=0, column=2, ipadx=20, ipady=20, sticky="we")

label2 = Label(page, text="Email: ", font="Helvetica 10 bold", fg="white", bg="black")
label2.grid(row=1, column=0, padx=10) 

entry1 = Entry(page, bg="white", fg="black")
entry1.grid(row=1, column=1)

label3 = Label(page, text="Password:", font="Helvetica 10 bold", fg="white", bg="black")
label3.grid(row=1, column=2, pady=10)

entry2 = Entry(page, bg="white", fg="black", show="*")
entry2.grid(row=1, column=3, pady=20)

checkbox = Checkbutton(page, text="ARE YOU READY!", font="Jokerman 10 bold", fg="white", bg="black")
checkbox.grid(row=2, column=1, columnspan=3)

logic = LoginLogic(entry1, entry2, page)

button1 = Button(page, text="LOG IN", font="Rupee 20 bold", fg="white", bg="black", command=logic.login)
button1.grid(row=3, column=1, columnspan=3, pady=20)

page.mainloop()
pass
