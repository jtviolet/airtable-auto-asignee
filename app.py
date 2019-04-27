import requests
import json
from airtable import AirTable as at

def main():
    # get list of projects records from your projects table
    # be sure you set your base id and table name
    project_records = get_projects()

    # grab your map of project phase and associated assignees from your base
    # be sure you set your base id and table name
    project_phase_owner_map = get_project_phase_owner_map()

    # check each records current phase value and assignee value
    # check who the assignee should be
    # if the 'should be' assignee is different, update the record with the new assignee
    for record in project_records:
        # store record id and grab project data
        record_id = record['id']
        project = record['fields']

        # check if a value is set for the project phase
        # if value is set, grab the value and check the phase/assignee map to see who owns it
        if at.PROJECT_PHASE_FIELD in project:
            current_phase = project[at.PROJECT_PHASE_FIELD]
            next_assignee = project_phase_owner_map[current_phase]['id']

            # check if an assignee is set for the given project record
            # if value is set, grab the current assignee
            # if value is not set, then set the correct assignee
            if at.ASSIGNEE_FIELD in project:
                current_assignee = project[at.ASSIGNEE_FIELD]['id']

                # check if the assignee currently listed for the given phase is the assignee that should be there
                # if the current assignee is not the assignee that should be, update the assignee to the correct one
                # if value is not set, do nothing
                if current_assignee != next_assignee:
                    update_project_owner(project_phase_owner_map, current_phase, record_id)
                else:
                    print('No need to auto-assign assignee--correct assignee is already in place.')
            else:
                update_project_owner(project_phase_owner_map, current_phase, record_id)

        else:
            print('No need to auto-assign asignee--single-select value is not present.')


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
def update_project_owner(project_owners_map, current_single_select_value, record_id):
    new_assignee = {
        "fields": {
            at.ASSIGNEE_FIELD: project_owners_map[current_single_select_value]
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

# get your map of phases and their owners from your base
def get_project_phase_owner_map():
    phase_owner_map = {}

    req = requests.get(
        url = f'https://api.airtable.com/v0/{at.BASE}/{at.PROJECT_PHASE_OWNERS_TABLE}/',
        headers={
            'Authorization': f'Bearer {at.API_KEY}'
        }
    )

    for record in req.json()['records']:
        fields = record['fields']
        phase_owner_map.update({fields['Project Phase']:fields['Assignee']})
    return phase_owner_map


if __name__ == '__main__':
    main()