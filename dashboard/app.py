import streamlit as st

def main():
    st.title("🚴‍♀️ Welcome to your biking Dashboard!")
    st.write("Here is an overview of your last biking session:")
    st.map()
    st.dataframe({
        "Distance (km)": [15.2],
        "Duration (min)": [45],
        "Average Speed (km/h)": [20.3],
        "Calories Burned": [350]
    })
    
if __name__ == "__main__":
    main()

    