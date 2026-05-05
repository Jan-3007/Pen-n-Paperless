

# Unit Tests

## Website

### Creation
Webpage:
- main page

Action:
- enter name

Result:
- successfully created new character or logged in

### Login
Webpage:
- main page

Action:
- click login next to existing character

Result:
- successfully logged in

### Logout
Webpage:
- character page

Requirement:
- must be logged in

Action:
- click logout

Result:
- successfully logged out



## Adding text to notes
Webpage:
- character page

Action:
- add or edit text in text field
- press save

Result:
- successfully saved
- text remains
- text remains after page refresh


## Avatar
### Upload
Webpage:
- Character Editor

Requirement:
- avatar exists
- avatar does not exist yet

Action:
- upload an avatar

Result:
- avatar successfully uploaded
- avatar is immediately shown
- avatar is shown on main page, character overview and character editor

### Deletion
#### Case 1
Webpage:
- Character Editor

Requirement:
- avatar exists

Action:
- delete avatar

Result:
- avatar successfully removed
- placeholder is immediately shown
- placeholder shown on main page, character overview and character editor

#### Case 2
Webpage:
- Character Editor

Requirement:
- avatar does not exist yet

Action:
- delete avatar

Result:
- no error
- warning okay
- placeholder remains active on main page, character overview and character editor


## Character Properties
Webpage:
- character editor page

### Tribe
Action:
- change tribe

Result:
- change of the attribute bonuses possible (see data in content.characters.tribe.py)
- change of the defense bonus possible (see data in content.characters.tribe.py)

### Profession
Action:
- change of profession

Result:
- change of the max hp possible
- change of the attribute bonuses possible (see data in content.characters.tribe.py)
- change of the defense bonus possible (see data in content.characters.tribe.py)

### Specialization
Action:
- change of specialization

Result:
- change of the attribute bonuses possible (see data in content.characters.tribe.py)
- change of the defense bonus possible (see data in content.characters.tribe.py)

