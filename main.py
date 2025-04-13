import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from model import ImageClassifier
from sklearn.exceptions import NotFittedError

class PetClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pet Classifier")
        self.root.geometry("1000x800")
        
        # Add custom theme colors
        self.colors = {
            'primary': '#2C3E50',      # Dark blue
            'secondary': '#3498DB',    # Light blue
            'accent': '#E74C3C',       # Red
            'background': '#ECF0F1',   # Light gray
            'text': '#2C3E50',         # Dark blue
            'success': '#2ECC71'       # Green
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['background'])
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base
        
        # Configure notebook style
        style.configure('Custom.TNotebook', 
            background=self.colors['background'],
            padding=5
        )
        style.configure('Custom.TNotebook.Tab',
            background=self.colors['primary'],
            foreground='white',
            padding=[20, 10],
            font=('Arial', 10, 'bold')
        )
        style.map('Custom.TNotebook.Tab',
            background=[('selected', self.colors['secondary'])],
            foreground=[('selected', 'white')]
        )
        
        # Initialize lists first
        self.cat_images = []
        self.dog_images = []
        self.cat_labels = []
        self.dog_labels = []
        
        # Add dataset paths
        self.cat_db_path = "c:/Users/Lenovo/OneDrive/Desktop/Mini-Project/DB/CAT"
        self.dog_db_path = "c:/Users/Lenovo/OneDrive/Desktop/Mini-Project/DB/DOG"
        
        # Initialize the ML model
        self.classifier = ImageClassifier()
        
        # Create main tabs
        # Style configuration for tabs
        style = ttk.Style()
        style.configure('Custom.TNotebook.Tab', 
            padding=[15, 5],
            font=('Arial', 10, 'bold'),
            background='#4a90e2',
            foreground='white'
        )
        
        self.tab_control = ttk.Notebook(root, style='Custom.TNotebook')
        
        # Training tab
        self.train_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.train_tab, text='Training')
        
        # Testing tab
        self.test_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.test_tab, text='Testing')
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Setup tabs
        self.setup_training_tab()
        self.setup_testing_tab()

    def setup_training_tab(self):
        # Create main container with left and right frames
        main_container = tk.Frame(self.train_tab)
        main_container.pack(fill='both', expand=True)
        
        # Create left frame for dataset (30% of width)
        left_frame = tk.Frame(main_container, relief='solid', borderwidth=1, width=300)
        left_frame.pack(side='left', fill='y', padx=10, pady=10)
        left_frame.pack_propagate(False)
        
        # Dataset title centered with better styling
        title_frame = tk.Frame(left_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', pady=5)
        tk.Label(title_frame, text="Dataset", font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=5)
        
        # Create container for cat and dog columns
        columns_container = tk.Frame(left_frame)
        columns_container.pack(fill='both', expand=True, padx=5)
        
        # Create columns with equal width
        cat_column = tk.Frame(columns_container, width=140)
        cat_column.pack(side='left', fill='both', expand=True, padx=5)
        cat_column.pack_propagate(False)
        
        dog_column = tk.Frame(columns_container, width=140)
        dog_column.pack(side='left', fill='both', expand=True, padx=5)
        dog_column.pack_propagate(False)
        
        # Labels for categories with better styling
        tk.Label(cat_column, text="Chats", font=('Arial', 10, 'bold'), fg='#404040').pack(pady=5)
        tk.Label(dog_column, text="Chiens", font=('Arial', 10, 'bold'), fg='#404040').pack(pady=5)
        
        # Create scrollable frames with larger width
        cat_canvas = tk.Canvas(cat_column, width=130)
        dog_canvas = tk.Canvas(dog_column, width=130)
        
        cat_scrollbar = tk.Scrollbar(cat_column, orient="vertical", command=cat_canvas.yview)
        dog_scrollbar = tk.Scrollbar(dog_column, orient="vertical", command=dog_canvas.yview)
        
        cat_scrollable = tk.Frame(cat_canvas)
        dog_scrollable = tk.Frame(dog_canvas)
        
        # Configure scrolling
        for scrollable, canvas in [(cat_scrollable, cat_canvas), (dog_scrollable, dog_canvas)]:
            scrollable.bind(
                "<Configure>",
                lambda e, c=canvas: c.configure(scrollregion=c.bbox("all"))
            )
        
        cat_canvas.create_window((0, 0), window=cat_scrollable, anchor="nw")
        dog_canvas.create_window((0, 0), window=dog_scrollable, anchor="nw")
        
        cat_canvas.configure(yscrollcommand=cat_scrollbar.set)
        dog_canvas.configure(yscrollcommand=dog_scrollbar.set)
        
        # Pack canvases and scrollbars
        for canvas, scrollbar in [(cat_canvas, cat_scrollbar), (dog_canvas, dog_scrollbar)]:
            canvas.pack(side="left", fill="both", expand=True, padx=2)
            scrollbar.pack(side="right", fill="y")
        
        # Load dataset images
        self.load_dataset_images(cat_scrollable, dog_scrollable)
        
        # Create right frame (70% of width)
        right_frame = tk.Frame(main_container)
        right_frame.pack(side='left', fill='both', expand=True)  # Removed padx=20
        
        # Content container for images selection
        content_frame = tk.Frame(right_frame)
        content_frame.pack(side='left', fill='both', expand=True)
        
        # Cat section in content frame
        tk.Label(content_frame, text="Sélectionner 10 images de chats", font=('Arial', 11)).pack(pady=10)
        cat_grid = tk.Frame(content_frame)
        cat_grid.pack(pady=10)
        
        # Create 5x2 grid for cat images
        for i in range(2):
            for j in range(5):
                frame = tk.Frame(cat_grid, width=120, height=120, relief='solid', borderwidth=1)
                frame.grid(row=i, column=j, padx=5, pady=5)
                frame.grid_propagate(False)
                label = tk.Label(frame)
                label.place(relx=0.5, rely=0.5, anchor='center')
                self.cat_labels.append(label)
        
        # Define button style
        button_style = {
            'bg': '#4a90e2',
            'fg': 'white',
            'font': ('Arial', 10),
            'relief': 'flat',
            'padx': 15,
            'pady': 5,
            'cursor': 'hand2'
        }
        
        # Add Cat Image button
        tk.Button(content_frame, 
                 text="Add Cat Image",
                 command=lambda: self.add_image("cat"),
                 **button_style).pack(pady=5)
        
        # Dog section in content frame
        tk.Label(content_frame, text="Sélectionner 10 images de chien", font=('Arial', 11)).pack(pady=10)
        dog_grid = tk.Frame(content_frame)
        dog_grid.pack(pady=10)
        
        # Create 5x2 grid for dog images
        for i in range(2):
            for j in range(5):
                frame = tk.Frame(dog_grid, width=120, height=120, relief='solid', borderwidth=1)
                frame.grid(row=i, column=j, padx=5, pady=5)
                frame.grid_propagate(False)
                label = tk.Label(frame)
                label.place(relx=0.5, rely=0.5, anchor='center')
                self.dog_labels.append(label)
        
        # Add Dog Image button with consistent style
        tk.Button(content_frame, 
                 text="Add Dog Image",
                 command=lambda: self.add_image("dog"),
                 **button_style).pack(pady=5)
        
        # Train button container (right side)
        train_container = tk.Frame(right_frame)
        train_container.pack(side='right', padx=20, fill='y')
        
        # Spacer to push button to bottom
        tk.Frame(train_container).pack(expand=True)
        
        # Train button with custom style
        train_button = tk.Button(
            train_container,
            text="Entrainer",
            command=self.train_model,
            bg='#2ECC71',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='raised',
            width=10,
            height=1,
            cursor='hand2'
        )
        train_button.pack(side='bottom', pady=20)

    def add_dataset_image(self, container, img_path):
        try:
            img = Image.open(img_path)
            img = img.resize((120, 120))  # Larger images in dataset
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(container, image=photo, relief='solid', borderwidth=1)
            label.image = photo
            label.pack(pady=5)
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")

    def add_image(self, category):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((120, 120))  # Matching size for selected images
            photo = ImageTk.PhotoImage(img)
            
            if category == "cat":
                if len(self.cat_images) < 10:
                    self.cat_images.append(file_path)
                    self.cat_labels[len(self.cat_images)-1].configure(image=photo)
                    self.cat_labels[len(self.cat_images)-1].image = photo
            else:
                if len(self.dog_images) < 10:
                    self.dog_images.append(file_path)
                    self.dog_labels[len(self.dog_images)-1].configure(image=photo)
                    self.dog_labels[len(self.dog_images)-1].image = photo

    def train_model(self):
        if len(self.cat_images) < 10 or len(self.dog_images) < 10:
            response = tk.messagebox.askokcancel(
                "Warning", 
                "Vous devez saisir des images\nVoulez-vous continuer sans entraînement ?",
                icon='warning'
            )
            if response:  # If user clicks OK
                self.tab_control.select(self.test_tab)
            return
        
        self.classifier.train(self.cat_images, self.dog_images)
        tk.messagebox.showinfo("Success", "Model trained successfully!")
        
        # Switch to testing tab
        self.tab_control.select(self.test_tab)

    def setup_testing_tab(self):
        # Create main container
        main_container = tk.Frame(self.test_tab)
        main_container.pack(fill='both', expand=True)
        
        # Left sidebar (30% width)
        left_frame = tk.Frame(main_container, relief='solid', borderwidth=1, width=300)
        left_frame.pack(side='left', fill='y', padx=10, pady=10)
        left_frame.pack_propagate(False)
        
        # New photo section
        tk.Label(left_frame, text="Nouvelle photo", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Placeholder for image
        self.left_image_frame = tk.Frame(left_frame, width=200, height=200, relief='solid', borderwidth=1)
        self.left_image_frame.pack(pady=10)
        self.left_image_frame.pack_propagate(False)
        
        # Label for selected image in left frame
        self.left_image_label = tk.Label(self.left_image_frame)
        self.left_image_label.pack(expand=True)
        
        # Text below the image frame
        tk.Label(left_frame, text="Chat ou chien ou autre", wraplength=180).pack(pady=5)
        
        # Browse button
        browse_button = tk.Button(left_frame, text="Parcourir", 
                                command=self.select_test_image,
                                width=15)
        browse_button.pack(pady=10)
        
        # Main content area (70% width)
        right_frame = tk.Frame(main_container)
        right_frame.pack(side='left', fill='both', expand=True, padx=20)
        
        # Selected photo section
        tk.Label(right_frame, text="Photo sélectionnée", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Frame for selected image
        self.selected_image_frame = tk.Frame(right_frame, width=300, height=300, relief='solid', borderwidth=1)
        self.selected_image_frame.pack(pady=10)
        self.selected_image_frame.pack_propagate(False)
        
        # Label for selected image
        self.selected_image_label = tk.Label(self.selected_image_frame)
        self.selected_image_label.pack(expand=True)
        
        # Instruction text
        #tk.Label(right_frame, text="puis cliquer sur prédiction", font=('Arial', 10)).pack(pady=5)
        
        # Prediction button
        predict_button = tk.Button(right_frame, text="Prédiction",
                                 command=self.make_prediction,
                                 width=15)
        predict_button.pack(pady=10)
        
        # Result frame with gradient-like effect
        self.result_frame = tk.Frame(right_frame, 
            bg='#FFE5B4',  # Peach color
            relief='raised',
            padx=20,
            pady=10,
            highlightthickness=1,
            highlightbackground='#FFB347'  # Darker peach
        )
        
        # Styled result label
        self.result_label = tk.Label(
            self.result_frame,
            text="", 
            font=('Arial', 12, 'bold'),
            bg='#FFE5B4',
            fg='#333333'
        )
        self.result_label.pack(pady=10)

    def select_test_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            # Store the path for prediction
            self.test_image_path = file_path
            # Display the selected image in both frames
            img = Image.open(file_path)
            
            # Resize for left frame
            left_img = img.resize((180, 180))
            left_photo = ImageTk.PhotoImage(left_img)
            self.left_image_label.configure(image=left_photo)
            self.left_image_label.image = left_photo
            
            # Resize for right frame
            right_img = img.resize((280, 280))
            right_photo = ImageTk.PhotoImage(right_img)
            self.selected_image_label.configure(image=right_photo)
            self.selected_image_label.image = right_photo

    def make_prediction(self):
        if not hasattr(self, 'test_image_path'):
            tk.messagebox.showwarning("Warning", "Please select an image first!")
            return
            
        try:
            prediction, confidence = self.classifier.predict(self.test_image_path)
            # Use the update_prediction_result method instead of direct configuration
            self.update_prediction_result(prediction, confidence)
            # Make sure the result frame is packed
            self.result_frame.pack(pady=20, fill='x')
        except NotFittedError:
            tk.messagebox.showwarning(
                "Warning", 
                "Please train the model first before making predictions!")
            # Switch back to training tab 
            self.tab_control.select(self.train_tab)
  
    def add_image(self, category):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            # Open and resize image
            img = Image.open(file_path)
            img = img.resize((90, 90))  # Resize to fit in the frame
            photo = ImageTk.PhotoImage(img)
            
            if category == "cat":
                if len(self.cat_images) < 10:
                    self.cat_images.append(file_path)
                    self.cat_labels[len(self.cat_images)-1].configure(image=photo)
                    self.cat_labels[len(self.cat_images)-1].image = photo
            else:
                if len(self.dog_images) < 10:
                    self.dog_images.append(file_path)
                    self.dog_labels[len(self.dog_images)-1].configure(image=photo)
                    self.dog_labels[len(self.dog_images)-1].image = photo

    def load_dataset_images(self, cat_container, dog_container):
        # Lists to store dataset image paths
        self.dataset_cat_images = []
        self.dataset_dog_images = []
        
        # Load cat images
        for img_name in os.listdir(self.cat_db_path):
            img_path = os.path.join(self.cat_db_path, img_name)
            self.dataset_cat_images.append(img_path)
            self.add_dataset_image(cat_container, img_path)
        
        # Load dog images
        for img_name in os.listdir(self.dog_db_path):
            img_path = os.path.join(self.dog_db_path, img_name)
            self.dataset_dog_images.append(img_path)
            self.add_dataset_image(dog_container, img_path)
            
        # Train the model with dataset images
        if self.dataset_cat_images and self.dataset_dog_images:
            self.classifier.train(self.dataset_cat_images, self.dataset_dog_images)

    def update_prediction_result(self, prediction, confidence):
        # Create gradient effect
        result_bg = self.colors['success'] if confidence > 70 else self.colors['accent']
        
        self.result_frame.configure(
            bg=result_bg,
            relief='raised'
        )
        
        # Animate confidence display
        def animate_confidence(current=0):
            if current <= confidence:
                self.result_label.configure(
                    text=f"{int(current)}% {prediction}",
                    bg=result_bg,
                    fg='white',
                    font=('Arial', 14, 'bold')
                )
                self.root.after(20, lambda: animate_confidence(current + 2))
        
        animate_confidence()

if __name__ == "__main__":
    root = tk.Tk()
    app = PetClassifierApp(root)
    root.mainloop()