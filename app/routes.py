from flask import current_app as app
from flask import render_template, request, redirect, url_for, session, flash, get_flashed_messages, jsonify
from .game.character.character import Character, get_by_name, create_character, delete_character
from werkzeug.utils import secure_filename
from pathlib import Path
import glob
from PIL import Image
#from .data.data_files import load_data, save_data
import os


from .game_settings import GameSettings
from .strings import Strings
from .game.armoury import Armoury
from .game.weaponry import Weaponry
from .game.tribe import Tribe
from .game.profession import Profession
from .game.specialization import Specialization
from .game.abilities import Abilities


# gets called when a user accesses the main page
@app.route('/')
def main():
    char_id = session.get('character_id')
    char_name = None
    avatar_url = None
    avatar_url_webp = None
    from .game.character.character import Character
    if char_id:
        c = Character.query.get(char_id)
        if c:
            char_name = c.name
            # try to find avatar file
            avatars_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'images', 'avatars')
            # prefer webp if present
            webp_path = os.path.join(avatars_dir, f"{char_id}.webp")
            if os.path.exists(webp_path):
                avatar_url_webp = url_for('static', filename=f'images/avatars/{char_id}.webp')
            else:
                pattern = os.path.join(avatars_dir, f"{char_id}.*")
                matches = glob.glob(pattern)
                if matches:
                    filename = os.path.basename(matches[0])
                    avatar_url = url_for('static', filename=f'images/avatars/{filename}')

    # also show all characters on the main page
    characters = Character.query.order_by(Character._name).all()

    # get name of the game
    world_name = GameSettings.world_name()

    # game_name:        name of the game world
    # character_name:   for when user is still loged in
    # characters:       list of all created characters
    return render_template('main.html', 
                           game_name=world_name, 
                           character_name=char_name, 
                           characters=characters, 
                           avatar_url=avatar_url, 
                           avatar_url_webp=avatar_url_webp)





@app.route('/login', methods=['POST'])
def login_or_create():
    from .game.character.character import Character
    if request.method == 'POST':

        # get string entered in input box
        name = request.form.get('name', '').strip()

        if not name:
            flash('Please provide a character name.', 'error')
            return redirect(url_for('main'))

        existing = get_by_name(name)
        if existing:
            # create new session with accessor 'character_id'
            session['character_id'] = existing.id
            flash(f'Logged in as {existing.name}', 'success')
            return redirect(url_for('my_character'))

        # create new character
        new_character = create_character(name)
        # create new session with accessor 'character_id'
        session['character_id'] = new_character.id
        flash(f'Created and logged in as {new_character.name}', 'success')
        return redirect(url_for('my_character'))

    # # GET: show existing characters and creation form
    # characters = Character.query.order_by(Character._name).all()
    # return render_template('login.html', characters=characters)





@app.route('/me')
def my_character():
    char_id = session.get('character_id')
    if not char_id:
        flash('Please login to view your character', 'error')
        return redirect(url_for('main'))

    # get character handle
    character_h = Character.query.get_or_404(char_id)
    # compute avatar urls if uploaded (prefer webp)
    avatar_url = None
    avatar_url_webp = None
    avatars_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'images', 'avatars')
    webp_path = os.path.join(avatars_dir, f"{char_id}.webp")
    if os.path.exists(webp_path):
        avatar_url_webp = url_for('static', filename=f'images/avatars/{char_id}.webp')
    else:
        pattern = os.path.join(avatars_dir, f"{char_id}.*")
        matches = glob.glob(pattern)
        if matches:
            filename = os.path.basename(matches[0])
            avatar_url = url_for('static', filename=f'images/avatars/{filename}')


    # provide tribe list
    tribe_list = Tribe.get_all_names()

    # provide profession list
    profession_list = Profession.get_all_names()

    # provide specialization list
    specialization_list = Specialization.get_all_names(character_h.profession, character_h.level)

    # provide armour list
    armour_list = Armoury.get_all_names()

    # provide weapons list
    weapon_list = Weaponry.get_all_names()

    # provide ability list
    ability_list = Abilities.get_all_names(character_h.profession)

    return render_template('me.html', 
                           character=character_h, 
                           tribe_list=tribe_list,
                           profession_list=profession_list,
                           specialization_list=specialization_list,
                           Strings=Strings, 
                           avatar_url=avatar_url, 
                           avatar_url_webp=avatar_url_webp,
                           armour_list=armour_list,
                           max_armour_sets=GameSettings.max_armour_sets(),
                           weapon_list=weapon_list,
                           max_nb_weapons=GameSettings.max_number_of_weapons(),
                           ability_list=ability_list
                           )




@app.route('/me/editor')
def editor():
    char_id = session.get('character_id')
    if not char_id:
        flash('Please login to view your character', 'error')
        return redirect(url_for('main'))

    # get character handle
    character_h = Character.query.get_or_404(char_id)


    # compute avatar urls (prefer webp)
    avatar_url = None
    avatar_url_webp = None
    avatars_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'images', 'avatars')
    webp_path = os.path.join(avatars_dir, f"{char_id}.webp")
    if os.path.exists(webp_path):
        avatar_url_webp = url_for('static', filename=f'images/avatars/{char_id}.webp')
    else:
        pattern = os.path.join(avatars_dir, f"{char_id}.*")
        matches = glob.glob(pattern)
        if matches:
            filename = os.path.basename(matches[0])
            avatar_url = url_for('static', filename=f'images/avatars/{filename}')


    # provide armour list for editor dropdown (use Armoury public API)
    # armour_list = {}
    # armour_name_list = {}
    # try:
    #     armour_keys = Armoury.get_all()
    #     print("keys: " + armour_keys)
    #     # fallback: if Armoury is empty
    #     if not armour_keys:
    #         armour_keys = {"None": "None  available"}
        
    #     else:
    #         for key in armour_keys:
    #             props = Armoury.get_properties(key)
    #             props[Strings.names.value] = props.get(Strings.names.value, "No name")[GameRules.language()]
    #             print("props: " + props)
    #             armour_list[key] = props
    #             armour_name_list[key] = props.get(Strings.names.value, "No name found")

    # except Exception:
    #     armour_list = {"Error": "error"}
    #     pass


    # provide armour list
    armour_list = Armoury.get_all_names()


    # provide weapons list
    weapon_list = Weaponry.get_all_names()


    # provide tribe list
    tribe_list = Tribe.get_all_names()

    

    # provide profession list
    profession_list = Profession.get_all_names()



    # provide specialization list
    specialization_list = Specialization.get_all_names(character_h.profession, character_h.level)



    # provide ability list
    ability_list = Abilities.get_all_names(character_h.profession)


    return render_template('editor.html', 
                           character=character_h, 
                           Strings=Strings, 
                           avatar_url=avatar_url, 
                           avatar_url_webp=avatar_url_webp, 
                           armour_list=armour_list, 
                           max_armour_sets=GameSettings.max_armour_sets(),
                           weapon_list=weapon_list,
                           max_nb_weapons=GameSettings.max_number_of_weapons(),
                           tribe_list=tribe_list,
                           profession_list=profession_list,
                           specialization_list=specialization_list,
                           ability_list=ability_list
                           )



@app.route('/me/upload_avatar', methods=['POST'])
def upload_avatar():
    char_id = session.get('character_id')
    if not char_id:
        flash('Please login to update avatar', 'error')
        return redirect(url_for('main'))

    if 'avatar' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('editor'))

    file = request.files['avatar']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('editor'))

    filename = secure_filename(file.filename)
    allowed = {'.png', '.jpg', '.jpeg', '.gif'}
    ext = Path(filename).suffix.lower()
    if ext not in allowed:
        flash('Unsupported file type', 'error')
        return redirect(url_for('editor'))

    avatars_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'images', 'avatars')
    Path(avatars_dir).mkdir(parents=True, exist_ok=True)

    # remove old avatars for this character
    for old in glob.glob(os.path.join(avatars_dir, f"{char_id}.*")):
        try:
            os.remove(old)
        except Exception:
            pass

    # process image: resize/recompress using Pillow
    try:
        img = Image.open(file.stream)
    except Exception:
        flash('Invalid image file', 'error')
        flashed = get_flashed_messages(with_categories=True)
        return jsonify(status='error', flashed=flashed), 400

    # resize to max dimensions
    MAX_SIZE = (512, 512)
    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.ANTIALIAS

    img.thumbnail(MAX_SIZE, resample)

    # convert/choose save format
    save_ext = ext
    if ext == '.gif':
        # convert gifs to png (to avoid animated complexity)
        save_ext = '.png'

    new_name = f"{char_id}{save_ext}"
    save_path = os.path.join(avatars_dir, new_name)

    try:
        if save_ext in ('.jpg', '.jpeg'):
            if img.mode in ('RGBA', 'LA'):
                img = img.convert('RGB')
            img.save(save_path, format='JPEG', quality=85, optimize=True)
        else:
            # PNG or converted GIF -> PNG
            img.save(save_path, format='PNG', optimize=True)
    except Exception:
        flash('Failed to process image', 'error')
        flashed = get_flashed_messages(with_categories=True)
        return jsonify(status='error', flashed=flashed), 500

    # also create a WebP version for smaller delivery
    webp_name = f"{char_id}.webp"
    webp_path = os.path.join(avatars_dir, webp_name)
    try:
        # convert mode if required
        webp_img = img
        if webp_img.mode not in ('RGB', 'RGBA'):
            webp_img = webp_img.convert('RGBA' if 'A' in webp_img.mode else 'RGB')
        webp_img.save(webp_path, format='WEBP', quality=80, method=6)
    except Exception:
        # not fatal — continue but warn
        flash('Avatar uploaded but failed to create WebP version', 'warning')

    # respond with flashed messages and avatar urls
    flash('Avatar uploaded', 'success')
    flashed = get_flashed_messages(with_categories=True)
    avatar_url = None
    avatar_url_webp = None
    if os.path.exists(webp_path):
        avatar_url_webp = url_for('static', filename=f'images/avatars/{webp_name}')
    elif os.path.exists(save_path):
        avatar_url = url_for('static', filename=f'images/avatars/{new_name}')
    return jsonify(status='ok', 
                   flashed=flashed, 
                   avatar_url=avatar_url, 
                   avatar_url_webp=avatar_url_webp
                   )


@app.route('/me/delete_avatar', methods=['POST'])
def delete_avatar():
    char_id = session.get('character_id')
    if not char_id:
        flash('Please login', 'error')
        flashed = get_flashed_messages(with_categories=True)
        return jsonify(status='error', flashed=flashed), 403

    avatars_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'images', 'avatars')
    removed = False
    for old in glob.glob(os.path.join(avatars_dir, f"{char_id}.*")):
        try:
            os.remove(old)
            removed = True
        except Exception:
            pass

    if removed:
        flash('Avatar removed', 'success')
    else:
        flash('No avatar to remove', 'error')

    flashed = get_flashed_messages(with_categories=True)
    return jsonify(status='ok', flashed=flashed, avatar_url=None)



# usage hint: update(Strings.name="Buddy", Strings.tribe="Strings.Tribes.elf")

# @app.route('/update/<data_dict>', methods=['POST'])
# def update(**data_dict) -> tuple:
#     char_id = session.get('character_id')
#     if not char_id:
#         return (json.dumps({'error': 'not logged in'}), 403, {'Content-Type': 'application/json'})

#     character = Character.query.get(char_id)


#     for key in data_dict.keys():
#         character.update(key, data_dict.get(key))





@app.route('/update', methods=['POST'])
def update() -> dict:
    """call this function from a html template"""

    char_id = session.get('character_id')
    if not char_id:
        flash('Please login to view your character', 'error')
        return redirect(url_for('main'))

    # get character handle
    character_h = Character.query.get_or_404(char_id)


    # get the json data from the html request as a dict
    # data = request.form.to_dict(flat=False)
    data = request.get_json() or {}


    success = False

    # track whether this update should trigger a client-side reload
    reload_page = False

    # collect canonical updated values to return to client for immediate UI update
    updated = {}

    for key in data.keys():
        # print(f"updating key: {key}")
        success = character_h.update(key, data.get(key))

        if success:
            # populate updated with canonical values depending on key
            try:
                # tribe/profession/specialization
                if key == Strings.tribe.value:
                    updated[key] = character_h.tribe

                elif key == Strings.profession.value:
                    # updated[key] = character_h.profession
                    
                    # request page reload, specialization is highly dependent of the selected profession
                    reload_page = True

                elif key == Strings.specialization.value:
                    updated[key] = Specialization.get_name(character_h.specialization, character_h.level)

                # armour
                elif key == Strings.Armour.armour.value:
                    ch_armour_name_list = [Armoury.get_name(armour) for armour in character_h.armour]
                    updated[key] = ch_armour_name_list

                # weapons
                elif key == Strings.Weapons.weapons.value:
                    ch_weapon_name_list = [Weaponry.get_name(weapon) for weapon in character_h.weapons]
                    print(ch_weapon_name_list)
                    updated[key] = ch_weapon_name_list
                    
                # abilities
                elif key in Strings.Abilities:
                    # print(f"Getting updated abilities for {key}")
                    updated[Strings.Abilities.abilities.value] = { 
                        key: character_h.abilities.get(key, {
                                Strings.Abilities.level.value: 0, 
                                Strings.Abilities.cost_history.value: []
                            }) 
                            }

                    print(character_h.abilities.get(key, {}))

                # notes
                elif key == Strings.notes.value:
                    updated[key] = character_h.notes

                # hp and xp history
                elif key == Strings.hp_history.value or key == Strings.xp_history.value:
                    # request page reload, hp and xp history are too complex
                    reload_page = True

                if not reload_page:
                    # always append full list of attributes and attr. bonuses
                    updated[Strings.Attributes.attributes.value] = character_h.attributes()
                    updated[Strings.Attributes.attribute_bonuses.value] = character_h.attribute_bonuses()
                    updated[Strings.Statistics.statistics.value] = character_h.statistics()
                    updated[Strings.Abilities.max_ability_points.value] = character_h.max_ability_points
                    updated[Strings.Abilities.remaining_ability_points.value] = character_h.remaining_ability_points

            except Exception:
                # on any error while building updated, skip adding that key
                pass

        else:
            # flash(f'Error updating {key}', 'error')
            flashed = get_flashed_messages(with_categories=True)
            return jsonify(status='error', flashed=flashed)

    # Collect any flashed messages and return them in the JSON response so AJAX callers can display them
    flashed = get_flashed_messages(with_categories=True)
    return jsonify(status='ok', flashed=flashed, reload=reload_page, updated=updated)





    # # get data to be saved
    # data = request.get_json() or {}

    # # load existing stats
    # stats = load_data(char_id, "stats")
    # for key in stats.keys():
    #     # check if key exists in incoming data
    #     if key in data:
    #         try:
    #             stats[key] = int(data[key])
    #         except Exception:
    #             pass

    # save_data(char_id, "stats", stats)

    # return (json.dumps({'status': 'ok', 'stats': stats}), 200, {'Content-Type': 'application/json'})



# # TODO repair
# @app.route('/me/update/notes', methods=['POST'])
# def update_notes() -> tuple:

#     # get data to be saved
#     data = request.get_json() or {}

#     # notes or other text fields
#     if 'notes' in data:
#         data['notes'] = data['notes']






@app.route('/logout', methods=['POST'])
def logout():

    # remove the username from the session if it's there
    session.pop('character_id', None)
    flash('Logged out', 'success')
    return redirect(url_for('main'))






@app.route('/characters')
def characters_list():
    from .game.character.character import Character
    q = request.args.get('q', '').strip()
    if q:
        chars = Character.query.filter(Character._name.ilike(f"%{q}%")).order_by(Character._name).all()
    else:
        chars = Character.query.order_by(Character._name).all()
    return render_template('characters.html', characters=chars, query=q)






@app.route('/delete', methods=['POST'])
def delete():
    char_id = session.get('character_id')
    if not char_id:
        flash('Please login to delete your character', 'error')
        return redirect(url_for('main'))


    success = delete_character(char_id)
    if success:
        session.pop('character_id', None)
        flash('Character deleted successfully', 'success')
    else:
        flash('Character deletion failed', 'error')

    return redirect(url_for('main'))