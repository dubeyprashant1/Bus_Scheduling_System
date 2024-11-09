# Automated Bus Scheduling and Route Management System

This project is an Automated Bus Scheduling and Route Management System designed to streamline and optimize the scheduling of buses for the Delhi Transport Corporation (DTC). The system is developed to improve operational efficiency, reduce human error, and automate several aspects of the bus scheduling process. The application is built with a focus on real-time management, crew assignments, and optimized route planning.

# Features
1. Crew Scheduling & Assignment: Automatically assigns crew members to buses, ensuring that each crew has sufficient rest time (minimum 30 minutes) between shifts.
2. Real-time Bus Scheduling: Optimizes bus schedules by considering crew availability, routes, and emergency requests.
3. Route Management: Provides functionality for managing bus routes, linking them to the schedules and crew assignments.
4. Emergency Handling: Supports emergency scheduling, with options to override assignments and automatically assign crews in case of an emergency.
5. Crew & Bus Database Management: Tracks crew availability, daily assignment limits, and bus schedules. Updates are made in the database as assignments are made.
6. Admin Control: Admins can manually override crew assignments and bus schedules in case of emergencies or other operational issues.
7. Time Validation: Ensures that all scheduled times are in the correct format and checks for the last crew assignment to ensure rest times.

# Technologies Used
Backend: Python (Flask)
Frontend: HTML, CSS, javascript
Database: MySQL
Data Storage: JSON (for bus schedule)
Other: RESTful API, SQL queries, datetime manipulation for time validation

# Key Database Tables
1. admins: manages manual assigning of crews to buses and their info - for login and signup purpose.
2. traveller: which regularly use application to locate real time location of bus and plan their journey - for login and signup purpose.
3. crews: Stores crew details, including last assignment time, assignment limits, and other relevant information.
4. buses: Stores bus details, including route, crew assignments, and schedule information.
5. assignments: Tracks the assignments of crew members to buses.

# Key Features in Detail:
1. Crew Validation: Ensures crews have at least 30 minutes of rest time before being assigned a new duty. If a crew member has reached the daily assignment limit (5), they 2. cannot be scheduled for more assignments.
3. Bus Assignment Validation: Checks if a bus or crew is already assigned before adding a new assignment.
4. Emergency Assignments: If a crew member is scheduled for an emergency, the system automatically updates the emergency count and relevant assignments.
5. Route Management: Each bus is linked to a specific route, and the bus's schedule is updated accordingly when new assignments are made.


