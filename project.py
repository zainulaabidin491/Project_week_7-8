import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import hashlib

class BusinessDirectory:
    def __init__(self, root):
        self.root = root
        self.root.title('Business Directory')

        # Create the database connection
        self.conn = sqlite3.connect('business_directory.db')
        self.cursor = self.conn.cursor()

        # Initialize the database
        self.init_db()

        # Create the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Show the splash screen
        self.show_splash_screen()

    def init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                password TEXT,
                city TEXT,
                address TEXT,
                picture BLOB
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS businesses (
                id INTEGER PRIMARY KEY,
                name TEXT,
                address TEXT,
                phone_number TEXT,
                category TEXT,
                description TEXT,
                photos BLOB,
                location TEXT,
                popularity INTEGER,
                owner_id INTEGER,
                FOREIGN KEY(owner_id) REFERENCES users(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                business_id INTEGER,
                rating INTEGER,
                review TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(business_id) REFERENCES businesses(id)
            )
        ''')

        self.conn.commit()

    def show_splash_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Business Directory", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.main_frame, text="Welcome to the Business Directory App!", font=("Arial", 16)).pack(pady=10)
        
        self.root.after(2000, self.show_login_screen)

    def show_login_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Login", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Email").pack()
        email_entry = tk.Entry(self.main_frame)
        email_entry.pack()

        tk.Label(self.main_frame, text="Password").pack()
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack()

        def login():
            email = email_entry.get()
            password = password_entry.get()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hashed_password))
            user = self.cursor.fetchone()
            if user:
                messagebox.showinfo("Success", "Login successful")
                self.show_home_screen()
            else:
                messagebox.showerror("Error", "Invalid email or password")

        tk.Button(self.main_frame, text="Login", command=login).pack(pady=10)
        tk.Button(self.main_frame, text="Sign Up", command=self.show_signup_screen).pack()

    def show_signup_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Sign Up", font=("Arial", 18)).pack(pady=10)

        tk.Label(self.main_frame, text="Name").pack()
        name_entry = tk.Entry(self.main_frame)
        name_entry.pack()

        tk.Label(self.main_frame, text="Email").pack()
        email_entry = tk.Entry(self.main_frame)
        email_entry.pack()

        tk.Label(self.main_frame, text="Password").pack()
        password_entry = tk.Entry(self.main_frame, show="*")
        password_entry.pack()

        tk.Label(self.main_frame, text="Confirm Password").pack()
        confirm_password_entry = tk.Entry(self.main_frame, show="*")
        confirm_password_entry.pack()

        tk.Label(self.main_frame, text="City").pack()
        city_entry = tk.Entry(self.main_frame)
        city_entry.pack()

        tk.Label(self.main_frame, text="Address").pack()
        address_entry = tk.Entry(self.main_frame)
        address_entry.pack()

        def register():
            if password_entry.get() == confirm_password_entry.get():
                self.register_user(name_entry.get(), email_entry.get(), password_entry.get(), city_entry.get(), address_entry.get())
                messagebox.showinfo("Success", "Registration successful")
                self.show_login_screen()
            else:
                messagebox.showerror("Error", "Passwords do not match")

        tk.Button(self.main_frame, text="Register", command=register).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Login", command=self.show_login_screen).pack()

    def register_user(self, name, email, password, city, address):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('''
            INSERT INTO users (name, email, password, city, address) 
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, hashed_password, city, address))
        self.conn.commit()

    def show_home_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Home", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.main_frame, text="Food", command=lambda: self.show_category_screen("Food")).pack(pady=5)
        tk.Button(self.main_frame, text="Healthcare", command=lambda: self.show_category_screen("Healthcare")).pack(pady=5)
        tk.Button(self.main_frame, text="Hotels", command=lambda: self.show_category_screen("Hotels")).pack(pady=5)
        tk.Button(self.main_frame, text="Education", command=lambda: self.show_category_screen("Education")).pack(pady=5)

        tk.Button(self.main_frame, text="Update Profile", command=self.show_update_profile_screen).pack(pady=10)
        tk.Button(self.main_frame, text="Logout", command=self.show_login_screen).pack()

    def show_category_screen(self, category):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text=f"{category} Businesses", font=("Arial", 18)).pack(pady=10)

        # Filters
        filter_frame = tk.Frame(self.main_frame)
        filter_frame.pack(fill="x", pady=5)

        tk.Label(filter_frame, text="Location:").grid(row=0, column=0, padx=5)
        location_entry = tk.Entry(filter_frame)
        location_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Sub-category:").grid(row=0, column=2, padx=5)
        subcategory_entry = tk.Entry(filter_frame)
        subcategory_entry.grid(row=0, column=3, padx=5)

        tk.Label(filter_frame, text="Popularity:").grid(row=0, column=4, padx=5)
        popularity_entry = tk.Entry(filter_frame)
        popularity_entry.grid(row=0, column=5, padx=5)

        def apply_filters():
            location = location_entry.get()
            subcategory = subcategory_entry.get()
            popularity = popularity_entry.get()

            query = 'SELECT name, address, description FROM businesses WHERE category = ?'
           
            params = [category]

            if location:
                query += ' AND location = ?'
                params.append(location)
            
            if subcategory:
                query += ' AND description LIKE ?'
                params.append(f'%{subcategory}%')
            
            if popularity:
                query += ' AND popularity >= ?'
                params.append(popularity)

            self.cursor.execute(query, tuple(params))
            businesses = self.cursor.fetchall()

            for widget in business_frame.winfo_children():
                widget.destroy()

            for business in businesses:
                name, address, description = business
                tk.Label(business_frame, text=f"{name}\n{address}\n{description}", font=("Arial", 12), justify="left", anchor="w").pack(fill="both", padx=10, pady=5)

        tk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=0, column=6, padx=5)

        business_frame = tk.Frame(self.main_frame)
        business_frame.pack(fill="both", expand=True)

        self.cursor.execute('SELECT name, address, description FROM businesses WHERE category = ?', (category,))
        businesses = self.cursor.fetchall()

        for business in businesses:
            name, address, description = business
            tk.Label(business_frame, text=f"{name}\n{address}\n{description}", font=("Arial", 12), justify="left", anchor="w").pack(fill="both", padx=10, pady=5)

        tk.Button(self.main_frame, text="Back to Home", command=self.show_home_screen).pack(pady=10)

    def show_update_profile_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Update Profile", font=("Arial", 18)).pack(pady=10)

        # Add fields to update profile (this is just a basic example)
        tk.Label(self.main_frame, text="Name").pack()
        name_entry = tk.Entry(self.main_frame)
        name_entry.pack()

        tk.Label(self.main_frame, text="Email").pack()
        email_entry = tk.Entry(self.main_frame)
        email_entry.pack()

        tk.Label(self.main_frame, text="City").pack()
        city_entry = tk.Entry(self.main_frame)
        city_entry.pack()

        tk.Label(self.main_frame, text="Address").pack()
        address_entry = tk.Entry(self.main_frame)
        address_entry.pack()

        def update_profile():
            # Implement the profile update logic here
            pass

        tk.Button(self.main_frame, text="Save Changes", command=update_profile).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Home", command=self.show_home_screen).pack()

if __name__ == '__main__':
    root = tk.Tk()
    app = BusinessDirectory(root)
    root.mainloop()
