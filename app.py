# Import necessary libraries
import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns  # Import the Seaborn library

# Set the title for the Streamlit sidebar
st.sidebar.title("WhatsApp Chat Analyzer")

# Create a file uploader in the Streamlit sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded file and decode it as UTF-8
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocess the data using a custom preprocessor
    df = preprocessor.preprocess(data)

    # Display the preprocessed data as a DataFrame
    st.dataframe(df)

    # Fetch unique users from the DataFrame
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    # Create a dropdown select box to choose the user for analysis
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # Create a button to trigger the analysis
    if st.sidebar.button("Show Analysis"):

        # Fetch statistics for the selected user
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        # Display top statistics in a 4-column layout
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        # Column 1: Total Messages
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        # Column 2: Total Words
        with col2:
            st.header("Total Words")
            st.title(words)

        # Column 3: Media Shared
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        # Column 4: Links Shared
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Analyze the busiest users in the group if "Overall" is selected
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            # Column 1: Bar chart of busiest users
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Column 2: DataFrame of busiest users
            with col2:
                st.dataframe(new_df)

        # Generate a Word Cloud for the selected user
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Analyze and display the most common words for the selected user
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most Common Words')
        st.pyplot(fig)

        # Analyze and display emoji usage for the selected user
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        # Column 1: DataFrame of emoji analysis
        with col1:
            st.dataframe(emoji_df)

        # Column 2: Pie chart of top emojis used
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(10), labels=emoji_df['Emoji'].head(10), autopct="%0.2f")
            st.pyplot(fig)

        # Analyze and display a monthly timeline of messages
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Analyze and display a daily timeline of messages
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Analyze and display activity maps
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        # Column 1: Most busy day bar chart
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Column 2: Most busy month bar chart
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Analyze and display a weekly activity map heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Analyze and display message count over time
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        time_span = st.selectbox("Select Time Span", ["Daily", "Weekly", "Monthly"])
        time_col = 'only_date' if time_span == 'Daily' else 'week_start' if time_span == 'Weekly' else 'month'
        chart_data = df.groupby(time_col).count()['message'].reset_index()
        chart_data.columns = [time_col, 'Message Count']

        chart = alt.Chart(chart_data).mark_line().encode(
            x=time_col,
            y='Message Count',
        ).properties(
            width=600,
            height=400,
            title=f"Message Count Over {time_span}"
        )

        st.altair_chart(chart, use_container_width=True)

        # Analyze and display message length distribution (word count) histogram
        word_counts = [len(message.split()) for message in df['message']]
        st.title("Message Length Distribution (Word Count)")
        fig, ax = plt.subplots()
        ax.hist(word_counts, bins=50, alpha=0.7, color='b', edgecolor='k')
        ax.set_xlabel("Word Count")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
