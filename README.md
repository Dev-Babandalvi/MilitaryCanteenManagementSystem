# Military Canteen Management System

**Created by**: Baban Ramdas Dalvi  
**Institution**: Dr. G.Y. Pathrikar College of Computer Science and IT, MGM University  
**Academic Year**: 2024-2025
**Email ID** - babandalvi20@gmail.com
**Mob No** - 8308175140

## Project Overview
The Military Canteen Management System is a desktop application designed to help manage inventory and sales in a canteen. It includes features such as item management, sales tracking, and generating sales reports.

## Features
- Add, edit, and delete items in the inventory
- Track item sales with date and quantity
- Generate reports within a specified date range
- View sales history

## Setup Instructions
1. Install Python and required libraries.
2. Clone or download the project files.
3. Run `db_setup.py` to create the database tables.
4. Run `main.py` to start the application.

## Setup Instructions

1. **Install Python and Required Libraries**
   - Ensure Python (version 3.x) is installed on your computer. 
   - Install the required libraries by running:
     ```bash
     pip install PyQt5
     ```
   - This installs PyQt5, which is necessary for running the graphical interface.

2. **Database Setup**
   - Before running the main application, set up the SQLite database by executing the `db_setup.py` file. This will create the necessary tables.
   - In your terminal or command prompt, navigate to the project folder and run:
     ```bash
     python db_setup.py
     ```

3. **Launching the Application**
   - Start the application by running the main program:
     ```bash
     python main.py
     ```

4. **Using the Application**
   - You can now add, edit, delete, and sell items within the application interface.
   - Use the search bar to find items quickly, and generate reports by selecting a date range.

5. **Troubleshooting**
   - If you encounter any errors, ensure all dependencies are installed correctly.
   - Confirm that the `canteen_db.db` database file exists in the project folder after running `db_setup.py`.
