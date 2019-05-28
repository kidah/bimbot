## greet
* greet
    - action_greet

* enter_data {"name": "sofiat"}
    - action_greet 

## thanks
* thank
    - utter_noworries
    - utter_anything_else


## bye
* bye
    - utter_bye

## enter project name 
* enter_data {"projectname": "UWE FBL building"}
   - action_project_info


## enter user name
* enter_data {"name": "sofiat"}
    - action_greet 

* affirmative
   - utter_ask_projectname

## ask what bot can do
* whats_possible
    - utter_whatspossible

## project information
 * project_information
    - action_project_info

## search project issues
* search_project_issues
    - action_project_issues

## bot chitchat
* bot_chitchat
    - action_chitchat

## negative + negative

* negative
    - utter_anything_else

* negative
    - utter_bye 


## negative  + positive
* negative
    - utter_anything_else

* affirmative
    - utter_great

## greet + no brief + nothing else
* greet
    - action_greet

* enter_data {"name": "sofiat"}
    - action_greet 

* negative
    - utter_anything_else

* negative
    - utter_bye

## greet + no brief + yes
* greet
    - action_greet

* enter_data {"name": "sofiat"}
    - action_greet 

* negative
    - utter_anything_else

* affirmative
    - utter_great


## greet + yes brief
* greet
    - action_greet

* enter_data {"name": "sofiat"}
    - action_greet 

* affirmative
    - utter_ask_projectname

* enter_data {"projectname": "UWE FBL building"}
    - action_project_info

* affirmative
   - utter_great


## greet + yes brief + yes to anything else +  project information + thanks + bye
* greet
    - action_greet

* enter_data {"name": "sofiat"}
    - action_greet 

* affirmative
    - utter_ask_projectname

* enter_data {"projectname": "UWE FBL building"}
    - action_project_info

* affirmative
    - utter_great

* project_information
    - action_project_info

* thank
    - utter_noworries

* bye
    - utter_bye


## greet + yes brief + nothing else +  project information + thanks + bye
* greet
    - action_greet

* enter_data {"name": "sofiat"}
    - action_greet 

* affirmative
    - utter_ask_projectname

* enter_data {"projectname": "UWE FBL building"}
    - action_project_info

* negative
    - utter_bye

## greet + no + search project information + thanks + bye
* greet
    - action_greet

* enter_data {"name": "sofiat"}
    - action_greet 

* negative
    - utter_askwhat

* project_information
    - action_project_info

* thank
    - utter_noworries

* bye
    - utter_bye

## greet + bot chitchat + thanks + bye
* greet
    - action_greet

* enter_data {"name": "sofiat"}
    - action_greet 

* negative
    - utter_askwhat

* bot_chitchat
    - action_chitchat

* thank
    - utter_noworries

* bye
    - utter_bye


## greet + yes brief + search project issues
* greet
    - action_greet

* enter_data {"name": "sofiat"}
    - action_greet 

* negative
    - utter_askwhat

* search_project_issues
    - action_project_issues

* thank
    - utter_noworries

* bye
    - utter_bye
