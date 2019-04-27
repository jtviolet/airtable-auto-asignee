# AirTable Auto Assignee
This will allow you to automate the change of an asignee in AirTable based on a single-select field. I wrote this quickly, so it will require a small amount of setup on your part.

## Setup
Run `pip install -r requirements.txt` to install the requirements, then proceed with the steps below.

### Table Variables
First, configure airtable.py file.
- `API_KEY` - This is the API_KEY found in your AirTable account.
- `BASE` - This is the app value for your base. It will be something like `appxxxxxxxxxxxxx`.
- `PROJECT_TABLE_NAME` - This is the table that has both the assignee field and the single-select field.
- `SINGLE_SELECT_FIELD` = This is the single-select field name that you want your assignees to switch baed on.
- `ASSIGNEE_FIELD` - This is the field name of your assignee field that you'd like to switch.

### Configuring Users
Next, you will need to create a user object for each user you want to be able to auto-assign. `airtable.py` comes with two example users. Create as many user objects as you need for auto-assigning.

### Configuring Steps
Lastly, you will need to configure the `steps_owners` dictionary. *These steps must match your single-select field values 1:1. The corresponding object must be the object name of the user you want to assign to that step. If you follow the example in the file, you should be fine.

### Run
Run the program with `python ./app.py` from the root directory.
