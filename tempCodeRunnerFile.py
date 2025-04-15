# Display the side photo
side_image_path = "bg\\main-page.jpeg"
side_image = Image.open(side_image_path)
side_image = side_image.resize((450, 420), Image.Resampling.LANCZOS)  # Resize image if necessary
side_image_tk = ImageTk.PhotoImage(side_image)
side_label = Label(main, image=side_image_tk)
side_label.image = side_image_tk  # Keep a reference to avoid garbage collection
side_label.place(x=120, y=200)  # Adjust the position as needed
