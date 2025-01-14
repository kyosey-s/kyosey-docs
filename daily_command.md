# build VR env
```bash
python -m venv venv
source venv/bin/activate
```

# install Homebrew 
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

# ffmpeg
- this is for translateing into mp4 file

```bash
brew install ffmpeg
```
# build local server

```
python3 -m http.server
http://localhost:8000/<my_file>.html
```