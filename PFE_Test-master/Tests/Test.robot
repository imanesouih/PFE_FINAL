*** Settings ***
Library    Browser
*** Test Cases ***
Test Google in Headless Mode
    [Tags]    FT-2    Google    Search
    [Documentation]    "Gets, types, and asserts"
    New Browser    headless=${True}    # Initialisez un nouveau navigateur en mode headless
    New Page       https://www.google.com/
    Type Text    id=APjFqb    Akkodis
    # Cliquer sur le bouton de recherche
    Close Browser    