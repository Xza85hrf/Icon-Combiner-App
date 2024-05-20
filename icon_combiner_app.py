import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import sv_ttk
import torch
import numpy as np
import logging

# Initialize logging
logging.basicConfig(
    filename="icon_combiner.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class IconCombinerApp:
    def __init__(self, root):
        """
        Initialize the application, set up the main window, and create widgets.
        """
        self.root = root
        self.root.title("Icon Combiner")
        self.root.geometry("400x500")
        sv_ttk.set_theme("light")

        # Initialize variables for storing icon paths and images
        self.icon1_path = None
        self.icon2_path = None
        self.icon1 = None
        self.icon2 = None
        self.combined_icon = None

        # Create the user interface widgets
        self.create_widgets()

    def create_widgets(self):
        """
        Create and place the widgets (buttons, labels, entry fields) in the main window.
        """
        # Load Icon 1 button
        self.load_icon1_button = ttk.Button(
            self.root, text="Load Icon 1", command=self.load_icon1
        )
        self.load_icon1_button.pack(pady=10)

        # Load Icon 2 button
        self.load_icon2_button = ttk.Button(
            self.root, text="Load Icon 2", command=self.load_icon2
        )
        self.load_icon2_button.pack(pady=10)

        # Combine Icons button
        self.combine_button = ttk.Button(
            self.root, text="Combine Icons", command=self.combine_icons
        )
        self.combine_button.pack(pady=10)

        # Save Combined Icon button
        self.save_button = ttk.Button(
            self.root, text="Save Combined Icon", command=self.save_combined_icon
        )
        self.save_button.pack(pady=10)

        # Label to display the combined icon
        self.combined_icon_label = ttk.Label(self.root, text="")
        self.combined_icon_label.pack(pady=10)

        # Size input
        self.size_label = ttk.Label(self.root, text="Enter size (e.g., 128):")
        self.size_label.pack(pady=5)
        self.size_entry = ttk.Entry(self.root)
        self.size_entry.pack(pady=5)

        # Automatic sizing checkbox
        self.auto_size_var = tk.BooleanVar()
        self.auto_size_check = ttk.Checkbutton(
            self.root, text="Automatic Sizing", variable=self.auto_size_var
        )
        self.auto_size_check.pack(pady=5)

    def load_icon1(self):
        """
        Open a file dialog to load the first icon and display it in the GUI.
        """
        try:
            self.icon1_path = filedialog.askopenfilename(
                filetypes=[("ICO files", "*.ico")]
            )
            if self.icon1_path:
                self.icon1 = Image.open(self.icon1_path)
                self.show_icon(self.icon1, "Icon 1 loaded")
        except Exception as e:
            logging.error(f"Error loading Icon 1: {e}")
            messagebox.showerror("Error", f"Failed to load Icon 1: {e}")

    def load_icon2(self):
        """
        Open a file dialog to load the second icon and display it in the GUI.
        """
        try:
            self.icon2_path = filedialog.askopenfilename(
                filetypes=[("ICO files", "*.ico")]
            )
            if self.icon2_path:
                self.icon2 = Image.open(self.icon2_path)
                self.show_icon(self.icon2, "Icon 2 loaded")
        except Exception as e:
            logging.error(f"Error loading Icon 2: {e}")
            messagebox.showerror("Error", f"Failed to load Icon 2: {e}")

    def show_icon(self, icon, message):
        """
        Display a thumbnail of the loaded icon in the GUI.

        Args:
            icon (PIL.Image.Image): The icon to display.
            message (str): The message to display in the info dialog.
        """
        try:
            icon.thumbnail((64, 64))
            icon_tk = ImageTk.PhotoImage(icon)
            icon_label = ttk.Label(self.root, image=icon_tk)
            icon_label.image = icon_tk  # Keep a reference to avoid garbage collection
            icon_label.pack()
            messagebox.showinfo("Info", message)
        except Exception as e:
            logging.error(f"Error showing icon: {e}")
            messagebox.showerror("Error", f"Failed to show icon: {e}")

    def upscale_image(self, image, size):
        """
        Upscale the given image to the specified size using CUDA if available, otherwise CPU.

        Args:
            image (PIL.Image.Image): The image to upscale.
            size (tuple): The target size (width, height).

        Returns:
            PIL.Image.Image: The upscaled image.
        """
        try:
            if torch.cuda.is_available():
                logging.info("Using CUDA for upscaling.")
                device = torch.device("cuda")
            else:
                logging.info("CUDA not available. Using CPU for upscaling.")
                device = torch.device("cpu")

            # Convert image to tensor
            image_tensor = torch.from_numpy(np.array(image)).float().to(device)
            image_tensor = image_tensor.unsqueeze(0).permute(
                0, 3, 1, 2
            )  # Convert to NCHW

            # Resize using interpolation
            upscaled_tensor = torch.nn.functional.interpolate(
                image_tensor, size=size, mode="bilinear", align_corners=False
            )
            upscaled_image = (
                upscaled_tensor.squeeze()
                .permute(1, 2, 0)
                .cpu()
                .numpy()
                .astype(np.uint8)
            )

            return Image.fromarray(upscaled_image)
        except Exception as e:
            logging.error(f"Error upscaling image: {e}")
            messagebox.showerror("Error", f"Failed to upscale image: {e}")
            return image.resize(size)

    def combine_icons(self):
        """
        Combine the two loaded icons into one image, either using automatic sizing or user-specified size.
        """
        if not self.icon1 or not self.icon2:
            messagebox.showwarning("Warning", "Please load both icons first")
            return

        try:
            if self.auto_size_var.get():
                icon_size = self.icon1.size  # Use size of the first icon
            else:
                try:
                    icon_size = int(self.size_entry.get()), int(self.size_entry.get())
                except ValueError:
                    messagebox.showwarning("Warning", "Please enter a valid size")
                    return

            self.icon1 = self.upscale_image(self.icon1, icon_size)
            self.icon2 = self.upscale_image(self.icon2, icon_size)

            # Create a new image with a transparent background
            combined_icon = Image.new(
                "RGBA", (icon_size[0] * 2, icon_size[1]), (255, 255, 255, 0)
            )

            # Paste the icons into the combined image
            combined_icon.paste(self.icon1, (0, 0))
            combined_icon.paste(self.icon2, (icon_size[0], 0))

            self.combined_icon = combined_icon
            self.show_combined_icon(combined_icon)
        except Exception as e:
            logging.error(f"Error combining icons: {e}")
            messagebox.showerror("Error", f"Failed to combine icons: {e}")

    def show_combined_icon(self, icon):
        """
        Display the combined icon in the GUI.

        Args:
            icon (PIL.Image.Image): The combined icon to display.
        """
        try:
            icon_tk = ImageTk.PhotoImage(icon)
            self.combined_icon_label.configure(image=icon_tk)
            self.combined_icon_label.image = icon_tk
        except Exception as e:
            logging.error(f"Error displaying combined icon: {e}")
            messagebox.showerror("Error", f"Failed to display combined icon: {e}")

    def save_combined_icon(self):
        """
        Save the combined icon to a file chosen by the user.
        """
        if not self.combined_icon:
            messagebox.showwarning("Warning", "No combined icon to save")
            return

        try:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".ico", filetypes=[("ICO files", "*.ico")]
            )
            if save_path:
                self.combined_icon.save(save_path)
                messagebox.showinfo("Info", "Combined icon saved successfully")
        except Exception as e:
            logging.error(f"Error saving combined icon: {e}")
            messagebox.showerror("Error", f"Failed to save combined icon: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = IconCombinerApp(root)
    root.mainloop()
