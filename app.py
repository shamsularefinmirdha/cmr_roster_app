import streamlit as st
from auth import check_login
import pandas as pd

st.set_page_config(page_title="Roster App", layout="wide")

# --- LOGIN ---
role = check_login()

# Load data
df = pd.read_csv("roster_data.csv")
staff_list = pd.read_csv("staff_list.csv")["Staff"].dropna().tolist()

if role == "admin":
    st.title("🧑‍💼 Admin Roster Editor")

    selected_date = st.date_input("Select Date")
    daily_df = df[df['Date'] == pd.to_datetime(selected_date).strftime("%Y-%m-%d")]

    if not daily_df.empty:
        index = daily_df.index[0]
        st.write("Edit assignments for:", daily_df.iloc[0]['Day'])

        for col in df.columns[2:]:  # Skip Date, Day
            current_value = df.at[index, col] if pd.notna(df.at[index, col]) else ""
            new_value = st.multiselect(f"{col}", options=staff_list, default=[s.strip() for s in str(current_value).split(",") if s.strip()])
            df.at[index, col] = ", ".join(new_value)

        if st.button("💾 Save Changes"):
            df.to_csv("roster_data.csv", index=False)
            st.success("Roster updated successfully!")

    else:
        st.warning("No entry found for this date.")

elif role == "viewer":
    st.title("👥 Staff Roster Viewer")
    staff_name = st.selectbox("Select your name", staff_list)
    filtered = df[df.apply(lambda row: staff_name in str(row.values), axis=1)]
    st.dataframe(filtered)

else:
    st.stop()