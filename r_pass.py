import tkinter as tk

from password import Password, calculate_entropy


def get_strength_level(entropy):
    if entropy < 28:
        return "Weak", 0.2
    elif entropy < 36:
        return "Fair", 0.4
    elif entropy < 60:
        return "Good", 0.6
    elif entropy < 128:
        return "Strong", 0.8
    else:
        return "Very Strong", 1.0


def get_strength_level(entropy):
    if entropy < 28:
        return "Weak", 0.2
    elif entropy < 36:
        return "Fair", 0.4
    elif entropy < 60:
        return "Good", 0.6
    elif entropy < 128:
        return "Strong", 0.8
    else:
        return "Very Strong", 1.0


class RPass:
    def __init__(self):
        # region ui elements
        self.strength_bar = None
        self.strength_label = None
        self.passphrase_format_frame = None
        self.spaces_button = None
        self.hyphens_button = None
        self.no_sep_button = None
        self.mixed_button = None
        self.mode_label = None
        self.current_length_label = None
        self.toggle_mode_button = None
        self.copy_button = None
        self.set_length_button = None
        self.pass_length_box = None
        self.pass_length_label = None
        self.window = None
        self.app_title = None
        self.generate_pass_button = None
        self.generated_pass_label = None
        self.generated_pass_box = None
        self.current_format_label = None
        # endregion

        self.mode = "random"
        self.init_ui_elements()
        self.password = Password()
        self.update_length_display()

    def on_generate_click(self):
        if self.mode == "random":
            password = self.password.generate_random_password()
            self.update_strength_display(password, is_passphrase=False)
        elif self.mode == "passphrase":
            password = self.password.generate_passphrase()
            self.update_strength_display(password, is_passphrase=True, num_words=self.password.no_of_tokens)
        else:
            password = ""

        self.generated_pass_box.config(state="normal")
        self.generated_pass_box.delete(0, tk.END)
        self.generated_pass_box.insert(0, password)
        self.generated_pass_box.config(state="readonly")

    def on_copy_click(self):
        password = self.generated_pass_box.get()
        self.window.clipboard_clear()
        self.window.clipboard_append(password)

        self.copy_button.config(text="Copied!")
        self.window.after(1500, lambda: self.copy_button.config(text="Copy"))

    def toggle_mode(self):
        if self.mode == "random":
            self.mode = "passphrase"
            self.show_passphrase_options()
        else:
            self.mode = "random"
            self.hide_passphrase_options()

        self.mode_label.config(text=f"Mode: {self.mode.capitalize()}")

    def show_passphrase_options(self):
        self.passphrase_format_frame.grid(row=7, column=0, columnspan=3, pady=10)

    def hide_passphrase_options(self):
        self.passphrase_format_frame.grid_remove()

    def set_spaces(self):
        self.password.spaces = True
        self.password.hyphens = False
        self.password.mixed = False
        self.update_format_display()

    def set_hyphens(self):
        self.password.spaces = False
        self.password.hyphens = True
        self.password.mixed = False
        self.update_format_display()

    def set_no_separator(self):
        self.password.spaces = False
        self.password.hyphens = False
        self.password.mixed = False
        self.update_format_display()

    def set_mixed(self):
        self.password.spaces = False
        self.password.hyphens = False
        self.password.mixed = True
        self.update_format_display()

    def set_length(self):
        length = int(self.get_length_text())
        self.password.no_of_tokens = length
        self.update_length_display()

    def get_length_text(self):
        return self.pass_length_box.get()

    def run(self):
        self.window.mainloop()

    def update_length_display(self):
        self.current_length_label.config(text=f"Current: {self.password.no_of_tokens}")

    def update_format_display(self):
        if self.password.hyphens:
            format_text = "Hyphens"
        elif self.password.spaces:
            format_text = "Spaces"
        elif self.password.mixed:
            format_text = "Mixed"
        else:
            format_text = "No Separator"

        self.current_format_label.config(text=f"Current: {format_text}")

    def update_strength_display(self, password, is_passphrase=False, num_words=None):
        entropy = calculate_entropy(password, is_passphrase, num_words)
        strength_text, strength_ratio = get_strength_level(entropy)

        # Calculate color (red to green)
        red = int(255 * (1 - strength_ratio))
        green = int(255 * strength_ratio)
        color = f'#{red:02x}{green:02x}00'

        # Update bar
        bar_width = int(200 * strength_ratio)
        self.strength_bar.config(width=bar_width, bg=color)

        # Update label - just show bits
        self.strength_label.config(text=f"{int(entropy)} bits")

    def init_ui_elements(self):
        self.window = tk.Tk()
        self.window.title("R-GEN96 Password Generator")
        self.window.geometry("600x550")
        self.window.tk.call('tk', 'scaling', 1.5)
        self.window.config(bg="#C0C0C0")

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        self.app_title = tk.Label(
            self.window,
            text="R-GEN96",
            font=("MS Sans Serif", 24, "bold"),
            bg="#000080",
            fg="white",
            relief="raised",
            bd=2
        )
        self.app_title.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(20, 30), padx=20)

        self.mode_label = tk.Label(
            self.window,
            text="Mode: Random",
            font=("MS Sans Serif", 10, "bold"),
            bg="#C0C0C0"
        )
        self.mode_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))

        self.toggle_mode_button = tk.Button(
            self.window,
            text="Toggle Mode",
            command=self.toggle_mode,
            font=("MS Sans Serif", 9),
            bg="#D3D3D3",
            relief="raised",
            bd=2,
            width=15
        )
        self.toggle_mode_button.grid(row=2, column=0, columnspan=3, pady=(0, 15))

        self.generate_pass_button = tk.Button(
            self.window,
            text="Generate Password",
            command=self.on_generate_click,
            font=("MS Sans Serif", 10),
            bg="#D3D3D3",
            relief="raised",
            bd=3,
            width=20
        )
        self.generate_pass_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.generated_pass_label = tk.Label(
            self.window,
            text="Password:",
            font=("MS Sans Serif", 10),
            bg="#C0C0C0"
        )
        self.generated_pass_label.grid(row=4, column=0, sticky="e", padx=(0, 10))

        self.generated_pass_box = tk.Entry(
            self.window,
            state="readonly",
            width=30,
            font=("Courier New", 10),
            bg="white",
            relief="sunken",
            bd=2
        )
        self.generated_pass_box.grid(row=4, column=1, pady=10)

        self.copy_button = tk.Button(
            self.window,
            text="Copy",
            command=self.on_copy_click,
            font=("MS Sans Serif", 9),
            bg="#D3D3D3",
            relief="raised",
            bd=2,
            width=8
        )
        self.copy_button.grid(row=4, column=2, padx=(10, 0))

        self.pass_length_label = tk.Label(
            self.window,
            text="Number of tokens:",
            font=("MS Sans Serif", 10),
            bg="#C0C0C0"
        )
        self.pass_length_label.grid(row=5, column=0, sticky="e", padx=(0, 10), pady=20)

        self.pass_length_box = tk.Entry(
            self.window,
            width=10,
            font=("MS Sans Serif", 10),
            bg="white",
            relief="sunken",
            bd=2
        )
        self.pass_length_box.grid(row=5, column=1, sticky="w", pady=20)

        self.set_length_button = tk.Button(
            self.window,
            text="Set",
            command=self.set_length,
            font=("MS Sans Serif", 9),
            bg="#D3D3D3",
            relief="raised",
            bd=2,
            width=8
        )
        self.set_length_button.grid(row=5, column=2, padx=(10, 0), pady=20)

        self.current_length_label = tk.Label(
            self.window,
            text="Current: 16",
            font=("MS Sans Serif", 9),
            bg="#C0C0C0"
        )
        self.current_length_label.grid(row=6, column=1, sticky="w")

        # Passphrase format options (hidden by default)
        self.passphrase_format_frame = tk.Frame(self.window, bg="#C0C0C0")

        format_label = tk.Label(
            self.passphrase_format_frame,
            text="Format:",
            font=("MS Sans Serif", 10),
            bg="#C0C0C0"
        )
        format_label.grid(row=0, column=0, padx=(0, 10))

        self.hyphens_button = tk.Button(
            self.passphrase_format_frame,
            text="Hyphens",
            command=self.set_hyphens,
            font=("MS Sans Serif", 8),
            bg="#D3D3D3",
            relief="raised",
            bd=2,
            width=10
        )
        self.hyphens_button.grid(row=0, column=1, padx=5)

        self.spaces_button = tk.Button(
            self.passphrase_format_frame,
            text="Spaces",
            command=self.set_spaces,
            font=("MS Sans Serif", 8),
            bg="#D3D3D3",
            relief="raised",
            bd=2,
            width=10
        )
        self.spaces_button.grid(row=0, column=2, padx=5)

        self.no_sep_button = tk.Button(
            self.passphrase_format_frame,
            text="No Sep",
            command=self.set_no_separator,
            font=("MS Sans Serif", 8),
            bg="#D3D3D3",
            relief="raised",
            bd=2,
            width=10
        )
        self.no_sep_button.grid(row=0, column=3, padx=5)

        self.mixed_button = tk.Button(
            self.passphrase_format_frame,
            text="Mixed",
            command=self.set_mixed,
            font=("MS Sans Serif", 8),
            bg="#D3D3D3",
            relief="raised",
            bd=2,
            width=10
        )
        self.mixed_button.grid(row=0, column=4, padx=5)

        self.current_format_label = tk.Label(
            self.passphrase_format_frame,
            text="Current: Hyphens",
            font=("MS Sans Serif", 9),
            bg="#C0C0C0"
        )
        self.current_format_label.grid(row=1, column=0, columnspan=5, pady=(10, 0))

        # Hide by default
        self.passphrase_format_frame.grid_remove()

        # Strength indicator
        strength_container = tk.Frame(self.window, bg="#C0C0C0")
        strength_container.grid(row=8, column=0, columnspan=3, pady=20)

        tk.Label(
            strength_container,
            text="Strength:",
            font=("MS Sans Serif", 9),
            bg="#C0C0C0"
        ).pack(side="left", padx=(0, 10))

        # Bar background
        bar_bg = tk.Frame(strength_container, bg="white", relief="sunken", bd=2, width=200, height=20)
        bar_bg.pack(side="left", padx=5)
        bar_bg.pack_propagate(False)

        # Actual strength bar
        self.strength_bar = tk.Label(bar_bg, bg="red", width=0, height=20)
        self.strength_bar.place(x=0, y=0)

        self.strength_label = tk.Label(
            strength_container,
            text="Weak (0 bits)",
            font=("MS Sans Serif", 9),
            bg="#C0C0C0"
        )
        self.strength_label.pack(side="left", padx=10)