# Form app_defiscalizare_rbc_precompletare_campuri

# Requirements for creating exe file:

- flask
- pyinstaller

- in PyCharm terminall run the following command to create exe file:
- keep xlsx file and app in the same folder

```
pyinstaller --onefile --noconsole --name app_defiscalizare_rbc_2025.exe --add-data "templates;templates" --add-data "static;static" app.py

```
