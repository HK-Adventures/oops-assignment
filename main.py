import streamlit as st
import datetime
from database import Database
import pandas as pd

# Initialize database
db = Database()

def main():
    st.title("Expense Splitter for Roommates/Friends")
    
    # Initialize session state
    if 'current_group_id' not in st.session_state:
        st.session_state.current_group_id = None
    
    # Get current group from session state
    current_group = None
    if st.session_state.current_group_id:
        current_group = db.get_group(st.session_state.current_group_id)
    
    # Sidebar for group selection
    st.sidebar.title("Group Management")
    
    # Create new group
    with st.sidebar.expander("Create New Group"):
        group_name = st.text_input("Group Name")
        members = st.text_input("Members (comma-separated)")
        if st.button("Create Group"):
            if group_name and members:
                members_list = [m.strip() for m in members.split(",")]
                group_id = db.create_group(group_name, members_list)
                st.session_state.current_group_id = group_id
                current_group = db.get_group(group_id)
                st.success("Group created successfully!")
            else:
                st.error("Please fill in all fields")
    
    # Display current group information
    if current_group:
        st.header(f"Group: {current_group.name}")
        
        # Display members
        st.subheader("Members")
        st.write(", ".join(current_group.members))
        
        # Add new expense
        st.subheader("Add New Expense")
        with st.form("expense_form", clear_on_submit=True):
            description = st.text_input("Description")
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
            paid_by = st.selectbox("Paid by", current_group.members)
            date = st.date_input("Date", datetime.date.today())
            
            if st.form_submit_button("Add Expense"):
                if description and amount:
                    db.add_expense(current_group.id, description, amount, paid_by, date.isoformat())
                    st.success("Expense added successfully!")
                else:
                    st.error("Please fill in all fields")
        
        # Display expenses
        st.subheader("Expenses")
        expenses = db.get_expenses(current_group.id)
        if expenses:
            expenses_data = [expense.to_dict() for expense in expenses]
            df = pd.DataFrame(expenses_data)
            st.dataframe(df)
        else:
            st.info("No expenses added yet")
        
        # Display balances
        st.subheader("Balances")
        balances = db.calculate_balances(current_group.id)
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
    else:
        st.info("Please create a new group to get started")

if __name__ == "__main__":
    main() 