# TLB FTP Rename

### How to use

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