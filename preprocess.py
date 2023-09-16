import pandas as pd
import re
def preprocessing(data):
    #extracting all code from jupyter file by copy and pasting the main code
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({"User_Message": messages, "Message_Date": dates})
    # converting "Message_Date" into actual universal Date-Time format
    df["Message_Date"] = pd.to_datetime(df["Message_Date"], format="%d/%m/%Y, %H:%M - ")

    users = []  # creating a list "user"
    messages = []
    for message in df["User_Message"]:
        entry = re.split("([\w\W]+?):\s", message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("Group_Notification")
            messages.append(entry[0])

    df["user"] = users
    df["message"] = messages
    df.drop(["User_Message"], axis="columns")
    df = df.drop(["User_Message"], axis="columns")

    df["Year"] = df["Message_Date"].dt.year

    df["Month"] = df["Message_Date"].dt.month

    df["Day"] = df["Message_Date"].dt.day

    df["Hour"] = df["Message_Date"].dt.hour

    df["Minutes"] = df["Message_Date"].dt.minute

    df["Only_Date"] = df["Message_Date"].dt.date

    df["DAY_NAME"] = df["Message_Date"].dt.day_name()

    df["month_name"] = df["Message_Date"].dt.month_name()


    # this column is made for time period i.e. 8-9 or 12-15 or 13-14 .......
    period = []
    for hour in df[["DAY_NAME", "Hour"]]["Hour"]:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df["Period"] = period
    #df = df.drop(["Message_Date"], axis="columns")
    return df
