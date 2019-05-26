## greet
* greet
    - utter_ask_name

## get user name
* enter_data{"name": "Sofiat"}
    - action_greet

## thanks
* thank
    - utter_noworries
    - utter_anything_else

## bye
* bye
    - utter_bye

## ask what bot can do
* whats_possible
    - utter_whatspossible

## deny or negative
*  negative
    - utter_deny

## affirmative
* affirmative
    - utter_great

## out of scope
* out_of_scope
    - utter_outofscope

## search project issues
* search_project_issues
    - action_project_issues
    
## search design data
* search_design_data
    - action_project_design

## greet + no brief
* greet
    - utter_ask_name
* enter_data{"name": "Sofiat"}
    - action_greet
* negative
    - utter_anything_else

## greet + yes brief
* greet
    - action_greet
* enter_data{"name": "Sofiat"}
    - action_greet
* affirmative
    - utter_great

## greet + yes brief + search design data
* greet
    - action_greet

* positive
    - utter_react_positive

* search_design_data
    - action_project_design

* thank
    - utter_noworries

## greet + no brief + search design data
* greet
    - action_greet

* negative
    - utter_react_negative

* search_design_data
    - action_project_design

* thank
    - utter_noworries

* bye
    - utter_bye


## greet + bot chitchat + thanks + bye
* greet
    - action_greet

* bot_chitchat
    - action_chitchat

* thank
    - utter_noworries

* bye
    - utter_bye

## greet + project information + thanks + bye
* greet
    - action_greet

* project_information
    - action_project_info

* thank
    - utter_noworries

* bye
    - utter_bye


## greet + yes brief + search project issues
* greet
    - action_greet

* positive
    - utter_react_positive

* search_project_issues
    - action_project_issues

* thank
    - utter_noworries

* bye
    - utter_bye

## greet + no brief + search project issues
* greet
    - action_greet

* negative
    - utter_react_negative

* search_project_issues
    - action_project_issues

* thank
    - utter_noworries

* bye
    - utter_bye
