import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import yt_dlp

class DownloaderLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.label = Label(
            text="تطبيق تنزيل الفيديوهات",
            font_size='22sp',
            size_hint=(1, 0.2)
        )
        self.add_widget(self.label)

        self.url_input = TextInput(
            hint_text="أدخل رابط الفيديو هنا...",
            multiline=False,
            size_hint=(1, 0.15),
            font_size='16sp'
        )
        self.add_widget(self.url_input)

        self.download_btn = Button(
            text="تنزيل الفيديو",
            size_hint=(1, 0.2),
            font_size='18sp',
            background_color=(0.2, 0.6, 1, 1)
        )
        self.download_btn.bind(on_press=self.start_download)
        self.add_widget(self.download_btn)

        self.status_label = Label(
            text="الحالة: جاهز",
            size_hint=(1, 0.45),
            font_size='14sp'
        )
        self.add_widget(self.status_label)

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "الحالة: يرجى إدخل رابط صحيح!"
            return

        self.status_label.text = "الحالة: جاري بدء التنزيل..."
        self.download_btn.disabled = True
        threading.Thread(target=self.download_video, args=(url,)).start()

    def download_video(self, url):
        # المسار الافتراضي لمجلد التنزيلات على أندرويد
        download_folder = '/sdcard/Download'
        if not os.path.exists(download_folder):
            download_folder = '.'

        ydl_opts = {
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'format': 'best',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            Clock.schedule_once(lambda dt: self.update_status("الحالة: تم التنزيل بنجاح في مجلد Downloads!"))
        except Exception as e:
            error_msg = str(e)
            Clock.schedule_once(lambda dt: self.update_status(f"حدث خطأ: {error_msg}"))

    def update_status(self, text):
        self.status_label.text = text
        self.download_btn.disabled = False

class DownloaderApp(App):
    def build(self):
        return DownloaderLayout()

if __name__ == '__main__':
    DownloaderApp().run()
