import os
import threading
import yt_dlp
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line, Triangle
from kivy.clock import Clock
from kivy.utils import platform

def scan_file_for_gallery(file_path):
    if platform == 'android':
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            MediaScannerConnection = autoclass('android.media.MediaScannerConnection')
            
            context = PythonActivity.mActivity
            MediaScannerConnection.scanFile(context, [file_path], None, None)
        except Exception as e:
            print(f"MediaScanner Error: {e}")

class YDLLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): print(msg)

class CustomLogo(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (70, 70)
        self.pos_hint = {'center_x': 0.5}
        
        with self.canvas:
            Color(0.2, 0.45, 0.85, 1)
            self.circle = Ellipse(pos=self.pos, size=self.size)
            Color(1, 1, 1, 1)
            self.line = Line(points=[], width=3)
            self.triangle = Triangle(points=[])

        self.bind(pos=self.update_shapes, size=self.update_shapes)

    def update_shapes(self, *args):
        x, y = self.pos
        w, h = self.size
        self.circle.pos = self.pos
        self.circle.size = self.size
        cx, cy = x + w / 2, y + h / 2
        
        self.line.points = [cx, cy + 14, cx, cy - 6]
        self.triangle.points = [
            cx - 12, cy - 4,
            cx + 12, cy - 4,
            cx, cy - 16
        ]

class CardContainer(BoxLayout):
    def __init__(self, bg_color=(0.14, 0.15, 0.21, 1), radius=20, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class VideoDownloaderApp(App):
    def build(self):
        self.title = "Video Downloader Pro"
        
        root_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        
        card = CardContainer(
            orientation='vertical', 
            padding=25, 
            spacing=15,
            size_hint=(0.9, None),
            height=450,
            bg_color=(0.14, 0.15, 0.21, 1),
            radius=20
        )

        card.add_widget(CustomLogo())

        title_label = Label(
            text="Video Downloader Pro",
            font_size='22sp',
            bold=True,
            color=(0.95, 0.95, 1, 1),
            size_hint_y=None,
            height=35
        )
        card.add_widget(title_label)

        self.url_input = TextInput(
            hint_text="Paste Video / Shorts Link Here...",
            multiline=False,
            size_hint_y=None,
            height=48,
            font_size='14sp',
            background_normal='',
            background_color=(0.2, 0.22, 0.3, 1),
            foreground_color=(1, 1, 1, 1),
            padding=[12, 12, 12, 12],
            cursor_color=(0.3, 0.7, 1, 1)
        )
        card.add_widget(self.url_input)

        path_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=45)
        
        self.path_input = TextInput(
            text=self.get_default_save_directory(),
            multiline=False,
            readonly=True,
            font_size='12sp',
            background_normal='',
            background_color=(0.2, 0.22, 0.3, 1),
            foreground_color=(0.8, 0.8, 0.8, 1),
            padding=[10, 12, 10, 12]
        )
        
        browse_btn = Button(
            text="Choose Folder",
            size_hint_x=0.38,
            background_normal='',
            background_color=(0.25, 0.45, 0.85, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size='12sp'
        )
        browse_btn.bind(on_press=self.open_folder_chooser)

        path_layout.add_widget(self.path_input)
        path_layout.add_widget(browse_btn)
        card.add_widget(path_layout)

        self.download_btn = Button(
            text="Start Download",
            size_hint_y=None,
            height=50,
            background_normal='',
            background_color=(0.1, 0.75, 0.45, 1),
            color=(1, 1, 1, 1),
            bold=True,
            font_size='16sp'
        )
        self.download_btn.bind(on_press=self.start_download)
        card.add_widget(self.download_btn)

        self.status_label = Label(
            text="",
            font_size='13sp',
            color=(0.7, 0.75, 0.85, 1),
            size_hint_y=None,
            height=30,
            halign='center'
        )
        card.add_widget(self.status_label)

        root_layout.add_widget(card)
        return root_layout

    def get_default_save_directory(self):
        if platform == 'android':
            from android.storage import primary_external_storage_path
            dir_path = os.path.join(primary_external_storage_path(), 'Download')
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            return dir_path
        return os.path.expanduser('~/Downloads') if os.path.exists(os.path.expanduser('~/Downloads')) else '.'

    def open_folder_chooser(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        filechooser = FileChooserIconView(
            path=self.path_input.text if os.path.exists(self.path_input.text) else '.',
            dirselect=True
        )
        btn_layout = BoxLayout(size_hint_y=None, height=45, spacing=10)
        
        select_btn = Button(text="Select This Folder", background_normal='', background_color=(0.1, 0.75, 0.45, 1), bold=True)
        cancel_btn = Button(text="Cancel", background_normal='', background_color=(0.8, 0.25, 0.25, 1), bold=True)

        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(select_btn)
        content.add_widget(filechooser)
        content.add_widget(btn_layout)

        popup = Popup(title="Select Download Directory", content=content, size_hint=(0.95, 0.85), title_size='16sp')

        def set_folder(btn):
            selected = filechooser.selection or [filechooser.path]
            if selected:
                target = selected[0]
                if os.path.isfile(target):
                    target = os.path.dirname(target)
                self.path_input.text = target
            popup.dismiss()

        select_btn.bind(on_press=set_folder)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    def start_download(self, instance):
        url = self.url_input.text.strip()
        save_dir = self.path_input.text.strip()

        if not url:
            self.status_label.text = "Please paste a video URL first!"
            return

        self.status_label.text = "Downloading... Please wait ⏳"
        self.download_btn.disabled = True

        threading.Thread(target=self._download_process, args=(url, save_dir), daemon=True).start()

    def _download_process(self, url, save_dir):
        try:
            ydl_opts = {
                # اقتطاع اسم الفيديو إلى أول 80 حرفاً لتجنب تجاوز الحد الأقصى في أندرويد
                'outtmpl': os.path.join(save_dir, '%(title).80s.%(ext)s'),
                'trim_file_name': 80,
                'format': 'b/18/best[vcodec!=none][acodec!=none]/best',
                'nocheckcertificate': True,
                'quiet': True,
                'no_warnings': True,
                'logger': YDLLogger(),
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web']
                    }
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)
                scan_file_for_gallery(downloaded_file)
            
            Clock.schedule_once(lambda dt: self._update_ui("Download completed successfully! ✅", False))
        except Exception as e:
            err_msg = str(e)[:70] + "..." if len(str(e)) > 70 else str(e)
            Clock.schedule_once(lambda dt: self._update_ui(f"Error: {err_msg}", False))

    def _update_ui(self, text, is_disabled):
        self.status_label.text = text
        self.download_btn.disabled = is_disabled

if __name__ == '__main__':
    VideoDownloaderApp().run()

