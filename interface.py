import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import os

class ClassificationUI:
    """
    Class that handles all TKinter GUI interface and camera operations
    Calls the OfficeObjectsClassifier to get predictions

    Args:
        root: Tkinter root window
    """

    def __init__(self, root):
        self.root = root
        self.title = "TicTacToe"
        self.base_color = "#f0f0f0"
        self.fps = 12  # target frames per second for webcam

        # import classifier class
        self.classifier = None

        # UI state variables
        self.current_image = "" # placeholder for displayed image
        self.base_empty_image = "images/blank_canvas.png" # image to be displayed when no image is loaded
        self.current_image_present = False # boolean to check if a real image is loaded
        self.is_camera_active = False

        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise RuntimeError("Cannot access camera. Please check your webcam.")

        # call functions to complete UI
        self.window_settings()
        self.add_buttons()
        # display blank image at start
        self.show_image(self.base_empty_image)


    def window_settings(self):
        """function to create dimensions of window and setup frames of images"""
        self.root.title(self.title)

        # define custom width+height for tkinter window
        tk_width = 600
        tk_height = 700

        # get monitor screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # calculate the center point and offset by tkinter window size
        offset_x = int(screen_width/2 - tk_width / 2)
        offset_y = int(screen_height/2 - tk_height / 2)
        # opening window in center of screen
        self.root.geometry(f'{tk_width}x{tk_height}+{offset_x}+{offset_y}')

        # # use this if dual monitors, it will appear on screen but not center
        # self.root.geometry(f'{tk_width}x{tk_height}')

        self.root.configure(bg=self.base_color)

        # title label
        tk.Label(
            self.root, text=self.title,
            font=("Arial", 15, "bold"), bg=self.base_color,
        ).pack(pady=10)

        # add a frame to display the image uploaded
        self.image_frame = tk.Frame(
            self.root, bg=self.base_color,
            width=tk_width, height=(tk_height-150) # image takes 150px less than window
        )
        self.image_frame.pack_propagate(False) # stop frame from resizing
        self.image_frame.pack(pady=(5, 5))

        # Label to contain actual image
        self.image_label = tk.Label(self.image_frame, bg=self.base_color)
        self.image_label.pack(expand=True)

        # label to show prediction
        self.active_prediction_label = tk.Label(
            self.root, text="",
            font=("Arial", 12), bg=self.base_color,
        )
        self.active_prediction_label.pack(pady=5)


    def add_buttons(self):
        """Add upload, camera and exit buttons"""
        # separate frame to house the buttons to place them in grids
        button_frame = tk.Frame(self.root, bg=self.base_color)
        button_frame.pack(pady=5, padx=5)
        # button for image upload from computer
        style = ttk.Style()
        style.theme_use("clam")  # allows color customization on Windows
        style.configure(
            "Green.TButton",
            background="#46C263", foreground="white",
            font=("Arial", 12), padding=8, borderwidth=0,
        )
        style.map(
            "Green.TButton",
            background=[("active", "#3AAA56"), ("disabled", "#5B9B6B")],
            foreground=[("disabled", "#E0E0E0")],
        )
        style.configure(
            "Red.TButton",
            background="#F32F21", foreground="white",
            font=("Arial", 12), padding=8, borderwidth=0,
        )
        style.map(
            "Red.TButton",
            background=[("active", "#D12218"), ("disabled", "#F9A9A4")],
            foreground=[("disabled", "#E0E0E0")],
        )

        self.predict_button = ttk.Button(
            button_frame, text="Predict Class", command=self.predict_image_class,
            style="Green.TButton",
        )

        self.camera_button = ttk.Button(
            button_frame, text="Start Game", command=self.toggle_camera,
            style="Red.TButton",
        )

        exit_button = ttk.Button(
            button_frame, text='Exit', command=self.close,
        )

        self.predict_button.grid(row=0, column=1, padx=10, ipadx=10, ipady=5)
        self.camera_button.grid(row=0, column=2, padx=10, ipadx=10, ipady=5)
        exit_button.grid(row=0, column=3, padx=10, ipadx=10, ipady=5)

    def show_image(self, image_path):
        """
        method to display uploaded or captured image in Tkinter window
        Args:
            image_path (str): path to the image file
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Background image not found: {image_path}, using blank background")

            image = Image.open(image_path)
            # resize image TODO
            image.thumbnail((600, 400))
            # need to convert to a format compatible with Tkinter
            photo = ImageTk.PhotoImage(image)
            # update label to display the image
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        except Exception as e:
            print("Error displaying image: ", e)

    def toggle_camera(self):
        """
        Turn camera on or off
        """
        if self.is_camera_active:
            print("Stopping camera...")
            self.stop_camera()
        else:
            print("Starting camera...")
            self.start_camera()


    def stop_camera(self):
        """Stop webcam and release resources."""
        # check if camera has been initialized
        if hasattr(self, 'camera') and self.camera.isOpened():
            self.camera.release()

        self.is_camera_active = False
        # remove image from UI
        self.current_image = ""
        self.current_image_present = False
        self.show_image(self.base_empty_image)
        self.active_prediction_label['text'] = ""
        print("Camera stopped.")
        # re-enable button
        self.camera_button.config(text="Start Game")
        self.predict_button.config(state=tk.NORMAL)


    def start_camera(self):
        """function to predict class from webcam live"""
        if self.is_camera_active:
            return  # Camera is already running

        try:
            # Initialize webcam (0 is default camera)
            self.camera = cv2.VideoCapture(0)
            # check if camera is available
            if not self.camera.isOpened():
                raise RuntimeError("Cannot access camera.")

            self.is_camera_active = True
            # disable button to prevent multiple clicks
            self.camera_button.config(text="Stop Camera")
            self.predict_button.config(state=tk.DISABLED)

            self.update_camera_frame()
        except Exception as e:
            # display error in popup window and terminal
            messagebox.showerror("Camera Error", f"Camera Error:\n{e}")
            print("Camera Error: ", e)


    def update_camera_frame(self):
        """Update the Tkinter image label with live camera feed."""
        if not self.is_camera_active:
            return  # Stop updating if camera is not active

        try:
            ret, frame = self.camera.read()
            if not ret:
                raise RuntimeError("Failed to read from camera.")

            # Convert frame to RGB for Tkinter display and image prediction
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)

            # resize for display
            img.thumbnail((600, 450))
            photo = ImageTk.PhotoImage(image=img)
            # update Tkinter UI
            self.image_label.configure(image=photo)
            self.image_label.image = photo

            # update camera depending on fps chosen
            delay = int(1000/self.fps) # calculate the number of ms per detection
            self.root.after(delay, self.update_camera_frame)
        except Exception as e:
            print(f"Camera update error: {e}")
            self.stop_camera()


    def predict_image_class(self):
        """Predict class for the current image"""
        if not self.current_image_present:
            messagebox.showerror("Error", "Please load an image first")
            print("Choose an image first")
            return

        try:
            image = Image.open(self.current_image).convert('RGB')
            # call classifier method to get prediction
            prediction_label = self.classifier.classify_image(image)
            # update UI
            print("Prediction:", prediction_label)
            self.active_prediction_label['text'] = prediction_label
        except Exception as e:
            # Show error to the user and print for debugging
            messagebox.showerror("Error", f"Prediction failed:\n{e}")
            print("Error predicting image: ", e)


    def close(self):
        """Shutdown applicationg cleanly"""
        try:
            if self.is_camera_active:
                self.stop_camera()
        finally:
            self.root.quit()
            self.root.destroy()
            print("Goodbye")

def main():
    """Entry point"""
    root = tk.Tk()
    app = ClassificationUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()