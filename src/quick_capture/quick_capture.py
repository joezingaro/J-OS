import sys
import os
import threading
from pynput import keyboard

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, Qt, QMetaObject, Q_ARG, QTimer, QEvent
from datetime import datetime

# --- Configuration ---
DEBUG_MODE = False  # Set to False for production to disable auto-quit and auto-show

# --- Logging Setup ---
# Force unbuffered output to ensure we see logs immediately
sys.stdout.reconfigure(line_buffering=True)

# --- Web Page with Console Logging ---
class WebPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JS Console: {message} (Line {lineNumber})")

# --- Backend Object for JS Communication ---
class Backend(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window

    @pyqtSlot()
    def close_window(self):
        print("Backend: Close requested")
        QMetaObject.invokeMethod(self.window, "hide_window", Qt.ConnectionType.QueuedConnection)

    def handle_title_change(self, title):
        # Title Transport Mechanism
        # JS sets title to "CMD:SAVE:Content" or "CMD:CLOSE"
        print(f"Title Changed: {title}")
        
        if title.startswith("CMD:CLOSE"):
            self.close_window()
        elif title.startswith("CMD:SAVE:"):
            content = title[9:] # Strip "CMD:SAVE:"
            self.save_content(content)

    @pyqtSlot(str)
    def save_content(self, text):
        print(f"Backend: Saving content '{text}'")
        if not text.strip():
            return
            
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__)) # src/quick_capture
            src_dir = os.path.dirname(current_dir) # src
            project_root = os.path.dirname(src_dir) # Project Root
            inbox_path = os.path.join(project_root, 'CH', 'inbox.md')
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            entry = f"- [ ] [{timestamp}] **[INBOX]** {text}\n"
            
            with open(inbox_path, "a", encoding="utf-8") as f:
                f.write(entry)
                
            print(f"Saved to {inbox_path}")
            
            QMetaObject.invokeMethod(self.window, "hide_window", Qt.ConnectionType.QueuedConnection)
            
        except Exception as e:
            print(f"Error saving content: {e}")

# --- Main Window ---
class QuickCaptureWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(800, 200)
        self.center()

        # Web View
        self.browser = QWebEngineView()
        self.browser.setStyleSheet("background: transparent;")
        
        # Use Custom Page for Logging
        self.page = WebPage(self.browser)
        self.page.setBackgroundColor(Qt.GlobalColor.transparent)
        self.browser.setPage(self.page)
        
        self.setCentralWidget(self.browser)

        # Install Event Filter to capture keys BEFORE WebEngine swallows them
        self.browser.installEventFilter(self)

        # Title Transport Setup (Replacing QWebChannel)
        self.backend = Backend(self)
        self.browser.titleChanged.connect(self.backend.handle_title_change)

        # Load Content
        current_dir = os.path.dirname(os.path.abspath(__file__))
        web_dir = os.path.join(current_dir, 'web_interface')
        index_path = os.path.join(web_dir, 'index.html')
        self.browser.load(QUrl.fromLocalFile(index_path))
        
        print(f"Loaded: {index_path}")

    def center(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def force_focus(self):
        # Windows-specific hack to force focus to this window from background
        if sys.platform == "win32":
            import ctypes
            from ctypes import wintypes
            
            user32 = ctypes.windll.user32
            
            foreground_hwnd = user32.GetForegroundWindow()
            foreground_thread_id = user32.GetWindowThreadProcessId(foreground_hwnd, None)
            
            our_hwnd = int(self.winId())
            our_thread_id = user32.GetWindowThreadProcessId(our_hwnd, None)
            
            if foreground_thread_id != our_thread_id:
                user32.AttachThreadInput(foreground_thread_id, our_thread_id, True)
                user32.BringWindowToTop(our_hwnd)
                user32.SetForegroundWindow(our_hwnd)
                user32.AttachThreadInput(foreground_thread_id, our_thread_id, False)
            else:
                user32.BringWindowToTop(our_hwnd)
                user32.SetForegroundWindow(our_hwnd)
    
    def changeEvent(self, event):
        if event.type() == QEvent.Type.ActivationChange:
            if not self.isActiveWindow():
                print("Lost focus, hiding window...")
                self.hide()
        super().changeEvent(event)
    
    def eventFilter(self, source, event):
        # Capture Escape key on the browser widget
        if event.type() == QEvent.Type.KeyPress:
            # ANALYTICAL DEBUG: Print key pressed
            print(f"EventFilter Key: {event.key()}")
            if event.key() == Qt.Key.Key_Escape:
                print("EventFilter: Escape pressed - Hiding")
                self.hide_window()
                return True # Consume event
        return super().eventFilter(source, event)

    @pyqtSlot()
    def show_capture(self):
        print("Showing Window")
        
        self.force_focus()
        
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.show()
        self.showNormal() 
        self.raise_()
        self.activateWindow()
        self.browser.setFocus()
        
        # ANALYTICAL FIX: Ensure Event Filter is on the actual focus proxy
        # WebEngine creates a child widget that handles input. We need THAT one.
        if self.browser.focusProxy():
             self.browser.focusProxy().installEventFilter(self)
        else:
             # Fallback if no proxy (rare in older Qt, but safe check)
             for child in self.browser.children():
                 if child.metaObject().className() == "QtWebEngineCore::RenderWidgetHostViewQtDelegateWidget":
                     child.installEventFilter(self)

        QTimer.singleShot(100, self.focus_input)

    def focus_input(self):
        self.force_focus() 
        self.activateWindow() 
        self.browser.setFocus()
        script = "document.getElementById('quick-input').focus(); document.getElementById('quick-input').select();"
        self.page.runJavaScript(script) # Run on page

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide_window()
        super().keyPressEvent(event)

    @pyqtSlot()
    def hide_window(self):
        print("Hiding Window")
        self.hide()

# --- Hotkey Listener ---
def start_listener(app, window):
    def on_activate():
        # Invoke 'show_capture' on the main thread
        QMetaObject.invokeMethod(window, "show_capture", Qt.ConnectionType.QueuedConnection)

    with keyboard.GlobalHotKeys({'<ctrl>+<shift>+<space>': on_activate}) as h:
        h.join()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create window (starts hidden)
    window = QuickCaptureWindow()
    
    if DEBUG_MODE:
        print("DEBUG MODE: Auto-showing window and scheduling exit in 5s...")
        window.show()
        QTimer.singleShot(5000, app.quit)

    # Start Hotkey Thread
    listener_thread = threading.Thread(target=start_listener, args=(app, window), daemon=True)
    listener_thread.start()

    print("Quick Capture (PyQt6) Running... Press Ctrl+Shift+Space")
    sys.exit(app.exec())
