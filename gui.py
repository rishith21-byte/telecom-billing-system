from screens.customer_screen import show_customer_screen
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Telecom Billing System")
root.geometry("1200x700")
root.resizable(False, False)

# ---------------- Sidebar ----------------

sidebar = ctk.CTkFrame(root, width=220)
sidebar.pack(side="left", fill="y")

title = ctk.CTkLabel(
    sidebar,
    text="TELECOM\nBILLING",
    font=("Arial", 26, "bold")
)
title.pack(pady=30)

btn1 = ctk.CTkButton(sidebar, text="🏠 Dashboard")
btn1.pack(pady=10)

btn2 = ctk.CTkButton(
    sidebar,
    text="👤 Customers",
    command=lambda: show_customer_screen(main)
)
btn2.pack(pady=10)

btn3 = ctk.CTkButton(sidebar, text="📶 Plans")
btn3.pack(pady=10)

btn4 = ctk.CTkButton(sidebar, text="🧾 Billing")
btn4.pack(pady=10)

btn5 = ctk.CTkButton(sidebar, text="📊 Reports")
btn5.pack(pady=10)

btn6 = ctk.CTkButton(
    sidebar,
    text="Exit",
    fg_color="red",
    hover_color="darkred",
    command=root.destroy
)
btn6.pack(side="bottom", pady=20)

# ---------------- Main Area ----------------

main = ctk.CTkFrame(root)
main.pack(side="right", fill="both", expand=True)

heading = ctk.CTkLabel(
    main,
    text="Welcome to Telecom Billing System",
    font=("Arial", 28, "bold")
)
heading.pack(pady=50)

info = ctk.CTkLabel(
    main,
    text="Select an option from the left menu.",
    font=("Arial", 18)
)
info.pack()

root.mainloop()
