import tkinter as tk
from typing import Dict, Optional, Callable
from src.Utils.Enums.Constants import UIColors, ButtonLabels, ButtonType


class ButtonViewManager:
    """
    Manages dynamic button creation, destruction, and state for the game UI.
    
    This class provides a centralized way to handle buttons that need to be
    dynamically created and destroyed during different game phases, eliminating
    code duplication and providing consistent button styling.
    
    Attributes:
        button_frame: The tkinter frame where buttons will be placed
        buttons: Dictionary mapping button names to their tkinter Button instances
    """
    
    def __init__(self, button_frame: tk.Frame):
        """
        Initialize the ButtonManager with a target frame for buttons.
        
        Args:
            button_frame: The tkinter frame where buttons will be placed
        """
        self.button_frame = button_frame
        self.buttons: Dict[str, tk.Button] = {}
    
    def toggle_button(self, button_name: str, enabled: bool, text: str, command: Callable) -> None:
        """
        Create, show, hide or destroy a button based on the enabled parameter.
        
        Args:
            button_name: Unique identifier for the button
            enabled: True to create/show the button, False to destroy it
            text: Text to display on the button
            command: Callback function when button is clicked
        """
        if enabled:
            self._create_button(button_name, text, command)
        else:
            self._destroy_button(button_name)
    
    def _create_button(self, button_name: str, text: str, command: Callable) -> None:
        """
        Create a button if it doesn't exist and configure it.
        
        Args:
            button_name: Unique identifier for the button
            text: Text to display on the button
            command: Callback function when button is clicked
        """
        if button_name not in self.buttons or self.buttons[button_name] is None:
            self.buttons[button_name] = tk.Button(
                self.button_frame,
                text=text,
                command=command,
                bg=UIColors.BUTTON_BG,
                fg=UIColors.BUTTON_FG,
                activebackground=UIColors.BUTTON_ACTIVE_BG
            )
            self.buttons[button_name].pack(side=tk.LEFT, padx=5)
        
        self.buttons[button_name].config(state="normal")
    
    def _destroy_button(self, button_name: str) -> None:
        """
        Destroy a button if it exists.
        
        Args:
            button_name: Unique identifier for the button to destroy
        """
        if button_name in self.buttons and self.buttons[button_name] is not None:
            self.buttons[button_name].destroy()
            self.buttons[button_name] = None
    
    def get_button(self, button_name: str) -> Optional[tk.Button]:
        """
        Get a button instance by name.
        
        Args:
            button_name: Unique identifier for the button
            
        Returns:
            The button instance if it exists, None otherwise
        """
        return self.buttons.get(button_name)
    
    def is_button_enabled(self, button_name: str) -> bool:
        """
        Check if a button exists and is enabled.
        
        Args:
            button_name: Unique identifier for the button
            
        Returns:
            True if button exists and is enabled, False otherwise
        """
        button = self.get_button(button_name)
        return button is not None and button['state'] == 'normal'
    
    def show_button_group(self, button_group: str, **button_configs) -> None:
        """
        Show specific button combinations based on game phase requirements.
        
        Args:
            button_group: Type of button group to show (ButtonType enum value)
            **button_configs: Dictionary of button configurations with command callbacks
        """
        if button_group == ButtonType.CONFIRMATION.value:
            self.toggle_button("orientation", False, "", None)
            if "confirmation" in button_configs:
                self.toggle_button("confirmation", True, 
                                 ButtonLabels.CONFIRM_SELECTION, 
                                 button_configs["confirmation"])
        elif button_group == ButtonType.ORIENTATION.value:
            self.toggle_button("confirmation", False, "", None)
            if "orientation" in button_configs:
                self.toggle_button("orientation", True,
                                 ButtonLabels.TOGGLE_ORIENTATION,
                                 button_configs["orientation"])
        elif button_group == ButtonType.NONE.value:
            self.toggle_button("orientation", False, "", None)
            self.toggle_button("confirmation", False, "", None)
    
    def cleanup(self) -> None:
        """
        Destroy all managed buttons and clean up resources.
        """
        for button_name in list(self.buttons.keys()):
            self._destroy_button(button_name)
        self.buttons.clear()