import re  # Import the regular expressions module
import pandas as pd  # Import the pandas library for data manipulation

def preprocess(data):
    # Define a regular expression pattern to match date-time strings
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s-\s'

    # Use the regular expression pattern to split the input data into messages and dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create a DataFrame to store the messages and dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    
    # Adjust the date format to match your data (2-digit year)
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

    # Rename the 'message_date' column to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Create lists to store user names and messages after splitting each message
    users = []
    messages = []
    for message in df['user_message']:
        # Split each message using a regular expression to separate user names and messages
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # Check if there's a user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')  # Handle group notification messages
            messages.append(entry[0])

    # Add 'user' and 'message' columns to the DataFrame
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)  # Drop the original 'user_message' column

    # Extract additional date-related information from the 'date' column
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create a 'period' column based on the hour of the message
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period  # Add the 'period' column to the DataFrame

    return df  # Return the preprocessed DataFrame
