@echo on
x:
set VENV_PATH=X:\Fund Management\Fund Management Team Files\FM Personal Folders\Richard\PycharmProjects\venv
set PATH=%VENV_PATH%;%PATH%
pip install comtypes
pip install python-docx
pip install exceptions
cd X:\Fund Management\Fund Management Team Files\FM Personal Folders\Richard\PycharmProjects\AOL
echo "Please wait a couple of seconds, then press enter"
python main_aol.py >> log.text
pause
