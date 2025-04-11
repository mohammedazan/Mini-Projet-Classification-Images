import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
from model import ImageClassifier
from sklearn.exceptions import NotFittedError

class PetClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pet Classifier")
        self.root.geometry("1000x800")
        
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
        self.tab_control = ttk.Notebook(root)
        
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
        right_frame.pack(side='left', fill='both', expand=True, padx=20)
        
        # Cat section in right frame
        tk.Label(right_frame, text="Sélectionner 10 images de chats", font=('Arial', 11)).pack(pady=10)
        cat_grid = tk.Frame(right_frame)
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
        
        tk.Button(right_frame, text="Add Cat Image", 
                 command=lambda: self.add_image("cat")).pack(pady=5)
    
        # Dog section in right frame
        tk.Label(right_frame, text="Sélectionner 10 images de chien", font=('Arial', 11)).pack(pady=10)
        dog_grid = tk.Frame(right_frame)
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
        
        tk.Button(right_frame, text="Add Dog Image", 
                 command=lambda: self.add_image("dog")).pack(pady=5)
    
        # Train button
        train_button = tk.Button(right_frame, text="Entrainer", 
                               command=self.train_model,
                               width=20,
                               font=('Arial', 10, 'bold'))
        train_button.pack(pady=20)

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
            tk.messagebox.showwarning(
                "Warning", 
                "Please select 10 images for each category!")
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
        image_frame = tk.Frame(left_frame, width=200, height=200, relief='solid', borderwidth=1)
        image_frame.pack(pady=10)
        image_frame.pack_propagate(False)
        
        # Default image icon or text
        tk.Label(image_frame, text="Chat ou chien ou autre", wraplength=180).pack(expand=True)
        
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
        tk.Label(right_frame, text="puis cliquer sur prédiction", font=('Arial', 10)).pack(pady=5)
        
        # Prediction button
        predict_button = tk.Button(right_frame, text="Prédiction",
                                 command=self.make_prediction,
                                 width=15)
        predict_button.pack(pady=10)
        
        # Result frame with yellow background
        self.result_frame = tk.Frame(right_frame, bg='#FFF3D4')  # Light yellow
        self.result_frame.pack(pady=20, fill='x')
        
        # Result label
        self.result_label = tk.Label(self.result_frame, text="", 
                                    font=('Arial', 11, 'bold'),
                                    bg='#FFF3D4')  # Same light yellow
        self.result_label.pack(pady=10)

    def select_test_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            # Store the path for prediction
            self.test_image_path = file_path
            # Display the selected image
            img = Image.open(file_path)
            img = img.resize((280, 280))  # Resize for display
            photo = ImageTk.PhotoImage(img)
            self.selected_image_label.configure(image=photo)
            self.selected_image_label.image = photo

    def make_prediction(self):
        if not hasattr(self, 'test_image_path'):
            tk.messagebox.showwarning("Warning", "Please select an image first!")
            return
            
        try:
            prediction, confidence = self.classifier.predict(self.test_image_path)
            result_text = f"{int(confidence)}% {prediction}"
            self.result_label.config(text=result_text)
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
        # Load cat images
        for img_name in os.listdir(self.cat_db_path):
            img_path = os.path.join(self.cat_db_path, img_name)
            self.add_dataset_image(cat_container, img_path)
        
        # Load dog images
        for img_name in os.listdir(self.dog_db_path):
            img_path = os.path.join(self.dog_db_path, img_name)
            self.add_dataset_image(dog_container, img_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PetClassifierApp(root)
    root.mainloop()