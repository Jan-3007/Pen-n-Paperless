
from argparse import ArgumentParser
from pathlib import Path


from pen_n_paperless import create_app
from pen_n_paperless.common.pyjs_shared_enums import CommonEnumGenerator


def main():

    parser = ArgumentParser()
    parser.add_argument("-i", "--init_only", help = "Only run initialization of the app.", action = "store_true")
    parser.add_argument("-d", "--debug", help = "Launch app in debug mode.", action = "store_true")
    # parser.add_argument("-e", "--export-characters", help="Only run the character export of the app.", action = "store_true")
    
    args = parser.parse_args()

    if args.init_only:
        python_enum_file = Path(__file__).parent / 'pen_n_paperless' / 'common' / 'keys.py'
        js_enum_file = Path(__file__).parent / 'pen_n_paperless' / 'frontend' / 'static' / 'js' / 'enums.js'

        with CommonEnumGenerator(   python_file_path=python_enum_file.absolute().as_posix(), 
                                    js_file_path=js_enum_file.absolute().as_posix()
                                ) as common_enum_generator:
            common_enum_generator.generate()
        return

    # start the actual app
    print("Starting up pen-n-paperless!")
    app = create_app()

    if args.debug:
        app.run(
            debug=True,
            host='127.0.0.1', port=5001     # app can be accessed using 'http://127.0.0.1:5001' or 'localhost:5000' only on your machine (except the network configuration is different)
            )
        return
    else:
        app.run(
            debug=False,
            host='0.0.0.0', port=5000      # app can be accessed from any device on your network using 'http://<your-devices-IP>:5000'
            )



if __name__ == "__main__":
    main()
