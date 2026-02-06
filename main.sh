# Generate the site
uv run main.py | tee build.log

# Start the server specifically inside the public folder
# Using -d (directory) is cleaner than manually cd-ing
python3 -m http.server 8888 -d docs