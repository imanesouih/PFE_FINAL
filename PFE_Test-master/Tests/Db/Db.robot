# *** Settings ***
# Library           DatabaseLibrary
# Library           Collections


# *** Keywords ***
# Connect To Database
#     [Arguments]    ${driver}    ${dbname}    ${user}    ${password}    ${host}    ${port}
    

# *** Variables ***
# ${DBHost}         ep-odd-mouse-a4br12y4-pooler.us-east-1.aws.neon.tech
# ${DBName}         verceldb
# ${DBPass}         7axBzIu0bVng
# ${DBPort}         5432
# ${DBUser}         default

# *** Test Cases ***
# Create Users Table 
#     Connect To Database    psycopg2    ${DBName}    ${DBUser}    ${DBPass}    ${DBHost}    ${DBPort}
#     @{query_results} =    Query    SELECT username, email, password FROM users
#     ${username}    Set Variable    ${query_results[0][0]}
#     ${email}    Set Variable    ${query_results[0][1]}
#     ${password}    Set Variable    ${query_results[0][2]}
#     Log    Username: ${username}
#     Log    Email: ${email}
#     Log    Password: ${password}
#     # Utilisez ces variables pour générer le token   

   
    