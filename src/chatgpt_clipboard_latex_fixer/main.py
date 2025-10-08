from .clipboard_factory import create_clipboard_listener


def main():
    """Main entry point for the clipboard listener application"""
    try:
        listener = create_clipboard_listener()
        if listener is None:
            print("Failed to initialize clipboard listener")
            return
        
        listener.start()
    except NotImplementedError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
