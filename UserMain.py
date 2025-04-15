from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from Block import *
from Blockchain import *
from hashlib import sha256
import os
import datetime
import webbrowser
import qrcode
import random
import cv2
import sys
import pickle
from PIL import ImageTk, Image
import pyzbar.pyzbar as pyzbar

main = Tk()
main.title("Fake Product Identification With QR-Code Using Blockchain")
main.geometry("1250x700+0+0")

global filename
blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)

def authenticateProduct():
    text.delete('1.0', END)
    filename_ = askopenfilename(initialdir="original_barcodes")
    image = cv2.imread(filename_)
    decodedObjects = pyzbar.decode(image)

    for obj in decodedObjects:
        digital_signature_ = obj.data
        digital_signature = digital_signature_.decode("utf-8")
        break
    else:
        text.insert(END, "No QR code found in the image.\n")
        return

    flag = True
    for i in range(1, len(blockchain.chain)):
        b = blockchain.chain[i]
        data = b.transactions[0]
        arr = data.split("#")
        if arr[5] == digital_signature:
            output = ''
            text.insert(END, "Uploaded Product Barcode Authentication Successful\n")
            text.insert(END, "Details extracted from Blockchain after Validation\n\n")
            text.insert(END, f"Product ID                 : {arr[0]}\n")
            text.insert(END, f"Product Name               : {arr[1]}\n")
            text.insert(END, f"Company/User Details       : {arr[2]}\n")
            text.insert(END, f"Address Details            : {arr[3]}\n")
            text.insert(END, f"Product registered Date    : {arr[4]}\n")
            text.insert(END, f"Product QR-Code            : {digital_signature}\n")

            output = '<html><body><table border=1>'
            output += '<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company/User Details</th><th>Address Details</th><th>Scan Date & Time</th><th>Product QR-Code</th></tr>'
            output += f'<tr><td>{i}</td><td>{arr[0]}</td><td>{arr[1]}</td><td>{arr[2]}</td><td>{arr[3]}</td><td>{arr[4]}</td><td>{digital_signature}</td></tr>'
            output += '</table></body></html>'

            with open("output.html", "w") as f:
                f.write(output)

            webbrowser.open("output.html", new=1)
            flag = False
            break

    if flag:
        text.insert(END, f"{digital_signature}, this hash is not present in the blockchain\n")
        text.insert(END, "Uploaded Product Barcode Authentication Failed")


def authenticateProductWeb():
    text.delete('1.0', END)
    cap = cv2.VideoCapture(0)
    digital_signature = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            digital_signature_ = obj.data
            digital_signature = digital_signature_.decode("utf-8")
            break

        cv2.imshow("QR-Code Scanner - Press 'c' to capture", frame)
        if cv2.waitKey(1) == ord("c") or digital_signature:
            break

    cap.release()
    cv2.destroyAllWindows()

    if not digital_signature:
        text.insert(END, "No QR code scanned.\n")
        return

    flag = True
    for i in range(1, len(blockchain.chain)):
        b = blockchain.chain[i]
        data = b.transactions[0]
        arr = data.split("#")
        if arr[5] == digital_signature:
            text.insert(END, "QR Code Authentication Successful\n")
            text.insert(END, "Details extracted from Blockchain:\n\n")
            text.insert(END, f"Product ID                 : {arr[0]}\n")
            text.insert(END, f"Product Name               : {arr[1]}\n")
            text.insert(END, f"Company/User Details       : {arr[2]}\n")
            text.insert(END, f"Address Details            : {arr[3]}\n")
            text.insert(END, f"Scan Date & Time           : {arr[4]}\n")
            text.insert(END, f"Product QR-Code            : {digital_signature}\n")

            output = '<html><body><table border=1>'
            output += '<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company/User Details</th><th>Address Details</th><th>Scan Date & Time</th><th>Product QR-Code</th></tr>'
            output += f'<tr><td>{i}</td><td>{arr[0]}</td><td>{arr[1]}</td><td>{arr[2]}</td><td>{arr[3]}</td><td>{arr[4]}</td><td>{digital_signature}</td></tr>'
            output += '</table></body></html>'

            with open("output.html", "w") as f:
                f.write(output)

            webbrowser.open("output.html", new=1)
            flag = False
            break

    if flag:
        text.insert(END, f"{digital_signature}, this hash is not present in the blockchain\n")
        text.insert(END, "QR Code Authentication Failed")


def logout():
    main.destroy()
    import Main


font = ('times', 30, 'bold')
title = Label(main, text='Fake Product Identification With QR-Code Using Blockchain', bg='black', fg='white')
title.config(font=font, height=3, width=50)
title.place(x=40, y=40)

font1 = ('times', 13, 'bold')

# Side image (optional)
side_image_path = "bg\\main-front.jpeg"
if os.path.exists(side_image_path):
    side_image = Image.open(side_image_path)
    side_image = side_image.resize((450, 420), Image.Resampling.LANCZOS)
    side_image_tk = ImageTk.PhotoImage(side_image)
    side_label = Label(main, image=side_image_tk)
    side_label.image = side_image_tk
    side_label.place(x=40, y=200)

logout_btn = Button(main, text="Logout", bg="#C6AC8F", command=logout)
logout_btn.place(x=830, y=590)
logout_btn.config(font=font1)

scan_device_btn = Button(main, text="SCAN QR FROM DEVICE", bg="#E0E1DD", fg="black", command=authenticateProduct)
scan_device_btn.place(x=600, y=230)
scan_device_btn.config(font=font1)

scan_webcam_btn = Button(main, text="SCAN QR BY WEBCAM", bg="#E0E1DD", fg="black", command=authenticateProductWeb)
scan_webcam_btn.place(x=960, y=230)
scan_webcam_btn.config(font=font1)

text = Text(main, height=15, width=79)
scroll = Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=530, y=290)
text.config(font=font1, bg="#E0E1DD")

main.config(bg='cornflower blue')
main.mainloop()
