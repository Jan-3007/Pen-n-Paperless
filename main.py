
from argparse import ArgumentParser

from pen_n_paperless import create_app,\
                            generate_files


def main():

    parser = ArgumentParser()
    parser.add_argument("-g", "--generate_only", help = "Files are pregenerated. Regenerates the files", action = "store_true")
    parser.add_argument("-d", "--debug", help = "Launch app in debug mode.", action = "store_true")
    # parser.add_argument("-e", "--export-characters", help="Only run the character export of the app.", action = "store_true")
    args = parser.parse_args()

    # arguments that don't require the whole app
    if args.generate_only:
        print("Generating files ...")
        generate_files()
        return


    # start the actual app
    print("Starting up pen-n-paperless!")
    app = create_app()

    if args.debug:
        print("The app can be accessed at: 'http://127.0.0.1:5001'")
        app.run(
            debug=True,
            # app can be accessed using 'http://127.0.0.1:5001' or 'localhost:5000' only on your machine (except the network configuration is different)
            host='127.0.0.1', port=5001     
            )
        return
    else:
        app.run(
            debug=False,
            # app can be accessed from any device on your network using 'http://<your-devices-IP>:5000'
            host='0.0.0.0', port=5000      
            )
        return
    
    



if __name__ == "__main__":
    main()
