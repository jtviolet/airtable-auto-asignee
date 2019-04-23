class AirTable:
    # AirTable configuration Variables
    API_KEY = ''
    BASE = ''
    PROJECT_TABLE_NAME = ''
    SINGLE_SELECT_FIELD = ''
    ASSIGNEE_FIELD = ''

    # Create as many users as you need from your possible assignees in your AirTable environment
    user_A = {
        'id': 'usrxxxxxxxxxxxxxx',
        'email': 'john.doe@email.com',
        'name': 'john doe'
    }

    user_B = {
        'id': 'usrxxxxxxxxxxxxxx',
        'email': 'jane.doe@email.com',
        'name': 'jane doe'
    }

    # The step names should match your step names in your single-selct field 1:1, and
    # the corresponding object name should be tue user you want to assign that step to.
    steps_owners = {
        'step one': user_A,
        'step two': user_B
    }