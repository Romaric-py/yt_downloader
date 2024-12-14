import ttkbootstrap as ttk
import dotenv
import os
import configparser
import threading

from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter.filedialog import askdirectory
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
from downloader import Downloader
from utils import stringify_size, extract_percentage

# Chargement des variables d'environnement
dotenv.load_dotenv()


class MainWindow(ttk.Window):
    def __init__(self, config_file,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.wm_title("YouTube Videos Downloader")
        self.geometry("768x768")  # Taille de la fenêtre
        
        # Constantes
        self.DARK, self.LIGHT = 0, 1
        
        # Charger les paramètres de l'application
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        
        # Vérifier si le fichier de configuration existe
        if os.path.exists(config_file):
            self.config.read(config_file)
            # Theme
            theme = self.config.get('settings', 'selected_theme', fallback='light')
            self.theme = ["dark", "light"].index(theme)
            
            # Dossier de destination
            self.dest = self.config.get('settings', 'destination_folder', fallback="~/YoutubeDownloads/")
            self.dest = os.path.expanduser(self.dest)
        else:
            print(f"Warning: {config_file} not found. Default configuration will be used.")
            self.theme = self.LIGHT
            self.dest = ""
            
        # Variables de thème et répertoire
        self.theme_var = ttk.IntVar(value=self.theme)
        self.dest_var = ttk.StringVar(value=self.dest) # destination folder
        self.media_path = os.environ.get('ASSETS_PATH', './')  # Chemin par défaut
        self.logo_path = os.path.join(self.media_path, "ytdwld_logo.png")
        
        # Instancier le téléchargeur
        self.downloader = Downloader(self.dest_var.get())
        
        # Logo
        try:
            self.logo = ttk.ImageTk.PhotoImage(file=self.logo_path)
        except Exception as e:
            print(f"Logo not found: {e}")
            self.logo = None  # Remplacement en cas d'erreur
        
        # Construction de l'interface utilisateur
        self.create_widgets()
        

    def create_widgets(self):
        """Crée les widgets de l'interface."""
        # Cadre principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.place(x=0, y=50, relwidth=1)
        self.style.configure("Custom.TLabel", background='#1046aa')
        
        if self.logo:
            ttk.Label(self.main_frame, image=self.logo, anchor=CENTER, style="Custom.TLabel").pack()
        
        ttk.Label(self.main_frame, text="Enter the video link").pack(pady=10, anchor=CENTER)
        self.url_field = ttk.Entry(self.main_frame, width=70)
        self.url_field.pack(anchor=CENTER)
        self.url_field.bind('<Return>', lambda event: self.download())
        
        ttk.Button(self.main_frame, text="DOWNLOAD", bootstyle="primary", command=self.download).pack(pady=10)
        
        self.progress_bar = ttk.Progressbar(self.main_frame, orient=HORIZONTAL, length=500, mode='determinate', bootstyle="success-striped")
        self.progress_bar.pack(pady=10)
        
        self.status_label = ttk.Label(self.main_frame, text="Donwloading state: ")
        self.status_label.pack(pady=10)
        

        # Bouton menu
        self.menu_btn = ttk.Button(self, text="≡", bootstyle=OUTLINE, command=self.toggle_menu)
        self.menu_btn.place(x=10, y=10)
        
        # Bouton fermer
        ttk.Button(self, text="Close", bootstyle=OUTLINE, command=self.quit).place(y=10, relx=0.9)
        
        # Cadre menu (initialement masqué)
        self.menu = ttk.Frame(self, border=1, relief=SOLID)
        
        # Bouton retour
        ttk.Button(self.menu, text="⤬", bootstyle=OUTLINE, command=self.toggle_menu).pack(pady=10, padx=10, anchor=W)
        
        # Section Thème
        self.menu_theme = ttk.Labelframe(self.menu, text="Theme", style="Custom.TLabelframe")
        self.menu_theme.pack(padx=10, pady=10, fill=X, anchor=W)
        ttk.Radiobutton(self.menu_theme, variable=self.theme_var, value=self.LIGHT, text="Light", command=self.apply_theme).pack(pady=5, padx=(10, 20), anchor=W)
        ttk.Radiobutton(self.menu_theme, variable=self.theme_var, value=self.DARK, text="Dark", command=self.apply_theme).pack(pady=5, padx=(10, 20), anchor=W)

        # Section Répertoire
        self.menu_dir = ttk.Frame(self.menu, style="Custom.TFrame")
        self.menu_dir.pack(padx=10, pady=10, fill=X, anchor=W)
        ttk.Label(self.menu_dir, text="Default Folder").pack(pady=(0, 5), anchor=W)
        self.dir_field = ttk.Entry(self.menu_dir, width=30, textvariable=self.dest_var)
        self.dir_field.pack(pady=(0, 5), anchor=W, side=LEFT)
        ttk.Button(self.menu_dir, text="Browse", bootstyle="primary", command=self.change_directory).pack(pady=(0, 5), anchor=W)
        
        
    def progress_hook(self, d):
        """Mise à jour de la barre de progression."""
        if d['status'] == 'downloading':
            percent = extract_percentage(d.get('_percent_str', '0.0%').strip())
            self.progress_bar['value'] = percent
            self.status_label.config(text=f"Progression : {percent}%")
        elif d['status'] == 'finished':
            self.progress_bar['value'] = 100
            self.status_label.config(text=f"Download completed: {d['filename']}")
            self.end_download()

        
    def download(self):
        """Gère le téléchargement via l'interface utilisateur."""
        url = self.url_field.get().strip()
        if not url:
            Messagebox.show_error("Please enter a URL", parent=self)
            return
        
        # demander a l'utilisateur de choisir le format
        # format_id = self.choose_format_id(url)
        # if format_id is None:
        #     return Messagebox.show_info("Download cancelled")
        format_id = None
        
        # Début du téléchargement
        self.status_label.config(text="The downloading has begun")
        thread = threading.Thread(target=self.downloader.download, args=(url, format_id, [self.progress_hook]))
        thread.start()
    
    def end_download(self):
        if not self.downloader.success:
            Messagebox.show_error("Invalid URL or download failed", parent=self)
        else:
            Messagebox.show_info("Download completed", parent=self)
    
    
    def choose_format_id(self, url):
        format_id = None
        response = self.downloader.get_formats(url)
        if not response:
            return Messagebox.show_error("An error has occured", parent=self)
        thumbnail, formats = response['thumbnail'], response['formats']
        
        # Construction d'une nouvelle fenetre
        def choose(id):
            nonlocal format_id
            format_id = id
            toplevel.destroy()
            
        
        toplevel = ttk.Toplevel(title="youtube_downloader")
        frame = ttk.Frame(toplevel)
        frame.pack()
        for i, format in enumerate(formats):
            sub_frame = ttk.Frame(frame)
            sub_frame.grid(row=i%4, column=i//4)
            # Thumbnail
            label = ttk.Label(sub_frame)
            thread = threading.Thread(target=self.set_label_background_from_url, args=(label, thumbnail))
            thread.start()
            
            label.grid(row=0, column=0, rowspan=2, sticky=EW, padx=5, pady=5)
            # Format
            ttk.Label(sub_frame, text=f"Format: {format['format']}").grid(row=0, column=1, sticky=EW, padx=5, pady=5)
            # taille du fichier
            size = stringify_size(format['size'])
            ttk.Label(sub_frame, text=f"Size: {size[0]:.2f}{size[1]}").grid(row=1, column=1, sticky=EW, padx=5, pady=5)
            # Boutton
            ttk.Button(sub_frame, bootstyle="primary", text="Select", command=lambda: choose(format['id'])).grid(row=0, column=2, rowspan=2, sticky=EW, padx=5, pady=5)
        # Attendre jusqu'à destruction de la fenetre
        toplevel.wait_window(toplevel)
        
        return format_id
        

    def toggle_menu(self):
        """Affiche ou masque le menu."""
        if self.menu.winfo_ismapped():
            self.menu.place_forget()
        else:
            self.menu.place(x=0, y=0, relheight=1)
            

    def apply_theme(self):
        """Applique le thème sélectionné."""
        selected_theme = "litera" if self.theme_var.get() == self.LIGHT else "darkly"
        self.style.theme_use(selected_theme)
        

    def change_directory(self):
        """Change le répertoire de destination."""
        new_dir = askdirectory() or self.dest_var.get()
        
        if not os.path.exists(new_dir):
            Messagebox.show_error("Invalid directory path", parent=self)
            return
        
        self.dest_var.set(new_dir)
        self.downloader.dest = new_dir
        self.config.set('settings', 'destination_folder', new_dir)
        # Sauvegarder les modifications
        with open(self.config_file, 'w') as cf:
            self.config.write(cf)
        Messagebox.show_info("Destination folder updated", parent=self)
    
    
    def set_label_background_from_url(self, label, image_url, w=150, h=100):
        try:
            with urlopen(image_url) as response:
                img_data = response.read()
            # Charger l'image avec Pillow
            img = Image.open(BytesIO(img_data))
        except:
            print("[ERROR]: Invalid image link")
            return 
        # Redimensionner l'image pour qu'elle s'adapte à la taille du label
        img = img.resize((100, 75))

        # Convertir l'image pour Tkinter
        img_tk = ImageTk.PhotoImage(img)
        
        # Appliquer l'image comme fond du label
        label.configure(image=img_tk, text="", anchor=CENTER, width=w)
        label.image = img_tk  # Garder une référence à l'image (car suppression par le garbage collector)