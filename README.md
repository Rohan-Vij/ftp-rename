# FTP Rename

[![Pylint](https://github.com/Rohan-Vij/ftp-rename/actions/workflows/pylint.yaml/badge.svg)](https://github.com/Rohan-Vij/ftp-rename/actions/workflows/pylint.yaml)

## What It Does

This utility program converts the file names of items in an FTP server en masse.

**For example, items with the following paths:**
1. `shirts/12943-the-north-face-shirt-detail.jpg`
2. `shirts/12943-the-north-face-shirt_th.jpg`
3. `shirts/12943-the-north-face-shirt.jpg`

(Item file format: `<category>/<id>-<item name>-<suffix>.<file type>`()

**When run with the program, can be changed to:**

1. `shirts/12943-the-north-face-green-shirt-detail.jpg`
2. `shirts/12943-the-north-face-green-shirt_th.jpg`
3. `shirts/12943-the-north-face-green-shirt.jpg`

## How To Use

### Configuration Files
#### config.yaml
`config.yaml` is a configuration file containing the directories of item categories and various possible image types.
Example:
```yaml
PATTERNS:
  IMAGES: 
    - -portrait
    - -high-canvas
    - -high
    - -fb
    - -detail-high
    - -detail
    - -square
    - _th
    - -detail-portrait

CATEGORIES:
    - shirts
    - pants
    - hats
```
Please note that the program only supports one specific "extra" case (_th). All other image types must be in the format `-<image type>`.

#### ftp_config.yaml
`ftp_config.yaml` is a configuration file containing connection parameters for the FTP server.
Example:
```yaml
FTP:
  HOST: 172.17.0.0
  PORT: 22
  USER: foo
  PASSWORD: pass
```

### Basic Steps
1. Run `pip install -r requirements.txt` in your terminal.
2. Change `config.yaml` (item categories, image types) and `ftp_config.yaml` (FTP server information) if needed.
3. Run `python main.py` in your terminal.

#### Development information, not needed for usage!

Pipreqs (requirements.txt): `pipreqs --force`

To bottom of `.spec` file add:
```python
import shutil
shutil.copyfile('config.yaml', '{0}/config.yaml'.format(DISTPATH))
shutil.copyfile('ftp_config.yaml', '{0}/ftp_config.yaml'.format(DISTPATH))
shutil.copyfile('assets/ftplogo.ico', '{0}/ftplogo.ico'.format(DISTPATH))
```

To initially build `.exe` run `pyinstaller.exe --onefile --windowed --icon=assets/ftplogo.ico main.py`

To rebuild the `.exe` run `pyinstaller --clean main.spec`

Follow https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184 for making sure the `.exe` is not shown as a virus!