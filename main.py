import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from model import ImageClassifier
from sklearn.exceptions import NotFittedError

class PetClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Classificateur d'Animaux")
        self.root.geometry("1000x800")
        
        # Theme colors
        self.colors = {
            'background': '#F5F7FA',
            'primary': '#4CAF50',
            'secondary': '#2196F3',
            'text_dark': '#333333',
            'text_light': '#555555',
            'card_bg': '#FFFFFF',
            'border': '#E0E0E0'
        }
        
        self.root.configure(bg=self.colors['background'])
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TNotebook', background=self.colors['background'], padding=5)
        style.configure('Custom.TNotebook.Tab',
            background=self.colors['secondary'],
            foreground='white',
            padding=[20, 10],
            font=('Arial', 10, 'bold'),
            borderwidth=0
        )
        style.map('Custom.TNotebook.Tab',
            background=[('selected', self.colors['secondary'])],
            foreground=[('selected', 'white')]
        )
        
        # Initialize variables
        self.cat_images = []
        self.dog_images = []
        self.cat_labels = []
        self.dog_labels = []
        self.cat_db_path = "c:/Users/Lenovo/OneDrive/Desktop/Mini-Project/DB/CAT"
        self.dog_db_path = "c:/Users/Lenovo/OneDrive/Desktop/Mini-Project/DB/DOG"
        self.classifier = ImageClassifier()
        
        # Create tabs
        self.tab_control = ttk.Notebook(root, style='Custom.TNotebook')
        self.train_tab = ttk.Frame(self.tab_control)
        self.test_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.train_tab, text='Entraînement')
        self.tab_control.pack(expand=1, fill="both")
        
        self.setup_training_tab()
        self.setup_testing_tab()

    def create_scrollable_frame(self, parent, width, height):
        canvas = tk.Canvas(parent, width=width, height=height, bg=self.colors['card_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card_bg'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event, canvas):
            canvas.yview_scroll(int(-1 * (event.delta/60)), "units")
        
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, canvas))
        
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_mousewheel)
        canvas.bind('<Leave>', _unbind_mousewheel)
        
        return canvas, scrollbar, scrollable_frame

    def create_image_grid(self, parent, rows=2, cols=5, width=120, height=120):
        grid = tk.Frame(parent)
        grid.pack(pady=10)
        labels = []
        
        for i in range(rows):
            for j in range(cols):
                frame = tk.Frame(
                    grid, 
                    width=width, 
                    height=height, 
                    bg=self.colors['card_bg'],
                    highlightbackground=self.colors['border'],
                    highlightthickness=1,
                    bd=0
                )
                frame.grid(row=i, column=j, padx=5, pady=5)
                frame.grid_propagate(False)
                label = tk.Label(frame, bg=self.colors['card_bg'])
                label.place(relx=0.5, rely=0.5, anchor='center')
                labels.append(label)
        
        return labels

    def setup_training_tab(self):
        main_container = tk.Frame(self.train_tab, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True)
        
        # Left frame
        left_frame = self._create_styled_frame(main_container, width=300)
        left_frame.pack(side='left', fill='y', padx=10, pady=10)
        left_frame.pack_propagate(False)
        
        # Dataset title
        title_frame = tk.Frame(left_frame, bg=self.colors['card_bg'])
        title_frame.pack(fill='x', pady=5)
        tk.Label(title_frame, text="Jeu de Données", font=('Arial', 12, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['text_dark']).pack(pady=5)
        
        # Columns container
        columns_container = tk.Frame(left_frame, bg=self.colors['card_bg'])
        columns_container.pack(fill='both', expand=True, padx=5)
        
        # Create columns
        cat_column = tk.Frame(columns_container, bg=self.colors['card_bg'], width=140)
        dog_column = tk.Frame(columns_container, bg=self.colors['card_bg'], width=140)
        cat_column.pack(side='left', fill='both', expand=True, padx=5)
        dog_column.pack(side='left', fill='both', expand=True, padx=5)
        cat_column.pack_propagate(False)
        dog_column.pack_propagate(False)
        
        # Category labels
        for col, text in [(cat_column, "Chats"), (dog_column, "Chiens")]:
            tk.Label(col, text=text, font=('Arial', 10, 'bold'),
                    fg=self.colors['text_dark'], bg=self.colors['card_bg']).pack(pady=5)
        
        # Scrollable frames
        cat_canvas, cat_scrollbar, cat_scrollable = self.create_scrollable_frame(cat_column, 130, 400)
        dog_canvas, dog_scrollbar, dog_scrollable = self.create_scrollable_frame(dog_column, 130, 400)
        
        cat_canvas.pack(side="left", fill="both", expand=True)
        cat_scrollbar.pack(side="right", fill="y")
        dog_canvas.pack(side="left", fill="both", expand=True)
        dog_scrollbar.pack(side="right", fill="y")
        
        # Load dataset
        self.load_dataset_images(cat_scrollable, dog_scrollable)
        
        # Right frame
        right_frame = tk.Frame(main_container)
        right_frame.pack(side='left', fill='both', expand=True)
        
        # Content frame
        content_frame = tk.Frame(right_frame)
        content_frame.pack(side='left', fill='both', expand=True)
        
        # Cat section
        tk.Label(content_frame, text="Sélectionner 10 images de chats",
                font=('Arial', 11)).pack(pady=10)
        self.cat_labels = self.create_image_grid(content_frame)
        
        # Dog section
        tk.Label(content_frame, text="Sélectionner 10 images de chiens",
                font=('Arial', 11)).pack(pady=10)
        self.dog_labels = self.create_image_grid(content_frame)
        
        # Buttons
        button_style = {
            'bg': self.colors['secondary'],
            'fg': 'white',
            'font': ('Arial', 10),
            'relief': 'flat',
            'padx': 15,
            'pady': 8,
            'cursor': 'hand2',
            'bd': 0
        }
        
        for category, text in [("cat", "Ajouter une image de chat"),
                             ("dog", "Ajouter une image de chien")]:
            tk.Button(content_frame, text=text,
                     command=lambda c=category: self.add_image(c),
                     **button_style).pack(pady=5)
        
        # Train button
        train_container = tk.Frame(right_frame)
        train_container.pack(side='right', padx=20, fill='y')
        tk.Frame(train_container).pack(expand=True)
        
        train_button = tk.Button(
            train_container,
            text="Entraîner",
            command=self.train_model,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='flat',
            width=12,
            height=1,
            cursor='hand2',
            bd=0
        )
        
        train_button.bind("<Enter>", lambda e: e.widget.configure(bg='#45a049'))
        train_button.bind("<Leave>", lambda e: e.widget.configure(bg=self.colors['primary']))
        train_button.pack(side='bottom', pady=20)

    def setup_testing_tab(self):
        main_container = tk.Frame(self.test_tab, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True)
        
        # Left sidebar
        left_frame = self._create_styled_frame(main_container, width=300)
        left_frame.pack(side='left', fill='y', padx=10, pady=10)
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame, text="Nouvelle photo", font=('Arial', 12, 'bold'),
                bg=self.colors['card_bg'], fg=self.colors['text_dark']).pack(pady=10)
        
        self.left_image_frame = self._create_styled_frame(left_frame, width=200, height=200)
        self.left_image_frame.pack(pady=10)
        self.left_image_frame.pack_propagate(False)
        
        self.left_image_label = tk.Label(self.left_image_frame, bg=self.colors['card_bg'])
        self.left_image_label.pack(expand=True)
        
        tk.Label(left_frame, text="Chat ou chien ou autre", wraplength=180,
                bg=self.colors['card_bg'], fg=self.colors['text_light']).pack(pady=5)
        
        browse_button = self._create_styled_button(
            left_frame, "Parcourir", self.select_test_image, is_primary=False)
        browse_button.pack(pady=10)
        
        # Right frame
        right_frame = tk.Frame(main_container, bg=self.colors['background'])
        right_frame.pack(side='left', fill='both', expand=True, padx=20)
        
        tk.Label(right_frame, text="Photo sélectionnée", font=('Arial', 12, 'bold'),
                bg=self.colors['background'], fg=self.colors['text_dark']).pack(pady=10)
        
        self.selected_image_frame = self._create_styled_frame(right_frame, width=300, height=300)
        self.selected_image_frame.pack(pady=10)
        self.selected_image_frame.pack_propagate(False)
        
        self.selected_image_label = tk.Label(self.selected_image_frame, bg=self.colors['card_bg'])
        self.selected_image_label.pack(expand=True)
        
        predict_button = self._create_styled_button(
            right_frame, "Prédiction", self.make_prediction, is_primary=True)
        predict_button.pack(pady=10)
        
        self.result_frame = self._create_styled_frame(right_frame, padx=20, pady=10)
        self.result_label = tk.Label(self.result_frame, text="",
                                   font=('Arial', 14, 'bold'), bg=self.colors['card_bg'])
        self.result_label.pack(pady=10)

    def train_model(self):
        if len(self.cat_images) < 10 or len(self.dog_images) < 10:
            if tk.messagebox.askokcancel("Avertissement",
                "Vous devez saisir des images\nVoulez-vous continuer sans entraînement ?",
                icon='warning'):
                self.tab_control.add(self.test_tab, text='Test')
                self.tab_control.select(self.test_tab)
            return
        
        self.classifier.train(self.cat_images, self.dog_images)
        self.tab_control.add(self.test_tab, text='Test')
        self.tab_control.select(self.test_tab)

    def add_image(self, category):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((120, 120))
            photo = ImageTk.PhotoImage(img)
            
            if category == "cat" and len(self.cat_images) < 10:
                self.cat_images.append(file_path)
                self.cat_labels[len(self.cat_images)-1].configure(image=photo)
                self.cat_labels[len(self.cat_images)-1].image = photo
            elif category == "dog" and len(self.dog_images) < 10:
                self.dog_images.append(file_path)
                self.dog_labels[len(self.dog_images)-1].configure(image=photo)
                self.dog_labels[len(self.dog_images)-1].image = photo

    def select_test_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Fichiers d'images", "*.jpg *.jpeg *.png")])
        if file_path:
            self.test_image_path = file_path
            img = Image.open(file_path)
            
            left_img = img.resize((180, 180))
            left_photo = ImageTk.PhotoImage(left_img)
            self.left_image_label.configure(image=left_photo)
            self.left_image_label.image = left_photo
            
            right_img = img.resize((280, 280))
            right_photo = ImageTk.PhotoImage(right_img)
            self.selected_image_label.configure(image=right_photo)
            self.selected_image_label.image = right_photo

    def make_prediction(self):
        if not hasattr(self, 'test_image_path'):
            tk.messagebox.showwarning("Avertissement", "Veuillez sélectionner une image d'abord !")
            return
            
        try:
            prediction, confidence = self.classifier.predict(self.test_image_path)
            self.update_prediction_result(prediction, confidence)
        except NotFittedError:
            tk.messagebox.showwarning("Avertissement",
                "Veuillez entraîner le modèle avant de faire des prédictions !")
            self.tab_control.select(self.train_tab)

    def load_dataset_images(self, cat_container, dog_container):
        self.dataset_cat_images = []
        self.dataset_dog_images = []
        
        for img_name in os.listdir(self.cat_db_path):
            img_path = os.path.join(self.cat_db_path, img_name)
            self.dataset_cat_images.append(img_path)
            self.add_dataset_image(cat_container, img_path)
        
        for img_name in os.listdir(self.dog_db_path):
            img_path = os.path.join(self.dog_db_path, img_name)
            self.dataset_dog_images.append(img_path)
            self.add_dataset_image(dog_container, img_path)
            
        if self.dataset_cat_images and self.dataset_dog_images:
            self.classifier.train(self.dataset_cat_images, self.dataset_dog_images)

    def update_prediction_result(self, prediction, confidence):
        result_bg = self.colors['primary'] if prediction.lower() == "chat" else self.colors['secondary']
        
        self.result_frame.configure(bg=result_bg)
        self.result_label.configure(bg=result_bg, fg='white', font=('Arial', 14, 'bold'))
        
        self.result_frame.pack_forget()
        self.result_frame.pack(pady=20, fill='x', padx=20)
        
        def animate_confidence(current=0):
            if current <= confidence:
                self.result_label.configure(text=f"{prediction} ({int(current)}%)")
                self.root.after(20, lambda: animate_confidence(current + 2))
        
        animate_confidence()

    def _create_styled_button(self, parent, text, command, is_primary=True, width=15):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.colors['primary'] if is_primary else self.colors['secondary'],
            fg='white',
            font=('Arial', 11, 'bold'),
            relief='flat',
            width=width,
            bd=0,
            cursor='hand2'
        )
        
        hover_color = '#45a049' if is_primary else '#1976D2'
        button.bind("<Enter>", lambda e: e.widget.configure(bg=hover_color))
        button.bind("<Leave>", lambda e: e.widget.configure(
            bg=self.colors['primary'] if is_primary else self.colors['secondary']))
        
        return button

    def _create_styled_frame(self, parent, width=None, height=None, padx=0, pady=0):
        frame = tk.Frame(
            parent,
            bg=self.colors['card_bg'],
            highlightbackground=self.colors['border'],
            highlightthickness=1,
            bd=0
        )
        if width:
            frame.configure(width=width)
        if height:
            frame.configure(height=height)
        if padx or pady:
            frame.configure(padx=padx, pady=pady)
        return frame

    def add_dataset_image(self, container, img_path):
        try:
            img = Image.open(img_path)
            img = img.resize((120, 120))
            photo = ImageTk.PhotoImage(img)
            
            frame = tk.Frame(container, bg=self.colors['card_bg'], padx=5, pady=5)
            frame.pack(fill='x', padx=5, pady=2)
            
            def on_enter(e):
                frame.configure(bg=self.colors['background'])
                label.configure(bg=self.colors['background'])
            
            def on_leave(e):
                frame.configure(bg=self.colors['card_bg'])
                label.configure(bg=self.colors['card_bg'])
            
            label = tk.Label(frame, image=photo, bg=self.colors['card_bg'], cursor='hand2')
            label.image = photo
            
            frame.bind('<Enter>', on_enter)
            frame.bind('<Leave>', on_leave)
            label.bind('<Enter>', on_enter)
            label.bind('<Leave>', on_leave)
            
            category = 'cat' if 'CAT' in img_path else 'dog'
            label.bind('<Button-1>',
                lambda e, path=img_path, cat=category: self.select_from_dataset(path, cat))
            label.pack()
            
            return label
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            return None

    def select_from_dataset(self, img_path, category):
        if category == "cat" and len(self.cat_images) >= 10:
            return
        if category == "dog" and len(self.dog_images) >= 10:
            return

        try:
            img = Image.open(img_path)
            img = img.resize((120, 120))
            photo = ImageTk.PhotoImage(img)
            
            if category == "cat":
                idx = len(self.cat_images)
                if idx < len(self.cat_labels):
                    self.cat_images.append(img_path)
                    self.cat_labels[idx].configure(image=photo)
                    self.cat_labels[idx].image = photo
            else:
                idx = len(self.dog_images)
                if idx < len(self.dog_labels):
                    self.dog_images.append(img_path)
                    self.dog_labels[idx].configure(image=photo)
                    self.dog_labels[idx].image = photo
        except Exception as e:
            print(f"Error selecting image {img_path}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PetClassifierApp(root)
    root.mainloop()