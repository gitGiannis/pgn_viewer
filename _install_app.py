import PyInstaller.__main__


def install_using_pyinstaller():
    """
    Install app using PyInstaller
    """
    PyInstaller.__main__.run([
        # source py file
        'main.py',
        # no console running in background
        '--noconsole',
        # app icon
        '--icon=icons/stonk.ico ',
        # app name
        '--name=pgn viewer',
        # adding images
        '--add-data="icons/stonk.ico;icons"',
        '--add-data="icons/chess.png;icons"',
        '--add-data="icons/piece_icons/*;icons/piece_icons"',
        '--add-data="icons/basic/*;icons/basic"',
        # adding sound effects
        '--add-data="sound_effects/*;sound_effects"',
        # adding pip3w
        '--add-data="pip3w;."',
        # adding pgn_files dir
        '--add-data="pgn_files/*;pgn_files"'
    ])


install_using_pyinstaller()
