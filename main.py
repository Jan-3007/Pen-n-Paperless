from pen_n_paperless import create_app



def main():
    print("Starting up pen-n-paperless!")
    
    app = create_app()

    app.run(
        debug=True,
        host='127.0.0.1', port=5001     # app can be accessed using 'http://127.0.0.1:5001' or 'localhost:5000' only on your machine (except the network configuration is different)
#        host='0.0.0.0', port=5000      # app can be accessed from any device on your network using 'http://<your-devices-IP>:5000'
        )


if __name__ == "__main__":
    main()
