# Import necessary libraries
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

import altair as alt

# Create an instance of URpipLExtract for extracting URLs from messages
extract = URLExtract()

# Define a function to fetch statistics for the selected user
def fetch_stats(selected_user, df):
    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Calculate the number of messages, total words, media messages, and links shared
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    
    return num_messages, len(words), num_media_messages, len(links)

# Define a function to find the most active users
def most_busy_users(df):
    # Count the number of messages sent by each user and retrieve the top users
    x = df['user'].value_counts().head()
    # Calculate the percentage of messages sent by each user
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df

# Define a function to create a Word Cloud for the selected user
def create_wordcloud(selected_user, df):
    # Open a file containing stop words
    f = open('stop_words.txt', 'r')
    stop_words = f.read()

    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove stop words from messages and generate a Word Cloud
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

# Define a function to find the most common words for the selected user
def most_common_words(selected_user, df):
    # Open a file containing stop words
    f = open('stop_words.txt', 'r')
    stop_words = f.read()

    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove stop words and count the most common words
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# Define a function to analyze and count emojis used by the selected user
def emoji_helper(selected_user, df):
    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    common_emojis = ['😀', '😂', '😃', '❤️', '😍', '😊', '👍', '👏', '🙌', '🎉']

    for message in df['message']:
        emojis.extend([c for c in message if c in common_emojis])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['Emoji', 'Count'])

    return emoji_df

# Define a function to create a monthly timeline of messages
def monthly_timeline(selected_user, df, time_span='year-month'):
    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    if time_span == 'year-month':
        # Group messages by year and month to create a timeline
        timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
        time = [f"{row['month']}-{row['year']}" for _, row in timeline.iterrows()]
    elif time_span == 'year':
        # Group messages by year to create a timeline
        timeline = df.groupby(['year']).count()['message'].reset_index()
        time = [str(year) for year in timeline['year']]
    else:
        raise ValueError("Invalid time span. Supported values are 'year-month' and 'year'.")

    timeline['time'] = time

    return timeline

# Define a function to create a daily timeline of messages
def daily_timeline(selected_user, df):
    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Group messages by date to create a daily timeline
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

# Define a function to calculate and plot weekly activity on specific days
def week_activity_map(selected_user, df):
    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

# Define a function to calculate and plot monthly activity
def month_activity_map(selected_user, df):
    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

# Define a function to create an activity heatmap
def activity_heatmap(selected_user, df):
    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Create a heatmap of activity based on days and periods
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

# Define a function to create a chart showing message count over time
def message_count_over_time(selected_user, df, time_span='daily'):
    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Determine the time column based on the selected time span
    time_col = 'only_date' if time_span == 'daily' else 'week_start' if time_span == 'weekly' else 'month'

    # Group data by time column and count messages
    chart_data = df.groupby(time_col).count()['message'].reset_index()
    chart_data.columns = [time_col, 'Message Count']

    # Create an Altair chart to visualize message count over time
    chart = alt.Chart(chart_data).mark_line().encode(
        x=time_col,
        y='Message Count',
    ).properties(
        width=600,
        height=400,
        title=f"Message Count Over {time_span.capitalize()}"
    )

    return chart

# Define a function to create a histogram of message length distribution
def message_length_distribution(selected_user, df):
    # Filter the DataFrame by the selected user if it's not "Overall"
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Calculate word counts for each message
    word_counts = [len(message.split()) for message in df['message']]
    hist_data = pd.DataFrame({'Word Count': word_counts})

    # Create an Altair chart to visualize message length distribution
    chart = alt.Chart(hist_data).mark_bar().encode(
        alt.X("Word Count", bin=alt.Bin(step=10), title="Word Count"),
        alt.Y("count()", title="Frequency"),
    ).properties(
        width=600,
        height=400,
        title="Message Length Distribution (Word Count)"
    )

    return chart
