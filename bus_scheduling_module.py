from datetime import datetime,timedelta
import mysql.connector
from mysql.connector import Error

def get_all_crew_data():
    # Connect to your database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='bus_scheduling'
    )
    
    cursor = connection.cursor(dictionary=True)
    
    # Fetch crew data along with accept_count, total_proposals, and last_assignment_time
    cursor.execute("""
        SELECT crew_id, name, phone_number, on_duty, reject_count, accept_count, total_proposals, last_assignment_time, assigned_bus
        FROM crews
    """)
    
    crew_data = cursor.fetchall()
    
    # Calculate efficiency and remaining_rest_time for each crew member
    for crew in crew_data:
        # Update the on_duty status
        crew['status'] = 'On Duty' if crew['on_duty'] == 1 else 'Off Duty'
        
        # Calculate efficiency
        if crew['total_proposals'] > 0:  # Avoid division by zero
            crew['efficiency'] = (crew['accept_count'] / crew['total_proposals']) * 100
        else:
            crew['efficiency'] = 0  # If no proposals, set efficiency to 0
        
        # Calculate remaining rest time
        if crew['last_assignment_time']:
            last_assignment_time = datetime.strptime(crew['last_assignment_time'], '%Y-%m-%d %H:%M:%S')
            current_time = datetime.now()
            time_diff = current_time - last_assignment_time
            crew['remaining_rest_time'] = time_diff.total_seconds() / 60  # Time in minutes
        else:
            crew['remaining_rest_time'] = 0  # No last assignment time, set to 0
        
    cursor.close()
    connection.close()
    
    return crew_data


def get_all_bus_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='bus_scheduling'
        )
        cursor = connection.cursor(dictionary=True)
        
        # Fetch bus data
        cursor.execute("""
            SELECT bus_id, route, on_road, assigned_crew, next_departure, arrival_time, schedule
            FROM buses
        """)
        
        bus_data = cursor.fetchall()
        
        for bus in bus_data:
            bus['status'] = 'On Road' if bus['on_road'] == 1 else 'Off Road'
            
            # Convert timedelta fields to string format for JSON serialization
            bus['next_departure'] = str(bus['next_departure']) if isinstance(bus['next_departure'], timedelta) else bus['next_departure']
            bus['arrival_time'] = str(bus['arrival_time']) if isinstance(bus['arrival_time'], timedelta) else bus['arrival_time']
            bus['schedule'] = str(bus['schedule']) if isinstance(bus['schedule'], timedelta) else bus['schedule']
        
        return bus_data
    
    except Error as e:
        print("Error while connecting to database:", e)
        return []
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
