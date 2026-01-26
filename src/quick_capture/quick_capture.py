import sys
import os
import threading
from pynput import keyboard

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QSizeGrip
from PyQt6.QtGui import QCursor
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtGui import QAction, QKeySequence, QIcon, QCursor
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, Qt, QPoint, QMetaObject, Q_ARG, QTimer, QEvent
from datetime import datetime
import ctypes
from ctypes import wintypes

# --- Configuration ---
DEBUG_MODE = False  # Set to False for production to disable auto-quit and auto-show

# --- Logging Setup ---
# Force unbuffered output to ensure we see logs immediately
sys.stdout.reconfigure(line_buffering=True)

# --- Web Page with Console Logging ---
class WebPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        pass # print(f"JS Console: {message} (Line {lineNumber})")

# --- Backend Object for JS Communication ---
class Backend(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window

    @pyqtSlot()
    def close_window(self):
        # print("Backend: Close requested")
        QMetaObject.invokeMethod(self.window, "hide_window", Qt.ConnectionType.QueuedConnection)

    @pyqtSlot(str)
    def handle_title_change(self, title):
        # Title Transport Mechanism
        # JS sets title to "CMD:SAVE:Content" or "CMD:CLOSE"
        # print(f"Title Changed: {title}")
        
        if title.startswith("CMD:CLOSE"):
            self.close_window()
        elif title.startswith("CMD:MAXIMIZE"):
            self.window.toggle_maximize(True)
        elif title.startswith("CMD:MINIMIZE"):
            self.window.toggle_maximize(False)
        elif title.startswith("CMD:START_DRAG"):
            self.window.start_system_drag()
        elif title.startswith("CMD:RESET_CLOSE"):
            self.window.reset_and_close()
        # Legacy CMD:START_DRAG / RESIZE removed - Native handled
        elif title.startswith("CMD:SAVE:"):
            content = title[9:] # Strip "CMD:SAVE:"
            self.save_content(content)

    @pyqtSlot()
    def save_content(self, text):
        # print(f"Backend: Saving content '{text}'")
        if not text.strip():
            return
            
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__)) # src/quick_capture
            src_dir = os.path.dirname(current_dir) # src
            project_root = os.path.dirname(src_dir) # Project Root
            inbox_path = os.path.join(project_root, 'log', 'inbox.md')
            
            # DEBUG: Use explicit absolute path for validation
            print(f"DEBUG: Calculated inbox path: {inbox_path}")
            if not os.path.exists(inbox_path):
                 print(f"DEBUG: WARNING - File does not exist: {inbox_path}")

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            entry = f"- [ ] [{timestamp}] **[INBOX]** {text}\n"
            
            with open(inbox_path, "a", encoding="utf-8") as f:
                f.write(entry)
                
            print(f"Saved to {inbox_path}")
            
            # Instant Close (Animation Reverted)
            QMetaObject.invokeMethod(self.window, "hide_window", Qt.ConnectionType.QueuedConnection)
            
        except Exception as e:
            print(f"Error saving content: {e}")

# --- Main Window ---
class QuickCaptureWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Production Mode: Frameless, Transparent, Tool
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Dimensions: Match new CSS compact style (Taller for status bar)
        self.resize(800, 115) 
         
        self.is_pinned = False # If True, auto-hide is disabled
        
        # Resizing Removed per User Request (Fixed Size)
        
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
        
        self.position_bottom_center()

    def position_bottom_center(self):
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry() # Respects Taskbar
            
            x = geo.center().x() - (self.width() // 2)
            y = geo.bottom() - self.height() - 50 # 50px float from bottom
            
            self.move(x, y)
            print(f"DEBUG: Positioned at {x}, {y} (Screen: {geo.width()}x{geo.height()})")

    def center(self):
         # Redundant but kept if called elsewhere; redirect to bottom center for consistency
         self.position_bottom_center()
    
    def reset_and_close(self):
        print("Backend: Full Reset & Close")
        self.is_pinned = False
        self.resizing = False
        
        # Hide FIRST to avoid jarring flash of resizing window
        self.hide_window()
        
        # Then Reset State off-screen
        self.resize(800, 115) # Reset Size
        self.position_bottom_center() # Reset Position

    # --- Native Event Override Removed (Unstable on Py3.12/Win) ---
    # Using Qt startSystemMove instead for safe native dragging
    
    @pyqtSlot()
    def start_system_drag(self):
        # Native Qt Drag (Safe)
        self.windowHandle().startSystemMove()

    # Resizing Removed

    # start_system_resize REMOVED (Replaced by Native HitTest)

    def resizeEvent(self, event):
        super().resizeEvent(event)


    
    def force_focus(self):
        # Windows-specific hack to force focus to this window from background
        if sys.platform == "win32":
            try:
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
            except Exception as e:
                print(f"Force Focus Error: {e}")

    def changeEvent(self, event):
        if event.type() == QEvent.Type.ActivationChange:
            if not self.isActiveWindow():
                if not self.is_pinned:
                    # print("Lost focus, hiding window...")
                    self.hide_window()
        super().changeEvent(event)

    def toggle_maximize(self, expand):
        current_geo = self.geometry()
        current_bottom = current_geo.bottom()
        
        if expand:
            # Grow UPWARDS to 500px
            new_h = 500
            new_y = current_bottom - new_h + 1 # +1 to maintain bottom alignment pixel perfect
        else:
            # Shrink back to 85px (Standard Mode)
            new_h = 85
            new_y = current_bottom - new_h + 1
            
        self.setGeometry(current_geo.x(), new_y, current_geo.width(), new_h)

    def reset_state(self):
        self.toggle_maximize(False) # Shrink
        self.position_bottom_center() # Reset Pos
        self.page.runJavaScript("resetUI();")

    @pyqtSlot()
    def reset_and_hide(self):
        print("Resetting and Hiding")
        self.reset_state()
        self.actual_hide()

    @pyqtSlot()
    def hide_window(self):
        print("Hiding Window (State Preserved)")
        self.actual_hide()

    def actual_hide(self):
        self.hide()
        self.is_pinned = False

    def eventFilter(self, source, event):
        # Handle Keys (Escape)
        if event.type() == QEvent.Type.KeyPress:
             self.is_pinned = True
             if event.key() == Qt.Key.Key_Escape:
                print("EventFilter: Escape pressed - Hiding")
                self.hide_window()
                return True 
        
        # Mouse events for dragging are now handled by JS Trigger + Python Timer
        # Only keeping KeyPress logic here.
        
        return super().eventFilter(source, event)
    
    @pyqtSlot()
    def show_capture(self):
        print("Showing Window")
        
        # Ensure position is correct every show (in case of screen changes)
        # self.position_bottom_center()
        
        self.force_focus()
        
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.show()
        self.showNormal() 
        self.raise_()
        self.activateWindow()
        self.browser.setFocus()
        
        # Trigger the Snappy Animation via JS
        # self.page.runJavaScript("triggerEntrance();") # Disabled as function was removed
        
        # ANALYTICAL FIX: Ensure Event Filter is on the actual focus proxy
        if self.browser.focusProxy():
             self.browser.focusProxy().installEventFilter(self)
        else:
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

    # Legacy Mouse Events (Press/Move/Release) REMOVED
    # to avoid conflict with nativeEvent WM_NCHITTEST logic
    # -----------------------------------------------------

    @pyqtSlot()
    def hide_window(self):
        # Trigger Exit Animation -> Wait -> Hide
        self.page.runJavaScript("document.getElementById('main-container').classList.add('animate-exit');")
        QTimer.singleShot(200, self.actual_hide) # Wait for CSS transition
        
    def actual_hide(self):
         self.hide()
         # Reset Pin State on Hide? User requested "persist UNLESS hit escape/x"
         # So if we are hiding via escape/x (which call hide_window), we hide.
         # But focusing out should NOT hide if pinned.
         # self.is_pinned = False # Reset pin state on explicit close - Assuming self.is_pinned exists
         self.page.runJavaScript("document.getElementById('main-container').classList.remove('animate-exit');") # Reset for next show

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
