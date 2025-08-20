"""
TTK style management for the GameUI class.

This module provides centralized TTK style configuration functionality,
separating UI styling concerns from the main GameUI class and providing
a clean interface for theme management.
"""

import tkinter as tk
from tkinter import ttk
from src.Utils.Constants import UIColors


class StyleManager:
    """
    Manages TTK style configuration for the game UI.
    
    This class provides centralized styling configuration for TTK widgets,
    implementing the brownish theme used throughout the application and
    separating styling concerns from the main UI logic.
    
    Attributes:
        window: The main tkinter window for option configuration
        style: The TTK Style instance for widget styling
    """
    
    def __init__(self, window: tk.Tk):
        """
        Initialize the StyleManager with a target window.
        
        Args:
            window: The main tkinter window for style configuration
        """
        self.window = window
        self.style = ttk.Style()
        self._configure_theme()
    
    def _configure_theme(self) -> None:
        """Configure the complete brownish theme for all TTK widgets."""
        # Set theme to default to ensure proper styling base
        self.style.theme_use('default')
        
        self._configure_button_style()
        self._configure_combobox_style()
        self._configure_frame_style()
        self._configure_global_options()
    
    def _configure_button_style(self) -> None:
        """Configure brown button style for TTK buttons."""
        self.style.configure('Brown.TButton',
                           background=UIColors.BUTTON_BG,
                           foreground=UIColors.BUTTON_FG,
                           borderwidth=1,
                           focuscolor='none')
        self.style.map('Brown.TButton',
                     background=[('active', UIColors.BUTTON_ACTIVE_BG),
                               ('pressed', UIColors.BUTTON_ACTIVE_BG)])
    
    def _configure_combobox_style(self) -> None:
        """Configure brown combobox style with comprehensive settings."""
        # Main combobox configuration
        self.style.configure('Brown.TCombobox',
                           fieldbackground=UIColors.BUTTON_BG,
                           background=UIColors.BUTTON_BG,
                           foreground=UIColors.BUTTON_FG,
                           borderwidth=1,
                           arrowcolor=UIColors.BUTTON_FG,
                           insertcolor=UIColors.BUTTON_FG,
                           relief='flat',
                           lightcolor=UIColors.BUTTON_BG,
                           darkcolor=UIColors.BUTTON_BG)
        
        # Combobox state mappings
        self.style.map('Brown.TCombobox',
                     fieldbackground=[('readonly', UIColors.BUTTON_BG),
                                    ('focus', UIColors.BUTTON_BG),
                                    ('!focus', UIColors.BUTTON_BG),
                                    ('active', UIColors.BUTTON_BG),
                                    ('!active', UIColors.BUTTON_BG)],
                     background=[('readonly', UIColors.BUTTON_BG),
                               ('focus', UIColors.BUTTON_BG),
                               ('!focus', UIColors.BUTTON_BG),
                               ('active', UIColors.BUTTON_BG),
                               ('!active', UIColors.BUTTON_BG)],
                     foreground=[('readonly', UIColors.BUTTON_FG),
                               ('focus', UIColors.BUTTON_FG),
                               ('!focus', UIColors.BUTTON_FG)],
                     selectbackground=[('readonly', UIColors.BUTTON_ACTIVE_BG)],
                     selectforeground=[('readonly', UIColors.BUTTON_FG)],
                     arrowcolor=[('readonly', UIColors.BUTTON_FG),
                               ('focus', UIColors.BUTTON_FG),
                               ('!focus', UIColors.BUTTON_FG)])
        
        self._configure_combobox_elements()
        self._configure_combobox_listbox()
    
    def _configure_combobox_elements(self) -> None:
        """Configure individual combobox elements and layout."""
        # Create custom elements
        self.style.element_create('Brown.TCombobox.field', 'from', 'default')
        self.style.element_create('Brown.TCombobox.downarrow', 'from', 'default')
        
        # Layout configuration
        self.style.layout('Brown.TCombobox', [
            ('Brown.TCombobox.field', {'sticky': 'nswe', 'children': [
                ('Brown.TCombobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [
                    ('Brown.TCombobox.textarea', {'sticky': 'nswe'})
                ]})
            ]}),
            ('Brown.TCombobox.downarrow', {'side': 'right', 'sticky': 'ns'})
        ])
        
        # Configure field element
        self.style.configure('Brown.TCombobox.field',
                           background=UIColors.BUTTON_BG,
                           fieldbackground=UIColors.BUTTON_BG,
                           bordercolor=UIColors.BUTTON_ACTIVE_BG,
                           lightcolor=UIColors.BUTTON_BG,
                           darkcolor=UIColors.BUTTON_BG)
        
        # Configure arrow element
        self.style.configure('Brown.TCombobox.downarrow',
                           background=UIColors.BUTTON_BG,
                           arrowcolor=UIColors.BUTTON_FG)
        
        # Configure Entry sub-element
        self.style.configure('Brown.TCombobox.Entry',
                           background=UIColors.BUTTON_BG,
                           fieldbackground=UIColors.BUTTON_BG,
                           foreground=UIColors.BUTTON_FG,
                           insertcolor=UIColors.BUTTON_FG)
        self.style.map('Brown.TCombobox.Entry',
                     background=[('readonly', UIColors.BUTTON_BG),
                               ('focus', UIColors.BUTTON_BG),
                               ('!focus', UIColors.BUTTON_BG)],
                     fieldbackground=[('readonly', UIColors.BUTTON_BG),
                                    ('focus', UIColors.BUTTON_BG),
                                    ('!focus', UIColors.BUTTON_BG)],
                     foreground=[('readonly', UIColors.BUTTON_FG),
                               ('focus', UIColors.BUTTON_FG),
                               ('!focus', UIColors.BUTTON_FG)])
    
    def _configure_combobox_listbox(self) -> None:
        """Configure combobox dropdown listbox styling."""
        self.style.configure('Brown.TCombobox.Listbox',
                           background=UIColors.BUTTON_BG,
                           foreground=UIColors.BUTTON_FG,
                           selectbackground=UIColors.BUTTON_ACTIVE_BG,
                           selectforeground=UIColors.BUTTON_FG,
                           borderwidth=1)
    
    def _configure_frame_style(self) -> None:
        """Configure brown frame style for containers."""
        self.style.configure('Brown.TFrame',
                           background=UIColors.FRAME_BG)
    
    def _configure_global_options(self) -> None:
        """Configure global widget options using option_add."""
        # Combobox dropdown window options
        self.window.option_add('*TCombobox*Listbox.Background', UIColors.BUTTON_BG)
        self.window.option_add('*TCombobox*Listbox.Foreground', UIColors.BUTTON_FG)
        self.window.option_add('*TCombobox*Listbox.selectBackground', UIColors.BUTTON_ACTIVE_BG)
        self.window.option_add('*TCombobox*Listbox.selectForeground', UIColors.BUTTON_FG)
        
        # Additional global combobox options
        self.window.option_add('*TCombobox*Entry.Background', UIColors.BUTTON_BG)
        self.window.option_add('*TCombobox*Entry.Foreground', UIColors.BUTTON_FG)
        self.window.option_add('*TCombobox.Background', UIColors.BUTTON_BG)
        self.window.option_add('*TCombobox.Foreground', UIColors.BUTTON_FG)
    
    def get_style(self) -> ttk.Style:
        """
        Get the configured TTK Style instance.
        
        Returns:
            The configured TTK Style instance
        """
        return self.style
    
    def apply_button_style(self, button: ttk.Button) -> None:
        """
        Apply the brown button style to a specific button.
        
        Args:
            button: The TTK button to style
        """
        button.configure(style='Brown.TButton')
    
    def apply_combobox_style(self, combobox: ttk.Combobox) -> None:
        """
        Apply the brown combobox style to a specific combobox.
        
        Args:
            combobox: The TTK combobox to style
        """
        combobox.configure(style='Brown.TCombobox')
    
    def apply_frame_style(self, frame: ttk.Frame) -> None:
        """
        Apply the brown frame style to a specific frame.
        
        Args:
            frame: The TTK frame to style
        """
        frame.configure(style='Brown.TFrame')