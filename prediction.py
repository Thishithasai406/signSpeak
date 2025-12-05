# Importing Libraries
import numpy as np
import math
import cv2

import os, sys
import traceback
import pyttsx3
from tensorflow.keras.models import load_model
from cvzone.HandTrackingModule import HandDetector
from string import ascii_uppercase
import enchant
ddd=enchant.Dict("en_US")
hd = HandDetector(maxHands=1)
hd2 = HandDetector(maxHands=1)
import tkinter as tk
from PIL import Image, ImageTk

offset=29


os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"


# Application :

class Application:

    def __init__(self):
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.model = load_model('cnn8grps_rad1_model.h5', compile=False)
        self.speak_engine=pyttsx3.init()
        self.speak_engine.setProperty("rate",100)
        voices=self.speak_engine.getProperty("voices")
        self.speak_engine.setProperty("voice",voices[0].id)

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        self.space_flag=False
        self.next_flag=True
        self.prev_char=""
        self.count=-1
        self.ten_prev_char=[]
        for i in range(10):
            self.ten_prev_char.append(" ")


        for i in ascii_uppercase:
            self.ct[i] = 0


        # Color scheme used in the React code
        # Background Colors
        self.bg_black = "#000000"           # Main page background
        self.gray_900 = "#111827"           # Dark gradient start
        self.gray_800 = "#1F2937"           # Dark gradient end, button base
        self.gray_700 = "#374151"           # Button gradient end

        # Text Colors
        self.white = "#FFFFFF"              # Main text color
        self.gray_400 = "#9CA3AF"           # Label text (Character, Sentence)
        self.cyan_400 = "#22D3EE"           # Character display text / gradient start
        self.red_500 = "#EF4444"            # "Suggestions" label, LIVE badge

        # Border & Accent Colors
        self.cyan_500 = "#06B6D4"           # Borders (with opacity variations)
        self.cyan_500_30 = "#06B6D44D"      # Camera border (30% opacity)
        self.cyan_500_40 = "#06B6D466"      # Box & button borders (40% opacity)

        # Gradient Colors (Header)
        self.blue_500 = "#3B82F6"           # Gradient middle
        self.purple_500 = "#A855F7"         # Gradient end

        # Shadow/Glow Colors
        self.cyan_500_20 = "#06B6D433"      # Camera glow (20% opacity)
        self.cyan_500_50 = "#06B6D480"      # Suggestion button hover glow (50% opacity)
        self.red_500_50 = "#EF444480"       # Clear button hover glow (50% opacity)
        self.green_500_50 = "#10B98180"     # Speak button hover glow (50% opacity)

        # LIVE Badge
        self.red_500_80 = "#EF4444CC"       # Badge background (80% opacity)

        # Hover State Colors
        self.cyan_600 = "#0891B2"           # Suggestion button hover start
        self.blue_600 = "#2563EB"           # Suggestion button hover end
        self.red_600 = "#DC2626"            # Clear button hover start
        self.green_600 = "#059669"          # Speak button hover start
        self.green_500 = "#10B981"          # Speak button hover end

        # Backward compatibility with existing attribute names
        self.bg_color = self.bg_black
        self.cyan = self.cyan_500
        self.blue = self.blue_500
        self.purple = self.purple_500
        self.red = self.red_500
        self.green = self.green_500
        self.gray = self.gray_400
        self.dark_gray = self.gray_800
        
        # Window setup
        self.root = tk.Tk()
        self.root.title("Sign Language To Text Conversion")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("1400x800")
        self.root.configure(bg=self.bg_color)
        
        # Create main container with padding
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header with gradient text
        self.header_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.header_frame.pack(pady=(0, 30))
        
        self.header_label = tk.Label(
            self.header_frame,
            text="Sign Language To Text Conversion",
            font=("Arial", 40, "bold"),
            bg=self.bg_color,
            fg=self.cyan_400
        )
        self.header_label.pack()
        self.create_gradient_text()
        
        # Main content area - side by side layout
        self.content_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # LEFT SIDE - Camera
        self.left_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Camera container with glowing border
        self.camera_container = tk.Frame(self.left_frame, bg=self.bg_color)
        self.camera_container.pack(fill=tk.BOTH, expand=True)
        
        self.camera_canvas = tk.Canvas(
            self.camera_container,
            bg=self.bg_color,
            highlightthickness=0,
            width=600,
            height=500
        )
        self.camera_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Video panel inside camera canvas (no border)
        self.panel = tk.Label(self.camera_canvas, bg=self.gray_900, borderwidth=0)
        self.panel.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        # LIVE badge removed
        
        # Suggestions section
        self.suggestions_label = tk.Label(
            self.left_frame,
            text="Suggestions :",
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.red_500,
            anchor="w"
        )
        self.suggestions_label.pack(pady=(20, 10), anchor="w")
        
        # Suggestion buttons container (with Clear and Speak in same row)
        self.suggestions_frame = tk.Frame(self.left_frame, bg=self.bg_color)
        self.suggestions_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.b1 = self.create_suggestion_button(self.suggestions_frame, " ")
        self.b1.pack(side=tk.LEFT, padx=(0, 10), fill=tk.BOTH, expand=True)
        
        self.b2 = self.create_suggestion_button(self.suggestions_frame, " ")
        self.b2.pack(side=tk.LEFT, padx=(0, 10), fill=tk.BOTH, expand=True)
        
        self.b3 = self.create_suggestion_button(self.suggestions_frame, " ")
        self.b3.pack(side=tk.LEFT, padx=(0, 10), fill=tk.BOTH, expand=True)
        
        self.b4 = self.create_suggestion_button(self.suggestions_frame, " ")
        self.b4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # RIGHT SIDE - Text outputs
        self.right_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Character display
        self.char_label = tk.Label(
            self.right_frame,
            text="Character :",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.gray_400,
            anchor="w"
        )
        self.char_label.pack(anchor="w", pady=(0, 10))
        
        self.char_canvas = tk.Canvas(
            self.right_frame,
            bg=self.gray_800,
            highlightthickness=0,
            width=600,
            height=180
        )
        self.char_canvas.pack(fill=tk.X, expand=False, pady=(0, 0))
        
        def update_char_border(e):
            width = self.char_canvas.winfo_width()
            height = self.char_canvas.winfo_height()
            if width > 1 and height > 1:
                self.draw_rounded_border(self.char_canvas, 0, 0, width, height, self.cyan, 2, 15)
        
        
        self.panel3 = tk.Label(
            self.char_canvas,
            text="",
            font=("Arial", 32, "bold"),
            bg=self.gray_800,
            fg=self.cyan_400
        )
        self.panel3.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Cursor line for empty character display
        def update_cursor():
            width = self.char_canvas.winfo_width()
            height = self.char_canvas.winfo_height()
            if width > 1 and height > 1:
                self.char_canvas.delete("cursor")
                self.char_cursor = self.char_canvas.create_line(
                    width//2 - 10, height//2, width//2 + 10, height//2,
                    fill=self.cyan_400,
                    width=2,
                    tags="cursor"
                )
        
        def update_char_all(e):
            update_char_border(e)
            update_cursor()
        
        self.char_canvas.bind("<Configure>", update_char_all)
        update_char_all(None)
        
        # Sentence display
        self.sentence_label = tk.Label(
            self.right_frame,
            text="Sentence :",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.gray_400,
            anchor="w"
        )
        self.sentence_label.pack(anchor="w", pady=(20, 10))
        
        self.sentence_canvas = tk.Canvas(
            self.right_frame,
            bg=self.gray_800,
            highlightthickness=0,
            width=600,
            height=180
        )
        self.sentence_canvas.pack(fill=tk.X, expand=False)
        
        def update_sentence_border(e):
            width = self.sentence_canvas.winfo_width()
            height = self.sentence_canvas.winfo_height()
            if width > 1 and height > 1:
                self.draw_rounded_border(self.sentence_canvas, 0, 0, width, height, self.cyan, 2, 15)
        
        self.sentence_canvas.bind("<Configure>", update_sentence_border)
        update_sentence_border(None)
        
        self.panel5 = tk.Label(
            self.sentence_canvas,
            text="Your sentence will appear here...",
            font=("Arial", 20),
            bg=self.gray_800,
            fg=self.gray_400,
            wraplength=580,
            justify=tk.LEFT,
            anchor="nw"
        )
        self.panel5.place(x=25, y=25, width=550, height=130)
        
        # Action buttons (Clear and Speak) - below sentence box
        self.action_buttons_frame = tk.Frame(self.right_frame, bg=self.bg_color)
        self.action_buttons_frame.pack(fill=tk.X, pady=(40, 0))
        
        self.clear = self.create_action_button(self.action_buttons_frame, "Clear", self.red, self.clear_fun)
        self.clear.pack(side=tk.LEFT, padx=(0, 10), fill=tk.BOTH, expand=True)
        
        self.speak = self.create_action_button(self.action_buttons_frame, "Speak", self.green, self.speak_fun)
        self.speak.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Hidden panel for hand tracking visualization
        self.panel2 = tk.Label(self.root)
        self.panel2.place_forget()





        self.str = " "
        self.ccc=0
        self.word = " "
        self.current_symbol = "C"
        self.photo = "Empty"


        self.word1=" "
        self.word2 = " "
        self.word3 = " "
        self.word4 = " "

        # In-memory template image for drawing hand skeleton (no disk file required)
        self.white_template = np.ones((400, 400, 3), dtype=np.uint8) * 255

        # Run prediction not on every single frame to keep UI smooth
        self.prediction_interval = 3

        self.video_loop()
    
    def create_gradient_text(self):
        """Create gradient text effect for header"""
        # Update header with gradient-like colors (approximated)
        colors = [self.cyan_400, self.blue_500, self.purple_500]
        # Tkinter has no true gradients; use the primary gradient start color
        self.header_label.config(fg=self.cyan_400)
    
    def draw_glowing_border(self, canvas, x1, y1, x2, y2, color, width):
        """Draw a glowing border effect on canvas"""
        canvas.delete("border")
        # Draw multiple borders with decreasing opacity for glow effect
        glow_colors = [color, color, color]
        for i, glow_color in enumerate(glow_colors):
            canvas.create_rectangle(
                x1 + i, y1 + i, x2 - i, y2 - i,
                outline=glow_color,
                width=width - i,
                tags="border"
            )
    
    def draw_rounded_border(self, canvas, x1, y1, x2, y2, color, width, radius):
        """Draw a rounded rectangle border with glow effect on canvas"""
        canvas.delete("border")
        # Draw rounded rectangle border
        # Create rounded rectangle using arcs and lines
        r = radius
        # Top-left arc
        canvas.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, 
                         outline=color, width=width, style=tk.ARC, tags="border")
        # Top-right arc
        canvas.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, 
                         outline=color, width=width, style=tk.ARC, tags="border")
        # Bottom-right arc
        canvas.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, 
                         outline=color, width=width, style=tk.ARC, tags="border")
        # Bottom-left arc
        canvas.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, 
                         outline=color, width=width, style=tk.ARC, tags="border")
        # Top line
        canvas.create_line(x1 + r, y1, x2 - r, y1, fill=color, width=width, tags="border")
        # Right line
        canvas.create_line(x2, y1 + r, x2, y2 - r, fill=color, width=width, tags="border")
        # Bottom line
        canvas.create_line(x2 - r, y2, x1 + r, y2, fill=color, width=width, tags="border")
        # Left line
        canvas.create_line(x1, y2 - r, x1, y1 + r, fill=color, width=width, tags="border")
    
    def create_suggestion_button(self, parent, text):
        """Create a styled suggestion button with hover effects"""
        btn_frame = tk.Frame(parent, bg=self.bg_color, height=40)
        btn_frame.pack_propagate(False)
        btn_canvas = tk.Canvas(
            btn_frame,
            bg=self.dark_gray,
            highlightthickness=0,
            height=40,
            relief=tk.FLAT
        )
        btn_canvas.pack(fill=tk.BOTH, expand=True)
        
        def draw_button():
            btn_canvas.delete("bg", "hover", "border")
            width = btn_canvas.winfo_width()
            height = btn_canvas.winfo_height()
            if width > 1 and height > 1:
                r = 10
                # Fill background using rounded rectangle approach
                # Center rectangle
                btn_canvas.create_rectangle(
                    2 + r, 2, width-2 - r, height-2,
                    outline="",
                    fill=self.dark_gray,
                    tags="bg"
                )
                # Top and bottom rectangles
                btn_canvas.create_rectangle(
                    2, 2 + r, width-2, height-2 - r,
                    outline="",
                    fill=self.dark_gray,
                    tags="bg"
                )
                # Fill corner circles
                btn_canvas.create_oval(2, 2, 2 + 2*r, 2 + 2*r, outline="", fill=self.dark_gray, tags="bg")
                btn_canvas.create_oval(width-2 - 2*r, 2, width-2, 2 + 2*r, outline="", fill=self.dark_gray, tags="bg")
                btn_canvas.create_oval(width-2 - 2*r, height-2 - 2*r, width-2, height-2, outline="", fill=self.dark_gray, tags="bg")
                btn_canvas.create_oval(2, height-2 - 2*r, 2 + 2*r, height-2, outline="", fill=self.dark_gray, tags="bg")
                # Draw rounded rectangle border
                self.draw_rounded_border(btn_canvas, 2, 2, width-2, height-2, self.cyan_500, 2, r)
        
        btn_canvas.bind("<Configure>", lambda e: draw_button())
        draw_button()
        
        btn_label = tk.Label(
            btn_canvas,
            text=text,
            font=("Arial", 16, "bold"),
            bg=self.dark_gray,
            fg=self.cyan_400
        )
        btn_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Hover effects
        def on_enter(e):
            width = btn_canvas.winfo_width()
            height = btn_canvas.winfo_height()
            if width > 1 and height > 1:
                btn_canvas.delete("hover", "bg", "border")
                r = 10
                # Fill with cyan using rounded rectangle approach
                # Center rectangle
                btn_canvas.create_rectangle(
                    2 + r, 2, width-2 - r, height-2,
                    outline="",
                    fill=self.cyan_600,
                    tags="hover"
                )
                # Top and bottom rectangles
                btn_canvas.create_rectangle(
                    2, 2 + r, width-2, height-2 - r,
                    outline="",
                    fill=self.cyan_600,
                    tags="hover"
                )
                # Fill corner circles
                btn_canvas.create_oval(2, 2, 2 + 2*r, 2 + 2*r, outline="", fill=self.cyan_600, tags="hover")
                btn_canvas.create_oval(width-2 - 2*r, 2, width-2, 2 + 2*r, outline="", fill=self.cyan_600, tags="hover")
                btn_canvas.create_oval(width-2 - 2*r, height-2 - 2*r, width-2, height-2, outline="", fill=self.cyan_600, tags="hover")
                btn_canvas.create_oval(2, height-2 - 2*r, 2 + 2*r, height-2, outline="", fill=self.cyan_600, tags="hover")
                # Draw rounded rectangle border
                self.draw_rounded_border(btn_canvas, 2, 2, width-2, height-2, self.cyan_600, 2, r)
            btn_canvas.config(bg=self.cyan_600)
            btn_label.config(bg=self.cyan_600, fg=self.bg_black)
            btn_label.lift()
        
        def on_leave(e):
            btn_canvas.delete("hover")
            btn_canvas.config(bg=self.dark_gray)
            btn_label.config(bg=self.dark_gray, fg=self.cyan_400)
            draw_button()  # Redraw the border
        
        btn_canvas.bind("<Enter>", on_enter)
        btn_canvas.bind("<Leave>", on_leave)
        btn_label.bind("<Enter>", on_enter)
        btn_label.bind("<Leave>", on_leave)
        
        # Store references for updating
        btn_frame.btn_canvas = btn_canvas
        btn_frame.btn_label = btn_label
        btn_frame.config_command = lambda t, c: self.update_suggestion_button(btn_frame, t, c)
        
        return btn_frame
    
    def update_suggestion_button(self, btn_frame, text, command):
        """Update suggestion button text and command"""
        btn_frame.btn_label.config(text=text)
        if command:
            btn_frame.btn_canvas.bind("<Button-1>", lambda e: command())
            btn_frame.btn_label.bind("<Button-1>", lambda e: command())
    
    def create_action_button(self, parent, text, hover_color, command):
        """Create action button (Clear/Speak) with hover effects"""
        btn_frame = tk.Frame(parent, bg=self.bg_color, height=40)
        btn_frame.pack_propagate(False)
        btn_canvas = tk.Canvas(
            btn_frame,
            bg=self.dark_gray,
            highlightthickness=0,
            relief=tk.FLAT,
            height=40
        )
        btn_canvas.pack(fill=tk.BOTH, expand=True)
        
        def draw_button():
            btn_canvas.delete("bg", "hover", "border")
            width = btn_canvas.winfo_width()
            height = btn_canvas.winfo_height()
            if width > 1 and height > 1:
                r = 10
                # Fill background using rounded rectangle approach
                # Center rectangle
                btn_canvas.create_rectangle(
                    2 + r, 2, width-2 - r, height-2,
                    outline="",
                    fill=self.dark_gray,
                    tags="bg"
                )
                # Top and bottom rectangles
                btn_canvas.create_rectangle(
                    2, 2 + r, width-2, height-2 - r,
                    outline="",
                    fill=self.dark_gray,
                    tags="bg"
                )
                # Fill corner circles
                btn_canvas.create_oval(2, 2, 2 + 2*r, 2 + 2*r, outline="", fill=self.dark_gray, tags="bg")
                btn_canvas.create_oval(width-2 - 2*r, 2, width-2, 2 + 2*r, outline="", fill=self.dark_gray, tags="bg")
                btn_canvas.create_oval(width-2 - 2*r, height-2 - 2*r, width-2, height-2, outline="", fill=self.dark_gray, tags="bg")
                btn_canvas.create_oval(2, height-2 - 2*r, 2 + 2*r, height-2, outline="", fill=self.dark_gray, tags="bg")
                # Draw rounded rectangle border
                self.draw_rounded_border(btn_canvas, 2, 2, width-2, height-2, self.cyan, 2, r)
        
        btn_canvas.bind("<Configure>", lambda e: draw_button())
        draw_button()
        
        btn_label = tk.Label(
            btn_canvas,
            text=text,
            font=("Arial", 16, "bold"),
            bg=self.dark_gray,
            fg=self.white
        )
        btn_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Hover effects
        def on_enter(e):
            width = btn_canvas.winfo_width()
            height = btn_canvas.winfo_height()
            if width > 1 and height > 1:
                btn_canvas.delete("hover", "bg", "border")
                r = 10
                # Fill with hover color using rounded rectangle approach
                # Center rectangle
                btn_canvas.create_rectangle(
                    2 + r, 2, width-2 - r, height-2,
                    outline="",
                    fill=hover_color,
                    tags="hover"
                )
                # Top and bottom rectangles
                btn_canvas.create_rectangle(
                    2, 2 + r, width-2, height-2 - r,
                    outline="",
                    fill=hover_color,
                    tags="hover"
                )
                # Fill corner circles
                btn_canvas.create_oval(2, 2, 2 + 2*r, 2 + 2*r, outline="", fill=hover_color, tags="hover")
                btn_canvas.create_oval(width-2 - 2*r, 2, width-2, 2 + 2*r, outline="", fill=hover_color, tags="hover")
                btn_canvas.create_oval(width-2 - 2*r, height-2 - 2*r, width-2, height-2, outline="", fill=hover_color, tags="hover")
                btn_canvas.create_oval(2, height-2 - 2*r, 2 + 2*r, height-2, outline="", fill=hover_color, tags="hover")
                # Draw rounded rectangle border
                self.draw_rounded_border(btn_canvas, 2, 2, width-2, height-2, hover_color, 2, r)
            btn_canvas.config(bg=hover_color)
            btn_label.config(bg=hover_color, fg=self.bg_color)
            btn_label.lift()
        
        def on_leave(e):
            btn_canvas.delete("hover")
            btn_canvas.config(bg=self.dark_gray)
            btn_label.config(bg=self.dark_gray, fg=self.white)
            draw_button()  # Redraw the border
        
        def on_click(e):
            command()
        
        btn_canvas.bind("<Enter>", on_enter)
        btn_canvas.bind("<Leave>", on_leave)
        btn_canvas.bind("<Button-1>", on_click)
        btn_label.bind("<Enter>", on_enter)
        btn_label.bind("<Leave>", on_leave)
        btn_label.bind("<Button-1>", on_click)
        btn_label.config(cursor="hand2")
        btn_canvas.config(cursor="hand2")
        
        return btn_frame
    
    def animate_live_badge(self):
        """Legacy hook for compatibility; LIVE badge is now static."""
        # Drawing is handled by draw_live_badge defined in __init__
        pass

    def video_loop(self):
        try:
            ok, frame = self.vs.read()
            if not ok or frame is None:
                # Camera not ready; try again shortly
                self.root.after(10, self.video_loop)
                return
            cv2image = cv2.flip(frame, 1)
            if cv2image is not None and cv2image.size != 0:
                hands, _ = hd.findHands(cv2image, draw=False, flipType=True)
                cv2image_copy = np.array(cv2image)
                cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
                # Resize to fit camera panel dynamically
                panel_width = self.panel.winfo_width()
                panel_height = self.panel.winfo_height()
                if panel_width > 1 and panel_height > 1:
                    cv2image_resized = cv2.resize(cv2image, (panel_width, panel_height))
                else:
                    cv2image_resized = cv2.resize(cv2image, (600, 500))
                self.current_image = Image.fromarray(cv2image_resized)
                imgtk = ImageTk.PhotoImage(image=self.current_image)
                self.panel.imgtk = imgtk
                self.panel.config(image=imgtk)

                if hands:
                    hand = hands[0]
                    x, y, w, h = hand['bbox']
                    H, W = cv2image_copy.shape[:2]
                    x1 = max(x - offset, 0)
                    y1 = max(y - offset, 0)
                    x2 = min(x + w + offset, W)
                    y2 = min(y + h + offset, H)
                    if x2 <= x1 or y2 <= y1:
                        self.root.after(10, self.video_loop)
                        return
                    image = cv2image_copy[y1:y2, x1:x2]
                    if image is None or image.size == 0:
                        self.root.after(10, self.video_loop)
                        return

                    # Use preloaded template instead of reading from disk every frame
                    white = self.white_template.copy() if self.white_template is not None else None
                    if white is None:
                        white = np.zeros((400, 400, 3), dtype=np.uint8)
                    # img_final=img_final1=img_final2=0
                    if image.size != 0:
                        handz, _ = hd2.findHands(image, draw=False, flipType=True)
                        self.ccc += 1
                        if handz:
                            hand = handz[0]
                            self.pts = hand['lmList']
                            # x1,y1,w1,h1=hand['bbox']

                            os = ((400 - w) // 2) - 15
                            os1 = ((400 - h) // 2) - 15
                            for t in range(0, 4, 1):
                                cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                         (0, 255, 0), 3)
                            for t in range(5, 8, 1):
                                cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                         (0, 255, 0), 3)
                            for t in range(9, 12, 1):
                                cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                         (0, 255, 0), 3)
                            for t in range(13, 16, 1):
                                cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                         (0, 255, 0), 3)
                            for t in range(17, 20, 1):
                                cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                         (0, 255, 0), 3)
                            cv2.line(white, (self.pts[5][0] + os, self.pts[5][1] + os1), (self.pts[9][0] + os, self.pts[9][1] + os1), (0, 255, 0),
                                     3)
                            cv2.line(white, (self.pts[9][0] + os, self.pts[9][1] + os1), (self.pts[13][0] + os, self.pts[13][1] + os1), (0, 255, 0),
                                     3)
                            cv2.line(white, (self.pts[13][0] + os, self.pts[13][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1),
                                     (0, 255, 0), 3)
                            cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[5][0] + os, self.pts[5][1] + os1), (0, 255, 0),
                                     3)
                            cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0),
                                     3)

                            for i in range(21):
                                cv2.circle(white, (self.pts[i][0] + os, self.pts[i][1] + os1), 2, (0, 0, 255), 1)

                            res = white

                            # Throttle prediction to every Nth processed frame
                            if self.ccc % self.prediction_interval == 0:
                                self.predict(res)

                                self.current_image2 = Image.fromarray(res)
                                imgtk = ImageTk.PhotoImage(image=self.current_image2)
                                self.panel2.imgtk = imgtk
                                self.panel2.config(image=imgtk)

                                if self.current_symbol and self.current_symbol.strip():
                                    self.panel3.config(text=self.current_symbol, font=("Arial", 32, "bold"), fg=self.cyan_400)
                                    self.char_canvas.itemconfig("cursor", state="hidden")
                                else:
                                    self.panel3.config(text="")
                                    self.char_canvas.itemconfig("cursor", state="normal")

                                #self.panel4.config(text=self.word, font=("Courier", 30))

                                self.update_suggestion_button(self.b1, self.word1, self.action1)
                                self.update_suggestion_button(self.b2, self.word2, self.action2)
                                self.update_suggestion_button(self.b3, self.word3, self.action3)
                                self.update_suggestion_button(self.b4, self.word4, self.action4)

                if self.str.strip():
                    self.panel5.config(text=self.str, font=("Arial", 20), fg=self.white)
                else:
                    self.panel5.config(text="Your sentence will appear here...", font=("Arial", 20), fg=self.gray_400)
        except Exception:
            # Fallback processing without crashing the loop
            hands = hd.findHands(cv2image, draw=False, flipType=True)
            cv2image_copy=np.array(cv2image)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
            # Resize to fit camera panel dynamically
            panel_width = self.panel.winfo_width()
            panel_height = self.panel.winfo_height()
            if panel_width > 1 and panel_height > 1:
                cv2image_resized = cv2.resize(cv2image, (panel_width, panel_height))
            else:
                cv2image_resized = cv2.resize(cv2image, (600, 500))
            self.current_image = Image.fromarray(cv2image_resized)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                image = cv2image_copy[y - offset:y + h + offset, x - offset:x + w + offset]

                # Use preloaded template instead of reading from disk every frame
                white = self.white_template.copy() if self.white_template is not None else None
                if white is None:
                    white = np.zeros((400, 400, 3), dtype=np.uint8)
                # img_final=img_final1=img_final2=0

                handz = hd2.findHands(image, draw=False, flipType=True)
                self.ccc += 1
                if handz:
                    hand = handz[0]
                    self.pts = hand['lmList']
                    # x1,y1,w1,h1=hand['bbox']

                    os = ((400 - w) // 2) - 15
                    os1 = ((400 - h) // 2) - 15
                    for t in range(0, 4, 1):
                        cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                 (0, 255, 0), 3)
                    for t in range(5, 8, 1):
                        cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                 (0, 255, 0), 3)
                    for t in range(9, 12, 1):
                        cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                 (0, 255, 0), 3)
                    for t in range(13, 16, 1):
                        cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                 (0, 255, 0), 3)
                    for t in range(17, 20, 1):
                        cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                 (0, 255, 0), 3)
                    cv2.line(white, (self.pts[5][0] + os, self.pts[5][1] + os1), (self.pts[9][0] + os, self.pts[9][1] + os1), (0, 255, 0),
                             3)
                    cv2.line(white, (self.pts[9][0] + os, self.pts[9][1] + os1), (self.pts[13][0] + os, self.pts[13][1] + os1), (0, 255, 0),
                             3)
                    cv2.line(white, (self.pts[13][0] + os, self.pts[13][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1),
                             (0, 255, 0), 3)
                    cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[5][0] + os, self.pts[5][1] + os1), (0, 255, 0),
                             3)
                    cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0),
                             3)

                    for i in range(21):
                        cv2.circle(white, (self.pts[i][0] + os, self.pts[i][1] + os1), 2, (0, 0, 255), 1)

                    res = white

                    # Throttle prediction to every Nth processed frame
                    if self.ccc % self.prediction_interval == 0:
                        self.predict(res)

                        self.current_image2 = Image.fromarray(res)
                        imgtk = ImageTk.PhotoImage(image=self.current_image2)
                        self.panel2.imgtk = imgtk
                        self.panel2.config(image=imgtk)

                        if self.current_symbol and self.current_symbol.strip():
                            self.panel3.config(text=self.current_symbol, font=("Arial", 32, "bold"), fg=self.cyan_400)
                            self.char_canvas.itemconfig("cursor", state="hidden")
                        else:
                            self.panel3.config(text="")
                            self.char_canvas.itemconfig("cursor", state="normal")

                        #self.panel4.config(text=self.word, font=("Courier", 30))

                        self.update_suggestion_button(self.b1, self.word1, self.action1)
                        self.update_suggestion_button(self.b2, self.word2, self.action2)
                        self.update_suggestion_button(self.b3, self.word3, self.action3)
                        self.update_suggestion_button(self.b4, self.word4, self.action4)

            if self.str.strip():
                self.panel5.config(text=self.str, font=("Arial", 24), fg=self.white)
            else:
                self.panel5.config(text="Your sentence will appear here...", font=("Arial", 24), fg=self.gray_400)
        except Exception:
            # Swallow unexpected errors to keep video loop running
            pass
        finally:
            # Slight delay keeps UI responsive and reduces CPU load
            self.root.after(10, self.video_loop)

    def distance(self,x,y):
        return math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))

    def action1(self):
        idx_space = self.str.rfind(" ")
        idx_word = self.str.find(self.word, idx_space)
        last_idx = len(self.str)
        self.str = self.str[:idx_word]
        self.str = self.str + self.word1.upper()


    def action2(self):
        idx_space = self.str.rfind(" ")
        idx_word = self.str.find(self.word, idx_space)
        last_idx = len(self.str)
        self.str=self.str[:idx_word]
        self.str=self.str+self.word2.upper()
        #self.str[idx_word:last_idx] = self.word2


    def action3(self):
        idx_space = self.str.rfind(" ")
        idx_word = self.str.find(self.word, idx_space)
        last_idx = len(self.str)
        self.str = self.str[:idx_word]
        self.str = self.str + self.word3.upper()



    def action4(self):
        idx_space = self.str.rfind(" ")
        idx_word = self.str.find(self.word, idx_space)
        last_idx = len(self.str)
        self.str = self.str[:idx_word]
        self.str = self.str + self.word4.upper()


    def speak_fun(self):
        txt = (self.str or "").strip()
        if not txt:
            return
        # Speak the full sentence instead of only the last word
        self.speak_engine.stop()
        self.speak_engine.say(txt)
        self.speak_engine.runAndWait()


    def clear_fun(self):
        self.str=" "
        self.word1 = " "
        self.word2 = " "
        self.word3 = " "
        self.word4 = " "
        self.update_suggestion_button(self.b1, " ", None)
        self.update_suggestion_button(self.b2, " ", None)
        self.update_suggestion_button(self.b3, " ", None)
        self.update_suggestion_button(self.b4, " ", None)
        self.panel5.config(text="Your sentence will appear here...", font=("Arial", 20), fg=self.gray_400)
        # Also clear the character box display and show the cursor again
        self.current_symbol = ""
        self.panel3.config(text="")
        self.char_canvas.itemconfig("cursor", state="normal")

    def predict(self, test_image):
        white=test_image
        white = white.reshape(1, 400, 400, 3)
        prob = np.array(self.model.predict(white)[0], dtype='float32')
        ch1 = np.argmax(prob, axis=0)
        prob[ch1] = 0
        ch2 = np.argmax(prob, axis=0)
        prob[ch2] = 0
        ch3 = np.argmax(prob, axis=0)
        prob[ch3] = 0

        pl = [ch1, ch2]

        # condition for [Aemnst]
        l = [[5, 2], [5, 3], [3, 5], [3, 6], [3, 0], [3, 2], [6, 4], [6, 1], [6, 2], [6, 6], [6, 7], [6, 0], [6, 5],
             [4, 1], [1, 0], [1, 1], [6, 3], [1, 6], [5, 6], [5, 1], [4, 5], [1, 4], [1, 5], [2, 0], [2, 6], [4, 6],
             [1, 0], [5, 7], [1, 6], [6, 1], [7, 6], [2, 5], [7, 1], [5, 4], [7, 0], [7, 5], [7, 2]]
        if pl in l:
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1]):
                ch1 = 0

        # condition for [o][s]
        l = [[2, 2], [2, 1]]
        if pl in l:
            if (self.pts[5][0] < self.pts[4][0]):
                ch1 = 0

        # condition for [c0][aemnst]
        l = [[0, 0], [0, 6], [0, 2], [0, 5], [0, 1], [0, 7], [5, 2], [7, 6], [7, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[4][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][
                0] and self.pts[0][0] > self.pts[20][0]) and self.pts[5][0] > self.pts[4][0]:
                ch1 = 2

        # condition for [c0][aemnst]
        l = [[6, 0], [6, 6], [6, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[8], self.pts[16]) < 52:
                ch1 = 2


        # condition for [gh][bdfikruvw]
        l = [[1, 4], [1, 5], [1, 6], [1, 3], [1, 0]]
        pl = [ch1, ch2]

        if pl in l:
            if self.pts[6][1] > self.pts[8][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][1] and self.pts[0][0] < self.pts[8][
                0] and self.pts[0][0] < self.pts[12][0] and self.pts[0][0] < self.pts[16][0] and self.pts[0][0] < self.pts[20][0]:
                ch1 = 3



        # con for [gh][l]
        l = [[4, 6], [4, 1], [4, 5], [4, 3], [4, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[4][0] > self.pts[0][0]:
                ch1 = 3

        # con for [gh][pqz]
        l = [[5, 3], [5, 0], [5, 7], [5, 4], [5, 2], [5, 1], [5, 5]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[2][1] + 15 < self.pts[16][1]:
                ch1 = 3

        # con for [l][x]
        l = [[6, 4], [6, 1], [6, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[4], self.pts[11]) > 55:
                ch1 = 4

        # con for [l][d]
        l = [[1, 4], [1, 6], [1, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.distance(self.pts[4], self.pts[11]) > 50) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 4

        # con for [l][gh]
        l = [[3, 6], [3, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[4][0] < self.pts[0][0]):
                ch1 = 4

        # con for [l][c0]
        l = [[2, 2], [2, 5], [2, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[1][0] < self.pts[12][0]):
                ch1 = 4

        # con for [l][c0]
        l = [[2, 2], [2, 5], [2, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[1][0] < self.pts[12][0]):
                ch1 = 4

        # con for [gh][z]
        l = [[3, 6], [3, 5], [3, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1]) and self.pts[4][1] > self.pts[10][1]:
                ch1 = 5

        # con for [gh][pq]
        l = [[3, 2], [3, 1], [3, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[4][1] + 17 > self.pts[8][1] and self.pts[4][1] + 17 > self.pts[12][1] and self.pts[4][1] + 17 > self.pts[16][1] and self.pts[4][
                1] + 17 > self.pts[20][1]:
                ch1 = 5

        # con for [l][pqz]
        l = [[4, 4], [4, 5], [4, 2], [7, 5], [7, 6], [7, 0]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[4][0] > self.pts[0][0]:
                ch1 = 5

        # con for [pqz][aemnst]
        l = [[0, 2], [0, 6], [0, 1], [0, 5], [0, 0], [0, 7], [0, 4], [0, 3], [2, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[0][0] < self.pts[8][0] and self.pts[0][0] < self.pts[12][0] and self.pts[0][0] < self.pts[16][0] and self.pts[0][0] < self.pts[20][0]:
                ch1 = 5

        # con for [pqz][yj]
        l = [[5, 7], [5, 2], [5, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[3][0] < self.pts[0][0]:
                ch1 = 7

        # con for [l][yj]
        l = [[4, 6], [4, 2], [4, 4], [4, 1], [4, 5], [4, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[6][1] < self.pts[8][1]:
                ch1 = 7

        # con for [x][yj]
        l = [[6, 7], [0, 7], [0, 1], [0, 0], [6, 4], [6, 6], [6, 5], [6, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[18][1] > self.pts[20][1]:
                ch1 = 7

        # condition for [x][aemnst]
        l = [[0, 4], [0, 2], [0, 3], [0, 1], [0, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[5][0] > self.pts[16][0]:
                ch1 = 6


        # condition for [yj][x]
        l = [[7, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[18][1] < self.pts[20][1] and self.pts[8][1] < self.pts[10][1]:
                ch1 = 6

        # condition for [c0][x]
        l = [[2, 1], [2, 2], [2, 6], [2, 7], [2, 0]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[8], self.pts[16]) > 50:
                ch1 = 6

        # con for [l][x]

        l = [[4, 6], [4, 2], [4, 1], [4, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[4], self.pts[11]) < 60:
                ch1 = 6

        # con for [x][d]
        l = [[1, 4], [1, 6], [1, 0], [1, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[5][0] - self.pts[4][0] - 15 > 0:
                ch1 = 6

        # con for [b][pqz]
        l = [[5, 0], [5, 1], [5, 4], [5, 5], [5, 6], [6, 1], [7, 6], [0, 2], [7, 1], [7, 4], [6, 6], [7, 2], [5, 0],
             [6, 3], [6, 4], [7, 5], [7, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][
                1]):
                ch1 = 1

        # con for [f][pqz]
        l = [[6, 1], [6, 0], [0, 3], [6, 4], [2, 2], [0, 6], [6, 2], [7, 6], [4, 6], [4, 1], [4, 2], [0, 2], [7, 1],
             [7, 4], [6, 6], [7, 2], [7, 5], [7, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and
                    self.pts[18][1] > self.pts[20][1]):
                ch1 = 1

        l = [[6, 1], [6, 0], [4, 2], [4, 1], [4, 6], [4, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and
                    self.pts[18][1] > self.pts[20][1]):
                ch1 = 1

        # con for [d][pqz]
        fg = 19
        l = [[5, 0], [3, 4], [3, 0], [3, 1], [3, 5], [5, 5], [5, 4], [5, 1], [7, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] < self.pts[20][1]) and (self.pts[2][0] < self.pts[0][0]) and self.pts[4][1] > self.pts[14][1]):
                ch1 = 1

        l = [[4, 1], [4, 2], [4, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.distance(self.pts[4], self.pts[11]) < 50) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 1

        l = [[3, 4], [3, 0], [3, 1], [3, 5], [3, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] < self.pts[20][1]) and (self.pts[2][0] < self.pts[0][0]) and self.pts[14][1] < self.pts[4][1]):
                ch1 = 1

        l = [[6, 6], [6, 4], [6, 1], [6, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[5][0] - self.pts[4][0] - 15 < 0:
                ch1 = 1

        # con for [i][pqz]
        l = [[5, 4], [5, 5], [5, 1], [0, 3], [0, 7], [5, 0], [0, 2], [6, 2], [7, 5], [7, 1], [7, 6], [7, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] > self.pts[20][1])):
                ch1 = 1

        # con for [yj][bfdi]
        l = [[1, 5], [1, 7], [1, 1], [1, 6], [1, 3], [1, 0]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[4][0] < self.pts[5][0] + 15) and (
            (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
             self.pts[18][1] > self.pts[20][1])):
                ch1 = 7

        # con for [uvr]
        l = [[5, 5], [5, 0], [5, 4], [5, 1], [4, 6], [4, 1], [7, 6], [3, 0], [3, 5]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] < self.pts[20][1])) and self.pts[4][1] > self.pts[14][1]:
                ch1 = 1

        # con for [w]
        fg = 13
        l = [[3, 5], [3, 0], [3, 6], [5, 1], [4, 1], [2, 0], [5, 0], [5, 5]]
        pl = [ch1, ch2]
        if pl in l:
            if not (self.pts[0][0] + fg < self.pts[8][0] and self.pts[0][0] + fg < self.pts[12][0] and self.pts[0][0] + fg < self.pts[16][0] and
                    self.pts[0][0] + fg < self.pts[20][0]) and not (
                    self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][0] and self.pts[0][0] > self.pts[20][
                0]) and self.distance(self.pts[4], self.pts[11]) < 50:
                ch1 = 1

        # con for [w]

        l = [[5, 0], [5, 5], [0, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1]:
                ch1 = 1

        # -------------------------condn for 8 groups  ends

        # -------------------------condn for subgroups  starts
        #
        if ch1 == 0:
            ch1 = 'S'
            if self.pts[4][0] < self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][0] and self.pts[4][0] < self.pts[18][0]:
                ch1 = 'A'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][0] and self.pts[4][0] < self.pts[18][
                0] and self.pts[4][1] < self.pts[14][1] and self.pts[4][1] < self.pts[18][1]:
                ch1 = 'T'
            if self.pts[4][1] > self.pts[8][1] and self.pts[4][1] > self.pts[12][1] and self.pts[4][1] > self.pts[16][1] and self.pts[4][1] > self.pts[20][1]:
                ch1 = 'E'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][0] > self.pts[14][0] and self.pts[4][1] < self.pts[18][1]:
                ch1 = 'M'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][1] < self.pts[18][1] and self.pts[4][1] < self.pts[14][1]:
                ch1 = 'N'

        if ch1 == 2:
            if self.distance(self.pts[12], self.pts[4]) > 42:
                ch1 = 'C'
            else:
                ch1 = 'O'

        if ch1 == 3:
            if (self.distance(self.pts[8], self.pts[12])) > 72:
                ch1 = 'G'
            else:
                ch1 = 'H'

        if ch1 == 7:
            if self.distance(self.pts[8], self.pts[4]) > 42:
                ch1 = 'Y'
            else:
                ch1 = 'J'

        if ch1 == 4:
            ch1 = 'L'

        if ch1 == 6:
            ch1 = 'X'

        if ch1 == 5:
            if self.pts[4][0] > self.pts[12][0] and self.pts[4][0] > self.pts[16][0] and self.pts[4][0] > self.pts[20][0]:
                if self.pts[8][1] < self.pts[5][1]:
                    ch1 = 'Z'
                else:
                    ch1 = 'Q'
            else:
                ch1 = 'P'

        if ch1 == 1:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][
                1]):
                ch1 = 'B'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1]):
                ch1 = 'D'
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][
                1]):
                ch1 = 'F'
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] > self.pts[20][
                1]):
                ch1 = 'I'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1]):
                ch1 = 'W'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1]) and self.pts[4][1] < self.pts[9][1]:
                ch1 = 'K'
            if ((self.distance(self.pts[8], self.pts[12]) - self.distance(self.pts[6], self.pts[10])) < 8) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 'U'
            if ((self.distance(self.pts[8], self.pts[12]) - self.distance(self.pts[6], self.pts[10])) >= 8) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]) and (self.pts[4][1] > self.pts[9][1]):
                ch1 = 'V'

            if (self.pts[8][0] > self.pts[12][0]) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 'R'

        if ch1 == 1 or ch1 =='E' or ch1 =='S' or ch1 =='X' or ch1 =='Y' or ch1 =='B':
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1=" "
        if ch1 == 'E' or ch1=='Y' or ch1=='B':
            if (self.pts[4][0] < self.pts[5][0]) and (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1="next"


        if ch1 == 'Next' or 'B' or 'C' or 'H' or 'F' or 'X':
            if (self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][0] and self.pts[0][0] > self.pts[20][0]) and (self.pts[4][1] < self.pts[8][1] and self.pts[4][1] < self.pts[12][1] and self.pts[4][1] < self.pts[16][1] and self.pts[4][1] < self.pts[20][1]) and (self.pts[4][1] < self.pts[6][1] and self.pts[4][1] < self.pts[10][1] and self.pts[4][1] < self.pts[14][1] and self.pts[4][1] < self.pts[18][1]):
                ch1 = 'Backspace'


        if ch1=="next" and self.prev_char!="next":
            if self.ten_prev_char[(self.count-2)%10]!="next":
                if self.ten_prev_char[(self.count-2)%10]=="Backspace":
                    self.str=self.str[0:-1]
                else:
                    if self.ten_prev_char[(self.count - 2) % 10] != "Backspace":
                        self.str = self.str + self.ten_prev_char[(self.count-2)%10]
            else:
                if self.ten_prev_char[(self.count - 0) % 10] != "Backspace":
                    self.str = self.str + self.ten_prev_char[(self.count - 0) % 10]


        if ch1=="  " and self.prev_char!="  ":
            self.str = self.str + "  "

        self.prev_char = ch1
        # Ensure current_symbol is always a string for UI checks like .strip()
        self.current_symbol = str(ch1)
        self.count += 1
        self.ten_prev_char[self.count%10]=ch1


        if len(self.str.strip())!=0:
            st=self.str.rfind(" ")
            ed=len(self.str)
            word=self.str[st+1:ed]
            self.word=word
            if len(word.strip())!=0:
                ddd.check(word)
                lenn = len(ddd.suggest(word))
                if lenn >= 4:
                    self.word4 = ddd.suggest(word)[3]

                if lenn >= 3:
                    self.word3 = ddd.suggest(word)[2]

                if lenn >= 2:
                    self.word2 = ddd.suggest(word)[1]

                if lenn >= 1:
                    self.word1 = ddd.suggest(word)[0]
            else:
                self.word1 = " "
                self.word2 = " "
                self.word3 = " "
                self.word4 = " "


    def destructor(self):
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = Application()
    app.root.mainloop()
