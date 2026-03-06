
# Python module imports
import os
from typing import Callable
from pathlib import Path
import logging

# Flask
from flask import flash, url_for, send_from_directory
from werkzeug.datastructures import FileStorage

# for file manipulation
import glob
from PIL import Image
from PIL.ImageFile import ImageFile



# internal imports
from pen_n_paperless import avatars_path

from pen_n_paperless.config.general import GeneralConfig


class Avatar():

    _allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif'}
    _extension = ""

    # data from the character
    _character_id = -1
    _character_name = ""


# -------------------------------------------------------------------------------

    def __init__(self, character_id: int, character_name: str) -> None:
        self._character_id = character_id
        self._character_name = character_name

        return


    def __str__(self) -> str:
        """Returns the file name belonging to this instance.
        """
        return self.file_path.as_posix() + self._extension 


    def __repr__(self) -> str:
        """Returns the file name belonging to this instance.
        """
        return self.file_path.as_posix() + self._extension 

# -------------------------------------------------------------------------------

    # Properties
    @property
    def filename(self) -> str:
        """Returns the file name of the avatar file without the file extension.
        """
        return f'avatar_{self._character_name}'
    
    @property
    def file_path(self) -> Path:
        """Returns the file path to the avatar without the file extension.
        """
        return avatars_path / self.filename
    
    @property
    def file_url(self) -> str:
        # prefer webp if present
        webp_path = avatars_path / (self.filename + '.webp')
        if os.path.exists(webp_path):
            return url_for('static', filename = f'avatars/{self.filename}.webp')
            # return self.filename + '.webp'
        else:
            # search for any type of file with the expected name
            pattern = avatars_path / (self.filename + '.*')
            matches = glob.glob(pattern.as_posix())
            if matches:
                filename = os.path.basename(matches[0])
                return url_for('static', filename = f'avatars/{filename}')
                # return (avatars_path / filename).as_posix()
        
        logging.warning(f'Search for avatar for character id "{self._character_id}" with name "{self._character_name}" did not yield a match.')
        return '#'


    @property
    def supported_file_types(self) -> str:
        file_types = ", ".join(map(str, self._allowed_extensions))
        return file_types



    def save(self, new_avatar_file: FileStorage) -> bool:

        # remove old avatars for this character
        self.delete()

        # retrieve file extension
        filename = new_avatar_file.filename
        if filename is None:
            logging.error(f"Given filename is '{filename}'")
            flash('No file uploaded', 'error')
            return False
        
        success = self._set_extension(Path(filename).suffix.lower())
        if not success:
            return False

        # process image
        try:
            img = Image.open(new_avatar_file.stream)
        except Exception:
            logging.error(f"Opening image for processing failed")
            flash('Invalid image file', 'error')
            return False

        # resize to max dimensions
        img.thumbnail(GeneralConfig.avatar_size(), Image.Resampling.LANCZOS)

        return self._convert_and_store(img)


    def _set_extension(self, extension_name: str) -> bool:

        if extension_name not in self._allowed_extensions:
            logging.error(f"Unsupported file type, got '{extension_name}'")
            flash('Unsupported file type', 'error')
            return False
        
        # convert/choose save format
        if extension_name == '.gif':
            # convert gifs to png (to avoid animated complexity)
            extension_name = '.png'
 

        self._extension = extension_name
        return True


    def _convert_and_store(self, img: ImageFile) -> bool:

        try:
            if self._extension in ('.jpg', '.jpeg'):
                if img.mode in ('RGBA', 'LA'):
                    converted_img = img.convert('RGB')
                else:
                    converted_img = img.convert()
                converted_img.save(self.file_path.as_posix() + self._extension, format='JPEG', quality=85, optimize=True)
            else:
                # PNG or converted GIF -> PNG
                img.save(self.file_path.as_posix() + self._extension, format='PNG', optimize=True)
        except Exception:
            logging.error(f'Failed to process image as jpg or png')
            flash('Failed to process image', 'error')
            return False
        
        # also create a WebP version for smaller delivery
        try:
            # convert mode if required
            if img.mode not in ('RGB', 'RGBA'):
                converted_img = img.convert('RGBA' if 'A' in img.mode else 'RGB')
            else:
                converted_img = img.convert()
            converted_img.save(self.file_path.as_posix() + self._extension, format='WEBP', quality=80, method=6)
        except Exception:
            # not fatal — continue but warn
            logging.warning(f'Avatar has been saved. Failed to create webp version.')
            flash('Avatar uploaded but failed to create WebP version', 'warning')

        # storing avatar successful
        logging.debug(f'Avatar has been saved.')
        flash('Avatar uploaded', 'success')
        return True




    def delete(self) -> None:
        """Best effort deletion of the avatar
        """
        file = avatars_path / self.filename

        for old in glob.glob(file.as_posix() + '.*'):
            try:
                os.remove(old)
            except Exception:
                pass
