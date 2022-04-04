import libs
# import logging
from structure_ui import init_UI, run_UI #, init_and_run_UI
from constructor_ui import Ui_ISR

# logging.basicConfig(
#     filename="details_harvester.log",
#     level=logging.WARNING,
#     # format=format,
#     # datefmt=datefmt
# )

# #### #### #### #### #
# Program Information #
# #### #### #### #### #
BRAND_NAME = "ISR UI"
APP_NAME = "TCP/IP Test Arayüzü"
VERSION = "1.0.0"
VERSION_NAME = "BETA"
TITLE = BRAND_NAME + " | " + APP_NAME + " v" + VERSION + " " + VERSION_NAME

LOGGER_LEVEL = 0  # 0, 1, 2, 3, 4
# IP_SENDER = "192.168.22.22"  # Fatih PC
# IP_SENDER = "127.0.0.1"  # Local TEST
# PORT_SENDER = 8888

# IP_RECEIVER = "127.0.0.1"
# PORT_RECEIVER = PORT_SENDER  # Local Test
# PORT_RECEIVER = 8889

# INTERNET_DATA_FORMAT = "[ethernetState]\nMetin Kutusu={}\n[cameraState]\nMetin Kutusu={}\n[componentOK]\nMetin Kutusu={}\n[componentNOK]\nMetin Kutusu={}\n[labelOK]\nMetin Kutusu={}\n[labelNOK]\nMetin Kutusu={}\n[processDone]\nMetin Kutusu={}\n"


if __name__ == "__main__":
    
    title = TITLE
    Class_UI = Ui_ISR
    UI_File_Path = "ISR_UI.ui"
    show_UI=True
    is_Maximized = False

    app, ui = init_UI(
        Class_UI,
        UI_File_Path=UI_File_Path,
    )

    # ui.init_Internet_Objects(

    #     ip_sender=IP_SENDER,
    #     port_sender=PORT_SENDER,
    #     regex_sender=None,
    #     parsing_format_sender=None,

    #     ip_receiver=IP_RECEIVER,
    #     port_receiver=PORT_RECEIVER,
    #     regex_receiver=None,
    #     parsing_format_receiver=None,

    #     internet_Parser_Format=INTERNET_DATA_FORMAT,

    #     delay=0.0000001
    # )
    
    run_UI(
        app=app,
        UI=ui,
        title=title,
        show_UI=show_UI,
        is_Maximized=is_Maximized
    )
