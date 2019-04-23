import requests
import json
from airtable import AirTable as at

def main():
    try:
        # get list of ongoing projects
        project_records = get_projects()
    
        # check each records single-select value and assignee value
        # check who the assignee should be
        # if the 'should be' assignee is different, update the record with the new assignee
        for record in project_records:
            record_id = record['id']
            project = record['fields']
    
            current_single_select_value = project[at.SINGLE_SELECT_FIELD]
            current_assignee = project[at.ASSIGNEE_FIELD]['id']
    
            next_assignee = at.steps_owners[current_single_select_value]['id']
    
            if current_assignee is not next_assignee:
                update_project_owner(current_single_select_value, record_id)
    except:
        print("There was a problem. Likely, the 'Current Stage' was not set for a record.")


# get a list of projects from airtable
def get_projects():
    req = requests.get(
        url = f'https://api.airtable.com/v0/{at.BASE}/{at.PROJECT_TABLE_NAME}/',
        headers={
            'Authorization': f'Bearer {at.API_KEY}'
        }
    )
    return req.json()['records']


# update the current assignee for the record
def update_project_owner(current_single_select_value, record_id):
    new_assignee = {
        "fields": {
            at.ASSIGNEE_FIELD: at.steps_owners[current_single_select_value]
        }
    }

    req = requests.request(
        'PATCH',
        url = f'https://api.airtable.com/v0/{at.BASE}/{at.PROJECT_TABLE_NAME}/{record_id}',
        headers = {
            'Authorization': f'Bearer {at.API_KEY}',
            'Content-Type': 'application/json'
        },
        data = json.dumps(new_assignee)
    )


if __name__ == '__main__':
    main()