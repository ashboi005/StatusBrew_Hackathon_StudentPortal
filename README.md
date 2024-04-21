# StatusBrew_Hackathon_StudentPortal
A basic Student Portal Website made for a hackathon held by StatusBrew

## Description

This project is a comprehensive web application designed to streamline administrative tasks and enhance communication within an educational institution. It includes features such as student dashboard, administrative dashboard, messaging system, fee management, result management, attendance tracking, and more.

## Team Members

- **Ashwath Soni** - *Team Lead, Backend, and Database*
- **Sahil Chabra** - *IoT: Handled the RFID-based attendance system and front end for admin dashboard*
- **Yuvika Khanna** - *Front end: Developed sub-pages for the website (login/register page, messages, fees, result, about us, and contact us)*
- **Sarah Jain** - *Front end: Designed Home Page and some other sub pages*

## Technologies Used

- **Python** - Flask web framework for backend development
- **SQLAlchemy** - Object-relational mapping (ORM) library for database management
- **MySQL** - Relational database management system
- **HTML/CSS/JavaScript** - Frontend development
- **Google Sheets API** - Integration for attendance tracking

## Features

- **User Authentication**: Secure login and registration system for students and administrators.
- **Student Dashboard**: Personalized dashboard for students to view and update their details, check results, and pay fees.
- **Administrative Dashboard**: Admin interface for managing student details, sending messages, managing fees, and generating reports.
- **Messaging System**: Internal messaging system for communication between students and administrators.
- **Fee Management**: Tracking and management of student fees with options for payment.
- **Result Management**: Recording and viewing student academic results.
- **Attendance Tracking**: Integration with an RFID-based attendance system for monitoring student attendance.
- **Responsive Design**: Mobile-friendly interface for seamless access across devices.

## Installation

1. Clone the repository: `git clone <repository_url>`
2. Install the required Python libraries
3. Set up Database: Create a MySQL database and update the database URI in `main.py` at line 11
4. Run the application: `python main.py`

## Usage

1. Access the application locally through the provided code. Use your own Sheet Credentials in sheet_credentials.json for the Google Sheets API and update the worksheet name accordingly in the code
2. Students can log in to their dashboard to view/update personal details, check results, pay fees, and view messages.
3. Administrators can log in to the admin dashboard to manage student details, send messages, manage fees, and generate reports.
4. Ensure proper connectivity for RFID-based attendance tracking.
5. Explore the various features and functionalities of the application.

## Contributors

- Ashwath Soni
- Sahil Chabra
- Yuvika Khanna
- Sarah Jain

## License

This project is licensed under the [MIT License](LICENSE).

