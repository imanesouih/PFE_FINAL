*** Settings ***
Library    RequestsLibrary
Library    OperatingSystem
Library    Collections
Library    generate_token.py
Library    jsonschema

*** Variables ***
${task_id}          ${EMPTY}
${TokenFile}        token.txt
${AuthToken}        ${EMPTY}
${schema_file}      task_schema.json    

*** Keywords ***
Generate Auth Token
    [Arguments]    ${username}    ${email}    ${password}
    ${auth_data}    Create Dictionary    username=${username}    email=${email}    password=${password}
    ${auth_headers}    Create Dictionary    Content-Type=application/json
    ${auth_response}    Post    ${BaseUrl}${CreateTokenEndpoint}    json=${auth_data}    headers=${auth_headers}

    # Verify the response status code
    Should Be Equal As Numbers    ${auth_response.status_code}    200

    # Extract the token from the response JSON
    ${token}    Set Variable    ${auth_response.json()['access_token']}
    Set Global Variable    ${AuthToken}    ${token}

*** Test Cases ***
Create New Task
    [Documentation]    Test creating a new task

    # Request headers avec le token d'authentification
    ${headers}    Create Dictionary    Authorization=Bearer ${AuthToken}    Content-Type=application/json

    # Données pour créer une nouvelle tâche
    ${task_data}    Create Dictionary    title=Acheter des NuGGET    description=Acheter du lait, des œufs et du pain.    deadline=2024-01-01    UserId=1

    # Send POST request to create a task
    ${response}    Post    ${url}${CreateTaskEndpoint}    json=${task_data}    headers=${headers}

    # Verify response status code
    Should Be Equal As Numbers    ${response.status_code}    201
    # Log response content
    Log    ${response.content}

Get Task Details
    [Documentation]    Test getting task details by ID
    ${task_id}    Set Variable    2

    # Request headers avec le token d'authentification
    ${headers}    Create Dictionary    Authorization=Bearer ${AuthToken}    Content-Type=application/json

    # Construct URL to get task details by ID
    ${url}    Set Variable    ${url}${GetTaskEndpoint}/${task_id}

    # Send GET request to retrieve task details by ID
    ${response}    Get    ${url}    headers=${headers}

    # Verify response status code
    Should Be Equal As Numbers    ${response.status_code}    200

    # Log response content
    Log    ${response.content}

Validate Task Schema
    [Documentation]    Test fetching a task and validate the schema
    ${task_id}    Set Variable    2
    ${headers}    Create Dictionary    Authorization=Bearer ${AuthToken}    Content-Type=application/json
    ${BaseUrl}    Set Variable    ${url}${GetTaskEndpoint}/${task_id}
    ${response}    Get    ${BaseUrl}    headers=${headers}
    Should Be Equal As Numbers    ${response.status_code}    200
    Log To Console    ${response.json()}
    Log To Console    ${response.content}

    # ${result}    Run Keyword And Ignore Error    Validate Task Schema    ${response.content}    ${schema_file}
    # Run Keyword If    '${result[0]}' == 'False'    Fail    JSON schema validation failed: ${result[1]}
    # Log    JSON schema validation successful
   

*** Settings ***
Suite Setup    Generate Auth Token    imane    imane@example.com    motdepasse123

