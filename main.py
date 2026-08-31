import os
import random
import time
import tkinter.filedialog
from tkinter import *
from tkinter import messagebox
from imageai.Detection import ObjectDetection
from imageai.Detection.Custom import CustomObjectDetection
import cv2
from random import randint
import pylabel

class PyPlant:
    #Инициализация.
    #1: Главное окно с предложением выбрать операцию
    def __init__(self, main):
        self.execution_path = os.getcwd()
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath('yolov3.pt')
        self.detector.loadModel()

        self.button_camera = Button(main, width=20, font=5,text="В реальном времени")
        self.button_ask_directory_button = Button (main, width=20,font=5, text="Выбрать фото")
        self.button_exit = Button(main, width=20,font=5, text="Выход")
        self.label_object = Label(font = "Arial", width=10)

        self.button_camera.pack()
        self.button_ask_directory_button.pack()
        self.button_exit.pack()

        self.button_camera.bind("<Button-1>", self.On_Camera)
        self.button_ask_directory_button.bind("<Button-1>", self.Choose_file)
        self.button_exit.bind("<Button-1>",exit)
    #2: Включение камеры
    def On_Camera(self,event):
        camera = cv2.VideoCapture(1)
        finish_cap = 0
        array_detection = []
        while camera.isOpened():
            ret, frame = camera.read()
            start_cap = time.time()
            if start_cap - finish_cap > 2:
                finish_cap = time.time()
                cv2.imshow('Rec', frame)
                _, array_detection = self.detector.detectObjectsFromImage(input_image=frame, output_type= "array",output_image_path = "result/Ready.jpg")
                print(array_detection)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            for obj in array_detection:
                coord = obj['box_points']
                cv2.rectangle(frame,(coord[0], coord[1], coord[2], coord[3]), (0,0,255))
                cv2.putText(frame, obj['name'], (coord[0], coord[1] - 6),cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255))
        camera.release()
        cv2.destroyAllWindows()
    #3: Выбор файла
    def Choose_file(self,event):
        PhotoIsSelected = tkinter.filedialog.askopenfilename(filetypes=[("JPG файлы", "*.jpg* *.jpeg"), ("PNG файлы", "*.png"), ("BMP файлы", "*.bmp"), ("Все", "*.*")])
        File_name_change = "abcdefghijklmnopqrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        File_name_change = list(File_name_change)
        File_Name_Result_Num = randint(10, 61)
        end_word = []
        for i in range(File_Name_Result_Num):
            File_Name_Letter = File_name_change[randint(0, len(File_name_change)-1)]
            end_word.append(File_Name_Letter)
        end_word = "".join(end_word)
        self.detector.detectObjectsFromImage(input_image=str(PhotoIsSelected), output_image_path="result/"+str(end_word)+".jpeg")
        img = cv2.imread(PhotoIsSelected)
        cv2.imshow("Res", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if PhotoIsSelected == '':
            pass
        # elif (".jpeg" or ".png" or ".jpg" or ".bmp" or ".gif") in PhotoIsSelected:
            # tkinter.messagebox.showerror(title="Ошибка", message="Запущен неверный файл. Повторите попытку.")
        answer = tkinter.messagebox.askquestion(title="Сохранение", message="Хотите ли Вы сохранить текущее изображение?")
        if answer == 'no':
            os.remove("result/"+str(end_word)+".jpeg")

#2: Вопрос с просьбой выбрать файл
root=Tk()
root.title("PyPlantDoctor")
root.minsize(300,150)
root.iconbitmap('photo/apple.ico')
start = PyPlant(root)

root.mainloop()