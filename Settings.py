import os

Programm_ort = os.getlogin()

if __name__ == "__main__":
    pass




def Check_settings():
    global see_the_text
    with open(f"C:\\Users\\{Programm_ort}\\Desktop\\Textmanager Daten\\Textmanager Zwischenspeicher\\see_the_text.txt") as see_the_textinfo:
        see_the_text = see_the_textinfo.read()
