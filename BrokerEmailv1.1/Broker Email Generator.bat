@echo on
x:
set VENV_PATH=X:\Fund Management\Fund Management Team Files\FM Personal Folders\Richard\PycharmProjects\venv
set PATH=%PTHON_PTH%;%PATH%
pip install requests
pip install bs4
pip install chardet
cd "X:\Fund Management\Fund Management Team Files\FM Personal Folders\Richard\PycharmProjects\BrokerEmailv1.1"
python main.py
pause