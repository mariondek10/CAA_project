import streamlit as st

def main():
    st.set_page_config(
    page_title="Bike Dashboard",
    page_icon="🚲",
)
    st.title("🚲 Welcome to your biking Dashboard!")
    st.write("Here is an overview of all your biking session:")
    st.map()
    st.subheader("Your Recent Biking Session:")
    # Display a selecter that allows the user to choose a time range for their biking sessions
    st.selectbox("Select a time range for your biking sessions:", options=["Last Week", "Last Month", "Last Year"])
    st.dataframe({
        "Distance (km)": [15.2],
        "Duration (min)": [45],
        "Average Speed (km/h)": [20.3],
        "Calories Burned": [350]
    })

if __name__ == "__main__":
    main()

    