# Japanese text area-screenshot ocr

## Description
This app allows you to take screenshots of certain areas and recognize Japanese text on them.

## Installation

### Linux

#### Arch

Qt5 installation:

```
sudo pacman -S qt5-base
```

Tesseract datapack installation:

```
sudo pacman -S tesseract-data-jpn
```

##### Manually

Copying repository:

```
git clone https://github.com/dacetascien/jpn_recongnition
cd jpn_recognition
```

Python libraries installtion into virtual enviroment:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -Ur requirements.txt
```

Copying files to /usr/bin and /usr/share/applications/:

```
sudo cp jpn_recognition.desktop /usr/share/applications
sudo cp -r . /usr/bin/jpn_recognition
```

Giving permissions to start script:

```
chmod +x start.sh
```

##### Via bash script

```
git clone https://github.com/dacetascien/jpn_recongnition
cd jpn_recognition
chmod +x install.sh
sudo ./install.sh
```
## Uninstallation

### Linux

#### Arch

##### Manually 

```
sudo rm /usr/share/applications/jpn_recognition.desktop
sudo rm -r /usr/bin/jpn_recognition
```

##### Via bash script

```
chmod +x uninstall.sh
sudo ./uninstall.sh
```

## Docker

To build docker:
```
sudo docker build -t jpn_recognition .
```

To run docker container:
```
sudo docker run -e "DISPLAY=$DISPLAY" -v "$HOME/.Xauthority:/root/.Xauthority:ro" --network host jpn_recognition
```

## References

All of the data comes from the following sources:

* [kanji-data](https://github.com/davidluzgouveia/kanji-data)

