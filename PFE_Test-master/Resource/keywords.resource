*** Settings ***
Resource    ../Resource/variables.resource
Resource    ../Resource/import.resource


*** Keywords ***
Get All Products 
    ${headers}=    Create Dictionary    Content-Type=application/json

    ${response}=    GET    url=${Host}${GET_ALL_PRODUCTS}    headers=${headers}

    Log    ${response.status_code}
    Log    ${response.content}

Get One Product By ID
    ${headers}=    Create Dictionary    Content-Type=application/json

    ${response}=    GET    url=${Host}${GET_SINGLE_PRODUCT}    headers=${headers}

    Log    ${response.status_code}
    Log    ${response.content}

   


