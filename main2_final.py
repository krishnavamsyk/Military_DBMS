from customtkinter import *                          #importing all necessary libraries
from tkinter import messagebox, Toplevel
from PIL import Image
import mysql.connector
import customtkinter as ctk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plti
import tkinter as tk

# Global variables for images, windows, and widgets
root = None
dashboard_window = None
login_img = None
user_icon = None
password_icon = None
logo_img = None
analytics_img = None

def on_login_close():
    root.destroy()  # Close the entire program

def setup_login_ui():     #Login function that displays login page
    global root, login_img, user_icon, password_icon, entry_username, entry_password

    # Add image to the login screen
    login_img = CTkImage(
        light_image=Image.open(r"icons and images\loginimg6.png"),
        dark_image=Image.open(r"icons and images\loginimg6.png"),
        size=(350, 430)
    )
    CTkLabel(master=root, text="", image=login_img).pack(expand=True, side="left")

    frame = CTkFrame(master=root, width=350, height=480, fg_color="#262625")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    # Setup login labels and buttons
    CTkLabel(master=frame, text="Welcome Back!", text_color="#04bf04", anchor="w", font=("Arial Bold", 30)).pack(anchor="w", pady=(20, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    user_icon_data = Image.open(r"icons and images\user-icon.png")
    password_icon_data = Image.open(r"icons and images\user-icon.png")
    user_icon = CTkImage(dark_image=user_icon_data, light_image=user_icon_data, size=(30, 20))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(30, 25))

    CTkLabel(master=frame, text="  Username:", text_color="#029c02", font=("Arial Bold", 14), image=user_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    entry_username = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
    entry_username.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Password:", text_color="#029c02", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    entry_password = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
    entry_password.pack(anchor="w", padx=(25, 0))

    CTkButton(master=frame, text="Login", fg_color="#601E88", font=("Arial Bold", 12), width=225, command=login).pack(anchor="w", pady=(40, 0), padx=(25, 0))
    CTkLabel(master=frame, text="If new user, contact higher officials", text_color="#7E7E7E", anchor="w", font=("Arial Bold", 12)).pack(anchor="w", pady=(43), padx=(20, 0))

    root.protocol("WM_DELETE_WINDOW", on_login_close)

def login():       #login verification function
    username = entry_username.get()
    password = entry_password.get()
    connection = connect_db()
    global user_id
    if connection:
        cursor = connection.cursor()
        query = "SELECT ID FROM login WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]
            query = "SELECT ranks FROM soldiers WHERE ID = %s"
            cursor.execute(query, (user_id,))
            rank_result = cursor.fetchone()

            if rank_result:
                rank = rank_result[0]
                print(rank)
                root.withdraw()  # Hide the login window
                if rank == "General" or rank=="Field Marshal":
                    open_general_view()  # Open the general view
                else:
                    soldier_view()
            else:
                messagebox.showerror("Error", "No rank found for the user.")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
        cursor.close()
        connection.close()

def connect_db():    #connecting to Mysql military database that was created
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="krishnavamsy@0411",
            database="militarydb"
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None
    
def soldier_view():       # Function for soldier view page
    ID=user_id
    global app,current_active_button

    app = Toplevel(root)  # Initialize the dashboard window here
    app.title("Soldier's Dashboard")
    app.geometry("1500x900")
    app.resizable(False, False)
    app.configure(bg="black")
    set_appearance_mode("light")

    #connecting to database
    try:
            # Update these parameters based on your database configuration
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="krishnavamsy@0411",
                database="militarydb"
            )
            
    except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            
    cursor = connection.cursor()

    # Define the default and active button colors
    inactive_button_color = "transparent"
    active_button_color = "#207244"  # Dark green for active button

    current_active_button = None   # Global variable to track the current active button
    def fetch_fit(soldier_id):
        query = """
        SELECT s.id, t.fitness_score
        FROM soldiers s
        JOIN training_Details t ON s.id = t.id
        WHERE s.id = %s  -- Filter by soldier_id
    """
        try:
            # Execute the query with the specific soldier_id
            cursor.execute(query, (soldier_id,))  # Pass soldier_id as a parameter
            data = cursor.fetchone()
            if data:
                id, fitness_score = data  # Unpack the tuple
                return id, fitness_score  # Return the specific soldier's id and fitness score
            else:
                return None, None  # Return None if no data found for that soldier

        except Exception as e:
            print(f"Error fetching fitness data: {e}")
            return None, None  # Return None in case of an error
    
    def fetch_achievements(soldier_id):    #function for fetching achievements
        query1 = """
        SELECT medal, date_of_receiving
        FROM achievements
        WHERE id = %s  -- Filter by soldier_id
    """
        try:
            # Execute the query with the specific soldier_id
            cursor.execute(query1, (soldier_id,))  # Pass soldier_id as a parameter
            data = cursor.fetchone()  # Fetch one row

            # Check if data exists and unpack the result
            if data:
                medal, date_of_receiving = data
                return medal, date_of_receiving
            else:
                return None, None
        except Exception as e:
            print(f"Error fetching achievements: {e}")
            return None, None
    def count_total_soldiers(cursor):         #To count total no of soldiers
        query = "SELECT COUNT(*) FROM soldiers"
        try:
            cursor.execute(query)
            total_count = cursor.fetchone()[0]  # Fetch the count from the result
            return total_count
        except Exception as e:
            print(f"Error counting soldiers: {e}")
            return 0

    # Function to fetch fitness score for a specific soldier
    def fetch_fit(soldier_id):
        query = "SELECT id, fitness_score FROM training_details WHERE id = %s"
        try:
            cursor.execute(query, (soldier_id,))
            result = cursor.fetchone()
            return result if result else (None, None)
        except Exception as e:
            print(f"Error fetching fitness data: {e}")
            return None, None
    
    def highlight_button(button):
        global current_active_button
        # Reset the color of the previously active button
        if current_active_button:
            current_active_button.configure(fg_color=inactive_button_color)
        
        # Set the current button as active
        button.configure(fg_color=active_button_color)
        current_active_button = button
    def dashboard():
        # Clear the current main view frame
        for widget in main_view.winfo_children():
            widget.destroy()

        # Highlight the dashboard button
        highlight_button(dashboard_button)
 # Return 0 in case of an error
        total_soldiers = count_total_soldiers(cursor)

        # Set up the dashboard UI
        title_frame = CTkFrame(master=main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Welcome, Soldier", font=("Arial Black", 30), text_color="#2A8C55").pack(anchor="nw", side="left")
        scframe = CTkScrollableFrame(
            master=main_view, 
            height=500,  # Set to desired height
            width=600,   # Set to desired width
            fg_color='black'
        )
        scframe.pack(fill="both", expand=True, padx=10, pady=20)
        main_frame = CTkFrame(master=scframe, bg_color="black", fg_color="black")
        main_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Achievements Section with two parts
            # Left side for Fitness Score (Graph)
            # Left side for Fitness Score (Graph)

        achievements_list_frame = CTkFrame(master=main_frame, bg_color="grey",fg_color="black")
        achievements_list_frame.pack(pady=(20, 10), fill="both", expand=True)  # Pack achievements_list_frame below fitness_frame

        # Title for Achievements section
        achievements_title_label = CTkLabel(master=achievements_list_frame, text="Achievements", font=("Arial", 20, "bold"), text_color="#2A8C55")
        achievements_title_label.pack(anchor="center", pady=(10, 10))
        highlight_soldier_id = ID
        # Fetch the achievements from the database
        result = fetch_achievements(highlight_soldier_id)
        print(f"Fetched Achievements: {result}")  # Fetch achievements from the database
        medal,date=result

        if result:  # Check if result is not empty
                    # Create a frame for each achievement to group the labels
                    achievement_frame = CTkFrame(master=achievements_list_frame, fg_color="black", border_width=2, border_color="white")
                    achievement_frame.pack(pady=(10, 10), padx=10, fill="x")  # Pack each achievement frame

                    # Create labels for each achievement detail
                    medal_label = CTkLabel(
                        master=achievement_frame, 
                        text=f"Medal: {medal}",
                        font=("Arial", 14, "bold"),
                        text_color="white",
                        bg_color="transparent"
                    )
                    medal_label.pack(anchor="w", padx=10, pady=(5, 0))

                    date_label = CTkLabel(
                        master=achievement_frame, 
                        text=f"Received on: {date}",
                        font=("Arial", 14, "bold"),
                        text_color="white",
                        bg_color="transparent"
                    )
                    date_label.pack(anchor="w", padx=10, pady=(5, 10))

        else:
            # Display a message when no achievements are found
            no_achievements_label = CTkLabel(
                master=achievements_list_frame, 
                text="No achievements found.", 
                font=("Arial", 14), 
                text_color="red"
            )
            no_achievements_label.pack(pady=(10, 0))

        # Achievements Section
        fitness_frame = ctk.CTkFrame(master=main_frame, bg_color="black", fg_color="black")
        fitness_frame.pack(pady=(30, 30), fill="x")

        # Title for the Fitness Score section
        fitness_title_label = ctk.CTkLabel(master=fitness_frame, text="Fitness Score", font=("Arial", 20, "bold"), text_color="#2A8C55")
        fitness_title_label.pack(anchor="center", pady=(0, 10))

        # Fetch fitness scores for all soldiers
        soldier_ids = list(range(27992, 28011))  # Include 0, 4, and IDs from 27992 to 28010
        fitness_scores = []

        for soldier_id in soldier_ids:
            _, fitness_score = fetch_fit(soldier_id)
            fitness_scores.append(fitness_score if fitness_score is not None else 0)  # Use 0 for missing scores

        # Highlight soldier ID (change this to the soldier ID you want to access)
        highlight_soldier_id = ID  # Example ID to highlight
        highlight_id, highlight_fitness_score = fetch_fit(highlight_soldier_id)

        if highlight_id is None or highlight_fitness_score is None:
            no_data_label = ctk.CTkLabel(master=fitness_frame, text="No fitness records found.", font=("Arial", 14), text_color="red")
            no_data_label.pack(pady=(10, 0))
        else:
            # If data exists, plot the graph
            fig, ax = plti.subplots(figsize=(10, 5))

            # Create a linear plot
            ax.plot(soldier_ids, fitness_scores, marker='o', color='skyblue', label='Fitness Score')

            # Highlight the specific soldier's score
            ax.plot(highlight_soldier_id, highlight_fitness_score, marker='o', color='orange', markersize=10, label='Highlighted Soldier')

            ax.set_title("Fitness Score vs Soldier ID")
            ax.set_xlabel("Soldier ID")
            ax.set_ylabel("Fitness Score")
            ax.grid(True, linestyle='--', linewidth=0.5)
            ax.legend()

            # Embed the plot in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=fitness_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

    def soldier_details():
        for widget in main_view.winfo_children():
            widget.destroy()

        #query for main
        connection = connect_db()
        cursor = connection.cursor()     
        #query for main
        query1 = '''SELECT s.name, s.dob, s.doj, s.gender, s.height, s.weight, s.division, s.maritial_status,s.blood_type,s.phone_no,s.ranks,s.squad_id
                FROM soldiers s
                WHERE s.ID = %s'''  # Using %s as a placeholder for parameterized query
        # Execute the query with the ID as a parameter
        cursor.execute(query1, (ID,))
        result = cursor.fetchone()
        #query for address
        query2 = '''SELECT a.Pincode, a.District, a.City, a.State, a.Home_phone_no,a.address_line
                FROM address a
                WHERE a.ID = %s'''
        cursor.execute(query2,(ID,))
        result1=cursor.fetchone()
        #query for weapon assigned
        query3 = '''SELECT wa.Weapon_ID, wa.Date,wcl.Weapon_name,wc.Category
                FROM weapon_assigned wa
                JOIN weapon_catalogue wcl ON wcl.Weapon_ID = wa.Weapon_ID 
                Join weapon_category wc on wcl.Category_no=wc.Category_no
                WHERE wa.ID = %s'''
        cursor.execute(query3,(ID,))
        result2=cursor.fetchone()
        #query for squad details:
        query4 = '''SELECT sq.Squad_ID, sq.Camp,c.Captain_name,sq.Year,veh.v_id,veh.V_name,veh.V_model
                FROM squad sq
                JOIN captains c ON c.Squad_ID = sq.Squad_ID 
                JOIN vehicles_assigned v ON v.Squad_ID=sq.Squad_ID
                JOIN vehicles veh ON veh.V_ID=v.V_ID
                WHERE sq.Squad_ID = %s'''
        cursor.execute(query4,(result[11],))
        result3=cursor.fetchone()
        #query for training detail:
        query5 = '''SELECT td.Fitness_score,td.Shooting_accuracy,td.Sprint_speed_100m 
                FROM training_details td
                WHERE td.ID = %s'''
        cursor.execute(query5,(ID,))
        result4=cursor.fetchone()
        # query for achievements:
        query6 = '''SELECT ac.Medal, ac.Date_of_receiving
                FROM achievements ac 
                WHERE ac.ID = %s'''
        cursor.execute(query6,(ID,))
        result5=cursor.fetchone()
        #query for promotion:
        query7 = '''SELECT prom.New_rank,prom.Promotion_date 
                FROM promotion prom 
                WHERE prom.Soldier_ID = %s'''
        cursor.execute(query7,(ID,))
        result6=cursor.fetchone()
        # query for Leaves:
        query8 = '''SELECT lt.No_of_leaves,lt.Reason
                FROM leaves_taken lt
                WHERE lt.ID = %s'''
        cursor.execute(query8,(ID,))
        result7=cursor.fetchone()
        # query for wars:
        query9='''SELECT sur.War_ID,w.Date from war w
                  JOIN soldier_status sur on sur.War_ID=w.War_no
                  where sur.ID=%s'''
        cursor.execute(query9,(ID,))
        result8=cursor.fetchone()
        # Highlight the dashboard button
        highlight_button(pers_button)

        # Function to get value or return "None" if result is None
        def safe_get(value, index):
            return value[index] if value else "None"

        # Add heading for "Personal Details"
        heading_frame = CTkFrame(master=main_view, fg_color="transparent")  
        heading_frame.pack(anchor="nw", fill="x", padx=27, pady=(15, 10))

        CTkLabel(
            master=heading_frame,
            text="Personal Details", 
            font=("Arial Black", 30), 
            text_color="#2A8C55"
        ).pack(anchor="nw", pady=(10, 10))
        IDframe = CTkLabel(master=main_view, text="  ID:  %s"%ID,font=('Arial Black',20,"bold"),text_color='#5bb5d9',fg_color="transparent", width=150)
        IDframe.pack(anchor="nw", padx=(10,10), pady=(50,0))
        # Create a scrollable frame for the main content
        scframe =CTkScrollableFrame(
            master=main_view, 
            height=500,  # Set to desired height
            width=600    # Set to desired width
            ,fg_color='black'
        )
        scframe.pack(fill="both", expand=True, padx=10, pady=20)

        # Personal Details Section

         #adding address title
        myfont=CTkFont(family="Arial",size=20,weight='bold',underline=True)
        main_tframe = CTkLabel(master=scframe, text="Main",font=myfont,fg_color="#b87a2e", width=1500)
        main_tframe.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        det_frame = CTkFrame(master=scframe, fg_color="black", width=1500,border_width=7,border_color='#30302f')  # Increased width for more space
        det_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        CTkLabel(master=det_frame, text="Name:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,0)}", font=("Arial", 14),text_color='white').grid(row=0, column=1, padx=(0, 20), pady=15)

        # Adding extra space for Rank
        CTkLabel(master=det_frame, text="Date of birth:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=2, padx=(80, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,1)}", font=("Arial", 14),text_color='white').grid(row=0, column=3, padx=(0, 20), pady=15)

        CTkLabel(master=det_frame, text="Date of joining:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,2)}", font=("Arial", 14),text_color='white').grid(row=1, column=1, padx=(0, 20), pady=15)

        # Adding extra space for Camp
        CTkLabel(master=det_frame, text="Gender:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=2, padx=(80, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,3)}", font=("Arial", 14),text_color='white').grid(row=1, column=3, padx=(0, 20), pady=15)

        CTkLabel(master=det_frame, text="Height:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,4)}", font=("Arial", 14),text_color='white').grid(row=2, column=1, padx=(0, 20), pady=15)

        # Adding extra space for Squad_ID
        CTkLabel(master=det_frame, text="Weight:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=2, padx=(80, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,5)}", font=("Arial", 14),text_color='white').grid(row=2, column=3, padx=(0, 20), pady=15)

        CTkLabel(master=det_frame, text="Division:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=3, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,6)}", font=("Arial", 14),text_color='white').grid(row=3, column=1, padx=(0, 20), pady=15)

        # Adding extra space for Birthplace pincode
        CTkLabel(master=det_frame, text="Maritial status:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=3, column=2, padx=(80, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,7)}", font=("Arial", 14),text_color='white').grid(row=3, column=3, padx=(0, 20), pady=15)
        
        CTkLabel(master=det_frame, text="Blood type:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=4, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,8)}", font=("Arial", 14),text_color='white').grid(row=4, column=1, padx=(0, 20), pady=15)

        CTkLabel(master=det_frame, text="Phone No", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=4, column=2, padx=(80, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,9)}", font=("Arial", 14),text_color='white').grid(row=4, column=3, padx=(0, 20), pady=15)

        CTkLabel(master=det_frame, text="Rank:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=5, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,10)}", font=("Arial", 14),text_color='white').grid(row=5, column=1, padx=(0, 20), pady=15)

        #--------------adding address 
        adres_tframe = CTkLabel(master=scframe, text="Address",font=myfont,fg_color="#b87a2e", width=1500)
        adres_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        addrs_frame = CTkFrame(master=scframe, fg_color="black", width=1500,border_width=7,border_color='#30302f')  # Increased width for more space
        addrs_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))
        #Pincode
        CTkLabel(master=addrs_frame, text="Pincode:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,0)}", font=("Arial", 14),text_color='white').grid(row=0, column=1, padx=(0, 20), pady=15)
        #District
        CTkLabel(master=addrs_frame, text="District:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=2, padx=(140, 10), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,1)}", font=("Arial", 14),text_color='white').grid(row=0, column=3, padx=(0, 20), pady=15)
        #city
        CTkLabel(master=addrs_frame, text="City:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,2)}", font=("Arial", 14),text_color='white').grid(row=1, column=1, padx=(0, 20), pady=15)
        #state
        CTkLabel(master=addrs_frame, text="State:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=2, padx=(140, 10), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,3)}", font=("Arial", 14),text_color='white').grid(row=1, column=3, padx=(10, 20), pady=15)
        #Home Phone
        CTkLabel(master=addrs_frame, text="Home Phone:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=0, padx=(10, 10), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,4)}", font=("Arial", 14),text_color='white').grid(row=2, column=1, padx=(10, 20), pady=15)
        #Address line
        CTkLabel(master=addrs_frame, text="Address line:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=2, padx=(140, 10), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,5)}", font=("Arial", 14),text_color='white').grid(row=2, column=3, padx=(0, 20), pady=15)

        #--------------adding weapon assigned
        was_tframe = CTkLabel(master=scframe, text="Weapon Assigned",font=myfont,fg_color="#b87a2e", width=1500)
        was_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        was_frame = CTkFrame(master=scframe, fg_color="black", width=1500,border_width=7,border_color='#30302f')  # Increased width for more space
        was_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))
        #Weapon ID
        CTkLabel(master=was_frame, text="Weapon ID:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=was_frame, text=f"{safe_get(result2,0)}", font=("Arial", 14),text_color='white').grid(row=0, column=1, padx=(0, 20), pady=15)
        #Date assigned
        CTkLabel(master=was_frame, text="Date assigned:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=was_frame, text=f"{safe_get(result2,1)}", font=("Arial", 14),text_color='white').grid(row=0, column=3, padx=(0, 20), pady=15)
        #Weapon name
        CTkLabel(master=was_frame, text="Weapon name:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=was_frame, text=f"{safe_get(result2,2)}", font=("Arial", 14),text_color='white').grid(row=1, column=1, padx=(0, 20), pady=15)
        #Category
        CTkLabel(master=was_frame, text="Category:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=was_frame, text=f"{safe_get(result2,3)}", font=("Arial", 14),text_color='white').grid(row=1, column=3, padx=(0, 20), pady=15)

        #--------------adding squad details
        sq_tframe = CTkLabel(master=scframe, text="Squad Details",font=myfont,fg_color="#b87a2e", width=1500)
        sq_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        sq_frame = CTkFrame(master=scframe, fg_color="black", width=1500,border_width=7,border_color='#30302f')  # Increased width for more space
        sq_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))
        #Squad ID
        CTkLabel(master=sq_frame, text="Squad ID:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,0)}", font=("Arial", 14),text_color='white').grid(row=0, column=1, padx=(0, 20), pady=15)
        #DCamp name
        CTkLabel(master=sq_frame, text="Camp name:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,1)}", font=("Arial", 14),text_color='white').grid(row=0, column=3, padx=(0, 20), pady=15)
        #Captain name
        CTkLabel(master=sq_frame, text="Captain name:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,2)}", font=("Arial", 14),text_color='white').grid(row=1, column=1, padx=(0, 20), pady=15)
        #Year
        CTkLabel(master=sq_frame, text="Year:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,3)}", font=("Arial", 14),text_color='white').grid(row=1, column=3, padx=(0, 20), pady=15)
        #Vehcile No
        CTkLabel(master=sq_frame, text="Vehcile No:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=0, padx=(70, 10), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,4)}", font=("Arial", 14),text_color='white').grid(row=2, column=1, padx=(0, 20), pady=15)
        #Vehicle Name
        CTkLabel(master=sq_frame, text="Vehicle Name:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,5)}", font=("Arial", 14),text_color='white').grid(row=2, column=3, padx=(0, 20), pady=15)
        #Vehicle model
        CTkLabel(master=sq_frame, text="Vehicle model:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=3, column=0, padx=(70, 10), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,6)}", font=("Arial", 14),text_color='white').grid(row=3, column=1, padx=(0, 20), pady=15)

        #------------training detials
        tr_tframe = CTkLabel(master=scframe, text="Training Details",font=myfont,fg_color="#b87a2e", width=1500)
        tr_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        tr_frame = CTkFrame(master=scframe, fg_color="black", width=1500,border_width=7,border_color='#30302f')  # Increased width for more space
        tr_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))
        #Squad ID
        CTkLabel(master=tr_frame, text="Fitness Score:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=tr_frame, text=f"{safe_get(result4,0)}", font=("Arial", 14),text_color='white').grid(row=0, column=1, padx=(0, 20), pady=15)
        #DCamp name
        CTkLabel(master=tr_frame, text="Shooting Accuracy:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=tr_frame, text=f"{safe_get(result4,1)}", font=("Arial", 14),text_color='white').grid(row=0, column=3, padx=(0, 20), pady=15)
        #Captain name
        CTkLabel(master=tr_frame, text="Sprint Speed (mph):", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=tr_frame, text=f"{safe_get(result4,2)}", font=("Arial", 14),text_color='white').grid(row=1, column=1, padx=(0, 20), pady=15)
        
        #------------Achievements
        ac_tframe = CTkLabel(master=scframe, text="Achievements", font=myfont, fg_color="#b87a2e", width=1500)
        ac_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        ac_frame = CTkFrame(master=scframe, fg_color="black", width=1500, border_width=7, border_color='#30302f')
        ac_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        if result5 and (result5[0] or result5[1]):
            CTkLabel(master=ac_frame, text="Medal:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
            CTkLabel(master=ac_frame, text="Date of receiving:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=2, padx=(123, 10), pady=15, sticky="w")

            if isinstance(result5[0], list) and isinstance(result5[1], list):
                for i in range(len(result5[0])):
                    CTkLabel(master=ac_frame, text=f"{result5[0][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=0, padx=(70, 20), pady=15)
                    CTkLabel(master=ac_frame, text=f"{result5[1][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=2, padx=(65, 20), pady=15)
            else:
                CTkLabel(master=ac_frame, text=f"{result5[0]}", font=("Arial", 14), text_color='white').grid(row=1, column=0, padx=(70, 20), pady=15)
                CTkLabel(master=ac_frame, text=f"{result5[1]}", font=("Arial", 14), text_color='white').grid(row=1, column=2, padx=(65, 20), pady=15)
        else:
            CTkLabel(master=ac_frame, text="Null", font=("Arial", 14), text_color='white').pack(pady=15)

        # Promotion
        tr_tframe = CTkLabel(master=scframe, text="Promotion", font=myfont, fg_color="#b87a2e", width=1500)
        tr_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        tr_frame = CTkFrame(master=scframe, fg_color="black", width=1500, border_width=7, border_color='#30302f')
        tr_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        if result6 and (result6[0] or result6[1]):
            CTkLabel(master=tr_frame, text="New Rank:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
            CTkLabel(master=tr_frame, text="Promotion Date:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=3, padx=(235, 10), pady=15, sticky="w")

            if isinstance(result6[0], list) and isinstance(result6[1], list):
                for i in range(len(result6[0])):
                    CTkLabel(master=tr_frame, text=f"{result6[0][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=0, padx=(0, 20), pady=15)
                    CTkLabel(master=tr_frame, text=f"{result6[1][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=3, padx=(0, 20), pady=15)
            else:
                CTkLabel(master=tr_frame, text=f"{result6[0]}", font=("Arial", 14), text_color='white').grid(row=1, column=0, padx=(27, 20), pady=15)
                CTkLabel(master=tr_frame, text=f"{result6[1]}", font=("Arial", 14), text_color='white').grid(row=1, column=3, padx=(185, 20), pady=15)
        else:
            CTkLabel(master=tr_frame, text="Null", font=("Arial", 14), text_color='white').pack(pady=15)

        # Leaves Taken
        lv_tframe = CTkLabel(master=scframe, text="Leaves taken", font=myfont, fg_color="#b87a2e", width=1500)
        lv_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        lv_frame = CTkFrame(master=scframe, fg_color="black", width=1500, border_width=7, border_color='#30302f')
        lv_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        if result7 and (result7[0] or result7[1]):
            CTkLabel(master=lv_frame, text="No of leaves:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
            CTkLabel(master=lv_frame, text="Reason:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=2, padx=(220, 10), pady=15, sticky="w")

            if isinstance(result7[0], list) and isinstance(result7[1], list):
                for i in range(len(result7[0])):
                    CTkLabel(master=lv_frame, text=f"{result7[0][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=0, padx=(70, 20), pady=15)
                    CTkLabel(master=lv_frame, text=f"{result7[1][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=2, padx=(185, 20), pady=15)
            else:
                CTkLabel(master=lv_frame, text=f"{result7[0]}", font=("Arial", 14), text_color='white').grid(row=1, column=0, padx=(0, 20), pady=15)
                CTkLabel(master=lv_frame, text=f"{result7[1]}", font=("Arial", 14), text_color='white').grid(row=1, column=2, padx=(220, 10), pady=15)
        else:
            CTkLabel(master=lv_frame, text="Null", font=("Arial", 14), text_color='white').pack(pady=15)

        # Contributed Wars
        war_tframe = CTkLabel(master=scframe, text="Contributed Wars:", font=myfont, fg_color="#b87a2e", width=1500)
        war_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        war_frame = CTkFrame(master=scframe, fg_color="black", width=1500, border_width=7, border_color='#30302f')
        war_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        if result8 and (result8[0] or result8[1]):
            CTkLabel(master=war_frame, text="War ID:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
            CTkLabel(master=war_frame, text="Date:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=2, padx=(260, 10), pady=15, sticky="w")

            if isinstance(result8[0], list) and isinstance(result8[1], list):
                for i in range(len(result8[0])):
                    CTkLabel(master=war_frame, text=f"{result8[0][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=0, padx=(32, 20), pady=15)
                    CTkLabel(master=war_frame, text=f"{result8[1][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=3, padx=(260, 20), pady=15)
            else:
                CTkLabel(master=war_frame, text=f"{result8[0]}", font=("Arial", 14), text_color='white').grid(row=1, column=0, padx=(32, 20), pady=15)
                CTkLabel(master=war_frame, text=f"{result8[1]}", font=("Arial", 14), text_color='white').grid(row=1, column=2, padx=(260, 10), pady=15)
        else:
            CTkLabel(master=war_frame, text="Null", font=("Arial", 14), text_color='white').pack(pady=15)


    def fetch_account(soldier_id):        
        query="""
            SELECT ID, Username, Password
            FROM login
            WHERE ID=%s
        """
        try:
            # Execute the query with the specific soldier_id
            cursor.execute(query, (soldier_id,))  # Pass soldier_id as a parameter
            data = cursor.fetchone()  # Use fetchone() since we're looking for one record

            # Check if data exists and unpack the result into two variables
            if data:
                id, username, password = data  # Unpack the tuple
                return id, username, password  # Return the specific soldier's id and fitness score
            else:
                return None, None, None  # Return None if no data found for that soldier

        except Exception as e:
            print(f"Error fetching fitness data: {e}")
            return None, None, None
        
    def soldier_name(soldier_id):
        query="""
            SELECT Name 
            FROM Soldiers
            WHERE ID=%s
        """
        try:
            # Execute the query with the specific soldier_id
            cursor.execute(query, (soldier_id,))  # Pass soldier_id as a parameter
            data = cursor.fetchone()  # Use fetchone() since we're looking for one record

            # Check if data exists and unpack the result into two variables
            if data:
                return data[0]  # Return the specific soldier's id and fitness score
            else:
                return None # Return None if no data found for that soldier

        except Exception as e:
            print(f"Error fetching fitness data: {e}")
            return None
        
    def account():         # Global variable to track the current active button
        connection = connect_db()
        cursor = connection.cursor() 

        # Clear the current main view frame
        for widget in main_view.winfo_children():
            widget.destroy()
        
        highlight_button(account_button)

        # Title
        title_frame = CTkFrame(master=main_view, fg_color="black")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        user_frame = CTkFrame(master=main_view, fg_color="black")
        user_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        s_name = soldier_name(user_id)
        print(s_name)

        # Load and resize the image
        person_img_data = Image.open(r"icons and images\soldicon.jpg")
        person_img_data = person_img_data.resize((70, 60), Image.LANCZOS)
        person_img = ImageTk.PhotoImage(person_img_data)

        CTkLabel(master=title_frame, text="Account", font=("Arial Black", 30), text_color="#2A8C55").pack(anchor='nw', pady=(10, 10))
        CTkLabel(
            master=user_frame,
            text=s_name,
            font=("Arial Black", 30),
            text_color="#5bb5d9", image=person_img, compound="left"
        ).pack(anchor="nw", pady=(10, 10), padx=(20, 50))

        # Scrollable frame for content


        m_frame = CTkFrame(master=main_view, bg_color="black", fg_color="black", width=400)
        m_frame.pack(padx=30, pady=20, fill="both", expand=True, anchor="center")

        # Fetch account info
        soldier_id = user_id  # Replace with the logged-in user's ID
        _, username, password = fetch_account(soldier_id)
        main_frame = CTkFrame(master=m_frame, bg_color="black", fg_color="black", width=300,border_width=3,border_color="grey")
        main_frame.pack(padx=30, pady=20, fill="both", expand=True, anchor="center")

        # Handle missing or null username/password
        if username is None:
            CTkLabel(
                master=main_frame,
                text="No account information found!",
                font=("Arial", 20),
                text_color="red",
            ).pack(pady=20)
            return

        # Display account details
        # Create a frame to hold the labels and values
        credentials_frame = CTkFrame(master=main_frame, fg_color="black")
        credentials_frame.pack(anchor="center", pady=20)

        # Username Label
        CTkLabel(
            master=credentials_frame,
            text="Username:",
            font=("Arial", 20),
            text_color="lightblue",  # Change this to your desired color
            fg_color="black",
            corner_radius=10,
            padx=10,
        ).grid(row=0, column=0, padx=10, sticky="w")  # Place in the first row, first column

        # Username Value
        CTkLabel(
            master=credentials_frame,
            text=username,  # Display the actual username
            font=("Arial", 20),
            text_color="white",  # Change this to your desired color for the output
            fg_color="black",
            corner_radius=10,
            padx=10,
        ).grid(row=0, column=1, padx=10, sticky="w")  # Place in the first row, second column

        # Password Label
        CTkLabel(
            master=credentials_frame,
            text="Password:",
            font=("Arial", 20),
            text_color="lightblue",  # Change this to your desired color
            fg_color="black",
            corner_radius=10,
            padx=10,
        ).grid(row=1, column=0, padx=10, sticky="w")  # Place in the second row, first column

        # Hide password
        hide_pass = '*' * len(password)

        # Password Value
        CTkLabel(
            master=credentials_frame,
            text=hide_pass,  # Display the hidden password
            font=("Arial", 20),
            text_color="white",  # Change this to your desired color for the output
            fg_color="black",
            corner_radius=10,
            padx=10,
        ).grid(row=1, column=1, padx=10, sticky="w")  # Place in the second row, second column
        # Password Entry
        password_entry = CTkEntry(
            master=main_frame,
            placeholder_text="Verify your password",
            font=("Arial", 16),
            fg_color="#3A3A3A",
            text_color="lightblue",
            border_width=2,
            corner_radius=5,
            width=250,
        )
        password_entry.pack(anchor="center", pady=10, padx=10 )

        def validate_password():
            """Validate the entered password with the database."""
            connection = connect_db()
            cursor = connection.cursor() 
            entered_password = password_entry.get()

            # Query to fetch the password from the database
            query = "SELECT Password FROM login WHERE ID = %s"
            try:
                cursor.execute(query, (soldier_id,))
                result = cursor.fetchone()

                if result:
                    stored_password = result[0]  # Retrieve the password from the query result
                    if entered_password == stored_password:
                        messagebox.showinfo("Done!", "Successfully verified")
                        # Perform any action upon successful validation
                    else:
                        messagebox.showerror("Error", "Password does not match! Please try again.")
                else:
                    messagebox.showerror("Error", "No password found for the given soldier ID.")
            except Exception as e:
                messagebox.showerror("Error", f"Error validating password: {e}")
            finally:
                cursor.close()  # Ensure the cursor is closed after use
                connection.close()  # Close the connection to the database

        # Submit button to validate the password
        CTkButton(
            master=main_frame,
            text="Submit",
            command=validate_password,
            font=("Arial Bold", 14),
            fg_color="#2A8C55",
            text_color="white",
            hover_color="#1E8E3E",
            width=200,
        ).pack(anchor="center", pady=10, padx=10)
        
        # Change Username Button
        # Create a new frame for the buttons
        button_frame = CTkFrame(master=main_frame, fg_color="black")
        button_frame.pack(anchor="center", pady=20)

        # Change Username Button
        CTkButton(
            master=button_frame,
            text="Change Username",
            font=("Arial", 14),
            command=lambda: change_username_window(soldier_id, dashboard_window),
            fg_color="#1E90FF",
            text_color="white",
            hover_color="#4682B4",
            width=140,  # Adjust width as needed
        ).pack(side="left", padx=(10, 20), pady=10)  # Adjust padding as needed

        # Forgot Password Button
        CTkButton(
            master=button_frame,
            text="Forgot Password?",
            command=lambda: forget_password_window(soldier_id, dashboard_window),
            font=("Arial Bold", 14),
            fg_color="#FF4500",
            text_color="white",
            hover_color="#FF6347",
            width=140,  # Adjust width as needed
        ).pack(side="left", padx=(5, 10), pady=10)  # Adjust padding as needed


    def change_username_window(soldier_id,app):
        """Open a new window to change the username."""
        # Create a new window for changing the username
        window = CTkToplevel()
        window.title("Change Username")
        window.geometry("400x300")
        window.resizable(False, False)

        app.withdraw()

        # Make sure the window pops up in front and stays there
        window.attributes("-topmost", True)
        window.focus_force()  # Force focus on this window

        



        CTkLabel(
            master=window,
            text="Change Username",
            font=("Arial Black", 20),
            text_color="#2A8C55",
        ).pack(pady=(20, 10))

        # Entry fields for old and new usernames
        old_username_entry = CTkEntry(
            master=window,
            placeholder_text="Enter Old Username",
            font=("Arial", 14),
            fg_color="white",
            border_width=2,
            corner_radius=5,
        )
        old_username_entry.pack(pady=(10, 5), padx=20, fill="x")

        new_username_entry = CTkEntry(
            master=window,
            placeholder_text="Enter New Username",
            font=("Arial", 14),
            fg_color="white",
            border_width=2,
            corner_radius=5,
        )
        new_username_entry.pack(pady=(5, 20), padx=20, fill="x")
        def on_close():
            """Restore the main window and close the username change window."""
            app.deiconify()  # Restore the main window
            app.geometry("950x645")  # Set the main window to the desired size
            window.destroy()  #
        
        

        def update_username():
            """Update the username in the database."""
            old_username = old_username_entry.get()
            new_username = new_username_entry.get()

            if not old_username or not new_username:
                messagebox.showerror("Error", "Please fill in both fields.")
                return

            query = """
                UPDATE login SET Username = %s WHERE ID = %s AND Username = %s
            """
            try:
                cursor.execute(query, (new_username, soldier_id, old_username))
                if cursor.rowcount > 0:
                    connection.commit()
                    messagebox.showinfo("Success", "Username updated successfully!")
                      # Close the window
                else:
                    messagebox.showerror(
                        "Error",
                        "Old username does not match our records. Please try again.",
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Error updating username: {e}")

        # Confirm button to submit the username change
        CTkButton(
            master=window,
            text="Confirm",
            command=lambda: (update_username() and on_close()),
            font=("Arial Bold", 14),
            fg_color="#2A8C55",
            text_color="white",
            hover_color="#1E8E3E",
        ).pack(pady=(10, 20))

        # Cancel button to close the window
        CTkButton(
            master=window,
            text="Cancel",
            command=on_close,
            font=("Arial Bold", 14),
            fg_color="#FF4500",
            text_color="white",
            hover_color="#FF6347",
        ).pack(pady=(5, 10))
        window.protocol("WM_DELETE_WINDOW", on_close)
        

    def change_password_window(soldier_id):
        """Open a new window with only the 'Forgot Password' option."""
        window = CTkToplevel()
        window.title("Forgot Password")
        window.geometry("400x300")
        window.resizable(False, False)
        app.attributes("-disabled", True)
        
        # Make sure the window pops up in front and stays there
        window.attributes("-topmost", True)
        window.focus_force()  # Force focus on this window


        CTkLabel(
            master=window, text="Forgot Password", font=("Arial Black", 20), text_color="#2A8C55"
        ).pack(pady=20)

        def forget_password():
            """Open a new window for resetting the password."""
            #window.destroy()  # Close the current window
            forget_password_window(soldier_id)

        # Button for "Forgot Password"
        CTkButton(
            master=window, text="Forgot Password?", command=forget_password, fg_color="#FF4500"
        ).pack(pady=50)
        

    def forget_password_window(soldier_id,app):
        """Open a new window to reset the password."""
        forget_window = CTkToplevel()
        forget_window.title("Reset Password")
        forget_window.geometry("400x300")
        forget_window.resizable(False, False)
        app.withdraw()
        
        # Make sure the window pops up in front and stays there
        forget_window.attributes("-topmost", True)
        forget_window.focus_force()  # Force focus on this window

        CTkLabel(
            master=forget_window,
            text="Reset Password",
            font=("Arial Black", 20),
            text_color="#2A8C55",
        ).pack(pady=20)

        # New Password and Confirm Password Entries
        new_password_entry = CTkEntry(
            master=forget_window,
            placeholder_text="Enter New Password",
            font=("Arial", 16),
            fg_color="#3A3A3A",
            border_width=2,
            corner_radius=5,
            text_color="white"
        )
        new_password_entry.pack(pady=10, padx=20,fill='x')


        confirm_password_entry = CTkEntry(
            master=forget_window,
            placeholder_text="Confirm New Password",
            font=("Arial", 16),
            fg_color="#3A3A3A",
            border_width=2,
            corner_radius=5,
            show='*',
            text_color="white"
        )
        confirm_password_entry.pack(pady=10, padx=20,fill='x')
        
        def on_close():
            """Restore the main window and close the username change window."""
            app.deiconify()  # Restore the main window
            app.geometry("950x645")  # Set the main window to the desired size
            forget_window.destroy()
        

        def reset_password():
            """Reset the password in the database."""
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            if not new_password or not confirm_password:
                messagebox.showerror("Error", "Please fill all fields.")
                return

            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            query = """
                UPDATE login SET Password = %s WHERE ID = %s
            """
            try:
                cursor.execute(query, (new_password, soldier_id))
                if cursor.rowcount > 0:
                    connection.commit()
                    messagebox.showinfo("Success", "Password reset successfully.")
                    #forget_window.destroy()  # Close the window
                else:
                    messagebox.showerror("Error", "User not found. Password not reset.")
            except Exception as e:
                messagebox.showerror("Error", f"Error resetting password: {e}")

        # Button to confirm the reset
        CTkButton(
            master=forget_window,
            text="Reset Password",
            command=lambda:(reset_password() and on_close()),
            font=("Arial Bold", 14),
            fg_color="#2A8C55",
            text_color="white",
            hover_color="#1E8E3E",
        ).pack(pady=20)
        
            
        forget_window.protocol("WM_DELETE_WINDOW", on_close)
            


    #--------------adding address 
    sidebar_frame = CTkFrame(master=app, fg_color="#2A8C55", width=176, height=650, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")


    from PIL import Image
    from customtkinter import CTkImage
    import os

    # Use the correct image path
    image_path = r'icons and images\loginimg2.png'

    # Open image using PIL
    logo_img_data = Image.open(image_path)
    global logo_img  # Ensure the image is persistent
    # Convert it to CTkImage for customtkinter
    logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(150, 100))

    # Now use this image in the CTkLabel
    label = CTkLabel(master=sidebar_frame, text="", image=logo_img)
    label.pack(pady=(38, 0), anchor="center")

    analytics_img_data = Image.open(r"icons and images\user-icon.png")
    analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

    # Set up the 'Dashboard' button to call the dashboard function
    dashboard_button = CTkButton(master=sidebar_frame, image=analytics_img, text="Dashboard", fg_color=inactive_button_color, font=("Arial Bold", 14), hover_color=active_button_color, anchor="w", command=dashboard)
    dashboard_button.pack(anchor="center", ipady=5, pady=(60, 0))

    #Set up the 'Personal' button to call the personal function
    personal_img_data = Image.open(r"icons and images\pasw-icon.png")
    personal_img = CTkImage(dark_image=personal_img_data, light_image=personal_img_data)
    pers_button=CTkButton(master=sidebar_frame, image=personal_img, text="Personal", fg_color=inactive_button_color, font=("Arial Bold", 14), text_color="#fff", hover_color=active_button_color, anchor="w",command=soldier_details)
    pers_button.pack(anchor="center", ipady=5, pady=(16, 0))

    
    person_img_data = Image.open(r"icons and images\pasw-icon.png")
    person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
    account_button=CTkButton(master=sidebar_frame, image=person_img, text="Account", fg_color=inactive_button_color, font=("Arial Bold", 14), text_color="#fff", hover_color=active_button_color, anchor="w",command=account)
    account_button.pack(anchor="center", ipady=5, pady=(16, 0))

    # Main view setup
    main_view = CTkFrame(master=app, fg_color="black", width=800, height=650, corner_radius=0)
    main_view.pack_propagate(0)
    main_view.pack(side="left")

    # Automatically call the dashboard when the app starts
    app.protocol("WM_DELETE_WINDOW", lambda: on_close_app())
    dashboard()
#---------------------------------------------------
def on_close_app():
    app.destroy()
    root.deiconify()
    # Reset the login fields
    entry_username.delete(0, "end")
    entry_password.delete(0, "end")


# Function for General view page
def open_general_view():
    global dashboard_window, logo_img, analytics_img, main_view, current_active_button
    dashboard_window = Toplevel(root)  # Initialize the dashboard window here
    dashboard_window.title("General's Dashboard")
    dashboard_window.geometry("1500x900")
    dashboard_window.resizable(False, False)
    dashboard_window.configure(bg="black")

    # Colors for button states
    inactive_button_color = "transparent"
    active_button_color = "#207244"  # Dark green for active button
    current_active_button = None

    # Sidebar frame setup
    sidebar_frame = CTkFrame(master=dashboard_window, fg_color="#2A8C55", width=176, height=650, corner_radius=0)
    sidebar_frame.pack_propagate(0)
    sidebar_frame.pack(fill="y", anchor="w", side="left")

    # Load the logo image for sidebar
    logo_img = CTkImage(dark_image=Image.open(r"icons and images\loginimg2.png"),
                        light_image=Image.open(r"icons and images\loginimg2.png"),
                        size=(150, 100))
    CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

    
    
    # Define the dashboard button in the sidebar
    user_img = CTkImage(dark_image=Image.open(r"icons and images\user-icon.png"),
                             light_image=Image.open(r"icons and images\user-icon.png"))
    dashboard_button = CTkButton(master=sidebar_frame, image=user_img, text="Dashboard",
                                 fg_color="transparent", font=("Arial Bold", 14),
                                 hover_color="#207244", anchor="w", 
                                 command=lambda: dashboard())
    dashboard_button.pack(anchor="center", ipady=5, pady=(60, 0))

    #Set up the 'Personal' button to call the personal function
    personal_img_data = Image.open(r"icons and images\pasw-icon.png")
    personal_img = CTkImage(dark_image=personal_img_data, light_image=personal_img_data)
    pers_button=CTkButton(master=sidebar_frame, image=personal_img, text="Personal", fg_color=inactive_button_color, font=("Arial Bold", 14), text_color="#fff", hover_color=active_button_color, anchor="w",command=lambda: personal())
    pers_button.pack(anchor="center", ipady=5, pady=(16, 0))


    #Set up the 'Add/Edit' button to call the add_edit function
    package_img_data = Image.open(r"icons and images\pasw-icon.png")
    package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)
    add_edit_button=CTkButton(master=sidebar_frame, image=package_img, text="Add/Edit", fg_color=inactive_button_color, font=("Arial Bold", 14), text_color="#fff", hover_color=active_button_color, anchor="w",command=lambda: add_edit())
    add_edit_button.pack(anchor="center", ipady=5, pady=(16, 0))


    #Set up the 'Account' button to call the account function
    person_img_data = Image.open(r"icons and images\user-icon.png")
    person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)

    def account1():
        connection = connect_db()
        cursor = connection.cursor() 

        # Clear the current main view frame
        for widget in main_view.winfo_children():
            widget.destroy()
        
        highlight_button(account_button)

        # Title
        title_frame = CTkFrame(master=main_view, fg_color="black")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        user_frame = CTkFrame(master=main_view, fg_color="black")
        user_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))
        s_name = soldier_name(user_id)
        
        # Load and resize the image
        person_img_data = Image.open(r"icons and images\user2.jpg")
        person_img_data = person_img_data.resize((70, 60), Image.LANCZOS)
        person_img = ImageTk.PhotoImage(person_img_data)

        CTkLabel(master=title_frame, text="Account", font=("Arial Black", 30), text_color="#2A8C55").pack(anchor='nw', pady=(10, 10))
        CTkLabel(
            master=user_frame,
            text=s_name,
            font=("Arial Black", 30),
            text_color="#5bb5d9", image=person_img, compound="left"
        ).pack(anchor="nw", pady=(10, 10), padx=(20, 50))

        # Scrollable frame for content


        m_frame = CTkFrame(master=main_view, bg_color="black", fg_color="black", width=400)
        m_frame.pack(padx=30, pady=20, fill="both", expand=True, anchor="center")

        # Fetch account info
        soldier_id = user_id  # Replace with the logged-in user's ID
        _, username, password = fetch_account(soldier_id)
        main_frame = CTkFrame(master=m_frame, bg_color="black", fg_color="black", width=300,border_width=3,border_color="grey")
        main_frame.pack(padx=30, pady=20, fill="both", expand=True, anchor="center")

        # Handle missing or null username/password
        if username is None:
            CTkLabel(
                master=main_frame,
                text="No account information found!",
                font=("Arial", 20),
                text_color="red",
            ).pack(pady=20)
            return

        # Display account details
        # Create a frame to hold the labels and values
        credentials_frame = CTkFrame(master=main_frame, fg_color="black")
        credentials_frame.pack(anchor="center", pady=20)

        # Username Label
        CTkLabel(
            master=credentials_frame,
            text="Username:",
            font=("Arial", 20),
            text_color="lightblue", 
            fg_color="black",
            corner_radius=10,
            padx=10,
        ).grid(row=0, column=0, padx=10, sticky="w")  

        # Username Value
        CTkLabel(
            master=credentials_frame,
            text=username,  # Display the actual username
            font=("Arial", 20),
            text_color="white",  
            fg_color="black",
            corner_radius=10,
            padx=10,
        ).grid(row=0, column=1, padx=10, sticky="w")  

        # Password Label
        CTkLabel(
            master=credentials_frame,
            text="Password:",
            font=("Arial", 20),
            text_color="lightblue",
            fg_color="black",
            corner_radius=10,
            padx=10,
        ).grid(row=1, column=0, padx=10, sticky="w")

        # Hide password
        hide_pass = '*' * len(password)

        # Password Value
        CTkLabel(
            master=credentials_frame,
            text=hide_pass,  # Display the hidden password
            font=("Arial", 20),
            text_color="white", 
            fg_color="black",
            corner_radius=10,
            padx=10,
        ).grid(row=1, column=1, padx=10, sticky="w")

        # Password Entry
        password_entry = CTkEntry(
            master=main_frame,
            placeholder_text="Verify your password",
            font=("Arial", 16),
            fg_color="#3A3A3A",
            text_color="lightblue",
            border_width=2,
            corner_radius=5,
            width=250,
        )
        password_entry.pack(anchor="center", pady=10, padx=10 )

        def validate_password():
            """Validate the entered password with the database."""
            connection = connect_db()
            cursor = connection.cursor() 
            entered_password = password_entry.get()

            # Query to fetch the password from the database
            query = "SELECT Password FROM login WHERE ID = %s"
            try:
                cursor.execute(query, (soldier_id,))
                result = cursor.fetchone()

                if result:
                    stored_password = result[0]  # Retrieve the password from the query result
                    if entered_password == stored_password:
                        messagebox.showinfo("Done!", "Successfully verified")
                        # Perform any action upon successful validation
                    else:
                        messagebox.showerror("Error", "Password does not match! Please try again.")
                else:
                    messagebox.showerror("Error", "No password found for the given soldier ID.")
            except Exception as e:
                messagebox.showerror("Error", f"Error validating password: {e}")
            finally:
                cursor.close()  # Ensure the cursor is closed after use
                connection.close()  # Close the connection to the database

        # Submit button to validate the password
        CTkButton(
            master=main_frame,
            text="Submit",
            command=validate_password,
            font=("Arial Bold", 14),
            fg_color="#2A8C55",
            text_color="white",
            hover_color="#1E8E3E",
            width=200,
        ).pack(anchor="center", pady=10, padx=10)
        
        # Change Username Button
        # Create a new frame for the buttons
        button_frame = CTkFrame(master=main_frame, fg_color="black")
        button_frame.pack(anchor="center", pady=20)

        # Change Username Button
        CTkButton(
            master=button_frame,
            text="Change Username",
            font=("Arial", 14),
            command=lambda: change_username_window(soldier_id, dashboard_window),
            fg_color="#1E90FF",
            text_color="white",
            hover_color="#4682B4",
            width=140,  # Adjust width as needed
        ).pack(side="left", padx=(10, 20), pady=10)  # Adjust padding as needed

        # Forgot Password Button
        CTkButton(
            master=button_frame,
            text="Forgot Password?",
            command=lambda: forget_password_window(soldier_id, dashboard_window),
            font=("Arial Bold", 14),
            fg_color="#FF4500",
            text_color="white",
            hover_color="#FF6347",
            width=140,  # Adjust width as needed
        ).pack(side="left", padx=(5, 10), pady=10)  # Adjust padding as needed

    account_button=CTkButton(master=sidebar_frame, image=person_img, text="Account",
              fg_color=inactive_button_color, font=("Arial Bold", 14),
              hover_color=active_button_color, anchor="w",command=account1)
    account_button.pack(anchor="center",ipady=5, pady=(130, 0))
 
    # Main content area
    main_view = CTkFrame(master=dashboard_window, fg_color="black", width=800, height=650, corner_radius=0)
    main_view.pack_propagate(0)
    main_view.pack(side="left", fill="both", expand=True)
    #---------------------------------------------------------------------------------------
    # Function to load the dashboard view
    def dashboard():
        # Clear the main view frame
        for widget in main_view.winfo_children():
            widget.destroy()

        connection = connect_db()
        cursor = connection.cursor()
        # Highlight the dashboard button
        highlight_button(dashboard_button)

        # Set up the dashboard UI
        title_frame = CTkFrame(master=main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Welcome, Admin", font=("Arial Black", 30), text_color="#2A8C55").pack(anchor="nw", side="left")

        metrics_frame = CTkFrame(master=main_view, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(36, 0))

        # Soldier metrics
        soldier_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
        soldier_metric.grid_propagate(0)
        soldier_metric.pack(side="left")

        soldier_img_data = Image.open(r"icons and images\military-logos.png")
        soldier_img = CTkImage(light_image=soldier_img_data, dark_image=soldier_img_data, size=(43, 43))
        CTkLabel(master=soldier_metric, image=soldier_img, text="").grid(row=0, column=0, rowspan=2, padx=(12, 5), pady=10)

        query = "SELECT COUNT(ID) from soldiers"
        cursor.execute(query)
        result = cursor.fetchone()
        CTkLabel(master=soldier_metric, text="Total Soldiers", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=soldier_metric, text=result[0], text_color="#fff", font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0, 10))

        # Squad metrics
        squad_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
        squad_metric.grid_propagate(0)
        squad_metric.pack(side="left", expand=True, anchor="center")

        squad_img_data = Image.open(r"icons and images\dbmsicon.png")
        squad_img = CTkImage(light_image=squad_img_data, dark_image=squad_img_data, size=(43, 43))
        CTkLabel(master=squad_metric, image=squad_img, text="").grid(row=0, column=0, rowspan=2, padx=(12, 5), pady=10)

        query = "SELECT COUNT(Squad_ID) from squad"
        cursor.execute(query)
        result = cursor.fetchone()
        CTkLabel(master=squad_metric, text="Total Squads", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=squad_metric, text=result[0], text_color="#fff", font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0, 10))

        # Camp metrics
        camp_metric = CTkFrame(master=metrics_frame, fg_color="#2A8C55", width=200, height=60)
        camp_metric.grid_propagate(0)
        camp_metric.pack(side="right")

        camp_img_data = Image.open(r"icons and images\dbmsicon.png")
        camp_img = CTkImage(light_image=camp_img_data, dark_image=camp_img_data, size=(43, 43))
        CTkLabel(master=camp_metric, image=camp_img, text="").grid(row=0, column=0, rowspan=2, padx=(12, 5), pady=10)

        query = "SELECT COUNT(Camp_name) from camps"
        cursor.execute(query)
        result = cursor.fetchone()
        CTkLabel(master=camp_metric, text="Total Camps", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=camp_metric, text=result[0], text_color="#fff", font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0, 10))

        # Additional Frames for other content
        second_frame = CTkFrame(master=main_view, fg_color="transparent")
        second_frame.pack(anchor="n", fill="x", padx=27, pady=(50, 0))

        CTkLabel(master=second_frame, text="Achievements", font=("Arial Black", 20), text_color="#2A8C55").pack(anchor="nw", side="left")


        third_frame=CTkFrame(master=main_view, fg_color="#2A8C55",height=300,width=100,border_color="grey",border_width=2)
        third_frame.pack(anchor="nw", padx=(40,20), pady=(40, 10))
        cursor.execute("""
        SELECT medal, date_of_receiving
        FROM achievements
        WHERE id = %s
        """,(user_id,))
        result=cursor.fetchone() 
        print(user_id)

        
        print(f"Fetched Achievements: {result}")  # Fetch achievements from the database

        if result:  # Check if result is not empty
              # Loop through each achievement
                medal, date_of_receiving = result

                
        # Create labels for each achievement detail
                soldier_id_label = CTkLabel(
                    master=third_frame, 
                    text=f"Soldier ID: {user_id}",
                    font=("Arial", 14, "bold"),
                    text_color="white",
                    bg_color="transparent"
                )
                soldier_id_label.pack(anchor="w", padx=10, pady=(5, 0))

                medal_label = CTkLabel(
                    master=third_frame, 
                    text=f"Medal: {medal}",
                    font=("Arial", 14, "bold"),
                    text_color="white",
                    bg_color="transparent"
                )
                medal_label.pack(anchor="w", padx=10, pady=(5, 0))

                date_label = CTkLabel(
                    master=third_frame, 
                    text=f"Received on: {date_of_receiving}",
                    font=("Arial", 14, "bold"),
                    text_color="white",
                    bg_color="transparent"
                )
                date_label.pack(anchor="w", padx=10, pady=(5, 10))

        else:
            # Display a message when no achievements are found
            no_achievements_label = CTkLabel(
                master=third_frame, 
                text="No achievements found.", 
                font=("Arial", 14), 
                text_color="red"
            )
            no_achievements_label.pack(pady=(10, 0))

    def personal():
        # Clear the main view
        for widget in main_view.winfo_children():
            widget.destroy()

        connection = connect_db()
        cursor = connection.cursor()
        ID=user_id     

        query1 = '''SELECT s.name, s.dob, s.doj, s.gender, s.height, s.weight, s.division, s.maritial_status,s.blood_type,s.phone_no,s.ranks,s.squad_id
                FROM soldiers s
                WHERE s.ID = %s'''  # Using %s as a placeholder for parameterized query
        # Execute the query with the ID as a parameter
        cursor.execute(query1, (ID,))
        result = cursor.fetchone()
        #query for address
        query2 = '''SELECT a.Pincode, a.District, a.City, a.State, a.Home_phone_no,a.address_line
                FROM address a
                WHERE a.ID = %s'''
        cursor.execute(query2,(ID,))
        result1=cursor.fetchone()
        #query for weapon assigned
        query3 = '''SELECT wa.Weapon_ID, wa.Date,wcl.Weapon_name,wc.Category
                FROM weapon_assigned wa
                JOIN weapon_catalogue wcl ON wcl.Weapon_ID = wa.Weapon_ID 
                Join weapon_category wc on wcl.Category_no=wc.Category_no
                WHERE wa.ID = %s'''
        cursor.execute(query3,(ID,))
        result2=cursor.fetchone()
        #query for squad details:
        query4 = '''SELECT sq.Squad_ID, sq.Camp,c.Captain_name,sq.Year,veh.v_id,veh.V_name,veh.V_model
                FROM squad sq
                JOIN captains c ON c.Squad_ID = sq.Squad_ID 
                JOIN vehicles_assigned v ON v.Squad_ID=sq.Squad_ID
                JOIN vehicles veh ON veh.V_ID=v.V_ID
                WHERE sq.Squad_ID = %s'''
        cursor.execute(query4,(result[11],))
        result3=cursor.fetchone()
        #query for training detail:
        query5 = '''SELECT td.Fitness_score,td.Shooting_accuracy,td.Sprint_speed_100m 
                FROM training_details td
                WHERE td.ID = %s'''
        cursor.execute(query5,(ID,))
        result4=cursor.fetchone()
        # query for achievements:
        query6 = '''SELECT ac.Medal, ac.Date_of_receiving
                FROM achievements ac 
                WHERE ac.ID = %s'''
        cursor.execute(query6,(ID,))
        result5=cursor.fetchone()
        #query for promotion:
        query7 = '''SELECT prom.New_rank,prom.Promotion_date 
                FROM promotion prom 
                WHERE prom.Soldier_ID = %s'''
        cursor.execute(query7,(ID,))
        result6=cursor.fetchone()
        # query for Leaves:
        query8 = '''SELECT lt.No_of_leaves,lt.Reason
                FROM leaves_taken lt
                WHERE lt.ID = %s'''
        cursor.execute(query8,(ID,))
        result7=cursor.fetchone()
        # query for wars:
        query9='''SELECT sur.War_ID,w.Date from war w
                  JOIN soldier_status sur on sur.War_ID=w.War_no
                  where sur.ID=%s'''
        cursor.execute(query9,(ID,))
        result8=cursor.fetchone()
        # Highlight the dashboard button
        highlight_button(pers_button)

        # Function to get value or return "None" if result is None
        def safe_get(value, index):
            return value[index] if value else "None"

        # Add heading for "Personal Details"
        heading_frame = CTkFrame(master=main_view, fg_color="transparent")  
        heading_frame.pack(anchor="nw", fill="x", padx=27, pady=(15, 10))

        CTkLabel(
            master=heading_frame,
            text="Personal Details", 
            font=("Arial Black", 30), 
            text_color="#2A8C55"
        ).pack(anchor="nw", pady=(10, 10))
        IDframe = CTkLabel(master=main_view, text="  ID:  %s"%ID,font=('Arial Black',20,"bold"),text_color='#5bb5d9',fg_color="transparent", width=150)
        IDframe.pack(anchor="nw", padx=(10,10), pady=(50,0))
        # Create a scrollable frame for the main content
        scframe =CTkScrollableFrame(
            master=main_view, 
            height=500,  # Set to desired height
            width=600    # Set to desired width
            ,fg_color='black'
        )
        scframe.pack(fill="both", expand=True, padx=10, pady=20)

        # Personal Details Section

         #adding address title
        myfont=CTkFont(family="Arial",size=20,weight='bold',underline=True)
        main_tframe = CTkLabel(master=scframe, text="Main",font=myfont,fg_color="#b87a2e", width=1500)
        main_tframe.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        det_frame = CTkFrame(master=scframe, fg_color="black", width=1500,border_width=7,border_color='#30302f')  # Increased width for more space
        det_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        CTkLabel(master=det_frame, text="Name:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,0)}", font=("Arial", 14),text_color='white').grid(row=0, column=1, padx=(0, 20), pady=15)

        # Adding details
        CTkLabel(master=det_frame, text="Date of birth:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=2, padx=(80, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,1)}", font=("Arial", 14),text_color='white').grid(row=0, column=3, padx=(0, 20), pady=15)
        CTkLabel(master=det_frame, text="Date of joining:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,2)}", font=("Arial", 14),text_color='white').grid(row=1, column=1, padx=(0, 20), pady=15)
        CTkLabel(master=det_frame, text="Gender:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=2, padx=(80, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,3)}", font=("Arial", 14),text_color='white').grid(row=1, column=3, padx=(0, 20), pady=15)
        CTkLabel(master=det_frame, text="Height:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,4)}", font=("Arial", 14),text_color='white').grid(row=2, column=1, padx=(0, 20), pady=15)
        CTkLabel(master=det_frame, text="Weight:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=2, padx=(80, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,5)}", font=("Arial", 14),text_color='white').grid(row=2, column=3, padx=(0, 20), pady=15)
        CTkLabel(master=det_frame, text="Division:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=3, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,6)}", font=("Arial", 14),text_color='white').grid(row=3, column=1, padx=(0, 20), pady=15)
        CTkLabel(master=det_frame, text="Maritial status:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=3, column=2, padx=(80, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,7)}", font=("Arial", 14),text_color='white').grid(row=3, column=3, padx=(0, 20), pady=15)
        CTkLabel(master=det_frame, text="Blood type:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=4, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,8)}", font=("Arial", 14),text_color='white').grid(row=4, column=1, padx=(0, 20), pady=15)
        CTkLabel(master=det_frame, text="Phone No", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=4, column=2, padx=(80, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,9)}", font=("Arial", 14),text_color='white').grid(row=4, column=3, padx=(0, 20), pady=15)
        CTkLabel(master=det_frame, text="Rank:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=5, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=det_frame, text=f"{safe_get(result,10)}", font=("Arial", 14),text_color='white').grid(row=5, column=1, padx=(0, 20), pady=15)

        #--------------adding address 
        adres_tframe = CTkLabel(master=scframe, text="Address",font=myfont,fg_color="#b87a2e", width=1500)
        adres_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        addrs_frame = CTkFrame(master=scframe, fg_color="black", width=1500,border_width=7,border_color='#30302f')  # Increased width for more space
        addrs_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))
        #Pincode
        CTkLabel(master=addrs_frame, text="Pincode:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,0)}", font=("Arial", 14),text_color='white').grid(row=0, column=1, padx=(0, 20), pady=15)
        #District
        CTkLabel(master=addrs_frame, text="District:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=2, padx=(140, 10), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,1)}", font=("Arial", 14),text_color='white').grid(row=0, column=3, padx=(0, 20), pady=15)
        #city
        CTkLabel(master=addrs_frame, text="City:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,2)}", font=("Arial", 14),text_color='white').grid(row=1, column=1, padx=(0, 20), pady=15)
        #state
        CTkLabel(master=addrs_frame, text="State:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=2, padx=(140, 10), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,3)}", font=("Arial", 14),text_color='white').grid(row=1, column=3, padx=(0, 20), pady=15)
        #Home Phone
        CTkLabel(master=addrs_frame, text="Home Phone:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=0, padx=(140, 10), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,4)}", font=("Arial", 14),text_color='white').grid(row=2, column=1, padx=(0, 20), pady=15)
        #Address line
        CTkLabel(master=addrs_frame, text="Address line:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=2, padx=(140, 10), pady=15, sticky="w")
        CTkLabel(master=addrs_frame, text=f"{safe_get(result1,5)}", font=("Arial", 14),text_color='white').grid(row=2, column=3, padx=(0, 20), pady=15)

        #--------------adding weapon assigned
        was_tframe = CTkLabel(master=scframe, text="Weapon Assigned",font=myfont,fg_color="#b87a2e", width=1500)
        was_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        was_frame = CTkFrame(master=scframe, fg_color="black", width=1500,border_width=7,border_color='#30302f')  # Increased width for more space
        was_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))
        #Weapon ID
        CTkLabel(master=was_frame, text="Weapon ID:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=was_frame, text=f"{safe_get(result2,0)}", font=("Arial", 14),text_color='white').grid(row=0, column=1, padx=(0, 20), pady=15)
        #Date assigned
        CTkLabel(master=was_frame, text="Date assigned:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=was_frame, text=f"{safe_get(result2,1)}", font=("Arial", 14),text_color='white').grid(row=0, column=3, padx=(0, 20), pady=15)
        #Weapon name
        CTkLabel(master=was_frame, text="Weapon name:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=was_frame, text=f"{safe_get(result2,2)}", font=("Arial", 14),text_color='white').grid(row=1, column=1, padx=(0, 20), pady=15)
        #Category
        CTkLabel(master=was_frame, text="Category:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=was_frame, text=f"{safe_get(result2,3)}", font=("Arial", 14),text_color='white').grid(row=1, column=3, padx=(0, 20), pady=15)

        #--------------adding squad details
        sq_tframe = CTkLabel(master=scframe, text="Squad Details",font=myfont,fg_color="#b87a2e", width=1500)
        sq_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        sq_frame = CTkFrame(master=scframe, fg_color="black", width=1500,border_width=7,border_color='#30302f')  # Increased width for more space
        sq_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))
        #Squad ID
        CTkLabel(master=sq_frame, text="Squad ID:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,0)}", font=("Arial", 14),text_color='white').grid(row=0, column=1, padx=(0, 20), pady=15)
        #DCamp name
        CTkLabel(master=sq_frame, text="Camp name:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,1)}", font=("Arial", 14),text_color='white').grid(row=0, column=3, padx=(0, 20), pady=15)
        #Captain name
        CTkLabel(master=sq_frame, text="Captain name:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,2)}", font=("Arial", 14),text_color='white').grid(row=1, column=1, padx=(0, 20), pady=15)
        #Year
        CTkLabel(master=sq_frame, text="Year:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,3)}", font=("Arial", 14),text_color='white').grid(row=1, column=3, padx=(0, 20), pady=15)
        #Vehcile No
        CTkLabel(master=sq_frame, text="Vehcile No:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=0, padx=(70, 10), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,4)}", font=("Arial", 14),text_color='white').grid(row=2, column=1, padx=(0, 20), pady=15)
        #Vehicle Name
        CTkLabel(master=sq_frame, text="Vehicle Name:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=2, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,5)}", font=("Arial", 14),text_color='white').grid(row=2, column=3, padx=(0, 20), pady=15)
        #Vehicle model
        CTkLabel(master=sq_frame, text="Vehicle model:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=3, column=0, padx=(70, 10), pady=15, sticky="w")
        CTkLabel(master=sq_frame, text=f"{safe_get(result3,6)}", font=("Arial", 14),text_color='white').grid(row=3, column=1, padx=(0, 20), pady=15)

        #------------training detials
        tr_tframe = CTkLabel(master=scframe, text="Training Details",font=myfont,fg_color="#b87a2e", width=1500)
        tr_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        tr_frame = CTkFrame(master=scframe, fg_color="black", width=1500,border_width=7,border_color='#30302f')  # Increased width for more space
        tr_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))
        #Squad ID
        CTkLabel(master=tr_frame, text="Fitness Score:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=tr_frame, text=f"{safe_get(result4,0)}", font=("Arial", 14),text_color='white').grid(row=0, column=1, padx=(0, 20), pady=15)
        #DCamp name
        CTkLabel(master=tr_frame, text="Shooting Accuracy:", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=0, column=2, padx=(123, 10), pady=15, sticky="w")
        CTkLabel(master=tr_frame, text=f"{safe_get(result4,1)}", font=("Arial", 14),text_color='white').grid(row=0, column=3, padx=(0, 20), pady=15)
        #Captain name
        CTkLabel(master=tr_frame, text="Sprint Speed (mph):", font=("Georgia", 16, "bold"),text_color='#3bbf75').grid(row=1, column=0, padx=(70, 20), pady=15, sticky="w")
        CTkLabel(master=tr_frame, text=f"{safe_get(result4,2)}", font=("Arial", 14),text_color='white').grid(row=1, column=1, padx=(0, 20), pady=15)
        
        #------------Achievements
        ac_tframe = CTkLabel(master=scframe, text="Achievements", font=myfont, fg_color="#b87a2e", width=1500)
        ac_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        ac_frame = CTkFrame(master=scframe, fg_color="black", width=1500, border_width=7, border_color='#30302f')
        ac_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        if result5 and (result5[0] or result5[1]):
            CTkLabel(master=ac_frame, text="Medal:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
            CTkLabel(master=ac_frame, text="Date of receiving:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=2, padx=(123, 10), pady=15, sticky="w")

            if isinstance(result5[0], list) and isinstance(result5[1], list):
                for i in range(len(result5[0])):
                    CTkLabel(master=ac_frame, text=f"{result5[0][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=0, padx=(70, 20), pady=15)
                    CTkLabel(master=ac_frame, text=f"{result5[1][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=2, padx=(65, 20), pady=15)
            else:
                CTkLabel(master=ac_frame, text=f"{result5[0]}", font=("Arial", 14), text_color='white').grid(row=1, column=0, padx=(70, 20), pady=15)
                CTkLabel(master=ac_frame, text=f"{result5[1]}", font=("Arial", 14), text_color='white').grid(row=1, column=2, padx=(65, 20), pady=15)
        else:
            CTkLabel(master=ac_frame, text="Null", font=("Arial", 14), text_color='white').pack(pady=15)

        # Promotion
        tr_tframe = CTkLabel(master=scframe, text="Promotion", font=myfont, fg_color="#b87a2e", width=1500)
        tr_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        tr_frame = CTkFrame(master=scframe, fg_color="black", width=1500, border_width=7, border_color='#30302f')
        tr_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        if result6 and (result6[0] or result6[1]):
            CTkLabel(master=tr_frame, text="New Rank:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
            CTkLabel(master=tr_frame, text="Promotion Date:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=3, padx=(235, 10), pady=15, sticky="w")

            if isinstance(result6[0], list) and isinstance(result6[1], list):
                for i in range(len(result6[0])):
                    CTkLabel(master=tr_frame, text=f"{result6[0][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=0, padx=(0, 20), pady=15)
                    CTkLabel(master=tr_frame, text=f"{result6[1][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=3, padx=(0, 20), pady=15)
            else:
                CTkLabel(master=tr_frame, text=f"{result6[0]}", font=("Arial", 14), text_color='white').grid(row=1, column=0, padx=(27, 20), pady=15)
                CTkLabel(master=tr_frame, text=f"{result6[1]}", font=("Arial", 14), text_color='white').grid(row=1, column=3, padx=(185, 20), pady=15)
        else:
            CTkLabel(master=tr_frame, text="Null", font=("Arial", 14), text_color='white').pack(pady=15)

        # Leaves Taken
        lv_tframe = CTkLabel(master=scframe, text="Leaves taken", font=myfont, fg_color="#b87a2e", width=1500)
        lv_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        lv_frame = CTkFrame(master=scframe, fg_color="black", width=1500, border_width=7, border_color='#30302f')
        lv_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        if result7 and (result7[0] or result7[1]):
            CTkLabel(master=lv_frame, text="No of leaves:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
            CTkLabel(master=lv_frame, text="Reason:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=2, padx=(220, 10), pady=15, sticky="w")

            if isinstance(result7[0], list) and isinstance(result7[1], list):
                for i in range(len(result7[0])):
                    CTkLabel(master=lv_frame, text=f"{result7[0][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=0, padx=(70, 20), pady=15)
                    CTkLabel(master=lv_frame, text=f"{result7[1][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=2, padx=(185, 20), pady=15)
            else:
                CTkLabel(master=lv_frame, text=f"{result7[0]}", font=("Arial", 14), text_color='white').grid(row=1, column=0, padx=(0, 20), pady=15)
                CTkLabel(master=lv_frame, text=f"{result7[1]}", font=("Arial", 14), text_color='white').grid(row=1, column=2, padx=(220, 10), pady=15)
        else:
            CTkLabel(master=lv_frame, text="Null", font=("Arial", 14), text_color='white').pack(pady=15)

        # Contributed Wars
        war_tframe = CTkLabel(master=scframe, text="Contributed Wars:", font=myfont, fg_color="#b87a2e", width=1500)
        war_tframe.pack(anchor="n", fill="x", padx=27, pady=(30, 0))

        war_frame = CTkFrame(master=scframe, fg_color="black", width=1500, border_width=7, border_color='#30302f')
        war_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

        if result8 and (result8[0] or result8[1]):
            CTkLabel(master=war_frame, text="War ID:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=0, padx=(70, 20), pady=15, sticky="w")
            CTkLabel(master=war_frame, text="Date:", font=("Georgia", 16, "bold"), text_color='#3bbf75').grid(row=0, column=2, padx=(260, 10), pady=15, sticky="w")

            if isinstance(result8[0], list) and isinstance(result8[1], list):
                for i in range(len(result8[0])):
                    CTkLabel(master=war_frame, text=f"{result8[0][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=0, padx=(32, 20), pady=15)
                    CTkLabel(master=war_frame, text=f"{result8[1][i]}", font=("Arial", 14), text_color='white').grid(row=1 + i, column=3, padx=(260, 20), pady=15)
            else:
                CTkLabel(master=war_frame, text=f"{result8[0]}", font=("Arial", 14), text_color='white').grid(row=1, column=0, padx=(32, 20), pady=15)
                CTkLabel(master=war_frame, text=f"{result8[1]}", font=("Arial", 14), text_color='white').grid(row=1, column=2, padx=(260, 10), pady=15)
        else:
            CTkLabel(master=war_frame, text="Null", font=("Arial", 14), text_color='white').pack(pady=15)
    
    #add/edit function
    def add_edit():
        # Additional functions:
        def submit_edits_camp():
            connection = connect_db()
            cursor = connection.cursor()

            # Get input values
            ent = str_entry.get()
            camp = c_combo.get()

            try:
                # Validate if the entered value is an integer
                ent_int = int(ent)  # Convert entry value to an integer
                if ent_int > 0:
                    # Execute the insertion into the database
                    cursor.execute("UPDATE camps SET camp_strength = %s WHERE camp_name = %s", (ent_int, camp))
                    connection.commit()  # Ensure changes are saved
                    messagebox.showinfo("Submit", "Details have been successfully edited!")
                else:
                    messagebox.showerror("Input Error", "Camp strength must be greater than 0.")
            except ValueError:
                # Handle cases where ent cannot be converted to an integer
                messagebox.showerror("Input Error", "Please enter a valid integer for camp strength.")
            
            connection.close()

        def submit_edits_squad():
            connection = connect_db()
            cursor = connection.cursor()

            # Get input values
            sq=int(sq_id.get())
            nos=int(n_sold.get())
            camp=camp_e.get()
            yr=year_e.get()

            try:
                if nos > 0:
                    # Execute the insertion into the database
                    cursor.execute("""UPDATE squad SET No_of_soldiers = %s, camp=%s, year=%s
                                     WHERE squad_id = %s""", (nos, camp,yr,sq))
                    connection.commit()  # Ensure changes are saved
                    messagebox.showinfo("Submit", "Details have been successfully edited!")
                else:
                    messagebox.showerror("Input Error", "Number of soldiers must be greater than 0.")
            except ValueError:
                # Handle cases where ent cannot be converted to an integer
                messagebox.showerror("Input Error", "Please enter valid inputs.")
            
            connection.close()

        def submit_edit_recruit():
            connection = connect_db()
            cursor = connection.cursor()

            # Get input values
            id=id_e.get()
            name=nam.get()
            dateob=dob.get()
            dateoj=doj.get()
            gender=gend.get()
            hght=height.get()
            wght=weight.get()
            divis=div.get()
            mari=mart.get()
            bld=bld_type.get()
            phono=phn.get()
            rnk=rank.get()
            cmp=camp.get()
            squadid=sid.get()
            adrs=adrs_line_entry.get()
            city=city_entry.get()
            state=state_entry.get()
            district=district_entry.get()
            pin=pin_entry.get()
            hmphn=hmphn_entry.get()
            un=login_entry.get()
            pw=pw_entry.get()

            try:
                # Perform validation checks (you can add more if necessary)
                if not name or not dateob or not dateoj or not gender or not hght or not wght or not divis or not mari or not bld or not phono or not rnk or not cmp or not squadid:
                    messagebox.showerror("Input Error", "All fields must be filled out.")
                    return

                # Execute the update in the database
                cursor.execute("""
                    UPDATE soldiers
                    SET name = %s, dob = %s, doj = %s, gender = %s,
                        height = %s, weight = %s, division = %s, maritial_status = %s,
                        blood_type = %s, phone_no= %s, ranks = %s, camp = %s, squad_id = %s
                    WHERE id = %s
                """, (name, dateob, dateoj, gender, hght, wght, divis, mari, bld, phono, rnk, cmp, squadid,id))

                cursor.execute("""Update address set pincode=%s,district=%s,city=%s,state=%s,home_phone_no=%s,address_line=%s 
                               where id=%s""",(pin,district,city,state,hmphn,adrs,id))
                cursor.execute("""update login set username=%s,password=%s where id=%s
                               """,(un,pw,id))
                connection.commit()  # Commit changes to the database
                messagebox.showinfo("Submit", "Recruit details have been successfully updated!")
            
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid inputs.")            
            connection.close()

        def fetch_values_from_db():
            try:
                connection = connect_db()
                cursor = connection.cursor()

                cursor.execute("SELECT DISTINCT rank_name FROM Ranks")
                ranks = [row[0] for row in cursor.fetchall()] or ["No value"]

                cursor.execute("SELECT DISTINCT Camp_name FROM Camps")
                camps = [row[0] for row in cursor.fetchall()] or ["No value"]

                cursor.execute("SELECT DISTINCT Squad_ID FROM Squad")
                squads = [row[0] for row in cursor.fetchall()] or ["No value"]
                
                cursor.execute("SELECT DISTINCT Div_name FROM Divisions")
                divis = [row[0] for row in cursor.fetchall()] or ["No value"]

            except Exception as e:
                messagebox.showerror("Database Error", f"Error fetching values: {str(e)}")
                ranks, camps, squads, divis = ["No value"], ["No value"], ["No value"],["No value"]

            finally:
                connection.close()

            return ranks, camps, squads, divis

        # Submit function with validation and storing data in variables
        def submit_add():
            #Adding values to table rank and division
            
            if validate_form_add():
                # Capture entered data from the form
                recruit_id = id_entry.get()
                name = name_entry.get()
                dob = dob_entry.get()
                doj = doj_entry.get()
                gender = gender_combo.get()
                height = height_entry.get()
                weight = weight_entry.get()
                division=div_combo.get()
                maritial=marr_combo.get()
                blood=blood_entry.get()
                pno=pno_entry.get()
                rank = rank_combo.get()
                camp_name = camp_combo.get()
                squad_id = squad_combo.get()

                adrline=adrs_line_entry.get()
                city=city_entry.get()
                district=district_entry.get()
                state=state_entry.get()
                pin=pin_entry.get()
                hmphn=hmphn_entry.get()

                un=login_entry.get()
                pw=pw_entry.get()

                # Check if the phone number has exactly 10 digits
                if len(pno) != 10 or not pno.isdigit():
                    messagebox.showerror("Input Error", "Phone number must be exactly 10 digits.")
                    return
                        
                connection=connect_db()
                cursor=connection.cursor()
                cursor.execute("""
                INSERT INTO soldiers (id,name, dob, doj, gender, height, weight,division,maritial_status,blood_type,phone_no,ranks, camp, squad_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (recruit_id,name, dob, doj, gender, height, weight,division,maritial,blood,pno, rank, camp_name, squad_id))
                
                cursor.execute("""INSERT into address(id,pincode,district,city,state,home_phone_no,address_line)
                               values (%s,%s,%s,%s,%s,%s,%s)""",(recruit_id,pin,district,city,state,hmphn,adrline))
                
                cursor.execute("""Insert into login(id,username,password) values(%s,%s,%s)""",(recruit_id,un,pw))
                messagebox.showinfo("Submit", "Details have been successfully added!")  # Logic to capture edited data and update in the database
                connection.commit()
                connection.close()
            else:
                return
        
        #--- -------        -----------------      -----------------
        
        # Function to create form for adding new recruit
        def create_recruit_form(parent_frame):
            # Create a scrollable frame for the main content
            scframe = ctk.CTkScrollableFrame(
                master=parent_frame, 
                height=500,  # Set to desired height
                width=1500    # Set to desired width
                ,fg_color='black'
            )
            scframe.pack(fill="x", expand=True, padx=10, pady=(10,0))

            # Predefined options for Gender and Marital Status
            global name_entry, id_entry, dob_entry, doj_entry, gender_combo, rank_combo, camp_combo, squad_combo, height_entry, weight_entry, div_combo, marr_combo, blood_entry, pno_entry
            global adrs_line_entry,pin_entry,state_entry,city_entry,hmphn_entry,district_entry,login_entry,pw_entry
            genders = ["Male", "Female"]
            marri = ["Married", "Unmarried"]
            
            CTkLabel(master=scframe, text="Add New Recruit", font=("Arial", 18), text_color="#2A8C55").pack(anchor="nw", pady=(15, 10))

            # Create a frame for the form with increased width
            form_frame = CTkFrame(master=scframe, fg_color="#d5ebe6", width=1000)  # Increased width for more space
            form_frame.pack(anchor="n", fill="x", padx=20, pady=(10, 0))


            # Grid layout with adjusted padding and spacing for better alignment
            CTkLabel(master=form_frame, text="Name:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            name_entry = CTkEntry(master=form_frame, width=200)
            name_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="ID:", font=("Arial", 14)).grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            id_entry = CTkEntry(master=form_frame, width=200)
            id_entry.grid(row=0, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="DOB:", font=("Arial", 14)).grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            dob_entry = CTkEntry(master=form_frame, width=200)
            dob_entry.grid(row=1, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="DOJ:", font=("Arial", 14)).grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            doj_entry = CTkEntry(master=form_frame, width=200)
            doj_entry.grid(row=1, column=3, padx=(0, 10), pady=(10, 10))

            # Dropdowns for Gender, Rank, Camp Name, and Squad ID
            ranks, camps, squads, divis = fetch_values_from_db()

            CTkLabel(master=form_frame, text="Gender:", font=("Arial", 14)).grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            gender_combo = CTkComboBox(master=form_frame, values=genders, width=200)
            gender_combo.set("Select Gender")
            gender_combo.grid(row=2, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Rank:", font=("Arial", 14)).grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            rank_combo = CTkComboBox(master=form_frame, values=ranks, width=200)
            rank_combo.set("Select Rank")
            rank_combo.grid(row=2, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Camp Name:", font=("Arial", 14)).grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            camp_combo = CTkComboBox(master=form_frame, values=camps, width=200)
            camp_combo.set("Select Camp")
            camp_combo.grid(row=3, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Squad ID:", font=("Arial", 14)).grid(row=3, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            squads = [str(squad) for squad in squads]  # Ensure all items are strings
            squad_combo = CTkComboBox(master=form_frame, values=squads, width=200)
            squad_combo.set("Select Squad ID")
            squad_combo.grid(row=3, column=3, padx=(0, 10), pady=(10, 10))

            # Additional fields for Height and Weight
            CTkLabel(master=form_frame, text="Height:", font=("Arial", 14)).grid(row=4, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            height_entry = CTkEntry(master=form_frame, width=200)
            height_entry.grid(row=4, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Weight:", font=("Arial", 14)).grid(row=4, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            weight_entry = CTkEntry(master=form_frame, width=200)
            weight_entry.grid(row=4, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Division:", font=("Arial", 14)).grid(row=5, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            div_combo = CTkComboBox(master=form_frame, values=divis, width=200)
            div_combo.set("Select division")
            div_combo.grid(row=5, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Marital Status:", font=("Arial", 14)).grid(row=5, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            marr_combo = CTkComboBox(master=form_frame, values=marri, width=200)
            marr_combo.set("Select status")
            marr_combo.grid(row=5, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Blood Type:", font=("Arial", 14)).grid(row=6, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            blood_entry = CTkEntry(master=form_frame, width=200)
            blood_entry.grid(row=6, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Phone Number:", font=("Arial", 14)).grid(row=6, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            pno_entry = CTkEntry(master=form_frame, width=200)
            pno_entry.grid(row=6, column=3, padx=(0, 10), pady=(10, 10))

            #now adding address frame and their entries
            CTkLabel(master=scframe, text="Add address detail", font=("Arial", 18), text_color="#2A8C55").pack(anchor="nw", pady=(25, 10))
            adrs_frame = CTkFrame(master=scframe, fg_color="#d5ebe6", width=1000)  # Increased width for more space
            adrs_frame.pack(anchor="n", fill="x", padx=20, pady=(10, 20))

            CTkLabel(master=adrs_frame, text="Address line:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            adrs_line_entry = CTkEntry(master=adrs_frame, width=200)
            adrs_line_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=adrs_frame, text="City:", font=("Arial", 14)).grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            city_entry = CTkEntry(master=adrs_frame, width=200)
            city_entry.grid(row=0, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=adrs_frame, text="State:", font=("Arial", 14)).grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            state_entry = CTkEntry(master=adrs_frame, width=200)
            state_entry.grid(row=1, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=adrs_frame, text="District:", font=("Arial", 14)).grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            district_entry = CTkEntry(master=adrs_frame, width=200)
            district_entry.grid(row=1, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=adrs_frame, text="Pincode:", font=("Arial", 14)).grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            pin_entry = CTkEntry(master=adrs_frame, width=200)
            pin_entry.grid(row=2, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=adrs_frame, text="Home-PhoneNo:", font=("Arial", 14)).grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            hmphn_entry = CTkEntry(master=adrs_frame, width=200)
            hmphn_entry.grid(row=2, column=3, padx=(0, 10), pady=(10, 10))


            #now adding login frame and their entries
            CTkLabel(master=scframe, text="Add Login detail", font=("Arial", 18), text_color="#2A8C55").pack(anchor="nw", pady=(25, 10))
            log_frame = CTkFrame(master=scframe, fg_color="#d5ebe6", width=1000)  # Increased width for more space
            log_frame.pack(anchor="n", fill="x", padx=20, pady=(10, 20))

            CTkLabel(master=log_frame, text="Username:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            login_entry = CTkEntry(master=log_frame, width=200)
            login_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=log_frame, text="Password:", font=("Arial", 14)).grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            pw_entry = CTkEntry(master=log_frame, width=200)
            pw_entry.grid(row=0, column=3, padx=(0, 10), pady=(10, 10))

            
            # Submit Button
            submit_button = CTkButton(
                master=scframe,
                text="Submit",
                fg_color='#029cd9',
                font=("Arial Bold", 14),
                text_color="#fff",
                hover_color="#207244",
                command=submit_add 
            )
            submit_button.pack(pady=(5, 50), anchor="center")
        
        def validate_form_add():
            # Check if all required fields have data
            if not name_entry.get():
                messagebox.showerror("Input Error", "Please enter the Name.")
                return False
            if not id_entry.get():
                messagebox.showerror("Input Error", "Please enter the ID.")
                return False
            if not dob_entry.get():
                messagebox.showerror("Input Error", "Please enter the Date of Birth.")
                return False
            if not doj_entry.get():
                messagebox.showerror("Input Error", "Please enter the Date of Joining.")
                return False
            if gender_combo.get() == "Select Gender":
                messagebox.showerror("Input Error", "Please select the Gender.")
                return False
            if rank_combo.get() == "Select Rank":
                messagebox.showerror("Input Error", "Please select the Rank.")
                return False
            if camp_combo.get() == "Select Camp":
                messagebox.showerror("Input Error", "Please select the Camp Name.")
                return False
            if squad_combo.get() == "Select Squad ID":
                messagebox.showerror("Input Error", "Please select the Squad ID.")
                return False
            if not height_entry.get():
                messagebox.showerror("Input Error", "Please enter the Height.")
                return False
            if not weight_entry.get():
                messagebox.showerror("Input Error", "Please enter the Weight.")
                return False
            if div_combo.get() == "Select division":
                messagebox.showerror("Input Error", "Please select the Division.")
                return False
            if marr_combo.get() == "Select status":
                messagebox.showerror("Input Error", "Please select the Marital Status.")
                return False
            if not blood_entry.get():
                messagebox.showerror("Input Error", "Please enter the Blood Type.")
                return False
            if not pno_entry.get() or len(pno_entry.get()) != 10 or not pno_entry.get().isdigit():
                messagebox.showerror("Input Error", "Phone number must be exactly 10 digits.")
                return False
            if not adrs_line_entry.get() or not city_entry.get() or not district_entry.get() or not pin_entry.get() or not state_entry.get() or not hmphn_entry.get():
                messagebox.showerror("Input Error","Please enter all the address details")
            if not hmphn_entry.get() or len(hmphn_entry.get()) != 10 or not hmphn_entry.get().isdigit():
                messagebox.showerror("Input Error", "Phone number must be exactly 10 digits.")
                return False
            # If all checks pass, return True
            return True

        
        def create_edit_recruit_form(parent_frame):
            global id_e, nam, dob, doj, gend, rank, height, weight, camp, sid, div, mart, bld_type, phn,adrs_line_entry,city_entry,state_entry,district_entry
            global pin_entry,hmphn_entry,login_entry,pw_entry

            # Create a scrollable frame for the main content
            scframe = ctk.CTkScrollableFrame(
                master=parent_frame, 
                height=500,  # Set to desired height
                width=1500,  # Set to desired width
                fg_color='black'
            )
            scframe.pack(fill="x", expand=True, padx=10, pady=(10, 0))

            connection = connect_db()
            cursor = connection.cursor()
            CTkLabel(master=scframe, text="Edit Recruit Details", font=("Arial", 18), text_color="#2A8C55").pack(anchor="nw", pady=(15, 10))

            # Create a frame for the form with increased width
            form_frame = CTkFrame(master=scframe, fg_color="#d5ebe6", width=1200)  # Increased width for more space
            form_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

            cursor.execute("""SELECT ID FROM soldiers""")
            ids = cursor.fetchall()
            id_list = [str(a[0]) for a in ids]
            def set_field(entry, value):
                entry.delete(0, 'end')
                entry.insert(0, value if value is not None else "None")
            # Define the function to handle selection
            def on_id_selected(selected_id):
                try:
                    connection = connect_db()  # Ensure connection is established
                    cursor = connection.cursor()
                    cursor.execute("""SELECT name, dob, doj, gender, ranks, height, weight, maritial_status, blood_type, phone_no, camp, squad_id, division FROM soldiers WHERE ID = %s""", (selected_id,))
                    result = cursor.fetchone()
                    cursor.execute("""SELECT address_line,city,state,district,pincode,home_phone_no from address where ID = %s""", (selected_id,))
                    result1=cursor.fetchone()
                    cursor.execute("""SELECT username,password from login where ID = %s""", (selected_id,))
                    result2=cursor.fetchone()

                    if result:
                        # Populate the form fields with the fetched data for soldier details
                        set_field(nam, result[0])  # Name
                        set_field(dob, result[1])  # DOB
                        set_field(doj, result[2])  # DOJ
                        gend.set(result[3] if result[3] is not None else "None")  # Gender
                        rank.set(result[4] if result[4] is not None else "None")  # Rank
                        set_field(height, result[5])  # Height
                        set_field(weight, result[6])  # Weight
                        mart.set(result[7] if result[7] is not None else "None")  # Marital Status
                        set_field(bld_type, result[8])  # Blood Type
                        set_field(phn, result[9])  # Phone No
                        camp.set(result[10] if result[10] is not None else "None")  # Camp Name
                        sid.set(result[11] if result[11] is not None else "None")  # Squad ID
                        div.set(result[12] if result[12] is not None else "None")  # Division

                        if result1:  # Check if result1 is not None
                            set_field(adrs_line_entry, result1[0])  # Address line
                            set_field(city_entry, result1[1])  # City
                            set_field(state_entry, result1[2])  # State
                            set_field(district_entry, result1[3])  # District
                            set_field(pin_entry, result1[4])  # Pincode
                            set_field(hmphn_entry, result1[5])  # Home Phone No
                        else:
                            # If result1 is None, clear the address fields or set them to "None"
                            set_field(adrs_line_entry, None)
                            set_field(city_entry, None)
                            set_field(state_entry, None)
                            set_field(district_entry, None)
                            set_field(pin_entry, None)
                            set_field(hmphn_entry, None)

                        # Populate the login details if they exist
                        if result2:  # Check if result2 is not None
                            login_entry.delete(0, 'end')
                            login_entry.insert(0, result2[0] if result2[0] is not None else "None")  # Username
                            pw_entry.delete(0, 'end')
                            pw_entry.insert(0, result2[1] if result2[1] is not None else "None")  # Password
                        else:
                            login_entry.delete(0, 'end')
                            login_entry.insert(0, "None")  # Username
                            pw_entry.delete(0, 'end')
                            pw_entry.insert(0, "None")  # Password

                    else:
                        print("No data found for the selected ID.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    connection.close()  # Ensure the connection is closed

            # Create the ComboBox for selecting Recruit ID
            CTkLabel(master=form_frame, text="ID:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            id_e = CTkComboBox(master=form_frame, values=id_list, width=180, command=on_id_selected)
            id_e.grid(row=0, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Name:", font=("Arial", 14)).grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            nam = CTkEntry(master=form_frame, width=180)
            nam.grid(row=1, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="DOB:", font=("Arial", 14)).grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            dob = CTkEntry(master=form_frame, width=180)
            dob.grid(row=1, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="DOJ:", font=("Arial", 14)).grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            doj = CTkEntry(master=form_frame, width=180)
            doj.grid(row=2, column=1, padx=(0, 10), pady=(10,  10))

            CTkLabel(master=form_frame, text="Gender:", font=("Arial", 14)).grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            gend = CTkComboBox(master=form_frame, values=["Male", "Female"], width=180)
            gend.grid(row=2, column=3, padx=(0, 10), pady=(10, 10))

            cursor.execute("""SELECT rank_name FROM ranks """)
            values = [a[0] for a in cursor.fetchall()]
            CTkLabel(master=form_frame, text="Rank:", font=("Arial", 14)).grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            rank = CTkComboBox(master=form_frame, values=values, width=180)
            rank.grid(row=3, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Height(cm):", font=("Arial", 14)).grid(row=3, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            height = CTkEntry(master=form_frame, width=180)
            height.grid(row=3, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Weight(kg):", font=("Arial", 14)).grid(row=4, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            weight = CTkEntry(master=form_frame, width=180)
            weight.grid(row=4, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Marital status:", font=("Arial", 14)).grid(row=4, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            mart = CTkComboBox(master=form_frame, values=["Married", "Unmarried"], width=180)
            mart.grid(row=4, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Blood type:", font=("Arial", 14)).grid(row=5, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            bld_type = CTkEntry(master=form_frame, width=180)
            bld_type.grid(row=5, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=form_frame, text="Phone No:", font=("Arial", 14)).grid(row=5, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            phn = CTkEntry(master=form_frame, width=180)
            phn.grid(row=5, column=3, padx=(0, 10), pady=(10, 10))

            cursor.execute("""SELECT camp_name FROM camps""")
            camps = cursor.fetchall()
            camp_values = [camp[0] for camp in camps]
            CTkLabel(master=form_frame, text="Camp Name:", font=("Arial", 14)).grid(row=6, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            camp = CTkComboBox(master=form_frame, values=camp_values, width=180)
            camp.grid(row=6, column=1, padx=(0, 10), pady=(10, 10))

            cursor.execute("""SELECT squad_id FROM squad """)
            sq_values = [str(a[0]) for a in cursor.fetchall()]
            CTkLabel(master=form_frame, text="Squad ID:", font=("Arial", 14)).grid(row=6, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            sid = CTkComboBox(master=form_frame, values=sq_values, width=180)
            sid.grid(row=6, column=3, padx=(0, 10), pady=(10, 10))

            cursor.execute("""SELECT div_name FROM divisions """)
            div_values = [str(a[0]) for a in cursor.fetchall()]
            CTkLabel(master=form_frame, text="Division:", font=("Arial", 14)).grid(row=7, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            div = CTkComboBox(master=form_frame, values=div_values, width=180)
            div.grid(row=7, column=1, padx=(0, 10), pady=(10, 10))

            connection.close()  # Close the database connection after use
            # Now adding address frame and their entries
            CTkLabel(master=scframe, text="Add Address Detail", font=("Arial", 18), text_color="#2A8C55").pack(anchor="nw", pady=(25, 10))

            adrs_frame = CTkFrame(master=scframe, fg_color="#d5ebe6", width=1000)  # Increased width for more space
            adrs_frame.pack(anchor="n", fill="x", padx=20, pady=(10, 20))

            CTkLabel(master=adrs_frame, text="Address Line:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            adrs_line_entry = CTkEntry(master=adrs_frame, width=200)
            adrs_line_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=adrs_frame, text="City:", font=("Arial", 14)).grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            city_entry = CTkEntry(master=adrs_frame, width=200)
            city_entry.grid(row=0, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=adrs_frame, text="State:", font=("Arial", 14)).grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            state_entry = CTkEntry(master=adrs_frame, width=200)
            state_entry.grid(row=1, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=adrs_frame, text="District:", font=("Arial", 14)).grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            district_entry = CTkEntry(master=adrs_frame, width=200)
            district_entry.grid(row=1, column=3, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=adrs_frame, text="Pincode:", font=("Arial", 14)).grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            pin_entry = CTkEntry(master=adrs_frame, width=200)
            pin_entry.grid(row=2, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=adrs_frame, text="Home Phone No:", font=("Arial", 14)).grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            hmphn_entry = CTkEntry(master=adrs_frame, width=200)
            hmphn_entry.grid(row=2, column=3, padx=(0, 10), pady=(10, 10))

            # Now adding login frame and their entries
            CTkLabel(master=scframe, text="Add Login Detail", font=("Arial", 18), text_color="#2A8C55").pack(anchor="nw", pady=(25, 10))
            log_frame = CTkFrame(master=scframe, fg_color="#d5ebe6", width=1000)  # Increased width for more space
            log_frame.pack(anchor="n", fill="x", padx=20, pady=(10, 20))

            # Correctly add username and password labels and entries to log_frame
            CTkLabel(master=log_frame, text="Username:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
            login_entry = CTkEntry(master=log_frame, width=200)
            login_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 10))

            CTkLabel(master=log_frame, text="Password:", font=("Arial", 14)).grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="w")
            pw_entry = CTkEntry(master=log_frame, width=200, show="*")  # Use show="*" to mask password input
            pw_entry.grid(row=0, column=3, padx=(0, 10), pady=(10, 10))

            submit_button = CTkButton(
                master=scframe,
                text="Submit",
                fg_color='#029cd9',
                font=("Arial Bold", 14),
                text_color="#fff",
                hover_color="#207244",
                command=lambda: submit_edit_recruit()
            )
            submit_button.pack(pady=(20 , 50), anchor="center")
        def submit_camp_create():
            ce=camp_entry.get()
            se=strength_entry.get()
            connection=connect_db()
            cursor=connection.cursor()
            if ce and se:
                # Check for duplicate Squad ID
                cursor.execute("SELECT 1 FROM camps WHERE camp_name = %s", (ce,))
                if cursor.fetchone() is not None:
                    messagebox.showerror("Duplicate Camp name", "The camp name already exists. Please enter a unique camp name.")
                    return
                cursor.execute("""INSERT into Camps values(%s,%s) """,(ce,int(se)))
                messagebox.showinfo("Submit", "Details have been successfully added!")  # Logic to capture edited data and update in the database
                camp_entry.delete(0, 'end')
                strength_entry.delete(0, 'end')
                connection.commit()
            else:
                messagebox.showerror("Input Error", "Please select the Marital Status.")
            # Function to create form for adding new camp
        def create_camp_form(parent_frame):
                global camp_entry,strength_entry
                CTkLabel(master=parent_frame, text="Add New Camp", font=("Arial", 18), text_color="#2A8C55").pack(anchor="nw")
                # Create a frame for the form
                form_frame = CTkFrame(master=parent_frame, fg_color="#d5ebe6", width=500)  # Increased width for more space
                form_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

                CTkLabel(master=form_frame, text="Camp Name:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 20), pady=15, sticky="w")
                camp_entry=CTkEntry(master=form_frame, width=200)
                camp_entry.grid(row=0, column=1, padx=(0, 20), pady=15)
                CTkLabel(master=form_frame, text="Camp strength:", font=("Arial", 14)).grid(row=1, column=0, padx=(10, 20), pady=15, sticky="w")
                strength_entry=CTkEntry(master=form_frame, width=200)
                strength_entry.grid(row=1, column=1, padx=(0, 20), pady=15)

                submit_button = CTkButton(
                master=parent_frame,
                text="Submit",
                fg_color='#029cd9',
                font=("Arial Bold", 14),
                text_color="#fff",
                hover_color="#207244",
                command=lambda: submit_camp_create()  
                )
                submit_button.pack(pady=(20, 0), anchor="center")




        
        # Function to create form for editing camp details
        def create_edit_camp_form(parent_frame):
            global str_entry, c_combo
            connection = connect_db()
            cursor = connection.cursor()
            # Form UI setup
            CTkLabel(master=parent_frame, text="Edit Camp Details", font=("Arial", 18), text_color="#2A8C55").pack(anchor="nw")
            form_frame = CTkFrame(master=parent_frame, fg_color="#d5ebe6", width=800)
            form_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))

            # Fetch camps from the database
            cursor.execute("""SELECT camp_name FROM camps""")
            camps = cursor.fetchall()
            camp_values = [camp[0] for camp in camps]  # Extract the first element from each tuple

            # Form fields
            CTkLabel(master=form_frame, text="Select Camp:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 20), pady=15, sticky="w")
            c_combo = CTkComboBox(master=form_frame, values=camp_values, width=180)
            c_combo.grid(row=0, column=1, padx=(0, 20), pady=15)

            CTkLabel(master=form_frame, text="Camp Strength", font=("Arial", 14)).grid(row=1, column=0, padx=(10, 20), pady=15, sticky="w")
            str_entry = CTkEntry(master=form_frame, width=180)
            str_entry.grid(row=1, column=1, padx=(0, 20), pady=15)

            submit_button = CTkButton(
                master=parent_frame,
                text="Submit",
                fg_color='#029cd9',
                font=("Arial Bold", 14),
                text_color="#fff",
                hover_color="#207244",
                command=submit_edits_camp
            )
            submit_button.pack(pady=(20, 0), anchor="center")

            # Close the connection after data is fetched
            connection.close()
        
        # Function to create form for adding new squad
        def submit_squad_create():
            sid_entry = s_id.get()
            nos_entry = no_s.get()
            camp_entry = camp_combo.get()
            year_entry = year.get()
            
            connection = connect_db()
            cursor = connection.cursor()
            
            # Check that the entries are filled before processing
            if sid_entry and nos_entry and camp_entry and year_entry:
                try:
                    nos_entry = int(nos_entry)  # Convert number of soldiers to integer
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter a valid number of soldiers.")
                    return
                
                # Check for duplicate Squad ID
                cursor.execute("SELECT 1 FROM Squad WHERE Squad_id = %s", (sid_entry,))
                if cursor.fetchone() is not None:
                    messagebox.showerror("Duplicate Squad ID", "The Squad ID already exists. Please enter a unique Squad ID.")
                    return
                # Get current number of soldiers in the selected camp
                cursor.execute("SELECT IFNULL(SUM(No_of_soldiers), 0) FROM Squad WHERE Camp = %s", (camp_entry,))
                current_strength = cursor.fetchone()[0]  # Ensure this is an integer, 0 if none exists
                
                # Get total allowed strength of the selected camp
                cursor.execute("SELECT camp_strength FROM Camps WHERE Camp_name = %s", (camp_entry,))
                total_strength = cursor.fetchone()[0]
                
                # Ensure total strength capacity is not exceeded
                if (current_strength + nos_entry) <= total_strength:
                    # Insert the squad information into the database
                    cursor.execute(
                        """INSERT INTO Squad (Squad_id, No_of_soldiers, Camp, Year) VALUES (%s, %s, %s, %s)""",
                        (sid_entry, nos_entry, camp_entry, year_entry)
                    )
                    messagebox.showinfo("Submit", "Details have been successfully added!")
                    
                    # Clear form entries
                    s_id.delete(0, 'end')
                    no_s.delete(0, 'end')
                    year.delete(0, 'end')
                    camp_combo.set("Select Camp")
                    
                    # Commit the transaction to save changes
                    connection.commit()
                else:
                    messagebox.showerror("Camp Strength Exceeded", "The total number of soldiers exceeds the camp limit.")
            else:
                messagebox.showerror("Input Error", "Please fill all the details.")
            
            # Close cursor and connection after operation
            cursor.close()
            connection.close()

        def create_squad_form(parent_frame):
            global s_id,no_s,camp_combo,year
            ranks, camps, squads, divis = fetch_values_from_db()

            CTkLabel(master=parent_frame, text="Add New Squad", font=("Arial", 18), text_color="#2A8C55").pack(anchor="nw")
            form_frame = CTkFrame(master=parent_frame, fg_color="#d5ebe6", width=800)  
            form_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))
            CTkLabel(master=form_frame, text="Squad ID:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 20), pady=15, sticky="w")
            s_id=CTkEntry(master=form_frame, width=200)
            s_id.grid(row=0, column=1, padx=(0, 20), pady=15)
            CTkLabel(master=form_frame, text="No. of soldiers:", font=("Arial", 14)).grid(row=0, column=2, padx=(10, 20), pady=15, sticky="w")
            no_s=CTkEntry(master=form_frame, width=200)
            no_s.grid(row=0, column=3, padx=(0, 20), pady=15)
            CTkLabel(master=form_frame, text="Camp Name:", font=("Arial", 14)).grid(row=1, column=0, padx=(10, 20), pady=15, sticky="w")
            camp_combo = CTkComboBox(master=form_frame, values=camps, width=200)
            camp_combo.set("Select Camp")
            camp_combo.grid(row=1, column=1, padx=(0, 20), pady=15)
            CTkLabel(master=form_frame, text="Year:", font=("Arial", 14)).grid(row=1, column=2, padx=(10, 20), pady=15, sticky="w")
            year=CTkEntry(master=form_frame, width=200)
            year.grid(row=1, column=3, padx=(0, 20), pady=15)

            submit_button = CTkButton(
            master=parent_frame,
            text="Submit",
            fg_color='#029cd9',
            font=("Arial Bold", 14),
            text_color="#fff",
            hover_color="#207244",
            command=lambda: submit_squad_create()  
            )
            submit_button.pack(pady=(20, 0), anchor="center")

        # Function to create form for editing squad details
        def create_edit_squad_form(parent_frame):
            connection=connect_db()
            cursor=connection.cursor()
            global sq_id,n_sold,camp_e,year_e
            CTkLabel(master=parent_frame, text="Edit Squad Details", font=("Arial", 18), text_color="#2A8C55").pack(anchor="nw")
            form_frame = CTkFrame(master=parent_frame, fg_color="#d5ebe6", width=800)  
            form_frame.pack(anchor="n", fill="x", padx=27, pady=(10, 0))
            
            cursor.execute("""SELECT squad_id from squad """)
            CTkLabel(master=form_frame, text="Squad ID:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 20), pady=15, sticky="w")
            sq=cursor.fetchall()
            sq_values=[str(a[0]) for a in sq ]
            sq_id=CTkComboBox(master=form_frame, values=sq_values, width=180)
            sq_id.grid(row=0, column=1, padx=(0, 20), pady=15)
            CTkLabel(master=form_frame, text="No. of soldiers:", font=("Arial", 14)).grid(row=1, column=0, padx=(10, 20), pady=15, sticky="w")
            n_sold=CTkEntry(master=form_frame, width=200)
            n_sold.grid(row=1, column=1, padx=(0, 20), pady=15)

            cursor.execute("""SELECT camp_name from camps """)
            camp=[str(a[0]) for a in cursor.fetchall()]
            CTkLabel(master=form_frame, text="Camp:", font=("Arial", 14)).grid(row=1, column=2, padx=(10, 20), pady=15, sticky="w")
            camp_e=CTkComboBox(master=form_frame, values=camp, width=200)
            camp_e.grid(row=1, column=3, padx=(0, 20), pady=15)
            CTkLabel(master=form_frame, text="Year:", font=("Arial", 14)).grid(row=2, column=0, padx=(10, 20), pady=15, sticky="w")
            year_e=CTkEntry(master=form_frame, width=200)
            year_e.grid(row=2, column=1, padx=(0, 20), pady=15)

            submit_button = CTkButton(
            master=parent_frame,
            text="Submit",
            fg_color='#029cd9',
            font=("Arial Bold", 14),
            text_color="#fff",
            hover_color="#207244",
            command=lambda: submit_edits_squad()  
            )
            submit_button.pack(pady=(20, 0), anchor="center")


        # Clear the current main view frame
        for widget in main_view.winfo_children():
            widget.destroy()

        # Highlight the Add/Edit button
        highlight_button(add_edit_button)

        # Set up the Add/Edit UI
        title_frame = CTkFrame(master=main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Add/Edit", font=("Arial Black", 30), text_color="#2A8C55").pack(anchor="nw", side="left")

        # Create a frame for the dropboxes
        dropdown_frame = CTkFrame(master=main_view, fg_color="transparent")
        dropdown_frame.pack(anchor="n", fill="x", padx=27, pady=(20, 0))

        # First dropbox for Add/Edit
        option1 = CTkComboBox(master=dropdown_frame, values=["Add", "Edit"], font=("Arial", 14), width=150)
        option1.grid(row=0, column=0, padx=(0, 10), pady=5)

        # Second dropbox for type of details
        option2 = CTkComboBox(master=dropdown_frame, values=["Recruit Details", "Camp Details", "Squad Details","Leaves taken","Weapons","Captains","Vehicle","Promotion","Achievements","War","Training details"], font=("Arial", 14), width=200)
        option2.grid(row=0, column=1, padx=(10, 0), pady=5)

        # Frame to hold dynamic content based on selections
        form_frame = CTkFrame(master=main_view, fg_color="transparent")
        form_frame.pack(anchor="n", fill="x", padx=27, pady=(20, 0))

        # Function to update the form based on dropbox selections
        def update_form(event=None):
            # Clear the current contents of the form_frame
            for widget in form_frame.winfo_children():
                widget.destroy()

            # Get the current selections from dropboxes
            action = option1.get()
            detail_type = option2.get()

            if action == "Add" and detail_type == "Recruit Details":
                create_recruit_form(form_frame)
            elif action == "Edit" and detail_type == "Recruit Details":
                create_edit_recruit_form(form_frame)
            elif action == "Add" and detail_type == "Camp Details":
                create_camp_form(form_frame)
            elif action == "Edit" and detail_type == "Camp Details":
                create_edit_camp_form(form_frame)
            elif action == "Add" and detail_type == "Squad Details":
                create_squad_form(form_frame)
            elif action == "Edit" and detail_type == "Squad Details":
                create_edit_squad_form(form_frame)

        # Trigger form update when any option is changed
        option1.bind("<<ComboboxSelected>>", update_form)
        option2.bind("<<ComboboxSelected>>", update_form)

        # Button to confirm
        confirm_button = CTkButton(
            master=dropdown_frame,
            text="Confirm",
            fg_color='#029cd9',
            font=("Arial Bold", 14),
            text_color="#fff",
            hover_color=active_button_color,
            anchor="center",
            command=update_form  # You might want to call a different function here
        )
        confirm_button.grid(row=0, column=2, padx=(20, 0), pady=5)

    def fetch_account(soldier_id):
        connection = connect_db()
        cursor = connection.cursor() 
        query="""
            SELECT ID, Username, Password
            FROM login
            WHERE ID=%s
        """
        try:
            # Execute the query with the specific soldier_id
            cursor.execute(query, (soldier_id,))  # Pass soldier_id as a parameter
            data = cursor.fetchone()  # Use fetchone() since we're looking for one record

            # Check if data exists and unpack the result into two variables
            if data:
                id, username, password = data  # Unpack the tuple
                return id, username, password  # Return the specific soldier's id and fitness score
            else:
                return None, None, None  # Return None if no data found for that soldier

        except Exception as e:
            print(f"Error fetching fitness data: {e}")
            return None, None, None
    def soldier_name(soldier_id):
        connection = connect_db()
        cursor = connection.cursor() 
        query="""
            SELECT Name 
            FROM Soldiers
            WHERE ID=%s
        """
        try:
            # Execute the query with the specific soldier_id
            cursor.execute(query, (soldier_id,))  # Pass soldier_id as a parameter
            data = cursor.fetchone()  # Use fetchone() since we're looking for one record

            # Check if data exists and unpack the result into two variables
            if data:
                (name,)=data # Unpack the tuple
                return name  
            else:
                return None # Return None if no data found for that soldier

        except Exception as e:
            print(f"Error fetching fitness data: {e}")
            return None
    
    def change_username_window(soldier_id,dashboard_window):
        """Open a new window to change the username."""
        # Create a new window for changing the username
        window = CTkToplevel()
        window.title("Change Username")
        window.geometry("400x300")
        window.resizable(False, False)

        dashboard_window.withdraw()

        # Make sure the window pops up in front and stays there
        window.attributes("-topmost", True)
        window.focus_force()  # Force focus on this window

        

    # Schedule the main window to be disabled after a short delay
        


        CTkLabel(
            master=window,
            text="Change Username",
            font=("Arial Black", 20),
            text_color="#2A8C55",
        ).pack(pady=(20, 10))

        # Entry fields for old and new usernames
        old_username_entry = CTkEntry(
            master=window,
            placeholder_text="Enter Old Username",
            font=("Arial", 14),
            fg_color="white",
            border_width=2,
            corner_radius=5,
        )
        old_username_entry.pack(pady=(10, 5), padx=20, fill="x")

        new_username_entry = CTkEntry(
            master=window,
            placeholder_text="Enter New Username",
            font=("Arial", 14),
            fg_color="white",
            border_width=2,
            corner_radius=5,
        )
        new_username_entry.pack(pady=(5, 20), padx=20, fill="x")
        def on_close():
            """Restore the main window and close the username change window."""
            dashboard_window.deiconify()  # Restore the main window
            dashboard_window.geometry("1500x900")  # Set the main window to the desired size
            window.destroy()  #
        
        

        def update_username():
            connection = connect_db()
            cursor = connection.cursor() 
            """Update the username in the database."""
            old_username = old_username_entry.get()
            new_username = new_username_entry.get()

            if not old_username or not new_username:
                messagebox.showerror("Error", "Please fill in both fields.")
                return

            query = """
                UPDATE login SET Username = %s WHERE ID = %s AND Username = %s
            """
            try:
                cursor.execute(query, (new_username, soldier_id, old_username))
                if cursor.rowcount > 0:
                    connection.commit()
                    messagebox.showinfo("Success", "Username updated successfully!")
                      # Close the window
                else:
                    messagebox.showerror(
                        "Error",
                        "Old username does not match our records. Please try again.",
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Error updating username: {e}")

        # Confirm button to submit the username change
        CTkButton(
            master=window,
            text="Confirm",
            command=lambda: (update_username() and on_close()),
            font=("Arial Bold", 14),
            fg_color="#2A8C55",
            text_color="white",
            hover_color="#1E8E3E",
        ).pack(pady=(10, 20))

        # Cancel button to close the window
        CTkButton(
            master=window,
            text="Cancel",
            command=on_close,
            font=("Arial Bold", 14),
            fg_color="#FF4500",
            text_color="white",
            hover_color="#FF6347",
        ).pack(pady=(5, 10))
        window.protocol("WM_DELETE_WINDOW", on_close)
        

    def change_password_window(soldier_id):
        """Open a new window with only the 'Forgot Password' option."""
        window = CTkToplevel()
        window.title("Forgot Password")
        window.geometry("400x300")
        window.resizable(False, False)
        app.attributes("-disabled", True)
        
        # Make sure the window pops up in front and stays there
        window.attributes("-topmost", True)
        window.focus_force()  # Force focus on this window


        CTkLabel(
            master=window, text="Forgot Password", font=("Arial Black", 20), text_color="#2A8C55"
        ).pack(pady=20)

        def forget_password():
            """Open a new window for resetting the password."""
            #window.destroy()  # Close the current window
            forget_password_window(soldier_id)

        # Button for "Forgot Password"
        CTkButton(
            master=window, text="Forgot Password?", command=forget_password, fg_color="#FF4500"
        ).pack(pady=50)
        

    def forget_password_window(soldier_id,dashboard_window):
        """Open a new window to reset the password."""
        forget_window = CTkToplevel()
        forget_window.title("Reset Password")
        forget_window.geometry("400x300")
        forget_window.resizable(False, False)
        dashboard_window.withdraw()
        
        # Make sure the window pops up in front and stays there
        forget_window.attributes("-topmost", True)
        forget_window.focus_force()  # Force focus on this window

        CTkLabel(
            master=forget_window,
            text="Reset Password",
            font=("Arial Black", 20),
            text_color="#2A8C55",
        ).pack(pady=20)

        # New Password and Confirm Password Entries
        new_password_entry = CTkEntry(
            master=forget_window,
            placeholder_text="Enter New Password",
            font=("Arial", 16),
            fg_color="#3A3A3A",
            border_width=2,
            corner_radius=5,
            text_color="white"
        )
        new_password_entry.pack(pady=10, padx=20,fill='x')


        confirm_password_entry = CTkEntry(
            master=forget_window,
            placeholder_text="Confirm New Password",
            font=("Arial", 16),
            fg_color="#3A3A3A",
            border_width=2,
            corner_radius=5,
            show='*',
            text_color="white"
        )
        confirm_password_entry.pack(pady=10, padx=20,fill='x')
        
        def on_close():
            """Restore the main window and close the username change window."""
            dashboard_window.deiconify()  # Restore the main window
            dashboard_window.geometry("1500x900")  # Set the main window to the desired size
            forget_window.destroy()
        

        def reset_password():
            connection = connect_db()
            cursor = connection.cursor() 
            """Reset the password in the database."""
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            if not new_password or not confirm_password:
                messagebox.showerror("Error", "Please fill all fields.")
                return

            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            query = """
                UPDATE login SET Password = %s WHERE ID = %s
            """
            try:
                cursor.execute(query, (new_password, soldier_id))
                if cursor.rowcount > 0:
                    connection.commit()
                    messagebox.showinfo("Success", "Password reset successfully.")
                    #forget_window.destroy()  # Close the window
                else:
                    messagebox.showerror("Error", "User not found. Password not reset.")
            except Exception as e:
                messagebox.showerror("Error", f"Error resetting password: {e}")

        # Button to confirm the reset
        CTkButton(
            master=forget_window,
            text="Reset Password",
            command=lambda:(reset_password() and on_close()),
            font=("Arial Bold", 14),
            fg_color="#2A8C55",
            text_color="white",
            hover_color="#1E8E3E",
        ).pack(pady=20)
        
            
        forget_window.protocol("WM_DELETE_WINDOW", on_close)
            



    # Function to highlight active sidebar button
    def highlight_button(button):
        global current_active_button
        if current_active_button:
            current_active_button.configure(fg_color=inactive_button_color)
        button.configure(fg_color=active_button_color)
        current_active_button = button

    # Set protocol to handle window close
    dashboard_window.protocol("WM_DELETE_WINDOW", lambda: on_close_dashboard())
    dashboard()

def on_close_dashboard():
    global dashboard_window
    dashboard_window.destroy()   # Close the General view window
    root.deiconify()             # Show login window again
    
    # Reset the login fields
    entry_username.delete(0, "end")
    entry_password.delete(0, "end")

def run():
    global root
    root = CTk()
    root.title("Military DBMS Login")
    root.maxsize(650,400)
    root.geometry("650x400")
    root.configure(fg_color="black")

    setup_login_ui()
    root.mainloop()

# Run the application
run()
