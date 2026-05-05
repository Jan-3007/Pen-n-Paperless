

# Activate venv
```
.venv\Scripts\activate
```


# Run this project in debug mode
```
uv run main.py -d
```

# Run py-spy on this project for performance analysis
```
py-spy record -o performance_profile.svg -r 100 -- uv run .\main.py -d
```




# Convert Python enums to JavaScript enums
This step is necessary befor the app can be executed.
```
uv run main.py -g
```



# SQL database viewer

https://inloop.github.io/sqlite-viewer/

