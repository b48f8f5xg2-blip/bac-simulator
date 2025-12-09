"""
Modern Apple-Inspired GUI for BAC Simulator
Clean, minimalist design with form-based profile and chatbot interface
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from datetime import datetime, timedelta
import threading
import math

class BACSimulatorGUI:
    def __init__(self, root, calculator, chatbot):
        self.root = root
        self.calculator = calculator
        self.chatbot = chatbot
        self.root.title("BAC Simulator")
        self.root.geometry("1400x900")
        
        # BAC Simulator Design System Colors
        self.colors = {
            'bg': '#FFFFFF',
            'secondary_bg': '#F5F5F7',
            'tertiary_bg': '#E8E8ED',
            'text': '#4A4A63',           # Dark Slate
            'secondary_text': '#6F6F77',
            'accent': '#00BFAE',          # Primary Teal
            'accent_dark': '#004040',     # Dark Teal
            'accent_light': '#E0F7F5',
            'green': '#029922',           # Green Accent (safe)
            'caution': '#F59E0B',         # Yellow (caution)
            'orange': '#F97316',          # Orange (warning)
            'red': '#EF4444',             # Red (danger)
            'critical': '#991B1B',        # Dark red (critical)
            'border': '#BFBEBE',          # Light Neutral
            'neutral': '#BFBEBE'          # Light Neutral
        }

        # BAC status color mapping
        self.bac_colors = {
            'safe': '#029922',
            'caution': '#F59E0B',
            'warning': '#F97316',
            'danger': '#EF4444',
            'critical': '#991B1B'
        }
        
        self.setup_styles()
        self.profile_complete = False
        self.create_layout()
        self.update_display()

    def setup_styles(self):
        """Setup modern font sizes and styles"""
        self.fonts = {
            'title_large': ('Helvetica', 28, 'bold'),
            'title': ('Helvetica', 20, 'bold'),
            'subtitle': ('Helvetica', 16, 'bold'),
            'body': ('Helvetica', 14),
            'body_small': ('Helvetica', 12),
            'caption': ('Helvetica', 11),
        }

    def create_layout(self):
        """Create modern layout"""
        self.root.configure(bg=self.colors['bg'])
        
        # Main container with proper padding
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Top section: Profile form
        self.create_profile_section(main_container)
        
        # Divider
        divider = tk.Frame(main_container, bg=self.colors['border'], height=1)
        divider.pack(fill=tk.X, padx=20, pady=0)
        
        # Middle section: Chat and BAC display side by side
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side: Chat
        self.create_chat_section(content_frame)
        
        # Right side: BAC Display and Timeline
        self.create_display_section(content_frame)

    def create_profile_section(self, parent):
        """Create modern profile form section"""
        profile_frame = tk.Frame(parent, bg=self.colors['bg'])
        profile_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Title
        title = tk.Label(profile_frame, text="Your Profile", font=self.fonts['title'],
                        bg=self.colors['bg'], fg=self.colors['text'])
        title.pack(anchor=tk.W, pady=(0, 15))
        
        # Profile inputs in a grid
        inputs_frame = tk.Frame(profile_frame, bg=self.colors['bg'])
        inputs_frame.pack(fill=tk.X)
        
        # Row 1
        tk.Label(inputs_frame, text="Sex", font=self.fonts['body_small'],
                bg=self.colors['bg'], fg=self.colors['secondary_text']).grid(row=0, column=0, sticky=tk.W, padx=(0, 15), pady=5)
        self.sex_var = tk.StringVar()
        sex_combo = ttk.Combobox(inputs_frame, textvariable=self.sex_var, 
                                 values=['Male', 'Female'], state='readonly', width=12)
        sex_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 30), pady=5)
        
        tk.Label(inputs_frame, text="Weight (lbs)", font=self.fonts['body_small'],
                bg=self.colors['bg'], fg=self.colors['secondary_text']).grid(row=0, column=2, sticky=tk.W, padx=(0, 15), pady=5)
        self.weight_var = tk.StringVar()
        weight_entry = tk.Entry(inputs_frame, textvariable=self.weight_var, width=12,
                               font=self.fonts['body_small'], bg=self.colors['secondary_bg'],
                               fg=self.colors['text'], relief=tk.FLAT, bd=0)
        weight_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 30), pady=5)
        
        tk.Label(inputs_frame, text="Height", font=self.fonts['body_small'],
                bg=self.colors['bg'], fg=self.colors['secondary_text']).grid(row=0, column=4, sticky=tk.W, padx=(0, 15), pady=5)
        self.height_var = tk.StringVar()
        height_entry = tk.Entry(inputs_frame, textvariable=self.height_var, width=12,
                               font=self.fonts['body_small'], bg=self.colors['secondary_bg'],
                               fg=self.colors['text'], relief=tk.FLAT, bd=0)
        height_entry.grid(row=0, column=5, sticky=tk.W, padx=(0, 30), pady=5)
        
        tk.Label(inputs_frame, text="Age", font=self.fonts['body_small'],
                bg=self.colors['bg'], fg=self.colors['secondary_text']).grid(row=0, column=6, sticky=tk.W, padx=(0, 15), pady=5)
        self.age_var = tk.StringVar()
        age_entry = tk.Entry(inputs_frame, textvariable=self.age_var, width=8,
                            font=self.fonts['body_small'], bg=self.colors['secondary_bg'],
                            fg=self.colors['text'], relief=tk.FLAT, bd=0)
        age_entry.grid(row=0, column=7, sticky=tk.W, padx=(0, 30), pady=5)
        
        # Row 2
        tk.Label(inputs_frame, text="Drink Frequency", font=self.fonts['body_small'],
                bg=self.colors['bg'], fg=self.colors['secondary_text']).grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=5)
        self.chronic_var = tk.StringVar()
        freq_combo = ttk.Combobox(inputs_frame, textvariable=self.chronic_var,
                                  values=['Rarely', 'Regularly'], state='readonly', width=12)
        freq_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 30), pady=5)
        
        tk.Label(inputs_frame, text="Started Drinking", font=self.fonts['body_small'],
                bg=self.colors['bg'], fg=self.colors['secondary_text']).grid(row=1, column=2, sticky=tk.W, padx=(0, 15), pady=5)
        self.start_time_var = tk.StringVar()
        time_entry = tk.Entry(inputs_frame, textvariable=self.start_time_var, width=12,
                             font=self.fonts['body_small'], bg=self.colors['secondary_bg'],
                             fg=self.colors['text'], relief=tk.FLAT, bd=0)
        time_entry.grid(row=1, column=3, sticky=tk.W, padx=(0, 30), pady=5)
        
        # Apply button
        apply_btn = tk.Button(inputs_frame, text="Apply Profile", font=self.fonts['body_small'],
                             bg=self.colors['accent'], fg='white', relief=tk.FLAT, bd=0,
                             padx=20, pady=8, command=self.apply_profile)
        apply_btn.grid(row=1, column=4, sticky=tk.W, padx=(0, 10), pady=5)
        
        # Status label
        self.profile_status = tk.Label(inputs_frame, text="", font=self.fonts['caption'],
                                      bg=self.colors['bg'], fg=self.colors['green'])
        self.profile_status.grid(row=1, column=5, columnspan=3, sticky=tk.W, padx=10, pady=5)

    def apply_profile(self):
        """Apply profile data from form"""
        try:
            sex = self.sex_var.get()
            weight = float(self.weight_var.get())
            age = int(self.age_var.get())
            height_str = self.height_var.get()
            chronic = self.chronic_var.get()
            time_str = self.start_time_var.get()
            
            if not all([sex, weight, age, height_str, chronic, time_str]):
                messagebox.showwarning("Incomplete", "Please fill all profile fields")
                return
            
            # Parse height
            height = self.chatbot.parse_height(height_str)
            if not height or height < 48 or height > 96:
                messagebox.showerror("Invalid Height", "Please enter valid height (e.g., '6 feet' or '72 inches')")
                return
            
            # Parse start time
            start_time = self.chatbot.parse_time_phrase(time_str)
            if not start_time:
                messagebox.showerror("Invalid Time", "Please enter time (e.g., '7pm' or '2 hours ago')")
                return
            
            # Set profile
            self.chatbot.set_profile(
                sex=sex.lower(),
                weight=weight,
                age=age,
                height=height,
                chronic_drinker=(chronic == 'Regularly'),
                start_time=start_time
            )
            
            # Update calculator
            self.calculator.set_profile(
                sex=sex.lower(),
                weight_lbs=weight,
                age=age,
                chronic_drinker=(chronic == 'Regularly')
            )
            self.calculator.start_time = start_time
            
            self.profile_complete = True
            self.profile_status.config(text="✓ Profile applied", fg=self.colors['green'])
            self.display_bot_message("Great! Your profile is set. Now tell me about your drinks and food.")
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please check your inputs: {str(e)}")

    def create_chat_section(self, parent):
        """Create modern chat section"""
        chat_frame = tk.Frame(parent, bg=self.colors['secondary_bg'], relief=tk.FLAT, bd=0)
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Chat title
        title = tk.Label(chat_frame, text="Chat", font=self.fonts['subtitle'],
                        bg=self.colors['secondary_bg'], fg=self.colors['text'])
        title.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Chat display with larger font
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, height=30, width=45,
            font=self.fonts['body'],  # LARGER FONT
            bg='white', fg=self.colors['text'],
            wrap=tk.WORD, relief=tk.FLAT, bd=0,
            padx=12, pady=12
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        # Input area
        input_frame = tk.Frame(chat_frame, bg=self.colors['secondary_bg'])
        input_frame.pack(fill=tk.X, padx=15, pady=(10, 15))
        
        self.input_field = tk.Entry(input_frame, font=self.fonts['body'],
                                   bg='white', fg=self.colors['text'],
                                   relief=tk.FLAT, bd=0, insertbackground=self.colors['accent'])
        self.input_field.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0, 10), ipady=8)
        self.input_field.bind('<Return>', self.send_message)
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg=self.colors['secondary_bg'])
        btn_frame.pack(side=tk.RIGHT)
        
        send_btn = tk.Button(btn_frame, text="Send", font=self.fonts['body_small'],
                            bg=self.colors['accent'], fg='white', relief=tk.FLAT, bd=0,
                            padx=16, pady=8, command=self.send_message)
        send_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        clear_btn = tk.Button(btn_frame, text="Clear", font=self.fonts['body_small'],
                             bg=self.colors['tertiary_bg'], fg=self.colors['text'], relief=tk.FLAT, bd=0,
                             padx=16, pady=8, command=self.clear_scenario)
        clear_btn.pack(side=tk.LEFT)
        
        # Welcome message
        self.display_bot_message("👋 Welcome to BAC Simulator! First, fill out your profile above, then tell me about your drinks and food.")

    def create_display_section(self, parent):
        """Create modern BAC display section"""
        display_frame = tk.Frame(parent, bg=self.colors['bg'])
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # BAC display - Large and prominent
        bac_card = tk.Frame(display_frame, bg=self.colors['secondary_bg'], relief=tk.FLAT, bd=0)
        bac_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(bac_card, text="Current BAC", font=self.fonts['subtitle'],
                bg=self.colors['secondary_bg'], fg=self.colors['secondary_text']).pack(anchor=tk.W, padx=15, pady=(15, 5))
        
        bac_container = tk.Frame(bac_card, bg=self.colors['secondary_bg'])
        bac_container.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # HUGE BAC number
        self.bac_label = tk.Label(bac_container, text="0.000%", font=('Helvetica', 56, 'bold'),
                                 bg=self.colors['secondary_bg'], fg=self.colors['green'])
        self.bac_label.pack(anchor=tk.W)
        
        # Status and legal
        info_frame = tk.Frame(bac_card, bg=self.colors['secondary_bg'])
        info_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.status_label = tk.Label(info_frame, text="Sober", font=self.fonts['subtitle'],
                                    bg=self.colors['secondary_bg'], fg=self.colors['text'])
        self.status_label.pack(anchor=tk.W)
        
        self.legal_label = tk.Label(info_frame, text="Legal to drive", font=self.fonts['body_small'],
                                   bg=self.colors['secondary_bg'], fg=self.colors['green'])
        self.legal_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Timeline graph
        graph_card = tk.Frame(display_frame, bg=self.colors['secondary_bg'], relief=tk.FLAT, bd=0)
        graph_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        tk.Label(graph_card, text="Timeline (6 Hours)", font=self.fonts['subtitle'],
                bg=self.colors['secondary_bg'], fg=self.colors['secondary_text']).pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        self.canvas = tk.Canvas(graph_card, bg='white', height=220, highlightthickness=0,
                               relief=tk.FLAT, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        self.canvas.bind("<Configure>", lambda e: self.draw_timeline_graph())
        
        # Details
        details_card = tk.Frame(display_frame, bg=self.colors['secondary_bg'], relief=tk.FLAT, bd=0)
        details_card.pack(fill=tk.X)
        
        tk.Label(details_card, text="Summary", font=self.fonts['subtitle'],
                bg=self.colors['secondary_bg'], fg=self.colors['secondary_text']).pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        self.details_text = scrolledtext.ScrolledText(details_card, height=8, width=40,
                                                     font=self.fonts['body_small'],
                                                     bg='white', fg=self.colors['text'],
                                                     wrap=tk.WORD, relief=tk.FLAT, bd=0,
                                                     padx=12, pady=12)
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        self.details_text.config(state='disabled')

    def display_bot_message(self, message: str):
        """Display bot message with larger font"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"Bot: {message}\n\n", 'bot')
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
        self.chat_display.tag_config('bot', foreground=self.colors['accent'])

    def display_user_message(self, message: str):
        """Display user message"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"You: {message}\n", 'user')
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
        self.chat_display.tag_config('user', foreground=self.colors['green'])

    def send_message(self, event=None):
        """Handle chat input"""
        if not self.profile_complete:
            messagebox.showinfo("Profile Required", "Please apply your profile first!")
            return
        
        message = self.input_field.get().strip()
        if not message:
            return

        self.display_user_message(message)
        response = self.chatbot.process_scenario_update(message)
        self.display_bot_message(response)
        self.input_field.delete(0, tk.END)
        
        # Process pending drinks/foods
        for drink in self.chatbot.get_pending_drinks():
            self.calculator.add_drink(drink['time'], drink['type'], 
                                     quantity=drink['quantity'], 
                                     alcohol_percent=drink['alcohol_percent'])
        
        for food in self.chatbot.get_pending_foods():
            self.calculator.add_food(food['time'], food['type'])

    def clear_scenario(self):
        """Clear drinks and food"""
        if messagebox.askyesno("Clear", "Clear all drinks and food?"):
            self.calculator.drinks_timeline = []
            self.calculator.food_timeline = []
            self.display_bot_message("Scenario cleared! Tell me about your drinks and food again.")
            self.update_display()

    def draw_timeline_graph(self):
        """Draw BAC timeline"""
        self.canvas.delete("all")

        # Get canvas dimensions, use defaults if not yet rendered
        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Use minimum dimensions if canvas not ready
        if width < 100:
            width = 400
        if height < 50:
            height = 220

        timeline = self.calculator.get_bac_timeline(hours=6)

        # Check if there are any drinks to show
        has_drinks = len(self.calculator.drinks_timeline) > 0

        if not has_drinks:
            self.canvas.create_text(width//2, height//2, text="Add drinks to see timeline",
                                   fill=self.colors['secondary_text'], font=self.fonts['body_small'])
            return

        if not timeline:
            return
        
        # Draw graph
        padding = 35
        graph_width = width - (padding * 2)
        graph_height = height - (padding * 2)
        
        if graph_width < 50 or graph_height < 50:
            return
        
        # Axes
        self.canvas.create_line(padding, height - padding, padding, padding, fill=self.colors['border'], width=2)
        self.canvas.create_line(padding, height - padding, width - padding, height - padding, fill=self.colors['border'], width=2)
        
        # Y-axis labels
        max_bac = max(bac for _, bac in timeline) if timeline else 0.2
        max_bac = max(0.2, max_bac * 1.1)
        
        for i in range(0, int(max_bac * 100) + 10, 5):
            bac_val = i / 100
            y = height - padding - (bac_val / max_bac) * graph_height
            self.canvas.create_text(padding - 20, y, text=f"{bac_val:.2f}%", 
                                   font=self.fonts['caption'], fill=self.colors['secondary_text'])
            self.canvas.create_line(padding - 5, y, padding, y, fill=self.colors['tertiary_bg'])
        
        # Legal limit line (0.08%)
        if 0.08 <= max_bac:
            legal_y = height - padding - (0.08 / max_bac) * graph_height
            self.canvas.create_line(padding, legal_y, width - padding, legal_y,
                                  fill=self.colors['red'], dash=(6, 4), width=2)
            self.canvas.create_text(width - padding - 60, legal_y - 10,
                                  text="Legal Limit 0.08%", font=self.fonts['caption'],
                                  fill=self.colors['red'])

        # Enhanced DUI line (0.15%)
        if 0.15 <= max_bac:
            enhanced_y = height - padding - (0.15 / max_bac) * graph_height
            self.canvas.create_line(padding, enhanced_y, width - padding, enhanced_y,
                                  fill=self.colors['critical'], dash=(6, 4), width=2)
            self.canvas.create_text(width - padding - 60, enhanced_y - 10,
                                  text="Enhanced DUI 0.15%", font=self.fonts['caption'],
                                  fill=self.colors['critical'])
        
        # Draw BAC curve
        if len(timeline) > 1:
            start_time = timeline[0][0]
            end_time = timeline[-1][0]
            time_span = (end_time - start_time).total_seconds() / 3600
            
            points = []
            for time_point, bac_val in timeline:
                if time_span > 0:
                    elapsed = (time_point - start_time).total_seconds() / 3600
                    x = padding + (elapsed / time_span) * graph_width
                else:
                    x = padding
                y = height - padding - (bac_val / max_bac) * graph_height
                points.append((x, y))
            
            # Draw line
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i+1]
                self.canvas.create_line(x1, y1, x2, y2, fill=self.colors['accent'], width=3)
            
            # Current point
            self.canvas.create_oval(points[0][0]-5, points[0][1]-5,
                                   points[0][0]+5, points[0][1]+5,
                                   fill=self.colors['orange'], outline=self.colors['red'], width=2)
        
        # X-axis labels
        for i in range(0, 7):
            x = padding + (i / 6) * graph_width
            self.canvas.create_text(x, height - padding + 20, text=f"{i}h",
                                   font=self.fonts['caption'], fill=self.colors['secondary_text'])

    def update_details(self):
        """Update summary text"""
        self.details_text.config(state='normal')
        self.details_text.delete(1.0, tk.END)
        
        try:
            current_bac = self.calculator.calculate_bac_at_time()
            peak_bac, peak_time = self.calculator.get_peak_bac()
            time_to_sober = self.calculator.get_time_to_sobriety()
            
            text = f"BAC: {current_bac:.4f}%\n"
            text += f"Peak: {peak_bac:.4f}%\n"
            text += f"Sober in: {self.format_td(time_to_sober)}\n\n"
            text += f"Drinks: {len(self.calculator.drinks_timeline)}\n"
            text += f"Foods: {len(self.calculator.food_timeline)}"
            
            self.details_text.insert(tk.END, text)
        except:
            pass
        finally:
            self.details_text.config(state='disabled')

    def format_td(self, td):
        """Format timedelta"""
        if not td:
            return "N/A"
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"

    def get_bac_color(self, bac: float) -> str:
        """Get color for BAC level based on design system"""
        if bac < 0.05:
            return self.bac_colors['safe']
        elif bac < 0.08:
            return self.bac_colors['caution']
        elif bac < 0.15:
            return self.bac_colors['warning']
        elif bac < 0.20:
            return self.bac_colors['danger']
        else:
            return self.bac_colors['critical']

    def update_display(self):
        """Update all displays"""
        try:
            if self.profile_complete:
                current_bac = self.calculator.calculate_bac_at_time()
                impairment = self.calculator.get_impairment_level(current_bac)

                # Use design system colors
                bac_color = self.get_bac_color(current_bac)

                self.bac_label.config(text=f"{current_bac:.3f}%", fg=bac_color)
                self.status_label.config(text=impairment['level'])

                # Update legal status with proper colors
                if impairment['fitness_to_drive'] == 'YES':
                    legal_text = "Safe to Drive"
                    legal_color = self.colors['green']
                elif impairment['fitness_to_drive'] == 'CAUTION':
                    legal_text = "Caution Advised"
                    legal_color = self.colors['caution']
                else:
                    legal_text = "Do NOT Drive"
                    legal_color = self.colors['red']

                self.legal_label.config(text=legal_text, fg=legal_color)

                self.draw_timeline_graph()
                self.update_details()
        except Exception as e:
            pass

        self.root.after(2000, self.update_display)  # Update every 2 seconds for responsiveness
