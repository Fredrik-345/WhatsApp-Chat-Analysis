import streamlit  as st
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.title("Whatsapp Chat Analyzer: ")
st.sidebar.title("Analyze Chats")


#to upload the file in the chat analyzer sidebar creating a button
uploaded_file = st.sidebar.file_uploader("Choose File:")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8") #convereting the  browsed file into string
    df = preprocess.preprocessing(data) #creating the string data into Dataframe
    st.dataframe(df)

    # here we can sort out messages with respect to  individual users in the group
    #we will create a dropup list to show the users
    user_list = df["user"].unique().tolist()
    user_list.remove("Group_Notification") #removing the group_notification option in thr dropdown list
    user_list.sort()
    user_list.insert(0,"Overall")
    #user_list.insert(1,"Most Active Users")
    #user_list.insert(2, "In Total: ")

    selected_user = st.sidebar.selectbox("Show Chat Analysis",user_list)
    if st.sidebar.button("Show Analysis: "):
        num_messages,words,num_media,num_links = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages:")
            st.title(num_messages)
        with col2:
            st.header("Total Words:")
            st.title(words)
        with col3:
            st.header("Media Shared:")
            st.title(num_media)
        with col4:
            st.header("Links Shared:")
            st.title(num_links)
          #finding the most active user
        if selected_user == "Overall":
            st.title("Most Active Users:")
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()
            col1,col2 = st.columns(2)
            with  col1:
                ax.bar(x.index , x.values, color="yellow")
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        df_wc = helper.create_word_cloud(selected_user,df)
        st.title("Generating  Word  Cloud:")
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #Most common words-->>
        new_df = helper.common_words(selected_user,df)
        st.title("Most Common Used words:")
        fig, ax = plt.subplots()
        ax.barh(new_df[0],new_df[1],color="green")  #barh is horizontal bar chart
        plt.xticks(rotation="vertical")
        st.pyplot(fig)


        #emoji analysis-->>>
        emoji_df = helper.emoji_check(selected_user,df)
        st.title("Used Emojis: ")
        st.dataframe(emoji_df)    # and to include labels we have to inlude a separate labels input


        #daily timeline-->>>
        st.title("Daily Timeline:")
        new_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize = (10,10))
        ax.barh(new_timeline["Only_Date"], new_timeline["message"], color="red")  # barh is horizontal bar chart
        plt.xticks(rotation="horizontal")
        st.pyplot(fig)

        ##Activity Map according to month and days
        st.title("Monthly and daily Actvity Map: ")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Days")
            busy_day = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values ,color="pink")  # barh is horizontal bar chart
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Months")
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values ,color="violet")  # barh is horizontal bar chart
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        #creating a time-period(hours to hours) heatmap
        st.title("Hourly Activity Map: ")
        df_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(df_heatmap)
        st.pyplot(fig)


