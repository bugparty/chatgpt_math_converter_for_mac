import platform


def create_clipboard_listener():
    """
    Factory function to create the appropriate clipboard listener based on the platform.
    
    Returns:
        A clipboard listener instance (WinClipboardListener or MacClipboardListener)
    
    Raises:
        NotImplementedError: If the platform is not supported
    """
    system = platform.system()
    
    if system == "Windows":
        from winclip import WinClipboardListener
        return WinClipboardListener()
    elif system == "Darwin":  # macOS
        from macclip import MacClipboardListener
        return MacClipboardListener.alloc().init()
    else:
        raise NotImplementedError(f"Platform '{system}' is not supported. Only Windows and macOS are supported.")
