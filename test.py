import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.processed_image = None

    def load_image(self):
        """Load an image using file dialog"""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.processed_image = self.original_image.copy()
            return True
        return False

    def display_image(self, image=None, window_name="Gambar"):
        """Display image with auto-resize"""
        if image is None:
            image = self.processed_image
        
        if image is None:
            messagebox.showerror("Error", "Tidak ada gambar untuk ditampilkan")
            return

        # Get screen resolution
        screen_res = tk.Tk()
        screen_width = screen_res.winfo_screenwidth()
        screen_height = screen_res.winfo_screenheight()
        screen_res.destroy()
        
        # Resize image to fit screen while maintaining aspect ratio
        height, width = image.shape[:2]
        scale = min(screen_width/width, screen_height/height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, new_width, new_height)
        cv2.imshow(window_name, resized_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def grayscale(self):
        """Convert image to grayscale"""
        if self.processed_image is not None:
            self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            return True
        return False

    def blur(self):
        """Apply Gaussian blur"""
        if self.processed_image is not None:
            # Ask user for blur intensity
            root = tk.Tk()
            root.withdraw()
            kernel_size = simpledialog.askinteger(
                "Blur", 
                "Masukkan ukuran kernel (harus bilangan ganjil):", 
                minvalue=1, 
                maxvalue=21
            )
            
            if kernel_size and kernel_size % 2 == 1:
                self.processed_image = cv2.GaussianBlur(
                    self.processed_image, 
                    (kernel_size, kernel_size), 
                    0
                )
                return True
        return False

    def edge_detection(self):
        """Detect edges using Canny algorithm"""
        if self.processed_image is not None:
            # Convert to grayscale if not already
            if len(self.processed_image.shape) == 3:
                gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            else:
                gray = self.processed_image

            # Ask user for threshold values
            root = tk.Tk()
            root.withdraw()
            lower = simpledialog.askinteger(
                "Edge Detection", 
                "Masukkan batas bawah threshold:", 
                minvalue=0, 
                maxvalue=255,
                initialvalue=50
            )
            upper = simpledialog.askinteger(
                "Edge Detection", 
                "Masukkan batas atas threshold:", 
                minvalue=0, 
                maxvalue=255,
                initialvalue=150
            )

            if lower is not None and upper is not None:
                self.processed_image = cv2.Canny(gray, lower, upper)
                return True
        return False

    def save_image(self):
        """Save processed image"""
        if self.processed_image is not None:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                messagebox.showinfo("Sukses", f"Gambar disimpan di {file_path}")
                return True
        return False

    def reset(self):
        """Reset to original image"""
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            return True
        return False

def main():
    processor = ImageProcessor()
    
    while True:
        # Create main menu
        root = tk.Tk()
        root.withdraw()
        
        choices = [
            "1. Pilih Gambar",
            "2. Tampilkan Gambar",
            "3. Ubah ke Grayscale",
            "4. Blur Gambar",
            "5. Deteksi Tepi",
            "6. Simpan Gambar",
            "7. Reset Gambar",
            "8. Keluar"
        ]
        
        choice = simpledialog.askinteger(
            "Pengolahan Gambar", 
            "\n".join(choices) + "\n\nPilih nomor menu:",
            minvalue=1, 
            maxvalue=8
        )
        
        # Process user choice
        if choice == 1:
            processor.load_image()
        elif choice == 2:
            processor.display_image()
        elif choice == 3:
            if processor.grayscale():
                messagebox.showinfo("Sukses", "Gambar diubah ke grayscale")
        elif choice == 4:
            if processor.blur():
                messagebox.showinfo("Sukses", "Blur diterapkan")
        elif choice == 5:
            if processor.edge_detection():
                messagebox.showinfo("Sukses", "Deteksi tepi selesai")
        elif choice == 6:
            processor.save_image()
        elif choice == 7:
            if processor.reset():
                messagebox.showinfo("Sukses", "Gambar dikembalikan ke semula")
        elif choice == 8:
            break
        elif choice is None:
            break

if __name__ == "__main__":
    main()