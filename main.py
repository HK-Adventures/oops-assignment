import streamlit as st
import datetime
from database import Database
import pandas as pd

# Initialize database
db = Database()

def get_share_url(share_link):
    # Create the share URL using the current URL
    return f"?share={share_link}"

def main():
    st.title("Expense Splitter for Roommates/Friends")
    
    # Initialize session state
    if 'current_group' not in st.session_state:
        st.session_state.current_group = None
    
    # Sidebar for group selection
    st.sidebar.title("Group Management")
    
    # Check if we're accessing via share link
    query_params = st.query_params
    share_link = query_params.get("share", [None])[0]
    
    # Handle share link
    if share_link:
        group = db.get_group_by_share_link(share_link)
        if group:
            st.session_state.current_group = group
            st.success("Successfully joined the group!")
        else:
            st.error("Invalid share link")
    
    # Create new group
    with st.sidebar.expander("Create New Group"):
        group_name = st.text_input("Group Name")
        members = st.text_input("Members (comma-separated)")
        if st.button("Create Group"):
            if group_name and members:
                members_list = [m.strip() for m in members.split(",")]
                group_id, share_link = db.create_group(group_name, members_list)
                group = db.get_group(group_id)
                st.session_state.current_group = group
                st.success("Group created successfully!")
                
                # Create and display shareable link
                share_url = get_share_url(share_link)
                st.markdown(f"Share this link with your group members:")
                st.code(f"{share_url}", language="text")
                st.markdown(f"[Click here to open shared group]({share_url})")
            else:
                st.error("Please fill in all fields")
    
    # Display current group information
    if st.session_state.current_group:
        group = st.session_state.current_group
        st.header(f"Group: {group.name}")
        
        # Display members
        st.subheader("Members")
        st.write(", ".join(group.members))
        
        # Add new expense
        st.subheader("Add New Expense")
        with st.form("expense_form", clear_on_submit=True):
            description = st.text_input("Description")
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
            paid_by = st.selectbox("Paid by", group.members)
            date = st.date_input("Date", datetime.date.today())
            
            if st.form_submit_button("Add Expense"):
                if description and amount:
                    db.add_expense(group.id, description, amount, paid_by, date.isoformat())
                    st.success("Expense added successfully!")
                else:
                    st.error("Please fill in all fields")
        
        # Display expenses
        st.subheader("Expenses")
        expenses = db.get_expenses(group.id)
        if expenses:
            expenses_data = [expense.to_dict() for expense in expenses]
            df = pd.DataFrame(expenses_data)
            st.dataframe(df)
        else:
            st.info("No expenses added yet")
        
        # Display balances
        st.subheader("Balances")
        balances = db.calculate_balances(group.id)
        if balances:
            for member, balance in balances.items():
                if balance > 0:
                    st.success(f"{member} should receive: ${balance:.2f}")
                elif balance < 0:
                    st.error(f"{member} should pay: ${abs(balance):.2f}")
                else:
                    st.info(f"{member} is settled up")
        else:
            st.info("No expenses to calculate balances")
            
        # Display share link for current group
        st.sidebar.subheader("Share Group")
        share_url = get_share_url(group.share_link)
        st.sidebar.markdown(f"Share this link with your group members:")
        st.sidebar.code(f"{share_url}", language="text")
        st.sidebar.markdown(f"[Click here to copy share link]({share_url})")
    else:
        st.info("Please create a new group or use a share link to access an existing group")

if __name__ == "__main__":
    main() 