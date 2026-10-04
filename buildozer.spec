[app]

# (str) Title of your application
title = Video Downloader

# (str) Package name
package.name = videodownloader

# (str) Package domain (needed for android packaging)
package.domain = org.downloader

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
requirements = python3,kivy,yt-dlp,pyjnius,requests,certifi

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (list) The Android architectures to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
