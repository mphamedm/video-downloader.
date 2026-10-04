[app]

# (str) اسم التطبيق الذي سيظهر على الهاتف
title = Video Downloader

# (str) اسم الحزمة (بدون مساحات أو رموز خاصة)
package.name = videodownloader

# (str) نطاق الحزمة (Domain)
package.domain = org.downloader

# (str) مجلد الكود المصدري (المجلد الحالي)
source.dir = .

# (list) امتدادات الملفات التي سيتم تضمينها
source.include_exts = py,png,jpg,kv,atlas

# (str) إصدار التطبيق
version = 0.1

# (list) المكتبات والمتطلبات الضرورية للتطبيق
# ملاحظة: تم إضافة openssl و certifi لضمان عمل الاتصالات المشفّرة (HTTPS) في yt-dlp
requirements = python3,kivy,yt-dlp,pyjnius,requests,certifi,openssl

# (str) اتجاه الشاشة (عمودي)
orientation = portrait

# (bool) هل يعمل التطبيق في وضع الشاشة الكاملة؟
fullscreen = 0

# (list) صلاحيات الأندرويد المطلوبة للإنترنت وحفظ الفيديوهات
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) إصدار Android API المستهدف
android.api = 33

# (int) الحد الأدنى لإصدار الأندرويد المدعوم (Android 5.0)
android.minapi = 21

# (bool) قبول تراخيص Android SDK تلقائياً
android.accept_sdk_license = True

# (list) المعماريات المدعومة للهواتف الحديثة والقديمة
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) مستوى إظهار التفاصيل أثناء التجميع (2 يظهر كافة التفاصيل لتشخيص الأخطاء)
log_level = 2

# (int) إظهار تحذير عند التشغيل بصلاحيات جذر (0 للإيقاف)
warn_on_root = 1

