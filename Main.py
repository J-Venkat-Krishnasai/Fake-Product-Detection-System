from tkinter import *
import tkinter
from Block import *
from Blockchain import *
from PIL import Image, ImageTk
import PIL.Image
import imageio
import threading

# Initialize the main Tkinter window
main = Tk()
main.geometry("1250x700+0+0")
main.title("Fake Product Identification With QR-Code Using Blockchain")

# Set the video background
#video_name = "bg/home.mp4" 
#video = imageio.get_reader(video_name)

'''
def stream(label):
    while True:
        for image in video.iter_data():
            frame_image = ImageTk.PhotoImage(PIL.Image.fromarray(image))
            label.config(image=frame_image)
            label.image = frame_image

my_label = tkinter.Label(main)
my_label.pack()
thread = threading.Thread(target=stream, args=(my_label,))
thread.daemon = 1
thread.start()
'''

# Define functions for the buttons
def run1():
    main.after(10000, lambda: main.destroy())
    import login

def run2():
    main.destroy()
    import UserMain

def run3():
    main.destroy()
    import userLogin

def quiti():
    main.destroy()

# Configure the title label
main.wm_attributes('-transparentcolor', '#ab23ff')
font = ('times', 30, 'bold')
title = Label(main, text='Fake Product Identification With QR-Code Using Blockchain')
title.config(bg='black', fg='white', bd=1, highlightbackground="cyan", highlightthickness=1)  
title.config(font=font)           
title.config(height=3, width=50)       
title.place(x=40,y=40)

font1 = ('times', 13, 'bold')

# Add buttons to the main window
saveButton = tkinter.Button(main, text="Manufacturer Login", bg="#8ECAE6", fg="black", command=run1)
saveButton.place(x=691, y=420)
saveButton.config(font=font1, height=2)

searchButton = tkinter.Button(main, text="User Login", bg="#8ECAE6", fg="black", command=run3)
searchButton.place(x=1025, y=420)
searchButton.config(font=font1, height=2)

closeButton = tkinter.Button(main, text="Exit The Page", command=quiti, bg="#C6AC8F")
closeButton.place(x=870, y=550)
closeButton.config(font=font1)

# Display the side photo
side_image_path = "bg\\main-page.png"
side_image = Image.open(side_image_path)
side_image = side_image.resize((450, 420), Image.Resampling.LANCZOS)  # Resize image if necessary
side_image_tk = ImageTk.PhotoImage(side_image)
side_label = Label(main, image=side_image_tk)
side_label.image = side_image_tk  # Keep a reference to avoid garbage collection
side_label.place(x=120, y=200)  # Adjust the position as needed
'''
side_image_path = "bg\\manufacturer-icon1.jpeg"
side_image = Image.open(side_image_path)
side_image = side_image.resize((100, 100), Image.Resampling.LANCZOS)  # Resize image if necessary
side_image_tk = ImageTk.PhotoImage(side_image)
side_label = Label(main, image=side_image_tk)
side_label.image = side_image_tk  # Keep a reference to avoid garbage collection
side_label.place(x=720, y=300) 


side_image_path = "bg\\user-icon1.jpeg"
side_image = Image.open(side_image_path)
side_image = side_image.resize((100, 100), Image.Resampling.LANCZOS)  # Resize image if necessary
side_image_tk = ImageTk.PhotoImage(side_image)
side_label = Label(main, image=side_image_tk)
side_label.image = side_image_tk  # Keep a reference to avoid garbage collection
side_label.place(x=1020, y=300) 
'''
# Set the background color of the main window
main.config(bg='cornflower blue')
main.mainloop()
