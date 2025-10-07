# pip install pywin32
import win32clipboard
import win32con
import win32api
import win32gui
import time
import threading
import ctypes
from common import convert_math_syntax

# Windows message constants
WM_CLIPBOARDUPDATE = 0x031D


class WinClipboardListener:
    def __init__(self):
        """Initialize the clipboard listener"""
        self.last_processed_content = None  # Save the last processed content to avoid redundant processing
        self.hwnd = None
        self.is_processing = False  # Flag to prevent recursive processing
        self.running = True  # Flag to control the message loop
        print("Clipboard listener successfully initialized")

    def get_clipboard_text(self):
        """Get text content from clipboard"""
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                return data
            win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"Error getting clipboard content: {e}")
            try:
                win32clipboard.CloseClipboard()
            except:
                pass
        return None

    def set_clipboard_text(self, text):
        """Set text content to clipboard"""
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
            win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"Error setting clipboard content: {e}")
            try:
                win32clipboard.CloseClipboard()
            except:
                pass

    def on_clipboard_change(self, content):
        """Process the changed clipboard content"""
        if self.is_processing:
            return
        
        print(f"Original clipboard content: {content[:100]}...")  # Show first 100 chars

        # Use convert_math_syntax to transform the content
        converted_content = convert_math_syntax(content)

        # If the converted content is the same as the current content, skip writing back to avoid loops
        if converted_content == content:
            print("Converted content is the same as the original content, skipping write-back")
            self.last_processed_content = content
            return

        print(f"Converted clipboard content: {converted_content[:100]}...")  # Show first 100 chars

        # Save the processed content
        self.last_processed_content = converted_content

        # Set flag to prevent recursive processing
        self.is_processing = True
        
        # Write the converted content back to the clipboard
        self.set_clipboard_text(converted_content)
        
        # Reset flag after a short delay
        time.sleep(0.1)
        self.is_processing = False

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        """Window procedure to handle messages"""
        if msg == WM_CLIPBOARDUPDATE:
            content = self.get_clipboard_text()
            if content and content != self.last_processed_content:
                self.on_clipboard_change(content)
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def create_window(self):
        """Create an invisible window to receive clipboard notifications"""
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.wnd_proc
        wc.lpszClassName = "ClipboardListenerWindow"
        wc.hInstance = win32api.GetModuleHandle(None)
        
        try:
            class_atom = win32gui.RegisterClass(wc)
            self.hwnd = win32gui.CreateWindow(
                class_atom,
                "Clipboard Listener",
                0,
                0, 0, 0, 0,
                0,
                0,
                wc.hInstance,
                None
            )
        except Exception as e:
            print(f"Error creating window: {e}")
            return False
        
        return True

    def start(self):
        """Start listening to clipboard changes"""
        if not self.create_window():
            print("Failed to create window")
            return
        
        # Add this window to the clipboard viewer chain
        ctypes.windll.user32.AddClipboardFormatListener(self.hwnd)
        print("Listening for clipboard content changes...")
        print("Press Ctrl+C to stop")
        
        try:
            # Custom message loop that can be interrupted
            while self.running:
                # Process all pending messages
                if win32gui.PumpWaitingMessages():
                    # If WM_QUIT was received, break
                    break
                # Sleep briefly to allow KeyboardInterrupt
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopped listening")
        finally:
            if self.hwnd:
                ctypes.windll.user32.RemoveClipboardFormatListener(self.hwnd)
                win32gui.DestroyWindow(self.hwnd)


def main():
    listener = WinClipboardListener()
    listener.start()


if __name__ == "__main__":
    main()
