'''
from tkinter import messagebox, Tk, Label, Button, Entry, Text, Scrollbar, Frame, Toplevel
from tkinter.ttk import Treeview
from PIL import ImageTk, Image, ImageDraw, ImageFont, ImageOps
import PIL.Image
import qrcode
import threading
from Blockchain import Blockchain
import os
import datetime
from hashlib import sha256
import imageio
import pickle
from login import logged_in_user_email

main = Tk()
main.title("Fake Product Identification With QR-Code Using Blockchain")
main.geometry("1250x700+0+0")

#video_name = "bg\\home.mp4"
#video = imageio.get_reader(video_name)

def stream(label):
    while True:
        for image in video.iter_data():
            frame_image = ImageTk.PhotoImage(PIL.Image.fromarray(image))
            label.config(image=frame_image)
            label.image = frame_image

my_label = Label(main)
my_label.pack()
thread = threading.Thread(target=stream, args=(my_label,))
thread.daemon = 1
thread.start()

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def get_current_admin():
    return logged_in_user_email

current_admin = get_current_admin()
if not current_admin:
    messagebox.showerror("Error", "Could not fetch the current admin from the database.")
    main.destroy()

def addProduct():
    text.delete('1.0', 'end')
    pid = tf1.get()
    name = tf2.get()
    user = tf3.get()
    address = tf4.get()
    
    # Generate a digital signature for the product
    digital_signature = sha256(os.urandom(32)).hexdigest()
    user_email = current_admin
    
    # Generate QR code for the product
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRcode.add_data(digital_signature)
    QRcode.make(fit=True)
    QRimg = QRcode.make_image().convert('RGBA')

    #watermarking : Adding the company na,e as a watermark to the qr
    watermark = Image.new('RGBA', QRimg.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark)
    font = ImageFont.truetype("arial.ttf", 40)
    text_bbox = draw.textbbox((0, 0), user, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_position = ((QRimg.size[0] - text_width) // 2, (QRimg.size[1] - text_height) // 2)
    draw.text(text_position, user, fill=(0, 0, 0, 128), font=font)
    QRimg = Image.alpha_composite(QRimg, watermark)
    
    QRimg = QRimg.convert('RGB')
    
    border_color = (0, 0, 0)
    border_width = 7
    QRimg_with_border = ImageOps.expand(QRimg, border=border_width, fill=border_color)
    
    # Save the QR code image
    if not os.path.exists('original_barcodes'):
        os.makedirs('original_barcodes')
    
    file_path = 'original_barcodes' + os.sep + str(pid) + 'productQR.png'
    QRimg_with_border.save(file_path)
    
    if pid and name and user and address:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f"{pid}#{name}#{user}#{address}#{current_time}#{digital_signature}#{user_email}"
        blockchain.add_new_transaction(data)
        blockchain.mine()
        blockchain.save_object(blockchain, 'blockchain_contract.txt')
        
        # Display information in the text widget
        text.insert('end', "Blockchain Previous Hash: {}\n".format(blockchain.last_block.previous_hash))
        text.insert('end', "Block No: {}\n".format(blockchain.last_block.index))
        text.insert('end', "Product QR-code no: {}\n".format(digital_signature))
        
        # Display the QR code image
        img2 = Image.open('original_barcodes' + os.sep + str(pid) + 'productQR.png')
        load = img2.resize((150, 150))
        render = ImageTk.PhotoImage(load)
        img = Label(main, image=render)
        img.image = render  # Keep a reference to prevent image from being garbage collected
        img.place(x=190, y=450)
        
        # Clear entry fields
        tf1.delete(0, 'end')
        tf2.delete(0, 'end')
        tf3.delete(0, 'end')
        tf4.delete(0, 'end')
        
        messagebox.showinfo("QR Code Generator", "Congratulations,  Your product is saved successfully & a QR Code is generated.")
    else:
        text.insert('end', "Please enter all details\n")

def searchProduct():
    # Create a new window to display the product list
    new_window = Toplevel(main)
    new_window.title("Product List")
    new_window.geometry("1000x600")
    new_window.config(bg="#DCDCDD")  # Set the transparency color to match

    
    product_tree = Treeview(new_window, columns=('Product ID', 'Product Name', 'Company/User Details', 'Address Details', 'Registered Date & Time', 'QR Code'), show='headings')
    product_tree.heading('Product ID', text='Product ID')
    product_tree.heading('Product Name', text='Product Name')
    product_tree.heading('Company/User Details', text='Company/User Details')
    product_tree.heading('Address Details', text='Address Details')
    product_tree.heading('Registered Date & Time', text='Registered Date & Time')
    product_tree.heading('QR Code', text='QR Code')
    product_tree.pack(fill='both', expand=True)
    
    showQRButton = Button(new_window, text="Show QR Code", command=lambda: showQR(product_tree))
    showQRButton.pack()

    # Fetch and display products added by the current admin
    for block in blockchain.chain:
        for data in block.transactions:
            arr = data.split("#")
            if len(arr)>=7 and arr[6] == current_admin:  # Only show products added by the current admin
                product_tree.insert('', 'end', values=(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5]))

def showQR(product_tree):
    selected_item = product_tree.selection()
    if selected_item:
        item = product_tree.item(selected_item)
        qr_code = item['values'][5]
        pid = item['values'][0]
        
        # Generate and save the QR code image
        QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        QRcode.add_data(qr_code)
        QRcode.make(fit=True)
        QRimg = QRcode.make_image().convert('RGBA')

        #watermarking : Adding the company na,e as a watermark to the qr
        watermark = Image.new('RGBA', QRimg.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark)
        font = ImageFont.truetype("arial.ttf", 40)
        text_bbox = draw.textbbox((0, 0), item['values'][2], font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        text_position = ((QRimg.size[0] - text_width) // 2, (QRimg.size[1] - text_height) // 2)
        draw.text(text_position, item['values'][2], fill=(0, 0, 0, 128), font=font)
        QRimg = Image.alpha_composite(QRimg, watermark)
    
        QRimg = QRimg.convert('RGB')
    
        border_color = (0, 0, 0)
        border_width = 7
        QRimg_with_border = ImageOps.expand(QRimg, border=border_width, fill=border_color)

    
        file_path = 'original_barcodes' + os.sep + str(pid) + 'productQR.png'
        QRimg_with_border.save(file_path)
        
        # Display the QR code image
        img2 = Image.open('original_barcodes' + os.sep + str(pid) + 'productQR.png')
        load = img2.resize((150, 150))
        render = ImageTk.PhotoImage(load)
        img = Label(product_tree, image=render)
        img.image = render  # Keep a reference to prevent image from being garbage collected
        img.place(x=600, y=300)
    else:
        messagebox.showinfo("Show QR Code", "Please select a product to show its QR code.")

def openHome():
    main.destroy()
    import Main    
    
scanButton = Button(main, text="Logout",bg="#C6AC8F", command=openHome)
scanButton.place(x=1100,y=160)

main.wm_attributes('-transparentcolor', '#ab23ff')
font = ('times', 30, 'bold')
title = Label(main, text='Fake Product Identificaion With QR-Code Using BlockChain')
title.config(bg='black', fg='white', bd=1, highlightbackground="cyan", highlightthickness=1)  
title.config(font=font)           
title.config(height=3, width=50)       
title.place(x=40,y=5)   

font = ('times', 13, 'bold')
l1 = Label(main, text='Product ID :', font=font, bg="#DCDCDD")
l1.place(x=180,y=200)

tf1 = Entry(main, width=80, font=font, bg="#DCDCDD")
tf1.place(x=370,y=200)

l2 = Label(main, text='Product Name :', font=font, bg="#DCDCDD")
l2.place(x=180,y=250)

tf2 = Entry(main, width=80, font=font, bg="#DCDCDD")
tf2.place(x=370,y=250)

l3 = Label(main, text='Company/User Details :', font=font, bg="#DCDCDD")
l3.place(x=180,y=300)

tf3 = Entry(main, width=80, font=font, bg="#DCDCDD")
tf3.place(x=370,y=300)

l4 = Label(main, text='Address Details :', font=font, bg="#DCDCDD")
l4.place(x=180,y=350)

tf4 = Entry(main, width=80, font=font, bg="#DCDCDD")
tf4.place(x=370,y=350)

saveButton = Button(main, text="Save Product with Blockchain Entry", command=addProduct, font=font, bg="#DCDCDD")
saveButton.place(x=420,y=400)

searchButton = Button(main, text="Retrieve Product Data", command=searchProduct, font=font, bg="#DCDCDD")
searchButton.place(x=850,y=400)

font1 = ('times', 13, 'bold')
text = Text(main, height=10, width=80, font=font1, bg="#DCDCDD")
scroll = Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=372, y=450)

main.config(bg='cornflower blue')
main.mainloop()
'''

from tkinter import messagebox, Tk, Label, Button, Entry, Text, Scrollbar, Frame, Toplevel
from tkinter.ttk import Treeview
from PIL import ImageTk, Image, ImageDraw, ImageFont, ImageOps
import PIL.Image
import qrcode
import threading
from Blockchain import Blockchain
import os
import datetime
from hashlib import sha256
import pickle
from login import logged_in_user_email
import mysql.connector
import sys
import subprocess

# MySQL DB connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sairaj12",  # Change to your MySQL root password
    database="fakeproductdb"
)
cursor = db.cursor()

main = Tk()
main.title("Fake Product Identification With QR-Code Using Blockchain")
main.geometry("1250x700+0+0")

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)

def get_current_admin():
    return logged_in_user_email

current_admin = get_current_admin()
if not current_admin:
    messagebox.showerror("Error", "Could not fetch the current admin from the database.")
    main.destroy()

def product_id_exists(pid):
    query = "SELECT COUNT(*) FROM products WHERE product_id = %s"
    cursor.execute(query, (pid,))
    count = cursor.fetchone()[0]
    return count > 0

def addProduct():
    text.delete('1.0', 'end')
    pid = tf1.get().strip()
    name = tf2.get().strip()
    user = tf3.get().strip()
    address = tf4.get().strip()

    if not (pid and name and user and address):
        messagebox.showerror("Error", "Please enter all product details.")
        return

    if product_id_exists(pid):
        messagebox.showerror("Error", "Product ID already exists! Please use a unique ID.")
        return

    digital_signature = sha256(os.urandom(32)).hexdigest()
    user_email = current_admin

    # Generate QR code
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRcode.add_data(digital_signature)
    QRcode.make(fit=True)
    QRimg = QRcode.make_image().convert('RGBA')

    watermark = Image.new('RGBA', QRimg.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark)
    font = ImageFont.truetype("arial.ttf", 40)
    text_bbox = draw.textbbox((0, 0), user, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_position = ((QRimg.size[0] - text_width) // 2, (QRimg.size[1] - text_height) // 2)
    draw.text(text_position, user, fill=(0, 0, 0, 128), font=font)
    QRimg = Image.alpha_composite(QRimg, watermark)

    QRimg = QRimg.convert('RGB')
    border_color = (0, 0, 0)
    border_width = 7
    QRimg_with_border = ImageOps.expand(QRimg, border=border_width, fill=border_color)

    if not os.path.exists('original_barcodes'):
        os.makedirs('original_barcodes')
    file_path = 'original_barcodes' + os.sep + str(pid) + 'productQR.png'
    QRimg_with_border.save(file_path)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = f"{pid}#{name}#{user}#{address}#{current_time}#{digital_signature}#{user_email}"
    blockchain.add_new_transaction(data)
    blockchain.mine()
    blockchain.save_object(blockchain, 'blockchain_contract.txt')

    try:
        insert_query = """
            INSERT INTO products (product_id, name, user_details, address_details, date_time, qr_code, registered_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (pid, name, user, address, current_time, digital_signature, user_email))
        db.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to insert into database: {err}")
        return

    text.insert('end', f"Blockchain Previous Hash: {blockchain.last_block.previous_hash}\n")
    text.insert('end', f"Block No: {blockchain.last_block.index}\n")
    text.insert('end', f"Product QR-code no: {digital_signature}\n")

    img2 = Image.open(file_path)
    load = img2.resize((150, 150))
    render = ImageTk.PhotoImage(load)
    img = Label(main, image=render)
    img.image = render
    img.place(x=190, y=450)

    tf1.delete(0, 'end')
    tf2.delete(0, 'end')
    tf3.delete(0, 'end')
    tf4.delete(0, 'end')

    messagebox.showinfo("QR Code Generator", "Product saved and QR Code generated successfully.")

def searchProduct():
    new_window = Toplevel(main)
    new_window.title("Product List")
    new_window.geometry("1000x600")
    new_window.config(bg="#DCDCDD")

    product_tree = Treeview(new_window, columns=('Product ID', 'Product Name', 'Company/User Details', 'Address Details', 'Registered Date & Time', 'QR Code'), show='headings')
    for col in product_tree["columns"]:
        product_tree.heading(col, text=col)
    product_tree.pack(fill='both', expand=True)

    showQRButton = Button(new_window, text="Show QR Code", command=lambda: showQR(product_tree))
    showQRButton.pack()

    cursor.execute("SELECT * FROM products WHERE registered_by = %s", (current_admin,))
    for row in cursor.fetchall():
        product_tree.insert('', 'end', values=row[:-1])  # Exclude email in display

def showQR(product_tree):
    selected_item = product_tree.selection()
    if selected_item:
        item = product_tree.item(selected_item)
        values = item['values']
        pid, qr_code, user = values[0], values[5], values[2]

        QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        QRcode.add_data(qr_code)
        QRcode.make(fit=True)
        QRimg = QRcode.make_image().convert('RGBA')

        watermark = Image.new('RGBA', QRimg.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark)
        font = ImageFont.truetype("arial.ttf", 40)
        text_bbox = draw.textbbox((0, 0), user, font=font)
        text_position = ((QRimg.size[0] - text_bbox[2]) // 2, (QRimg.size[1] - text_bbox[3]) // 2)
        draw.text(text_position, user, fill=(0, 0, 0, 128), font=font)
        QRimg = Image.alpha_composite(QRimg, watermark)

        QRimg = QRimg.convert('RGB')
        QRimg_with_border = ImageOps.expand(QRimg, border=7, fill=(0, 0, 0))

        file_path = 'original_barcodes' + os.sep + str(pid) + 'productQR.png'
        QRimg_with_border.save(file_path)

        img2 = Image.open(file_path)
        load = img2.resize((150, 150))
        render = ImageTk.PhotoImage(load)
        img = Label(product_tree, image=render)
        img.image = render
        img.place(x=600, y=300)
    else:
        messagebox.showinfo("Show QR Code", "Please select a product.")

#show_qr_button = Button(tab3, text="Show QR Code", command=lambda: showQR(product_tree), bg="green", fg="white")
#show_qr_button.place(x=650, y=250)  # Adjust coordinates to fit your layout

def openHome():
    main.destroy()
    subprocess.Popen([sys.executable, "Main.py"])
    import AdminMain

# GUI Layout
scanButton = Button(main, text="Logout", bg="#C6AC8F", command=openHome)
scanButton.place(x=1100, y=160)

font = ('times', 30, 'bold')
title = Label(main, text='Fake Product Identification With QR-Code Using Blockchain', font=font, bg='black', fg='white')
title.place(x=40, y=5)

font = ('times', 13, 'bold')
Label(main, text='Product ID :', font=font, bg="#DCDCDD").place(x=180, y=200)
tf1 = Entry(main, width=80, font=font, bg="#DCDCDD")
tf1.place(x=370, y=200)

Label(main, text='Product Name :', font=font, bg="#DCDCDD").place(x=180, y=250)
tf2 = Entry(main, width=80, font=font, bg="#DCDCDD")
tf2.place(x=370, y=250)

Label(main, text='Company/User Details :', font=font, bg="#DCDCDD").place(x=180, y=300)
tf3 = Entry(main, width=80, font=font, bg="#DCDCDD")
tf3.place(x=370, y=300)

Label(main, text='Address Details :', font=font, bg="#DCDCDD").place(x=180, y=350)
tf4 = Entry(main, width=80, font=font, bg="#DCDCDD")
tf4.place(x=370, y=350)

Button(main, text="Save Product with Blockchain Entry", command=addProduct, font=font, bg="#DCDCDD").place(x=420, y=400)
Button(main, text="Retrieve Product Data", command=searchProduct, font=font, bg="#DCDCDD").place(x=850, y=400)

font1 = ('times', 13, 'bold')
text = Text(main, height=10, width=80, font=font1, bg="#DCDCDD")
scroll = Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=372, y=450)

main.config(bg='cornflower blue')
main.mainloop()