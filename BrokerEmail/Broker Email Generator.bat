@echo on
x:
set VENV_PATH=X:\Fund Management\Fund Management Team Files\FM Personal Folders\Richard\PycharmProjects\venv
set PATH=%PTHON_PTH%;%PATH%
pip install bs4
pip install chardet
pip install aiohttp
cd "X:\Fund Management\Fund Management Team Files\FM Personal Folders\Richard\PycharmProjects\BrokerEmail"
python main_broker_email.py
pause