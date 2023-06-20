import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import face_recognition
import os.path
import subprocess
import datetime
class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'Login', '#575cff', self.login)
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register new user', 'grey', self.register_new_user, fg= 'black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place (x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.facedatabase_dir = './facedatabase'
        if not os.path.exists(self.facedatabase_dir):
            os.mkdir(self.facedatabase_dir)
        self.attendancesheet_path = './attendancesheet.txt'
    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label
        self.process_webcam()
    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)
    def login(self):
        unkown_img_path = './.tmp.jpg'
        cv2.imwrite(unkown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition', self.facedatabase_dir, unkown_img_path]))
        name = output.split(',')[1][:-5]
        if name in ['unknown_person']:
            util.msg_box('Failure!', 'Unknown student, please try again or register new user')
        elif name in ['no_persons_found']:
            util.msg_box('Failure!', 'No student found, please try again or register new user')
        else:
            util.msg_box('Welcome to class','Welcome, {}'.format(name))
            with open(self.attendancesheet_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
        os.remove(unkown_img_path)
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', '#13ad51', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', '#ff2155', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)
        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Student Name:')
        self.text_label_register_new_user.place(x=750, y=70)
    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()
    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
    def start(self):
        self.main_window.mainloop()
    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        cv2.imwrite(os.path.join(self.facedatabase_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        util.msg_box('Success!', 'The Student Was Registered Successfully')
        self.register_new_user_window.destroy()

if __name__ == '__main__':
    app = App()
    app.start()