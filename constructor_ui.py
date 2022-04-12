import logging
from time import time

import libs
from qt_tools import qtimer_Create_And_Run # , list_Widget_Item
from math_tools import random_Bulk_Data_Faster
# from tools import time_log, TIME_FLAGS, time_list, load_from_json, list_files, save_to_json, remove_file
from structure_ui import init_and_run_UI, Graphics_View, ROI_Rectangle  #, Structure_UI
from structure_ui_camera import Structure_Ui_Camera
# from structure_threading import Thread_Object
from structure_data import Structure_Buffer
from structure_camera import CAMERA_FLAGS


### ### ### ### ### ## ## ## ### ### ### ### ###
### ### ### CAMERA UI CONFIGURATIONS ### ### ###
### ### ### ### ### ## ## ## ### ### ### ### ###


class Ui_ISR(Structure_Ui_Camera):
    def __init__(self, *args, obj=None, logger_level=logging.INFO, **kwargs):
        super(Ui_ISR, self).__init__(*args, **kwargs)

        ### ### ### ### ###
        ### Constractor ###
        ### ### ### ### ###
        self.logger_level = logger_level
        self.__thread_Dict = dict()
        self.__buffer_Coordinates = Structure_Buffer(max_limit=3)

        ### ### ### ### ###
        ### ### Init ### ##
        ### ### ### ### ###
        self.init()


    ### ### ## ### ###
    ### OVERWRITES ###
    ### ### ## ### ###

    def init(self):
        self.configure_Other_Settings()
        self.graphicsView_Camera.init_Render_QTimer(
            connector_stream=self.camera_Instance.stream_Returner()
            if self.camera_Instance
            else None,
            delay=25
        )
        self.graphicsView_Stream.init_Render_QTimer(
            connector_stream=
            lambda: self.__thread_Dict["thread_Process"].get_Result() if self.__thread_Dict.get("thread_Process") is not None else None,
            delay=50
        )

        self.communication_Sender_Initialized = False

        self.ip_sender = "127.0.0.1"
        self.port_sender = 0000
        self.regex_sender = None
        self.parsing_format_sender = None

        self.internet_Parser_Format = None
        self.communication_Receiver_Initialized = False

        self.ip_receiver = "127.0.0.1"
        self.port_receiver = 0000
        self.regex_receiver = None
        self.parsing_format_receiver = None

        self.internet_Receiver_Node = None
        self.internet_Sender_Node = None

    def init_QTimers(self, *args, **kwargs):
        super(Ui_ISR, self).init_QTimers(*args, **kwargs)

    def configure_Button_Connections(self):
        # self.pushButton_Set_Exposure.clicked.connect(
        #     lambda: self.set_Camera_Exposure(
        #         self.spinBox_Exposure_Time.value()
        #     )
        # )
        # self.pushButton_Load_Image.clicked.connect(
        #     lambda: [
        #         self.stream_Switch(False),
        #         self.graphicsView_Renderer(
        #             self.graphicsView_Camera,
        #             self.load_Image_Action(
        #                 path=self.QFileDialog_Event(
        #                     "getOpenFileName",
        #                     [
        #                         "Open file",
        #                         "",
        #                         "Image files (*.png *.jpg *.jpeg)"
        #                     ]
        #                 )[0]
        #             )
        #         ),
        #     ]
        # )
        # self.pushButton_Crop_ROI_Drawer.clicked.connect(
        #     lambda: [
        #         self.graphicsView_Camera.clear_Scene_Foreground(),
        #         self.graphicsView_Camera.qtimer_Draw_ROI_Rectangle(
        #             trigger_exit=self.is_Quit_App,
        #             controller_start="mouseDoubleClick",
        #             controller_end="mouseDoubleClick",
        #             mouse_Event="mouseDoubleClick_position_scene",
        #             color="green",
        #             setAlphaF=0.13
        #         ),
        #         self.checkBox_is_Crop.setChecked(True)
        #     ]
        # )
        # self.pushButton_Crop_ROI_Clear.clicked.connect(
        #     lambda: [
        #         self.graphicsView_Camera.clear_Scene_Foreground(),
        #         self.graphicsView_Camera.clear_Last_Drawn_Item(),
        #         self.checkBox_is_Crop.setChecked(False)
        #     ]
        # )
        # self.pushButton_Save_Image.clicked.connect(
        #     lambda: self.save_Image_Action(
        #         # self.camera_Instance.stream_Returner(auto_pop=False),
        #         img=self.api_Get_Buffered_Image(),
        #         path=None,
        #         filename=[],
        #         format="png"
        #     )
        # )
        self.pushButton_Stream_Start.clicked.connect(
            lambda: [
                self.connect_to_Camera(
                    CAMERA_FLAGS.CV2,
                    # self.spinBox_Buffer_Size.value(),
                    0,
                    10,
                    # self.exposure_Time
                ),
                # self.camera_Instance.api_Set_Camera_Size(resolution=(1920, 1080)) if 
                # self.camera_Instance is not None else None
            ]
        )
        # self.pushButton_Remove_the_Camera.clicked.connect(
        #     self.camera_Remove
        # )
        # self.pushButton_Stream_Switch.clicked.connect(
        #     lambda: self.stream_Switch()
        # )
        
        # Internet Objects #
        self.pushButton_Sender_Start_Action.clicked.connect(
            lambda: [
                self.init_Sender_Internet_Object(
                    ip_sender=self.lineEdit_Sender_IP.text(),
                    port_sender=self.spinBox_Sender_Port.value(),
                    regex_sender=None,
                    parsing_format_sender=None,
                    internet_Parser_Format="{}",
                    delay=0.0000001
                )
            ]
        )
        self.pushButton_Sender_Stop_Action.clicked.connect(
            self.stop_Sender_Internet_Object
        )
        self.pushButton_Sender_Buffer_Clear.clicked.connect(
            lambda: self.internet_Sender_Dict[self.internet_Sender_Node].buffer_Clear() 
                if self.internet_Sender_Node is not None else None
        )
        
        self.pushButton_Receiver_Start_Action.clicked.connect(
            lambda: [
                self.init_Receiver_Internet_Object(
                    ip_receiver=self.lineEdit_Receiver_IP.text(),
                    port_receiver=self.spinBox_Receiver_Port.value(),
                    regex_receiver=None,
                    parsing_format_receiver=None,
                    internet_Parser_Format="{}",
                    delay=0.0000001
                )
            ]
        )
        self.pushButton_Receiver_Stop_Action.clicked.connect(
            self.stop_Receiver_Internet_Object
        )

        # Internet Object Actions #
        self.pushButton_Sender_Send_Action.clicked.connect(
            lambda: self.buffer_Sender_Set(
                self.textEdit_Sender_Input.toPlainText()
            )
        )
        self.pushButton_Create_Random_Data.clicked.connect(
            lambda: self.textEdit_Sender_Input.setText(
                "TimeStamp:{}|Data:{}".format(
                    time(),
                    random_Bulk_Data_Faster(
                        seed_number=time(),
                        start_range=self.spinBox_Random_Start_Range.value(),
                        end_range=self.spinBox_Random_End_Range.value() 
                        if self.spinBox_Random_Number.value() < self.spinBox_Random_End_Range.value()
                        else self.spinBox_Random_Number.value(),
                        number_of_data=self.spinBox_Random_Number.value()
                    )
                )
            )
        )
        self.pushButton_Receiver_Buffer_Clear.clicked.connect(
            lambda: self.internet_Receiver_Dict[self.internet_Receiver_Node].buffer_Clear() 
                if self.internet_Receiver_Node is not None else None
        )
        # self.pushButton_Send_Snapshot.clicked.connect(
        # )

    def configure_Other_Settings(self):
        self.checkBox_is_Live_Stream_Text.stateChanged.connect(
            self.stateChanged_is_Live_Stream_Text
        )
        self.checkBox_is_Live_Stream_Image.stateChanged.connect(
            self.stateChanged_is_Live_Stream_Image
        )

    def stateChanged_is_Live_Stream_Text(self):
        if self.checkBox_is_Live_Stream_Text.isChecked():
            self.QTimer_Dict["Internet Sender Live Stream Text"] = qtimer_Create_And_Run(
                self,
                connection=lambda: self.buffer_Sender_Set(
                    self.textEdit_Sender_Input.toPlainText()
                ),
                delay=50,
                is_needed_start=True,
                is_single_shot=False
            )
        else:
            if self.QTimer_Dict.get("Internet Sender Live Stream Text") is not None:
                self.QTimer_Dict["Internet Sender Live Stream Text"].stop()

    def stateChanged_is_Live_Stream_Image(self):
        if self.checkBox_is_Live_Stream_Text.isChecked():
            self.QTimer_Dict["Internet Sender Live Stream Image"] = qtimer_Create_And_Run(
                self,
                connection=lambda: self.buffer_Sender_Set(
                    self.textEdit_Sender_Input.toPlainText()
                ),
                delay=50,
                is_needed_start=True,
                is_single_shot=False
            )
        else:
            if self.QTimer_Dict.get("Internet Sender Live Stream Image") is not None:
                self.QTimer_Dict["Internet Sender Live Stream Image"].stop()
        
    def init_Sender_Internet_Object(
        self,
        ip_sender="127.0.0.1",
        port_sender=9999,
        regex_sender=None,
        parsing_format_sender=None,
        internet_Parser_Format="{}",
        delay=0.0000001
    ):
        self.communication_Sender_Initialized = True

        self.ip_sender = ip_sender
        self.port_sender = port_sender
        self.regex_sender = regex_sender
        self.parsing_format_sender = parsing_format_sender

        self.internet_Parser_Format = internet_Parser_Format

        self.internet_Sender_Node = self.init_Internet_Sender(
            ip_sender=self.ip_sender,
            port_sender=self.port_sender,
            logger_level=logging.CRITICAL,
            delay=delay,
            parsing_format=self.parsing_format_sender,
            regex=self.regex_sender,
            disable_Logger=False,
            max_buffer_limit=30
        )
        self.internet_Sender_Dict[self.internet_Sender_Node].buffer_Append(
            f"Sender '{self.internet_Sender_Node}' is Started!",
            lock_until_done=True,
            delay=0.00001
        )
        
        self.QTimer_Dict["Internet Sender Information"] = qtimer_Create_And_Run(
            self,
            connection=self.event_Sender_Information,
            delay=100,
            is_needed_start=True,
            is_single_shot=False
        )

    def stop_Sender_Internet_Object(self):
        if self.internet_Sender_Node is not None:
            self.internet_Sender_Dict[self.internet_Sender_Node].quit()
            self.QTimer_Dict["Internet Sender Information"].stop() \
                if self.QTimer_Dict["Internet Sender Information"].isActive() else None
            
            self.internet_Sender_Node = None

    def event_Sender_Information(self):
        if self.internet_Sender_Node is not None:
            information = self.internet_Sender_Dict[
                self.internet_Sender_Node
            ].get_Information()
            
            self.QTFunction_Caller_Event_Add([
                self.label_Sender_Is_Connection_Ok.setText,
                [f"{information['is_connection_ok']}"]
            ])
            
            self.QTFunction_Caller_Event_Add([
                self.label_Sender_Is_Set_Blocking.setText,
                [f"{information['set_blocking']}"]
            ])

            self.QTFunction_Caller_Event_Add([
                self.label_Sender_Timeout.setText,
                [f"{information['timeout']}"]
            ])

            self.QTFunction_Caller_Event_Add([
                self.label_Sender_Data_Last_Sended.setText,
                [f"{information['data_Last_Sended']}"]
            ])

            self.QTFunction_Caller_Event_Add([
                self.label_Sender_Buffer_Length.setText,
                [f"{information['buffer_Length']}"]
            ])

            # self.QTFunction_Caller_Event_Add([
            #     self.label_Sender_Buffer_Max_Length.setText,
            #     [f"{information['buffer_Max_Length']}"]
            # ])

            self.QTFunction_Caller_Event_Add([
                self.get_Sender_Buffer,
                []
            ])
        
    def get_Sender_Buffer(self):
        # bulk_buffer = self.internet_Sender_Dict[
        #     self.internet_Sender_Node
        # ].buffer_Get_Bulk(start=0, end=0)
        # item_list = list()
        # if bulk_buffer is not None:
        #     for buffer_item in bulk_buffer:
        #         self.qt_Priority()
        #         item_list.append(
        #             buffer_item
        #             # list_Widget_Item(
        #             #     title=buffer_item
        #             # )
        #         )
        # self.listWidget_Sender_Buffer.clear()
        # self.listWidget_Sender_Buffer.addItems(
        #     item_list
        # )
        # item_list = [buffer_item for buffer_item in bulk_buffer]
        if self.internet_Sender_Node is not None:
            bulk_buffer = self.internet_Sender_Dict[
                self.internet_Sender_Node
            ].buffer_Get_Bulk(start=0, end=0)
            self.listWidget_Sender_Buffer.clear()
            if bulk_buffer is not None:
                self.listWidget_Sender_Buffer.addItems(
                    bulk_buffer
                )

    def init_Receiver_Internet_Object(
        self,
        ip_receiver="127.0.0.1",
        port_receiver=9999,
        regex_receiver=None,
        parsing_format_receiver=None,
        internet_Parser_Format="{}",
        delay=0.0000001
    ):
        self.communication_Receiver_Initialized = True

        self.ip_receiver = ip_receiver
        self.port_receiver = port_receiver
        self.regex_receiver = regex_receiver
        self.parsing_format_receiver = parsing_format_receiver

        self.internet_Parser_Format = internet_Parser_Format

        self.internet_Receiver_Node = self.init_Internet_Receiver(
            ip_receiver=self.ip_receiver,
            port_receiver=self.port_receiver,
            logger_level=logging.CRITICAL,
            delay=delay,
            parsing_format=self.parsing_format_receiver,
            regex=self.regex_receiver,
            special_data_parsing=None,
            disable_Logger=False
        )
        self.internet_Receiver_Dict[self.internet_Receiver_Node].action_After_Receive = \
            lambda address, data: [
            # self.internet_Sender_Dict[self.internet_Sender_Node].buffer_Append(f"'{data}' Received!!!", False),
            # print("Data received:", data),
            self.buffer_Receiver_Set(
                f"|-[{address}]-> " + str(data) + "\n"
            ) if data is not None else None
        ]
        self.QTimer_Dict["Internet Receiver Information"] = qtimer_Create_And_Run(
            self,
            connection=self.event_Receiver_Information,
            delay=100,
            is_needed_start=True,
            is_single_shot=False
        )
        
    def stop_Receiver_Internet_Object(self):
        if self.internet_Receiver_Node is not None:
            self.internet_Receiver_Dict[self.internet_Receiver_Node].quit()
            self.QTimer_Dict["Internet Receiver Information"].stop() \
                if self.QTimer_Dict["Internet Receiver Information"].isActive() else None
            
            self.internet_Receiver_Node = None
        
    def event_Receiver_Information(self):
        if self.internet_Receiver_Node is not None:
            information = self.internet_Receiver_Dict[
                self.internet_Receiver_Node
            ].get_Information()

            self.QTFunction_Caller_Event_Add([
                self.label_Receiver_Is_Connection_Ok.setText,
                [f"{information['is_connection_ok']}"]
            ])

            self.QTFunction_Caller_Event_Add([
                self.label_Receiver_Is_Set_Blocking.setText,
                [f"{information['set_blocking']}"]
            ])

            self.QTFunction_Caller_Event_Add([
                self.label_Receiver_Timeout.setText,
                [f"{information['timeout']}"]
            ])

            self.QTFunction_Caller_Event_Add([
                self.label_Receiver_Address_Last.setText,
                [f"{information['address_Last']}"]
            ])

            self.QTFunction_Caller_Event_Add([
                self.label_Receiver_Data_Received.setText,
                [f"{information['data_Received']}"]
            ])
            
            # TODO: Need to see lively last received any info at connection
            # For Debug
            if information['data_Received']:
                print(
                    "information['data_Received']:",
                    information['data_Received']
                )

            self.QTFunction_Caller_Event_Add([
                self.label_Receiver_Data_Last_Received.setText,
                [f"{information['data_Last_Received']}"]
            ])

            self.QTFunction_Caller_Event_Add([
                self.label_Receiver_Buffer_Length.setText,
                [f"{information['buffer_Length']}"]
            ])

            self.QTFunction_Caller_Event_Add([
                self.get_Receiver_Buffer,
                []
            ])

    def get_Receiver_Buffer(self):
        # bulk_buffer = self.internet_Receiver_Dict[
        #     self.internet_Receiver_Node
        # ].buffer_Get_Bulk(start=0, end=0)
        # item_list = list()
        # if bulk_buffer is not None:
        #     for buffer_item in bulk_buffer:
        #         self.qt_Priority()
        #         item_list.append(
        #             buffer_item
        #             # list_Widget_Item(
        #             #     title=buffer_item
        #             # )
        #         )
        # self.listWidget_Receiver_Buffer.clear()
        # self.listWidget_Receiver_Buffer.addItems(
        #     item_list
        # )

        if self.internet_Receiver_Node is not None:
            bulk_buffer = self.internet_Receiver_Dict[
                self.internet_Receiver_Node
            ].buffer_Get_Bulk(start=0, end=0)
            self.listWidget_Receiver_Buffer.clear()
            if bulk_buffer is not None:
                self.listWidget_Receiver_Buffer.addItems(
                    bulk_buffer
                )

    def init_Internet_Objects(
        self,

        ip_sender="127.0.0.1",
        port_sender=9999,
        regex_sender=None,
        parsing_format_sender=None,

        ip_receiver="127.0.0.1",
        port_receiver=9999,
        regex_receiver=None,
        parsing_format_receiver=None,

        internet_Parser_Format="{}",

        delay=0.0000001
    ):
        self.init_Receiver_Internet_Object(
            ip_receiver=ip_receiver,
            port_receiver=port_receiver,
            regex_receiver=regex_receiver,
            parsing_format_receiver=parsing_format_receiver,
            internet_Parser_Format=internet_Parser_Format,
            delay=delay
        )
        self.init_Sender_Internet_Object(
            ip_sender=ip_sender,
            port_sender=port_sender,
            regex_sender=regex_sender,
            parsing_format_sender=parsing_format_sender,
            internet_Parser_Format=internet_Parser_Format,
            delay=delay
        )

    def buffer_Receiver_Set(self, data):
        # self.QTFunction_Caller_Event_Add([
        #     self.textEdit_Receiver_Output.setText,
        #     [self.textEdit_Receiver_Output.toPlainText() + f"{data}"]
        # ])
        self.QTFunction_Caller_Event_Add([
            self.textEdit_Receiver_Output.setText,
            [f"{data}"]
        ])
        

    def buffer_Sender_Set(self, data, lock_until_done=False):
        if self.internet_Sender_Dict.get(self.internet_Sender_Node) is not None and data != "":
            self.internet_Sender_Dict[self.internet_Sender_Node].buffer_Append(
                data,
                lock_until_done=lock_until_done,
                delay=0.00001
            )

    def closeEvent(self, *args, **kwargs):
        super(Ui_ISR, self).closeEvent(*args, **kwargs)

        self.camera_Remove()

if __name__ == "__main__":
    # title, Class_UI, run=True, UI_File_Path= "test.ui", qss_File_Path = ""
    # stdo(1, "Running {}...".format(__name__))
    app, ui = init_and_run_UI(
        title="ISR Test",
        Class_UI=Ui_ISR,
        UI_File_Path="ISR_UI.ui",
        run=True, 
        show_UI=True, 
        is_Maximized=False
    )
