"""
BAC Simulator - macOS Desktop Application
Matching the web app design and functionality
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from datetime import datetime, timedelta
import math

class BACSimulatorGUI:
    def __init__(self, root, calculator, chatbot):
        self.root = root
        self.calculator = calculator
        self.chatbot = chatbot
        self.root.title("BAC Simulator")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)

        # Design System Colors (matching web app)
        self.colors = {
            'primary': '#00BFAE',          # Primary Teal
            'primary_dark': '#004040',     # Dark Teal
            'primary_light': '#E0F7F5',
            'neutral': '#BFBEBE',          # Light Neutral
            'neutral_bg': '#F3F4F6',       # Background
            'accent': '#029922',           # Green Accent
            'slate': '#4A4A63',            # Dark Slate (text)
            'white': '#FFFFFF',
            'card_bg': '#FFFFFF',
            # BAC Status Colors
            'bac_safe': '#029922',
            'bac_caution': '#F59E0B',
            'bac_warning': '#F97316',
            'bac_danger': '#EF4444',
            'bac_critical': '#991B1B',
        }

        self.fonts = {
            'header': ('Helvetica', 18, 'bold'),
            'header_sub': ('Helvetica', 11),
            'title': ('Helvetica', 16, 'bold'),
            'subtitle': ('Helvetica', 13, 'bold'),
            'body': ('Helvetica', 13),
            'body_small': ('Helvetica', 11),
            'caption': ('Helvetica', 10),
            'bac_large': ('Helvetica', 72, 'bold'),
            'bac_medium': ('Helvetica', 48, 'bold'),
        }

        self.profile_complete = False
        self.consumption_items = []  # Track drinks and food

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        """Create the main UI layout matching web app"""
        self.root.configure(bg=self.colors['neutral_bg'])

        # Header Bar
        self.create_header()

        # Main Content Area (3 columns)
        main_frame = tk.Frame(self.root, bg=self.colors['neutral_bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configure grid weights for responsive layout
        main_frame.grid_columnconfigure(0, weight=1, minsize=320)
        main_frame.grid_columnconfigure(1, weight=1, minsize=320)
        main_frame.grid_columnconfigure(2, weight=1, minsize=320)
        main_frame.grid_rowconfigure(0, weight=1)

        # Left Column: Profile + Consumption Log
        left_col = tk.Frame(main_frame, bg=self.colors['neutral_bg'])
        left_col.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        self.create_profile_card(left_col)
        self.create_consumption_log(left_col)

        # Middle Column: BAC Display + Timeline
        middle_col = tk.Frame(main_frame, bg=self.colors['neutral_bg'])
        middle_col.grid(row=0, column=1, sticky='nsew', padx=10)
        self.create_bac_display(middle_col)
        self.create_timeline_card(middle_col)

        # Right Column: Chat Interface
        right_col = tk.Frame(main_frame, bg=self.colors['neutral_bg'])
        right_col.grid(row=0, column=2, sticky='nsew', padx=(10, 0))
        self.create_chat_interface(right_col)

        # Disclaimer Footer
        self.create_footer()

    def create_header(self):
        """Create header bar matching web app"""
        header = tk.Frame(self.root, bg=self.colors['primary_dark'], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Inner container
        inner = tk.Frame(header, bg=self.colors['primary_dark'])
        inner.pack(fill=tk.BOTH, expand=True, padx=20)

        # Left side: Logo placeholder + Title
        left = tk.Frame(inner, bg=self.colors['primary_dark'])
        left.pack(side=tk.LEFT, fill=tk.Y, pady=12)

        # Logo placeholder (teal square with B)
        logo_frame = tk.Frame(left, bg=self.colors['primary'], width=44, height=44)
        logo_frame.pack(side=tk.LEFT, padx=(0, 12))
        logo_frame.pack_propagate(False)
        logo_label = tk.Label(logo_frame, text="B", font=('Helvetica', 20, 'bold'),
                             bg=self.colors['primary'], fg=self.colors['white'])
        logo_label.place(relx=0.5, rely=0.5, anchor='center')

        # Title
        title_frame = tk.Frame(left, bg=self.colors['primary_dark'])
        title_frame.pack(side=tk.LEFT)
        tk.Label(title_frame, text="BAC Simulator", font=self.fonts['header'],
                bg=self.colors['primary_dark'], fg=self.colors['white']).pack(anchor='w')
        tk.Label(title_frame, text="Blood Alcohol Calculator", font=self.fonts['header_sub'],
                bg=self.colors['primary_dark'], fg=self.colors['primary']).pack(anchor='w')

        # Right side: Reset button
        reset_btn = tk.Button(inner, text="Reset", font=self.fonts['body_small'],
                             bg=self.colors['primary_dark'], fg=self.colors['primary'],
                             relief=tk.FLAT, bd=0, cursor='hand2',
                             activebackground=self.colors['primary_dark'],
                             activeforeground=self.colors['white'],
                             command=self.reset_scenario)
        reset_btn.pack(side=tk.RIGHT, pady=20)

    def create_card(self, parent, title=None):
        """Create a card container matching web app style"""
        card = tk.Frame(parent, bg=self.colors['card_bg'], relief=tk.FLAT, bd=0,
                       highlightbackground=self.colors['neutral'], highlightthickness=1)

        if title:
            header = tk.Frame(card, bg=self.colors['card_bg'])
            header.pack(fill=tk.X, padx=16, pady=(16, 8))
            tk.Label(header, text=title, font=self.fonts['subtitle'],
                    bg=self.colors['card_bg'], fg=self.colors['slate']).pack(anchor='w')

        return card

    def create_profile_card(self, parent):
        """Create profile form card"""
        card = self.create_card(parent, "Your Profile")
        card.pack(fill=tk.X, pady=(0, 15))

        # Subtitle
        tk.Label(card, text="This information helps calculate accurate BAC estimates",
                font=self.fonts['caption'], bg=self.colors['card_bg'],
                fg=self.colors['neutral']).pack(anchor='w', padx=16, pady=(0, 12))

        content = tk.Frame(card, bg=self.colors['card_bg'])
        content.pack(fill=tk.X, padx=16, pady=(0, 16))

        # Sex Selection
        tk.Label(content, text="Biological Sex", font=self.fonts['body_small'],
                bg=self.colors['card_bg'], fg=self.colors['slate']).pack(anchor='w', pady=(0, 6))

        sex_frame = tk.Frame(content, bg=self.colors['card_bg'])
        sex_frame.pack(fill=tk.X, pady=(0, 12))

        self.sex_var = tk.StringVar(value='male')

        self.male_btn = tk.Button(sex_frame, text="Male", font=self.fonts['body_small'],
                                 bg=self.colors['primary_light'], fg=self.colors['primary_dark'],
                                 relief=tk.FLAT, bd=0, padx=20, pady=10,
                                 command=lambda: self.select_sex('male'))
        self.male_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.female_btn = tk.Button(sex_frame, text="Female", font=self.fonts['body_small'],
                                   bg=self.colors['neutral_bg'], fg=self.colors['slate'],
                                   relief=tk.FLAT, bd=0, padx=20, pady=10,
                                   command=lambda: self.select_sex('female'))
        self.female_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # Weight
        tk.Label(content, text="Weight (lbs)", font=self.fonts['body_small'],
                bg=self.colors['card_bg'], fg=self.colors['slate']).pack(anchor='w', pady=(0, 6))
        self.weight_var = tk.StringVar()
        weight_entry = tk.Entry(content, textvariable=self.weight_var, font=self.fonts['body'],
                               bg=self.colors['neutral_bg'], fg=self.colors['slate'],
                               relief=tk.FLAT, bd=0)
        weight_entry.pack(fill=tk.X, pady=(0, 12), ipady=10)

        # Height (2 fields)
        tk.Label(content, text="Height", font=self.fonts['body_small'],
                bg=self.colors['card_bg'], fg=self.colors['slate']).pack(anchor='w', pady=(0, 6))
        height_frame = tk.Frame(content, bg=self.colors['card_bg'])
        height_frame.pack(fill=tk.X, pady=(0, 12))

        self.height_ft_var = tk.StringVar()
        ft_entry = tk.Entry(height_frame, textvariable=self.height_ft_var, font=self.fonts['body'],
                           bg=self.colors['neutral_bg'], fg=self.colors['slate'],
                           relief=tk.FLAT, bd=0, width=8)
        ft_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5), ipady=10)
        tk.Label(height_frame, text="ft", font=self.fonts['caption'],
                bg=self.colors['card_bg'], fg=self.colors['neutral']).pack(side=tk.LEFT, padx=(0, 10))

        self.height_in_var = tk.StringVar()
        in_entry = tk.Entry(height_frame, textvariable=self.height_in_var, font=self.fonts['body'],
                           bg=self.colors['neutral_bg'], fg=self.colors['slate'],
                           relief=tk.FLAT, bd=0, width=8)
        in_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5), ipady=10)
        tk.Label(height_frame, text="in", font=self.fonts['caption'],
                bg=self.colors['card_bg'], fg=self.colors['neutral']).pack(side=tk.LEFT)

        # Age
        tk.Label(content, text="Age", font=self.fonts['body_small'],
                bg=self.colors['card_bg'], fg=self.colors['slate']).pack(anchor='w', pady=(0, 6))
        self.age_var = tk.StringVar()
        age_entry = tk.Entry(content, textvariable=self.age_var, font=self.fonts['body'],
                            bg=self.colors['neutral_bg'], fg=self.colors['slate'],
                            relief=tk.FLAT, bd=0)
        age_entry.pack(fill=tk.X, pady=(0, 12), ipady=10)

        # Regular Drinker Toggle
        self.chronic_var = tk.BooleanVar(value=False)
        chronic_frame = tk.Frame(content, bg=self.colors['card_bg'])
        chronic_frame.pack(fill=tk.X, pady=(0, 16))

        self.chronic_btn = tk.Button(chronic_frame, text="○", font=('Helvetica', 16),
                                    bg=self.colors['neutral'], fg=self.colors['white'],
                                    relief=tk.FLAT, bd=0, width=3,
                                    command=self.toggle_chronic)
        self.chronic_btn.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(chronic_frame, text="Regular drinker", font=self.fonts['body_small'],
                bg=self.colors['card_bg'], fg=self.colors['slate']).pack(side=tk.LEFT)

        # Apply Button
        apply_btn = tk.Button(content, text="Apply Profile", font=self.fonts['body'],
                             bg=self.colors['primary'], fg=self.colors['white'],
                             relief=tk.FLAT, bd=0, padx=20, pady=12,
                             cursor='hand2', command=self.apply_profile)
        apply_btn.pack(fill=tk.X)

        # Status label
        self.profile_status = tk.Label(content, text="", font=self.fonts['caption'],
                                       bg=self.colors['card_bg'], fg=self.colors['accent'])
        self.profile_status.pack(anchor='w', pady=(8, 0))

    def create_consumption_log(self, parent):
        """Create consumption log card"""
        card = self.create_card(parent, "Consumption Log")
        card.pack(fill=tk.BOTH, expand=True)

        self.log_count_label = tk.Label(card, text="0 drinks, 0 food items",
                                        font=self.fonts['caption'],
                                        bg=self.colors['card_bg'], fg=self.colors['neutral'])
        self.log_count_label.pack(anchor='w', padx=16, pady=(0, 8))

        # Scrollable list
        list_frame = tk.Frame(card, bg=self.colors['card_bg'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))

        self.log_canvas = tk.Canvas(list_frame, bg=self.colors['card_bg'],
                                   highlightthickness=0, height=200)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.log_canvas.yview)
        self.log_inner = tk.Frame(self.log_canvas, bg=self.colors['card_bg'])

        self.log_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_canvas.create_window((0, 0), window=self.log_inner, anchor='nw')

        self.log_inner.bind("<Configure>", lambda e: self.log_canvas.configure(
            scrollregion=self.log_canvas.bbox("all")))

        # Empty state message
        self.empty_log_label = tk.Label(self.log_inner, text="No items logged yet\nAdd drinks or food using the chat",
                                        font=self.fonts['body_small'], bg=self.colors['card_bg'],
                                        fg=self.colors['neutral'], justify='center')
        self.empty_log_label.pack(pady=40)

    def create_bac_display(self, parent):
        """Create BAC display card"""
        self.bac_card = tk.Frame(parent, bg=self.colors['bac_safe'],
                                highlightbackground=self.colors['neutral'], highlightthickness=0)
        self.bac_card.pack(fill=tk.X, pady=(0, 15))

        content = tk.Frame(self.bac_card, bg=self.colors['bac_safe'])
        content.pack(fill=tk.X, padx=24, pady=24)

        # BAC Number
        self.bac_label = tk.Label(content, text="0.000", font=self.fonts['bac_large'],
                                 bg=self.colors['bac_safe'], fg=self.colors['white'])
        self.bac_label.pack()

        tk.Label(content, text="Blood Alcohol Content (%)", font=self.fonts['body_small'],
                bg=self.colors['bac_safe'], fg=self.colors['white']).pack(pady=(0, 16))

        # Status Badge
        self.status_badge = tk.Label(content, text="  Sober  ", font=self.fonts['subtitle'],
                                    bg=self.colors['primary_dark'], fg=self.colors['white'],
                                    padx=16, pady=6)
        self.status_badge.pack(pady=(0, 12))

        # Description
        self.status_desc = tk.Label(content, text="No detectable impairment",
                                   font=self.fonts['body_small'],
                                   bg=self.colors['bac_safe'], fg=self.colors['white'])
        self.status_desc.pack(pady=(0, 16))

        # Fitness to Drive
        drive_frame = tk.Frame(content, bg=self.colors['bac_safe'])
        drive_frame.pack(fill=tk.X, pady=(8, 0))

        # Divider
        tk.Frame(drive_frame, bg=self.colors['neutral'], height=1).pack(fill=tk.X, pady=(0, 12))

        self.drive_label = tk.Label(drive_frame, text="✓ Safe to Drive",
                                   font=self.fonts['subtitle'],
                                   bg=self.colors['bac_safe'], fg=self.colors['white'])
        self.drive_label.pack()

        self.legal_label = tk.Label(drive_frame, text="Legal Status: LEGAL",
                                   font=self.fonts['caption'],
                                   bg=self.colors['bac_safe'], fg=self.colors['white'])
        self.legal_label.pack(pady=(4, 0))

        # Stats Row
        stats_frame = tk.Frame(self.bac_card, bg=self.colors['neutral_bg'])
        stats_frame.pack(fill=tk.X, padx=16, pady=(0, 16))

        # Peak BAC
        peak_frame = tk.Frame(stats_frame, bg=self.colors['white'])
        peak_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8), pady=8)
        tk.Label(peak_frame, text="PEAK BAC", font=self.fonts['caption'],
                bg=self.colors['white'], fg=self.colors['slate']).pack(anchor='w', padx=12, pady=(8, 2))
        self.peak_label = tk.Label(peak_frame, text="0.000", font=self.fonts['subtitle'],
                                  bg=self.colors['white'], fg=self.colors['slate'])
        self.peak_label.pack(anchor='w', padx=12, pady=(0, 8))

        # Time to Sober
        sober_frame = tk.Frame(stats_frame, bg=self.colors['white'])
        sober_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0), pady=8)
        tk.Label(sober_frame, text="TIME TO SOBER", font=self.fonts['caption'],
                bg=self.colors['white'], fg=self.colors['slate']).pack(anchor='w', padx=12, pady=(8, 2))
        self.sober_label = tk.Label(sober_frame, text="0h 0m", font=self.fonts['subtitle'],
                                   bg=self.colors['white'], fg=self.colors['slate'])
        self.sober_label.pack(anchor='w', padx=12, pady=(0, 8))

    def create_timeline_card(self, parent):
        """Create timeline chart card"""
        card = self.create_card(parent, "BAC Timeline")
        card.pack(fill=tk.BOTH, expand=True)

        tk.Label(card, text="6-hour projection", font=self.fonts['caption'],
                bg=self.colors['card_bg'], fg=self.colors['neutral']).pack(anchor='w', padx=16)

        # Canvas for chart
        self.canvas = tk.Canvas(card, bg=self.colors['white'], height=220,
                               highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=16, pady=(8, 16))
        self.canvas.bind("<Configure>", lambda e: self.draw_timeline())

        # Legend
        legend = tk.Frame(card, bg=self.colors['card_bg'])
        legend.pack(fill=tk.X, padx=16, pady=(0, 16))

        # Your BAC
        tk.Frame(legend, bg=self.colors['primary'], width=16, height=4).pack(side=tk.LEFT)
        tk.Label(legend, text=" Your BAC", font=self.fonts['caption'],
                bg=self.colors['card_bg'], fg=self.colors['slate']).pack(side=tk.LEFT, padx=(4, 20))

        # Legal Limit
        tk.Frame(legend, bg=self.colors['bac_danger'], width=16, height=2).pack(side=tk.LEFT)
        tk.Label(legend, text=" Legal Limit", font=self.fonts['caption'],
                bg=self.colors['card_bg'], fg=self.colors['slate']).pack(side=tk.LEFT, padx=(4, 0))

    def create_chat_interface(self, parent):
        """Create chat interface card"""
        card = self.create_card(parent, "Chat")
        card.pack(fill=tk.BOTH, expand=True)

        tk.Label(card, text="Tell me about your drinks and food",
                font=self.fonts['caption'], bg=self.colors['card_bg'],
                fg=self.colors['neutral']).pack(anchor='w', padx=16, pady=(0, 8))

        # Chat messages area
        chat_frame = tk.Frame(card, bg=self.colors['card_bg'])
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=16)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, height=15, font=self.fonts['body'],
            bg=self.colors['neutral_bg'], fg=self.colors['slate'],
            wrap=tk.WORD, relief=tk.FLAT, bd=0, padx=12, pady=12
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state='disabled')

        # Quick Action Buttons
        quick_frame = tk.Frame(card, bg=self.colors['card_bg'])
        quick_frame.pack(fill=tk.X, padx=16, pady=12)

        quick_actions = [
            ("🍺 Beer", lambda: self.quick_add('beer_regular')),
            ("🍷 Wine", lambda: self.quick_add('wine_light')),
            ("🥃 Shot", lambda: self.quick_add('spirits')),
            ("🍔 Food", lambda: self.quick_add_food('moderate_meal')),
        ]

        for text, cmd in quick_actions:
            btn = tk.Button(quick_frame, text=text, font=self.fonts['body_small'],
                           bg=self.colors['neutral_bg'], fg=self.colors['slate'],
                           relief=tk.FLAT, bd=0, padx=12, pady=8,
                           cursor='hand2', command=cmd)
            btn.pack(side=tk.LEFT, padx=(0, 8))

        # Input area
        input_frame = tk.Frame(card, bg=self.colors['card_bg'])
        input_frame.pack(fill=tk.X, padx=16, pady=(0, 16))

        self.input_field = tk.Entry(input_frame, font=self.fonts['body'],
                                   bg=self.colors['neutral_bg'], fg=self.colors['slate'],
                                   relief=tk.FLAT, bd=0, insertbackground=self.colors['primary'])
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 8))
        self.input_field.bind('<Return>', self.send_message)

        send_btn = tk.Button(input_frame, text="Send", font=self.fonts['body'],
                            bg=self.colors['primary'], fg=self.colors['white'],
                            relief=tk.FLAT, bd=0, padx=20, pady=10,
                            cursor='hand2', command=self.send_message)
        send_btn.pack(side=tk.RIGHT)

        # Welcome message
        self.display_bot_message("Hi! I'm here to help track your drinks and food. Tell me what you're having, like '2 beers at 7pm' or 'had pizza for dinner'. You can also use the quick buttons above!")

    def create_footer(self):
        """Create disclaimer footer"""
        footer = tk.Frame(self.root, bg='#FEF3C7', height=80)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        inner = tk.Frame(footer, bg='#FEF3C7')
        inner.pack(fill=tk.X, padx=20, pady=12)

        tk.Label(inner, text="Important Disclaimer", font=self.fonts['subtitle'],
                bg='#FEF3C7', fg='#92400E').pack(anchor='w')
        tk.Label(inner, text="This simulator provides estimates only and should not be used to determine if you are fit to drive. When in doubt, don't drive.",
                font=self.fonts['body_small'], bg='#FEF3C7', fg='#78716C',
                wraplength=1300, justify='left').pack(anchor='w', pady=(4, 0))

    # ============ Helper Methods ============

    def select_sex(self, sex):
        """Handle sex selection"""
        self.sex_var.set(sex)
        if sex == 'male':
            self.male_btn.config(bg=self.colors['primary_light'], fg=self.colors['primary_dark'])
            self.female_btn.config(bg=self.colors['neutral_bg'], fg=self.colors['slate'])
        else:
            self.female_btn.config(bg=self.colors['primary_light'], fg=self.colors['primary_dark'])
            self.male_btn.config(bg=self.colors['neutral_bg'], fg=self.colors['slate'])

    def toggle_chronic(self):
        """Toggle chronic drinker status"""
        self.chronic_var.set(not self.chronic_var.get())
        if self.chronic_var.get():
            self.chronic_btn.config(text="●", bg=self.colors['primary'], fg=self.colors['white'])
        else:
            self.chronic_btn.config(text="○", bg=self.colors['neutral'], fg=self.colors['white'])

    def apply_profile(self):
        """Apply profile data"""
        try:
            sex = self.sex_var.get()
            weight = float(self.weight_var.get() or 0)
            height_ft = int(self.height_ft_var.get() or 0)
            height_in = int(self.height_in_var.get() or 0)
            age = int(self.age_var.get() or 0)
            chronic = self.chronic_var.get()

            if weight < 80 or weight > 500:
                messagebox.showwarning("Invalid", "Weight must be between 80-500 lbs")
                return
            if height_ft < 4 or height_ft > 8:
                messagebox.showwarning("Invalid", "Height must be between 4-8 feet")
                return
            if age < 18:
                messagebox.showwarning("Invalid", "You must be 18 or older")
                return

            height_inches = height_ft * 12 + height_in

            # Update calculator
            self.calculator.set_profile(
                sex=sex,
                weight_lbs=weight,
                age=age,
                chronic_drinker=chronic
            )
            self.calculator.start_time = datetime.now()

            # Update chatbot
            self.chatbot.set_profile(
                sex=sex,
                weight=weight,
                age=age,
                height=height_inches,
                chronic_drinker=chronic,
                start_time=datetime.now()
            )

            self.profile_complete = True
            self.profile_status.config(text="✓ Profile saved!", fg=self.colors['accent'])
            self.display_bot_message("Great! Your profile is set. Now tell me about your drinks and food.")

        except ValueError as e:
            messagebox.showerror("Error", "Please fill in all fields correctly")

    def quick_add(self, drink_type):
        """Quick add a drink"""
        if not self.profile_complete:
            messagebox.showinfo("Profile Required", "Please apply your profile first!")
            return

        self.calculator.add_drink(datetime.now(), drink_type, quantity=1)
        drink_name = drink_type.replace('_', ' ').title()
        self.display_user_message(f"🍺 {drink_name}")
        self.display_bot_message(f"Got it! Added {drink_name} at {datetime.now().strftime('%I:%M %p')}.")
        self.update_consumption_log()
        self.update_display()

    def quick_add_food(self, food_type):
        """Quick add food"""
        if not self.profile_complete:
            messagebox.showinfo("Profile Required", "Please apply your profile first!")
            return

        self.calculator.add_food(datetime.now(), food_type)
        food_name = food_type.replace('_', ' ').title()
        self.display_user_message(f"🍔 {food_name}")
        self.display_bot_message(f"Noted {food_name} at {datetime.now().strftime('%I:%M %p')}. This affects alcohol absorption.")
        self.update_consumption_log()
        self.update_display()

    def send_message(self, event=None):
        """Handle chat input"""
        if not self.profile_complete:
            messagebox.showinfo("Profile Required", "Please apply your profile first!")
            return

        message = self.input_field.get().strip()
        if not message:
            return

        self.display_user_message(message)
        self.input_field.delete(0, tk.END)

        response = self.chatbot.process_scenario_update(message)
        self.display_bot_message(response)

        # Process pending items
        for drink in self.chatbot.get_pending_drinks():
            self.calculator.add_drink(drink['time'], drink['type'],
                                     quantity=drink['quantity'],
                                     alcohol_percent=drink.get('alcohol_percent'))

        for food in self.chatbot.get_pending_foods():
            self.calculator.add_food(food['time'], food['type'])

        self.update_consumption_log()
        self.update_display()

    def display_bot_message(self, message):
        """Display bot message"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"Bot: {message}\n\n", 'bot')
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
        self.chat_display.tag_config('bot', foreground=self.colors['primary'])

    def display_user_message(self, message):
        """Display user message"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"You: {message}\n", 'user')
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
        self.chat_display.tag_config('user', foreground=self.colors['accent'])

    def update_consumption_log(self):
        """Update consumption log display"""
        # Clear existing items
        for widget in self.log_inner.winfo_children():
            widget.destroy()

        drinks = self.calculator.drinks_timeline
        foods = self.calculator.food_timeline

        self.log_count_label.config(
            text=f"{len(drinks)} drink{'s' if len(drinks) != 1 else ''}, {len(foods)} food item{'s' if len(foods) != 1 else ''}"
        )

        if not drinks and not foods:
            self.empty_log_label = tk.Label(self.log_inner,
                text="No items logged yet\nAdd drinks or food using the chat",
                font=self.fonts['body_small'], bg=self.colors['card_bg'],
                fg=self.colors['neutral'], justify='center')
            self.empty_log_label.pack(pady=40)
            return

        # Combine and sort by time
        all_items = []
        for d in drinks:
            all_items.append(('drink', d))
        for f in foods:
            all_items.append(('food', f))
        all_items.sort(key=lambda x: x[1]['time'], reverse=True)

        for item_type, item in all_items:
            item_frame = tk.Frame(self.log_inner, bg=self.colors['neutral_bg'])
            item_frame.pack(fill=tk.X, pady=2)

            if item_type == 'drink':
                emoji = "🍺" if 'beer' in item['type'] else "🍷" if 'wine' in item['type'] else "🥃"
                name = item['type'].replace('_', ' ').title()
                detail = f"{item['size_oz']}oz · {item['alcohol_percent']}%"
            else:
                emoji = "🍔"
                name = item['type'].replace('_', ' ').title()
                detail = ""

            tk.Label(item_frame, text=emoji, font=('Helvetica', 16),
                    bg=self.colors['neutral_bg']).pack(side=tk.LEFT, padx=8)

            info_frame = tk.Frame(item_frame, bg=self.colors['neutral_bg'])
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

            tk.Label(info_frame, text=name, font=self.fonts['body_small'],
                    bg=self.colors['neutral_bg'], fg=self.colors['slate']).pack(anchor='w')

            time_str = item['time'].strftime('%I:%M %p')
            sub_text = f"{time_str}" + (f" · {detail}" if detail else "")
            tk.Label(info_frame, text=sub_text, font=self.fonts['caption'],
                    bg=self.colors['neutral_bg'], fg=self.colors['neutral']).pack(anchor='w')

    def get_bac_color(self, bac):
        """Get color for BAC level"""
        if bac < 0.05:
            return self.colors['bac_safe']
        elif bac < 0.08:
            return self.colors['bac_caution']
        elif bac < 0.15:
            return self.colors['bac_warning']
        elif bac < 0.20:
            return self.colors['bac_danger']
        else:
            return self.colors['bac_critical']

    def update_display(self):
        """Update all displays"""
        try:
            if self.profile_complete:
                current_bac = self.calculator.calculate_bac_at_time()
                impairment = self.calculator.get_impairment_level(current_bac)
                peak_bac, peak_time = self.calculator.get_peak_bac()
                time_to_sober = self.calculator.get_time_to_sobriety()

                bac_color = self.get_bac_color(current_bac)

                # Update BAC card background
                self.bac_card.config(bg=bac_color)
                for widget in self.bac_card.winfo_children():
                    self._update_bg_recursive(widget, bac_color)

                # Update BAC label
                self.bac_label.config(text=f"{current_bac:.3f}", bg=bac_color)

                # Update status
                self.status_badge.config(text=f"  {impairment['level']}  ")
                self.status_desc.config(text=impairment['description'][:50] + "..."
                                       if len(impairment['description']) > 50
                                       else impairment['description'])

                # Update drive status
                if impairment['fitness_to_drive'] == 'YES':
                    self.drive_label.config(text="✓ Safe to Drive")
                elif impairment['fitness_to_drive'] == 'CAUTION':
                    self.drive_label.config(text="⚠ Caution Advised")
                else:
                    self.drive_label.config(text="✗ Do NOT Drive")

                self.legal_label.config(text=f"Legal Status: {impairment['legal_status']}")

                # Update peak and sober time
                self.peak_label.config(text=f"{peak_bac:.3f}")
                if time_to_sober:
                    hours = int(time_to_sober.total_seconds() // 3600)
                    mins = int((time_to_sober.total_seconds() % 3600) // 60)
                    self.sober_label.config(text=f"{hours}h {mins}m")

                self.draw_timeline()
        except Exception as e:
            pass

        self.root.after(2000, self.update_display)

    def _update_bg_recursive(self, widget, color):
        """Recursively update background color"""
        try:
            if 'FFFFFF' not in str(widget.cget('bg')):  # Skip stat boxes
                widget.config(bg=color)
        except:
            pass
        for child in widget.winfo_children():
            self._update_bg_recursive(child, color)

    def draw_timeline(self):
        """Draw BAC timeline chart"""
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 100:
            width = 400
        if height < 50:
            height = 200

        padding = 40
        graph_width = width - padding * 2
        graph_height = height - padding * 2

        if not self.profile_complete or not self.calculator.drinks_timeline:
            self.canvas.create_text(width // 2, height // 2,
                                   text="Add drinks to see timeline",
                                   font=self.fonts['body_small'],
                                   fill=self.colors['neutral'])
            return

        timeline = self.calculator.get_bac_timeline(hours=6)
        if not timeline:
            return

        # Calculate max BAC
        max_bac = max(max(bac for _, bac in timeline), 0.1) * 1.2

        # Draw grid lines
        for i in range(5):
            y = padding + (i / 4) * graph_height
            self.canvas.create_line(padding, y, width - padding, y,
                                   fill=self.colors['neutral_bg'], width=1)
            bac_val = max_bac * (4 - i) / 4
            self.canvas.create_text(padding - 8, y, text=f"{bac_val:.2f}",
                                   font=self.fonts['caption'], fill=self.colors['neutral'], anchor='e')

        # Legal limit line (0.08%)
        if 0.08 <= max_bac:
            legal_y = padding + (1 - 0.08 / max_bac) * graph_height
            self.canvas.create_line(padding, legal_y, width - padding, legal_y,
                                   fill=self.colors['bac_danger'], dash=(6, 4), width=2)
            self.canvas.create_text(width - padding - 5, legal_y - 10,
                                   text="0.08%", font=self.fonts['caption'],
                                   fill=self.colors['bac_danger'], anchor='e')

        # Draw BAC curve
        start_time = timeline[0][0]
        end_time = timeline[-1][0]
        time_span = (end_time - start_time).total_seconds()

        if time_span > 0:
            points = []
            for time_point, bac_val in timeline:
                elapsed = (time_point - start_time).total_seconds()
                x = padding + (elapsed / time_span) * graph_width
                y = padding + (1 - bac_val / max_bac) * graph_height
                points.append((x, y))

            # Fill area
            fill_points = [(padding, height - padding)] + points + [(width - padding, height - padding)]
            self.canvas.create_polygon(fill_points, fill=self.colors['primary_light'], outline='')

            # Draw line
            for i in range(len(points) - 1):
                self.canvas.create_line(points[i][0], points[i][1],
                                       points[i + 1][0], points[i + 1][1],
                                       fill=self.colors['primary'], width=3)

            # Current point
            self.canvas.create_oval(points[0][0] - 6, points[0][1] - 6,
                                   points[0][0] + 6, points[0][1] + 6,
                                   fill=self.colors['primary'], outline=self.colors['white'], width=2)

        # X-axis labels
        for i in range(7):
            x = padding + (i / 6) * graph_width
            self.canvas.create_text(x, height - padding + 15, text=f"{i}h",
                                   font=self.fonts['caption'], fill=self.colors['neutral'])

    def reset_scenario(self):
        """Reset entire scenario"""
        if messagebox.askyesno("Reset", "Clear all data and start over?"):
            self.calculator.clear_scenario()
            self.update_consumption_log()
            self.display_bot_message("Scenario cleared! Add new drinks and food anytime.")
            self.update_display()
