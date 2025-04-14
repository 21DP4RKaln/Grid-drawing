import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, ttk
from PIL import Image, ImageTk, ImageDraw
import os
import math

class RoundedButton(tk.Canvas):
    """Custom rounded button widget"""
    def __init__(self, parent, text, command=None, radius=15, bg="#4CAF50", fg="white", 
                 padx=15, pady=10, width=120, height=40, font_size=12, **kwargs):
        tk.Canvas.__init__(self, parent, borderwidth=0, highlightthickness=0, 
                          bg=parent["bg"], width=width, height=height, **kwargs)
        
        self.command = command
        self.text = text
        self.bg = bg
        self.fg = fg
        self.radius = radius
        
        
        self.rect_id = self.create_rounded_rect(0, 0, width, height, radius, fill=bg, outline=bg)
      
        self.text_id = self.create_text(width/2, height/2, text=text, fill=fg, font=("Arial", font_size))
 
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle"""
        points = [
            x1, y1 + radius,
            x1, y1,
            x1 + radius, y1,

            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,

            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,

            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
        ]
        
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _on_press(self, event):
        """Handle button press event"""
        darker_bg = self._darken_color(self.bg)
        self.itemconfig(self.rect_id, fill=darker_bg, outline=darker_bg)
    
    def _on_release(self, event):
        """Handle button release event"""
        self.itemconfig(self.rect_id, fill=self.bg, outline=self.bg)
  
        if 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height():
            if self.command:
                self.command()
    
    def _on_enter(self, event):
        """Handle mouse enter event"""
        lighter_bg = self._lighten_color(self.bg)
        self.itemconfig(self.rect_id, fill=lighter_bg, outline=lighter_bg)
        self.config(cursor="hand2")
    
    def _on_leave(self, event):
        """Handle mouse leave event"""
        self.itemconfig(self.rect_id, fill=self.bg, outline=self.bg)
        self.config(cursor="")
    
    def _darken_color(self, hex_color, factor=0.8):
        """Darken a color by a factor"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _lighten_color(self, hex_color, factor=0.1):
        """Lighten a color by a factor"""
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"

class StartPage:
    def __init__(self, root, start_callback):
        self.root = root
        self.start_callback = start_callback
        self.create_start_page()
        
    def create_start_page(self):
        # Configure window
        self.root.title("Grid Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Center frame for content
        center_frame = tk.Frame(main_frame, bg="#f0f0f0")
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        title_label = tk.Label(center_frame, text="GRID TOOL", font=("Arial", 36, "bold"), 
                             bg="#f0f0f0", fg="#4CAF50")
        title_label.pack(pady=(0, 30))
        
        # Subtitle
        subtitle_label = tk.Label(center_frame, text="Create customizable grids for your images", 
                               font=("Arial", 14), bg="#f0f0f0", fg="#555555")
        subtitle_label.pack(pady=(0, 50))

        start_btn = RoundedButton(center_frame, text="START", command=self.start_application, 
                                bg="#4CAF50", fg="white", width=180, height=45)
        start_btn.pack(pady=10)
        
        about_btn = RoundedButton(center_frame, text="ABOUT", command=self.show_about, 
                               bg="#e0e0e0", fg="#333333", width=180, height=45)
        about_btn.pack(pady=10)
        
        exit_btn = RoundedButton(center_frame, text="EXIT", command=self.root.quit, 
                              bg="#e0e0e0", fg="#333333", width=180, height=45)
        exit_btn.pack(pady=10)

        version_label = tk.Label(self.root, text="Version 1.0", font=("Arial", 8), 
                              bg="#f0f0f0", fg="#999999")
        version_label.pack(side=tk.BOTTOM, pady=10)
    
    def start_application(self):
        """Start the main application"""
        for widget in self.root.winfo_children():
            widget.destroy()
 
        self.start_callback(self.root)
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About Grid Tool", 
                         "Grid Tool v1.0\n\n"
                         "A modern application for adding customizable grids to images.\n\n"
                         "Features:\n"
                         "• Customizable grid size and color\n"
                         "• Square or rectangular grid cells\n"
                         "• Image rotation\n"
                         "• Zoom and pan functionality\n\n"
                         "Created by Nikola Lavriņenko\n"
                         "Design SVN (github - 21DP4RKaln)\n\n"
                         "all rights reserved ® 2077\n")

class ModernGridTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize variables
        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.display_image = None
        self.grid_count = tk.IntVar(value=10)
        self.grid_color = "#4CAF50" 
        self.grid_thickness = tk.IntVar(value=2)
        self.rotate_angle = tk.IntVar(value=0)
        self.use_square_cells = tk.BooleanVar(value=True)
        self.zoom_factor = tk.DoubleVar(value=1.0) 
        self.panning = False
        self.pan_start_x = 0
        self.pan_start_y = 0
   
        self.create_main_layout()
  
        self.status_var = tk.StringVar(value="Ready to start. Click 'Open Image' to begin.")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bg="#e0e0e0", fg="#555555", 
                                relief=tk.FLAT, anchor=tk.W, padx=10, pady=5)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_main_layout(self):
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
 
        toolbar = tk.Frame(main_container, bg="#f0f0f0")
        toolbar.pack(fill=tk.X, pady=(0, 10))
  
        open_btn = RoundedButton(toolbar, text="Open Image", command=self.load_image, 
                              bg="#5b5b5b", fg="white", radius=10, width=120, height=35)
        open_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_btn = RoundedButton(toolbar, text="Save Image", command=self.save_image, 
                              bg="#4CAF50", fg="white", radius=10, width=120, height=35)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        reset_btn = RoundedButton(toolbar, text="Reset All", command=self.reset_all, 
                               bg="#e0e0e0", fg="#333333", radius=10, width=120, height=35)
        reset_btn.pack(side=tk.LEFT)
        
        back_btn = RoundedButton(toolbar, text="Back to Start", command=self.go_to_start_page, 
                              bg="#e0e0e0", fg="#333333", radius=10, width=120, height=35)
        back_btn.pack(side=tk.LEFT, padx=(10, 0))
   
        zoom_frame = tk.Frame(toolbar, bg="#f0f0f0")
        zoom_frame.pack(side=tk.RIGHT)
        
        zoom_out_btn = RoundedButton(zoom_frame, text="−", command=self.zoom_out, 
                                  bg="#e0e0e0", fg="#333333", radius=10, width=35, height=35)
        zoom_out_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.zoom_label = tk.Label(zoom_frame, text="100%", bg="#f0f0f0", fg="#333333", width=5)
        self.zoom_label.pack(side=tk.LEFT)
        
        zoom_in_btn = RoundedButton(zoom_frame, text="+", command=self.zoom_in, 
                                 bg="#e0e0e0", fg="#333333", radius=10, width=35, height=35)
        zoom_in_btn.pack(side=tk.LEFT, padx=(5, 0))

        reset_zoom_btn = RoundedButton(zoom_frame, text="1:1", command=self.reset_zoom, 
                                    bg="#e0e0e0", fg="#333333", radius=10, width=35, height=35)
        reset_zoom_btn.pack(side=tk.LEFT, padx=(10, 0))

        content_frame = tk.Frame(main_container, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True)

        settings_frame = tk.Frame(content_frame, bg="white", bd=1, relief=tk.FLAT)
        settings_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        tk.Label(settings_frame, text="SETTINGS", bg="white", fg="#555555", 
               anchor=tk.W, padx=15, pady=10).pack(fill=tk.X)

        settings_content = tk.Frame(settings_frame, bg="white", padx=15, pady=5)
        settings_content.pack(fill=tk.BOTH, expand=True)

        tk.Label(settings_content, text="Grid Size", bg="white", fg="#555555", 
               anchor=tk.W).pack(fill=tk.X, pady=(10, 5))
        
        grid_slider = ttk.Scale(settings_content, from_=2, to=50, orient=tk.HORIZONTAL, 
                              variable=self.grid_count)
        grid_slider.pack(fill=tk.X)
        
        grid_value_frame = tk.Frame(settings_content, bg="white")
        grid_value_frame.pack(fill=tk.X)
        
        self.grid_value_label = tk.Label(grid_value_frame, text="10", bg="white", fg="#555555")
        self.grid_value_label.pack(side=tk.RIGHT)
        grid_slider.config(command=self.update_grid_label)

        tk.Label(settings_content, text="Line Thickness", bg="white", fg="#555555", 
               anchor=tk.W).pack(fill=tk.X, pady=(20, 5))
        
        thickness_slider = ttk.Scale(settings_content, from_=1, to=10, orient=tk.HORIZONTAL, 
                                   variable=self.grid_thickness)
        thickness_slider.pack(fill=tk.X)
        
        thickness_value_frame = tk.Frame(settings_content, bg="white")
        thickness_value_frame.pack(fill=tk.X)
        
        self.thickness_value_label = tk.Label(thickness_value_frame, text="2", bg="white", fg="#555555")
        self.thickness_value_label.pack(side=tk.RIGHT)
        thickness_slider.config(command=self.update_thickness_label)

        tk.Label(settings_content, text="Line Color", bg="white", fg="#555555", 
               anchor=tk.W).pack(fill=tk.X, pady=(20, 10))
        
        color_frame = tk.Frame(settings_content, bg="white")
        color_frame.pack(fill=tk.X)
        
        self.color_preview = tk.Canvas(color_frame, width=30, height=30, bd=0, highlightthickness=0)
        self.color_preview.create_rectangle(0, 0, 30, 30, fill=self.grid_color, outline="")
        self.color_preview.pack(side=tk.LEFT)
  
        reset_color_btn = RoundedButton(color_frame, text="Reset", command=self.reset_color,
                                     bg="#e0e0e0", fg="#555555", radius=8, width=50, height=30, font_size=10)
        reset_color_btn.pack(side=tk.LEFT, padx=(10, 5))
        
        color_btn = RoundedButton(color_frame, text="Choose Color", command=self.choose_color,
                               bg="#e0e0e0", fg="#555555", radius=8, width=90, height=30, font_size=10)
        color_btn.pack(side=tk.LEFT)

        tk.Label(settings_content, text="Cell Type", bg="white", fg="#555555", 
               anchor=tk.W).pack(fill=tk.X, pady=(20, 10))
        
        square_toggle = ttk.Checkbutton(settings_content, text="Use Square Cells", 
                                      variable=self.use_square_cells)
        square_toggle.pack(fill=tk.X)
 
        tk.Label(settings_content, text="Rotation", bg="white", fg="#555555", 
               anchor=tk.W).pack(fill=tk.X, pady=(20, 10))
        
        rotation_frame = tk.Frame(settings_content, bg="white")
        rotation_frame.pack(fill=tk.X)
        
        rot0_btn = RoundedButton(rotation_frame, text="0°", command=lambda: self.set_rotation(0),
                              bg="#e0e0e0", fg="#555555", radius=8, width=35, height=30)
        rot0_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        rot90_btn = RoundedButton(rotation_frame, text="90°", command=lambda: self.set_rotation(90),
                               bg="#e0e0e0", fg="#555555", radius=8, width=35, height=30)
        rot90_btn.pack(side=tk.LEFT, padx=5)
        
        rot180_btn = RoundedButton(rotation_frame, text="180°", command=lambda: self.set_rotation(180),
                                bg="#e0e0e0", fg="#555555", radius=8, width=35, height=30)
        rot180_btn.pack(side=tk.LEFT, padx=5)
        
        rot270_btn = RoundedButton(rotation_frame, text="270°", command=lambda: self.set_rotation(270),
                                bg="#e0e0e0", fg="#555555", radius=8, width=35, height=30)
        rot270_btn.pack(side=tk.LEFT, padx=5)

        apply_btn = RoundedButton(settings_content, text="APPLY CHANGES", command=self.apply_changes,
                               bg="#4CAF50", fg="white", radius=10, width=200, height=45)
        apply_btn.pack(fill=tk.X, pady=(30, 0))

        preview_frame = tk.Frame(content_frame, bg="white", bd=1, relief=tk.FLAT)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        preview_header = tk.Frame(preview_frame, bg="white")
        preview_header.pack(fill=tk.X)
        
        tk.Label(preview_header, text="PREVIEW", bg="white", fg="#555555", 
               anchor=tk.W, padx=15, pady=10).pack(side=tk.LEFT)
        
        zoom_info = tk.Label(preview_header, text="Drag to pan, Scroll to zoom", 
                          bg="white", fg="#999999", padx=15, pady=10)
        zoom_info.pack(side=tk.RIGHT)

        canvas_frame = tk.Frame(preview_frame, bg="#f5f5f5", padx=15, pady=15)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="white", bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind events for zooming and panning
        self.canvas.bind("<MouseWheel>", self.mouse_zoom) 
        self.canvas.bind("<Button-4>", self.mouse_zoom)  
        self.canvas.bind("<Button-5>", self.mouse_zoom)  
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan_image)
        self.canvas.bind("<ButtonRelease-1>", self.stop_pan)

        self.canvas.create_text(300, 200, text="Open an image to begin", 
                           font=("Arial", 14), fill="#CCCCCC")
    
    def go_to_start_page(self):
        """Return to the start page"""
        if self.original_image is not None:
            if not messagebox.askyesno("Confirm", "Are you sure you want to return to the start page?\nAny unsaved changes will be lost."):
                return

        for widget in self.root.winfo_children():
            widget.destroy()

        StartPage(self.root, lambda root: ModernGridTool(root))
    
    def reset_all(self):
        """Reset all settings to default values"""
        if self.original_image is None:
            return

        self.grid_count.set(10)
        self.update_grid_label()
        
        self.grid_thickness.set(2)
        self.update_thickness_label()
        
        self.reset_color()
        
        self.use_square_cells.set(True)

        self.rotate_angle.set(0)

        self.zoom_factor.set(1.0)
        self.update_zoom_label()

        self.processed_image = self.original_image.copy()

        self.update_preview()
        self.status_var.set("All settings reset to default values")
    
    def reset_color(self):
        """Reset grid color to default green"""
        self.grid_color = "#4CAF50"  
        self.color_preview.delete("all")
        self.color_preview.create_rectangle(0, 0, 30, 30, fill=self.grid_color, outline="")
        self.update_preview()
    
    def update_grid_label(self, event=None):
        """Update the grid count label"""
        value = int(self.grid_count.get())
        self.grid_value_label.config(text=str(value))
    
    def update_thickness_label(self, event=None):
        """Update the thickness label"""
        value = int(self.grid_thickness.get())
        self.thickness_value_label.config(text=str(value))
    
    def zoom_in(self):
        """Zoom in on the image"""
        if self.original_image is None:
            return
        
        current_zoom = self.zoom_factor.get()
        new_zoom = min(current_zoom * 1.25, 5.0)  
        self.zoom_factor.set(new_zoom)
        self.update_zoom_label()
        self.update_preview()
    
    def zoom_out(self):
        """Zoom out from the image"""
        if self.original_image is None:
            return
        
        current_zoom = self.zoom_factor.get()
        new_zoom = max(current_zoom / 1.25, 0.1)  
        self.zoom_factor.set(new_zoom)
        self.update_zoom_label()
        self.update_preview()
    
    def reset_zoom(self):
        """Reset zoom to 100%"""
        if self.original_image is None:
            return
        
        self.zoom_factor.set(1.0)
        self.update_zoom_label()
        self.update_preview()
    
    def update_zoom_label(self):
        """Update the zoom percentage label"""
        zoom_percent = int(self.zoom_factor.get() * 100)
        self.zoom_label.config(text=f"{zoom_percent}%")
    
    def mouse_zoom(self, event):
        """Handle mouse wheel events for zooming"""
        if self.original_image is None:
            return
        
        current_zoom = self.zoom_factor.get()

        if event.type == '4':  
            if event.num == 4:  
                new_zoom = min(current_zoom * 1.1, 5.0)
            else:  
                new_zoom = max(current_zoom / 1.1, 0.1)
        else:  
            if event.delta > 0:
                new_zoom = min(current_zoom * 1.1, 5.0)
            else:
                new_zoom = max(current_zoom / 1.1, 0.1)
        
        self.zoom_factor.set(new_zoom)
        self.update_zoom_label()
        self.update_preview()
    
    def start_pan(self, event):
        """Start panning the image"""
        if self.original_image is None:
            return
        
        self.panning = True
        self.pan_start_x = event.x
        self.pan_start_y = event.y
    
    def pan_image(self, event):
        """Pan the image as mouse moves"""
        if not self.panning or self.original_image is None:
            return

        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y

        self.canvas.scan_dragto(event.x, event.y, gain=1)

        self.pan_start_x = event.x
        self.pan_start_y = event.y
    
    def stop_pan(self, event):
        """Stop panning the image"""
        self.panning = False
        
    def set_rotation(self, angle):
        """Set the rotation angle and update preview"""
        self.rotate_angle.set(angle)
        self.update_preview()
        self.status_var.set(f"Rotation set to {angle}°")

    def reset_image(self):
        """Reset image to original"""
        if self.original_image is None:
            return
            
        self.processed_image = self.original_image.copy()
        self.rotate_angle.set(0)
        self.update_preview()
        self.status_var.set("Image reset to original")

    def load_image(self):
        """Load image from file"""
        file_type = [("Image files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All files", "*.*")]

        file_path = filedialog.askopenfilename(title="Open Image", filetypes=file_type)

        if file_path:
            try:
                self.image_path = file_path
                self.original_image = Image.open(file_path)
                self.processed_image = self.original_image.copy()
                self.zoom_factor.set(1.0)  
                self.update_zoom_label()
                self.update_preview()

                #update status
                file_name = os.path.basename(file_path)
                self.status_var.set(f"Loaded: {file_name}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def update_preview(self, event=None):
        """Update the canvas with the processed image"""
        if self.original_image is None:
            return
        
        if self.rotate_angle.get() != 0:
            rotated_image = self.original_image.rotate(self.rotate_angle.get(), expand=True, resample=Image.BICUBIC)
            self.processed_image = rotated_image
        else:
            self.processed_image = self.original_image.copy()

        grid_image = self.apply_grid(self.processed_image)

        self.display_image = self.prepare_image_for_display(grid_image)

        self.show_image_on_canvas()
        
    def apply_grid(self, image):
        """Apply grid to the image"""
        result = image.copy()
        draw = ImageDraw.Draw(result)

        width, height = result.size
        cells = self.grid_count.get()
        thickness = self.grid_thickness.get()

        if self.use_square_cells.get():
            cell_size = min(width, height) / cells
            num_cells_x = math.ceil(width / cell_size)
            num_cells_y = math.ceil(height / cell_size)

            for i in range(num_cells_x + 1):
                x = i * cell_size
                draw.line([(x, 0), (x, height)], fill=self.grid_color, width=thickness)

            for j in range(num_cells_y + 1):
                y = j * cell_size
                draw.line([(0, y), (width, y)], fill=self.grid_color, width=thickness)
        else:
            cell_width = width / cells
            cell_height = height / cells

            for i in range(cells + 1):
                x = i * cell_width
                draw.line([(x, 0), (x, height)], fill=self.grid_color, width=thickness)

            for j in range(cells + 1):
                y = j * cell_height
                draw.line([(0, y), (width, y)], fill=self.grid_color, width=thickness)

        return result

    def prepare_image_for_display(self, image):
        """Prepare image for display on canvas with zoom"""
        if image is None:
            return None

        if self.zoom_factor.get() != 1.0:
            zoom = self.zoom_factor.get()
            new_width = int(image.width * zoom)
            new_height = int(image.height * zoom)
            return image.resize((new_width, new_height), Image.LANCZOS)
        
        return image

    def show_image_on_canvas(self):
        """Display the image on the canvas"""
        if self.display_image is None:
            return
        
        self.tk_image = ImageTk.PhotoImage(self.display_image)
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1: 
            canvas_width = 600
            canvas_height = 400

        img_width = self.tk_image.width()
        img_height = self.tk_image.height()
        x = max(0, (canvas_width - img_width) // 2)
        y = max(0, (canvas_height - img_height) // 2)

        self.canvas.create_image(x, y, anchor=tk.NW, image=self.tk_image, tags="image")

        self.canvas.config(scrollregion=(0, 0, x*2 + img_width, y*2 + img_height))

        self.canvas.scan_mark(0, 0)

    def choose_color(self):
        """Choose a color for the grid"""
        color = colorchooser.askcolor(initialcolor=self.grid_color, title="Choose Grid Color")
        if color[1]:
            self.grid_color = color[1]
            self.color_preview.delete("all")
            self.color_preview.create_rectangle(0, 0, 30, 30, fill=self.grid_color, outline="")
            self.status_var.set(f"Grid Color: {self.grid_color}")
            self.update_preview()
            
    def apply_changes(self):
        """Apply changes to the image"""
        self.update_preview()
        self.status_var.set("Changes applied successfully!")

    def save_image(self):
        """Save the processed image to a file"""
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No image to save.")
            return

        final_image = self.apply_grid(self.processed_image)

        file_types = [("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")]

        save_path = filedialog.asksaveasfilename(filetypes=file_types, defaultextension=".png", title="Save Image")

        if save_path:
            try:
                final_image.save(save_path)

                file_name = os.path.basename(save_path)
                self.status_var.set(f"Saved: {file_name}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

def main():
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    StartPage(root, lambda root: ModernGridTool(root))
    
    root.mainloop()

if __name__ == "__main__":
    main()