import requests
import json
from airtable import AirTable as at

def main():
    # get list of ongoing projects
    project_records = get_projects()

    # check each records current single-select field and current owner
    # check who the owner should be
    # if the 'should be' owner is different, update the record with the new owner
    for record in project_records:
        record_id = record['id']
        project = record['fields']

        single_select_field = project[at.SINGLE_SELECT_FIELD]
        current_owner_id = project[at.SINGLE_SELECT_FIELD]['id']

        next_owner_id = at.steps_owners[single_select_field]['id']

        if current_owner_id is not next_owner_id:
            update_project_owner(single_select_field, record_id)


# get a list of projects from airtable
def get_projects():
    req = requests.get(
        url = f'https://api.airtable.com/v0/{at.BASE}/{at.PROJECT_TABLE_NAME}/',
        headers={
            'Authorization': f'Bearer {at.API_KEY}'
        }
    )
    return req.json()['records']


# update the current project owner
def update_project_owner(single_select_field, record_id):
    new_owner_data = {
        'fields': {
            at.ASSIGNEE_FIELD: at.steps_owners[single_select_field]
        }
    }

    req = requests.request(
        'PATCH',
        url = f'https://api.airtable.com/v0/{at.BASE}/{at.PROJECT_TABLE_NAME}/{record_id}',
        headers = {
            'Authorization': f'Bearer {at.API_KEY}',
            'Content-Type': 'application/json'
        },
        data = json.dumps(new_owner_data)
    )


# run the program
if __name__ == '__main__':
    main()