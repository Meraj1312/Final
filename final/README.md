# Tunedly
#### Video Demo:  <URL https://youtu.be/or0lEvIRYp8>
#### Description:
TODO
Project Overview: Tunedly Music App:

Introduction:

The Tunedly Music App is a personalized web application designed to streamline users' access to their favorite songs via YouTube links. Developed using Flask, a Python web framework, the application offers features for user registration, login, profile management, song addition, deletion, and search functionalities.


File Structure:

app.py: The main Python file of the Flask web application, handling user authentication, database operations, and routing.

layout.html: A base HTML template defining the overall structure of the application, including header, navigation, main content, and footer.

index.html: The landing page template providing an overview of the application and options for user registration and login.

login.html: The template for the login page where users can input their credentials to access their accounts.

register.html: The template for the registration page where users can create new accounts by providing a username and password.

dashboard.html: The template for the user dashboard displaying the user's added songs and providing options for adding, deleting, and searching songs.

profile.html: The template for the user profile page allowing users to update their username, password, and delete their profile.

styles.css: The CSS file containing styles for the application's visual presentation, including layout, colors, fonts, and responsiveness.

music_database.db: The SQLite database file storing user information (username, password) and song details (title, artist, URL).


Features:


User Authentication:

User registration with username and password.

Secure login functionality with password hashing.

Session management to track logged-in users.


Dashboard:

Display of user-specific songs.

Options to add, delete, and search songs.

Dynamic form toggling for adding songs.


Profile Management:

Ability to update username and password.

Profile deletion with password validation.


Challenges and Solutions:

CSS Styling: Iterative adjustments were made to the CSS file to address alignment issues, enhance color schemes, and improve font choices. Flexbox and grid layouts were utilized to achieve responsive design and ensure consistency across different screen sizes.

Dynamic Form Visibility: JavaScript was introduced to toggle the visibility of the song addition form, improving user experience by hiding the form when not in use. This approach minimized clutter on the dashboard page and provided users with a cleaner interface for adding new songs.

Password Hashing and Validation: Robust password hashing techniques were implemented to ensure the security of user credentials. Additionally, client-side validation was incorporated to prompt users to enter required fields during registration and profile deletion processes, enhancing data integrity and user experience.


Conclusion:


The Tunedly Music App project demonstrates the effective utilization of Flask, HTML, CSS, JavaScript, and SQLite to create a user-friendly platform for managing and accessing favorite songs. Through iterative development and strategic problem-solving, the application provides a seamless music listening experience while prioritizing security and usability.

