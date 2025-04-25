# Expense Splitter for Roommates/Friends

A Streamlit application that helps roommates and friends split expenses fairly. The application uses SQLite for persistent storage and provides shareable links for group access.

## Features

- Create expense groups with multiple members
- Add expenses with descriptions, amounts, and who paid
- View all expenses in a group
- Calculate fair splits and balances
- Share groups with others using unique links
- Persistent storage (data remains after page refresh)

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
streamlit run main.py
```

2. Create a new group:
   - Click on "Create New Group" in the sidebar
   - Enter a group name
   - Add members (comma-separated)
   - Click "Create Group"
   - Copy the share link to share with others

3. Add expenses:
   - Enter expense description
   - Enter amount
   - Select who paid
   - Add date
   - Click "Add Expense"

4. View balances:
   - The application automatically calculates who owes whom
   - Positive balances show who should receive money
   - Negative balances show who should pay

## Data Persistence

The application uses SQLite for data storage. All data is stored in `expense_splitter.db` in the same directory as the application.

## Share Links

Each group gets a unique share link that can be used to access the group. Share this link with your roommates/friends to allow them to view and add expenses to the group. 