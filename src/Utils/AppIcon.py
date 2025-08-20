import os
import platform

import tkinter as tk

class AppIcon:
    @staticmethod
    def set_icon(window):
        """Setzt das Fenstericon plattformabhängig (Windows = .ico, andere = .png)."""
        # Zwei Ebenen nach oben: von src/Utils → Projektroot
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        if platform.system() == "Windows":
            icon_path = os.path.join(project_root, "assets", "logo.ico")
            if os.path.exists(icon_path):
                window.iconbitmap(icon_path)
            else:
                print(f"[WARN] Icon nicht gefunden: {icon_path}")
        else:
            icon_path = os.path.join(project_root, "assets", "logo.png")
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                window.iconphoto(True, icon)
            else:
                print(f"[WARN] Icon nicht gefunden: {icon_path}")