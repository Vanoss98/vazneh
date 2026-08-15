from django.db import migrations


PRODUCT_TYPES = (
    ("overhead-cranes", "جرثقیل‌های سقفی"),
    ("jib-cranes", "جرثقیل‌های بازویی"),
    ("gantry-cranes", "جرثقیل‌های دروازه‌ای"),
    ("special-cranes", "جرثقیل‌های ویژه"),
    ("material-handling-equipment", "تجهیزات جابه‌جایی مواد"),
    ("crane-accessories", "تجهیزات جانبی جرثقیل"),
)


PRODUCTS = (
    {
        "slug": "single-girder-overhead-crane",
        "type": "overhead-cranes",
        "title": "جرثقیل سقفی تک پل",
        "subtitle": "ساختار ساده، اشغال فضای کمتر و ساخت اقتصادی",
        "description": (
            "جرثقیل سقفی تک پل به دلیل ساختار ساده‌تر، اشغال فضای کمتر، مدت ساخت کوتاه‌تر "
            "و هزینه پایین‌تر، یکی از پرطرفدارترین مدل‌های جرثقیل سقفی است. این مدل برای "
            "ظرفیت حداکثر ۳۲ تن و دهانه حداکثر ۳۰ متر طراحی می‌شود و با تمهیدات مناسب در "
            "فضاهای داخل یا خارج سالن قابل استفاده است."
        ),
        "features": ("ظرفیت تا ۳۲ تن", "دهانه تا ۳۰ متر", "مدل معمولی یا آویز"),
    },
    {
        "slug": "double-girder-overhead-crane",
        "type": "overhead-cranes",
        "title": "جرثقیل سقفی دو پل",
        "subtitle": "راهکار ایمن برای ظرفیت‌های بالا و دهانه‌های بزرگ",
        "description": (
            "جرثقیل سقفی دو پل یکی از ایمن‌ترین روش‌ها برای جابه‌جایی اجسام در فرایندهای "
            "تولید است و برای ظرفیت‌های ۱ تا ۵۰۰ تن طراحی می‌شود. دو پل موازی به وسیله "
            "راهبر به هم متصل می‌شوند و روی ریل‌های دو طرف سالن حرکت می‌کنند. این ساختار "
            "بیشترین ظرفیت و طول دهانه را فراهم می‌کند و به کمک کالسکه، حرکت نرم و روانی دارد."
        ),
        "features": ("ظرفیت ۱ تا ۵۰۰ تن", "مناسب دهانه‌های بزرگ", "حرکت نرم کالسکه"),
    },
    {
        "slug": "monorail-crane",
        "type": "overhead-cranes",
        "title": "مونوریل",
        "subtitle": "انتقال بار در مسیر مستقیم یا منحنی",
        "description": (
            "مونوریل نوعی جرثقیل سقفی است که در امتداد یک مسیر و در ارتفاع سالن حرکت می‌کند. "
            "این سامانه برای انتقال مواد و محصولات در کارخانه، انبار و کارگاه‌های کوچک مناسب "
            "است، بدون تغییر اساسی با سازه سالن هماهنگ می‌شود و در نوع دستی یا برقی و مسیر "
            "مستقیم یا منحنی عرضه می‌گردد. ظرفیت آن با توجه به مقاومت تیر و سقف تا ۱۰ تن است."
        ),
        "features": ("ظرفیت تا ۱۰ تن", "مسیر مستقیم یا منحنی", "نوع دستی یا برقی"),
    },
    {
        "slug": "suspension-crane",
        "type": "overhead-cranes",
        "title": "جرثقیل آویز (ساسپنشن)",
        "subtitle": "راهکار مناسب سالن‌های کم‌ارتفاع",
        "description": (
            "در سالن‌هایی با ارتفاع کم یا بدون امکان نصب جرثقیل روی سازه، می‌توان از راهبر "
            "آویز استفاده کرد. در این مدل پل به راهبر آویزان متصل می‌شود و امکان استفاده از "
            "سازه موجود سالن، هزینه ساخت تیرهای اضافی را کاهش می‌دهد. این جرثقیل به استحکام "
            "سازه وابسته است و بیشتر برای تناژ پایین و دهانه متوسط به کار می‌رود."
        ),
        "features": ("مناسب ارتفاع کم", "استفاده از سازه سالن", "مناسب تناژ پایین"),
    },
    {
        "slug": "pillar-jib-crane",
        "type": "jib-cranes",
        "title": "جرثقیل ستونی بازویی",
        "subtitle": "دسترسی چرخشی در ایستگاه‌های کاری محدود",
        "description": (
            "جرثقیل ستونی بازویی برای محیط‌ها و دسترسی‌های محدود مانند ایستگاه‌های جوشکاری، "
            "تراشکاری و بارگیری انبار طراحی می‌شود. چرخش بازو حول محور ستون، محدوده کاری "
            "مناسبی در اختیار اپراتور قرار می‌دهد و در فضاهای کوچک یک مزیت مهم محسوب می‌شود."
        ),
        "features": ("بازوی چرخشی", "مناسب فضای محدود", "کاربرد در ایستگاه کاری"),
    },
    {
        "slug": "wall-mounted-jib-crane",
        "type": "jib-cranes",
        "title": "جرثقیل دیواری بازویی",
        "subtitle": "بازوی باربرداری متصل به سازه موجود",
        "description": (
            "جرثقیل دیواری بازویی ساختاری مشابه مدل ستونی دارد، با این تفاوت که ستون حذف "
            "می‌شود و دیواره یا سازه موجود نقش تکیه‌گاه را بر عهده می‌گیرد. این طراحی فضای "
            "اشغال‌شده، هزینه و مدت ساخت را نسبت به مدل ستونی کاهش می‌دهد."
        ),
        "features": ("بدون ستون مستقل", "اشغال فضای کمتر", "زمان ساخت کوتاه‌تر"),
    },
    {
        "slug": "single-girder-gantry-crane",
        "type": "gantry-cranes",
        "title": "جرثقیل دروازه‌ای تک پل",
        "subtitle": "راهکار سبک برای باربرداری در فضای باز",
        "description": (
            "جرثقیل دروازه‌ای تک پل معمولا برای ظرفیت تا ۱۰ تن و دهانه کمتر از ۲۰ متر به کار "
            "می‌رود. سازه تک پل آن سبک‌تر و کم‌هزینه‌تر است و در محیط‌هایی با فضای محدود، "
            "به‌ویژه محوطه‌های باز، به‌راحتی قابل طراحی و استفاده است."
        ),
        "features": ("ظرفیت تا ۱۰ تن", "دهانه کمتر از ۲۰ متر", "مناسب فضای باز"),
    },
    {
        "slug": "double-girder-gantry-crane",
        "type": "gantry-cranes",
        "title": "جرثقیل دروازه‌ای دو پل",
        "subtitle": "جابه‌جایی سنگین در انبارها و محوطه‌های تولید",
        "description": (
            "جرثقیل دروازه‌ای دو پل برای بارهای بیش از ۱۰ تن یا دهانه‌های بالاتر از ۲۰ متر "
            "مناسب است. این مدل مزایای جرثقیل سقفی دو پل را در فضای باز فراهم می‌کند و در "
            "انبارها و مراکز تولیدی با نیاز باربرداری سنگین به کار می‌رود."
        ),
        "features": ("ظرفیت بیش از ۱۰ تن", "دهانه بالاتر از ۲۰ متر", "مناسب بارهای سنگین"),
    },
    {
        "slug": "semi-gantry-crane",
        "type": "gantry-cranes",
        "title": "جرثقیل نیم دروازه‌ای",
        "subtitle": "پوشش بخشی از فضای جابه‌جایی سالن",
        "description": (
            "در جرثقیل نیم دروازه‌ای یک طرف پل روی ستون‌های خود جرثقیل و مسیر ریلی حرکت "
            "می‌کند و طرف دیگر بر سازه سالن قرار می‌گیرد. این مدل در فضای باز یا داخل سالن، "
            "به صورت تک پل یا دو پل، برای پوشش جابه‌جایی در بخشی از سالن استفاده می‌شود."
        ),
        "features": ("مدل تک پل یا دو پل", "قابل استفاده داخل یا خارج سالن", "اشغال بخشی از سالن"),
    },
    {
        "slug": "ship-crane",
        "type": "special-cranes",
        "title": "جرثقیل بنادر",
        "subtitle": "بارگیری و تخلیه ایمن در پایانه‌های بندری",
        "description": (
            "جرثقیل بندری برای جابه‌جایی ایمن کانتینرها و اقلام کشتی‌ها در عملیات بارگیری و "
            "تخلیه طراحی می‌شود. انتخاب و طراحی متناسب با ظرفیت هر بندر، راندمان عملیات را "
            "افزایش می‌دهد و به تخصص، تجربه و شناخت کامل شرایط منطقه نیاز دارد."
        ),
        "features": ("طراحی متناسب با بندر", "بارگیری و تخلیه کانتینر", "افزایش راندمان عملیات"),
    },
    {
        "slug": "workshop-mobile-crane",
        "type": "special-cranes",
        "title": "جرثقیل موبایل کارگاهی",
        "subtitle": "جابه‌جایی بار محدود بدون سازه و مسیر ثابت",
        "description": (
            "جرثقیل موبایل کارگاهی در کارگاه‌ها و تعمیرگاه‌ها برای جابه‌جایی بارهای سبک به "
            "کار می‌رود. این مدل به سازه و مسیر حرکت ثابت نیاز ندارد و برای محل‌هایی مناسب "
            "است که استقرار جرثقیل دائم توجیه اقتصادی ندارد. طراحی معرفی‌شده برای حدود ۲ تن است."
        ),
        "features": ("ظرفیت حدود ۲ تن", "بدون مسیر ثابت", "قابل جابه‌جایی در کارگاه"),
    },
    {
        "slug": "heavy-duty-crane",
        "type": "special-cranes",
        "title": "جرثقیل سنگین کار",
        "subtitle": "کارکرد پیوسته و مطمئن در خطوط تولید سنگین",
        "description": (
            "صنایع فولاد، مس، آلومینیوم و ریخته‌گری به جرثقیل‌هایی نیاز دارند که به صورت "
            "مداوم و با ایمنی و قابلیت اطمینان بالا زیر بار کار کنند. سنگین‌کار بودن تنها به "
            "تناژ بار محدود نیست و توانایی کارکرد طولانی و پیوسته را نیز در بر می‌گیرد."
        ),
        "features": ("کارکرد طولانی و مداوم", "قابلیت اطمینان بالا", "مناسب صنایع فلزی"),
    },
    {
        "slug": "industrial-conveyor",
        "type": "material-handling-equipment",
        "title": "نقاله‌های زمینی یا هوایی",
        "subtitle": "انتقال پیوسته مواد و قطعات در خط تولید",
        "description": (
            "نقاله‌ها در صنایع تولیدی وظیفه جابه‌جایی پیوسته و بدون وقفه مواد، قطعات مونتاژ "
            "و محصولات را بر عهده دارند و متناسب با فضا در نوع زمینی یا هوایی طراحی می‌شوند. "
            "صنایع معدنی، فولاد، خودروسازی، لوازم خانگی، غذایی و دارویی از کاربردهای اصلی آن هستند."
        ),
        "features": ("مدل زمینی یا هوایی", "انتقال پیوسته", "طراحی متناسب با خط تولید"),
    },
    {
        "slug": "turning-device",
        "type": "material-handling-equipment",
        "title": "تجهیز برگردان",
        "subtitle": "چرخاندن ایمن محصول برای تکمیل فرایند تولید",
        "description": (
            "تجهیز برگردان امکان چرخاندن محصول و دسترسی به تمام وجوه آن را برای جوشکاری، "
            "افزودن قطعات و رنگ‌آمیزی فراهم می‌کند. تولید مخزن و شاسی‌سازی از مهم‌ترین "
            "کاربردهای این تجهیز در افزایش راندمان و کاهش هزینه تولید است."
        ),
        "features": ("دسترسی به تمام وجوه محصول", "مناسب مخزن و شاسی", "افزایش راندمان تولید"),
    },
    {
        "slug": "light-crane",
        "type": "special-cranes",
        "title": "جرثقیل سبک کار",
        "subtitle": "جابجایی قطعات سبک در خطوط مونتاژ",
        "description": (
            "جرثقیل‌های سبک یا KBK در خطوط تولید و ایستگاه‌های مونتاژ برای جابه‌جایی قطعات "
            "تا ۱۰۰۰ کیلوگرم استفاده می‌شوند. این سامانه متناسب با فضای کاری در انواع تک تیر "
            "و دو تیر طراحی می‌شود و بیشترین کاربرد آن در صنعت خودروسازی است."
        ),
        "features": ("ظرفیت تا ۱۰۰۰ کیلوگرم", "تک تیر یا دو تیر", "مناسب خطوط مونتاژ"),
    },
    {
        "slug": "c-hook",
        "type": "crane-accessories",
        "title": "سی هوک",
        "subtitle": "حمل ایمن کویل، رول و کلاف فلزی",
        "description": (
            "سی هوک از ابزارهای جانبی جرثقیل برای حمل ایمن کویل‌های فولادی، قرقره سیمی، "
            "رول و کلاف فلزی است. این تجهیز در مدل‌های مختلف و بر اساس نیاز پروژه، شرایط "
            "کاری و محصول طراحی می‌شود و راندمان خطوط تولید را افزایش می‌دهد."
        ),
        "features": ("طراحی متناسب با محصول", "حمل ایمن کویل", "افزایش راندمان خط تولید"),
    },
    {
        "slug": "special-crane-trolley",
        "type": "crane-accessories",
        "title": "کالسکه‌های گردان، خورجینی و خاص",
        "subtitle": "تأمین حرکت عرضی و چرخشی روی پل جرثقیل",
        "description": (
            "کالسکه وظیفه تأمین حرکت عرضی، چرخشی یا هر دو را در طول پل جرثقیل بر عهده دارد "
            "و متناسب با محیط کاری طراحی، ساخته و نصب می‌شود. کالسکه گردان در صنایع فولاد، "
            "مس، آلومینیوم و ریخته‌گری و مدل خورجینی در جرثقیل‌های نیمه‌سنگین و سنگین کاربرد دارد."
        ),
        "features": ("حرکت عرضی یا چرخشی", "طراحی متناسب با محیط", "مناسب کار سنگین"),
    },
    {
        "slug": "spreader-beam",
        "type": "crane-accessories",
        "title": "شاهین",
        "subtitle": "حفظ تعادل بارهای بلند و نامتعادل",
        "description": (
            "برای بلند کردن بارهای بلند یا نامتعادل از شاهین متصل به قلاب جرثقیل استفاده "
            "می‌شود. شاهین تعادل بار و ایمنی عملیات را افزایش می‌دهد و متناسب با نیاز مشتری "
            "در ظرفیت‌ها و مدل‌های مختلف طراحی و ساخته می‌شود."
        ),
        "features": ("حفظ تعادل بار", "افزایش ایمنی", "طراحی در ظرفیت‌های مختلف"),
    },
    {
        "slug": "crane-cabin",
        "type": "crane-accessories",
        "title": "کابین جرثقیل",
        "subtitle": "دید بهتر اپراتور و کنترل ایمن‌تر جرثقیل",
        "description": (
            "کابین یکی از تجهیزات مهم کنترل حرکت جرثقیل است و افزایش دید اپراتور، ایمنی "
            "تجهیزات و خود جرثقیل را بهبود می‌دهد. کابین‌های ثابت یا متحرک با امکاناتی مانند "
            "صندلی قابل تنظیم، تهویه مطبوع، جوی‌استیک و شیشه سکوریت ارائه می‌شوند."
        ),
        "features": ("مدل ثابت یا متحرک", "دید بهتر اپراتور", "امکانات قابل سفارش"),
    },
)


SERVICES = (
    {
        "slug": "maintenance",
        "title": "تعمیر، نگهداری و سرویس دوره‌ای",
        "subtitle": "پشتیبانی سطح بالا برای کارکرد ایمن و پایدار",
        "description": (
            "تعمیر و نگهداری جرثقیل در افزایش طول عمر، بهره‌وری و ایمنی تجهیزات نقش اساسی "
            "دارد. تعمیرات دوره‌ای به‌موقع، خطرات احتمالی را کاهش می‌دهد و از خرابی‌های "
            "بزرگ‌تر جلوگیری می‌کند. تیم مجرب وزنه با بازرسی، تهیه فهرست قطعات موردنیاز و "
            "انجام تعمیر یا تعویض اصولی قطعات، جرثقیل را در بهترین شرایط کاری نگه می‌دارد."
        ),
        "items": (
            ("benefit", "افزایش طول عمر تجهیزات", "سرویس منظم از فرسودگی و خرابی زودهنگام جلوگیری می‌کند."),
            ("benefit", "کاهش خطرات احتمالی", "بازرسی دوره‌ای ایرادها را پیش از تبدیل شدن به خرابی بزرگ آشکار می‌کند."),
            ("process", "بازرسی و عیب‌یابی", "کارشناسان وزنه وضعیت جرثقیل و سیستم‌های کنترلی را بررسی می‌کنند."),
            ("process", "تهیه فهرست قطعات", "قطعات معیوب یا فرسوده و اقدامات موردنیاز مشخص می‌شوند."),
            ("process", "تعمیر یا تعویض اصولی", "عملیات تعمیر و تعویض قطعات با هدف بازگشت ایمن تجهیز انجام می‌شود."),
        ),
    },
    {
        "slug": "industrial-structures",
        "title": "سازه‌های فلزی",
        "subtitle": "طراحی و ساخت سازه‌های صنعتی همراه با تجهیزات باربرداری",
        "description": (
            "سازه‌های فلزی و صنعتی شامل کارخانه‌ها، مراکز تولیدی، انبارها و نیروگاه‌ها هستند "
            "و برای فعالیت صنعتی یا تولید محصولات خاص ساخته می‌شوند. شرکت وزنه با بیش از "
            "۶۰ سال تجربه، مجموعه کاملی از سازه‌های فلزی را همراه با جرثقیل‌های موردنیاز "
            "در اختیار صاحبان صنایع قرار می‌دهد."
        ),
        "items": (
            ("benefit", "راهکار یکپارچه", "سازه فلزی و جرثقیل موردنیاز به صورت هماهنگ ارائه می‌شوند."),
            ("benefit", "مناسب صنایع مختلف", "کارخانه، انبار، مرکز تولیدی و نیروگاه از کاربردهای این سازه‌ها هستند."),
        ),
    },
    {
        "slug": "spare-parts",
        "title": "تأمین قطعات یدکی",
        "subtitle": "قطعات اصلی و باکیفیت برای تعمیر سریع و عمر بیشتر",
        "description": (
            "تأمین قطعات یدکی اصلی و باکیفیت، تعمیر سریع، افزایش طول عمر و استفاده طولانی‌مدت "
            "از جرثقیل را ممکن می‌کند. وزنه با همکاری تأمین‌کنندگان معتبر، قطعات مکانیکی، "
            "الکتریکی و سیستم‌های کنترلی را با سرعت و دقت تأمین می‌کند و برای انتخاب صحیح، "
            "مشاوره فنی در اختیار مشتریان قرار می‌دهد."
        ),
        "items": (
            ("benefit", "قطعات اصلی و باکیفیت", "انتخاب قطعه مناسب به افزایش عمر و اطمینان تجهیز کمک می‌کند."),
            ("benefit", "پوشش مکانیک و برق", "قطعات مکانیکی، الکتریکی و سیستم‌های کنترل قابل تأمین هستند."),
            ("process", "مشاوره فنی", "نیاز تجهیز و مشخصات قطعه موردنظر بررسی می‌شود."),
            ("process", "انتخاب و تأمین", "قطعه مناسب از تأمین‌کنندگان معتبر تهیه و ارائه می‌شود."),
        ),
    },
)


PROJECTS = (
    ("kohnuj-combined-cycle-power-plant", "جرثقیل نیروگاه سیکل ترکیبی مپنا کهنوج", "", "کهنوج"),
    ("samangan-combined-cycle-power-plant", "جرثقیل سه‌بالابر نیروگاهی مپنا سمنگان", "سه بالابر نیروگاهی", "سمنگان"),
    ("five-ton-pillar-jib-crane", "جرثقیل ستونی بازویی ۵ تن", "نصب روی پدستال با ارتفاع ستون ۱۲ متر", ""),
    ("zarshouran-gold-complex", "مجتمع معدنی و صنعتی طلای زرشوران", "افتتاح پروژه در سال ۱۳۹۲", "زرشوران"),
    ("fooladkaran-ofogh-abhar", "جرثقیل ۱۶ تن کالسکه گردان فولادکاران افق", "کالسکه گردان با ظرفیت ۱۶ تن", "ابهر"),
    ("kaghaz-kar-kasra", "جرثقیل سه‌بالابر شرکت کاغذ کار کسری", "سه بالابر ۱۸، ۱۸ و ۳۶ تن", ""),
    ("salafchegan-steel", "جرثقیل‌های فولاد سلفچگان", "", "سلفچگان"),
    ("khorasan-steel-complex", "جرثقیل ۱۵ تن مجتمع فولاد خراسان", "ساخت سال ۱۹۸۳ و همچنان در حال کار", "خراسان"),
    ("shahid-rajaei-power-plant", "نیروگاه شهید رجایی", "", ""),
)


SAMPLE_BLOG_SLUGS = (
    "choosing-workshop-crane",
    "preventive-crane-maintenance",
    "safe-load-handling",
    "single-vs-double-girder",
    "crane-modernization-signs",
    "lifting-equipment-inspection",
)


def load_catalogue_content(apps, schema_editor):
    ProductType = apps.get_model("main", "ProductType")
    Product = apps.get_model("main", "Product")
    ProductCapacity = apps.get_model("main", "ProductCapacity")
    ProductSize = apps.get_model("main", "ProductSize")
    ProductFeature = apps.get_model("main", "ProductFeature")
    Project = apps.get_model("main", "Project")
    ProjectFeature = apps.get_model("main", "ProjectFeature")
    Service = apps.get_model("main", "Service")
    ServiceItem = apps.get_model("main", "ServiceItem")
    BlogPost = apps.get_model("main", "BlogPost")

    Product.objects.filter(
        slug__in=("single-girder-overhead-crane", "double-girder-overhead-crane")
    ).delete()
    ProductType.objects.filter(
        slug__in=("جرثقیل-سقفی-تک-پل", "جرثقیل-سقفی-دو-پل")
    ).delete()

    product_types = {}
    for position, (slug, title) in enumerate(PRODUCT_TYPES, start=1):
        product_type, _ = ProductType.objects.update_or_create(
            slug=slug,
            defaults={"title": title, "title_en": "", "position": position},
        )
        product_types[slug] = product_type

    products = []
    for product_data in PRODUCTS:
        description = product_data["description"]
        product, _ = Product.objects.update_or_create(
            slug=product_data["slug"],
            defaults={
                "product_type": product_types[product_data["type"]],
                "title": product_data["title"],
                "title_en": "",
                "subtitle": product_data["subtitle"],
                "subtitle_en": "",
                "short_description": description,
                "short_description_en": "",
                "detailed_description": description,
                "detailed_description_en": "",
                "main_image": "",
                "header_image": "",
                "catalog_file": "",
                "price": 0,
                "is_active": True,
            },
        )
        ProductCapacity.objects.filter(product=product).delete()
        ProductSize.objects.filter(product=product).delete()
        ProductFeature.objects.filter(product=product).delete()
        ProductFeature.objects.bulk_create(
            [
                ProductFeature(product=product, title=title, position=position)
                for position, title in enumerate(product_data["features"], start=1)
            ]
        )
        products.append(product)

    for index, product in enumerate(products):
        related_products = [
            products[(index + offset) % len(products)] for offset in (1, 2, 3)
        ]
        product.similar_products.set(related_products)

    Project.objects.filter(
        slug__in=("tehran-industrial-hall-project", "mobarakeh-steel-project-isfahan")
    ).delete()
    for slug, title, subtitle, location in PROJECTS:
        project, _ = Project.objects.update_or_create(
            slug=slug,
            defaults={
                "title": title,
                "title_en": "",
                "subtitle": subtitle,
                "subtitle_en": "",
                "description": "",
                "description_en": "",
                "location": location,
                "location_en": "",
                "latitude": None,
                "longitude": None,
                "main_image": "",
                "is_active": True,
            },
        )
        ProjectFeature.objects.filter(project=project).delete()

    Service.objects.filter(
        slug__in=("lifting-equipment", "installation", "consulting")
    ).update(is_active=False)
    for position, service_data in enumerate(SERVICES, start=1):
        description = service_data["description"]
        service, _ = Service.objects.update_or_create(
            slug=service_data["slug"],
            defaults={
                "title": service_data["title"],
                "title_en": "",
                "subtitle": service_data["subtitle"],
                "subtitle_en": "",
                "short_description": description,
                "short_description_en": "",
                "detailed_description": description,
                "detailed_description_en": "",
                "main_image": "",
                "header_image": "",
                "catalog_file": "",
                "position": position,
                "is_active": True,
            },
        )
        ServiceItem.objects.filter(service=service).delete()
        ServiceItem.objects.bulk_create(
            [
                ServiceItem(
                    service=service,
                    kind=kind,
                    title=title,
                    description=item_description,
                    position=item_position,
                )
                for item_position, (kind, title, item_description) in enumerate(
                    service_data["items"], start=1
                )
            ]
        )

    BlogPost.objects.filter(slug__in=SAMPLE_BLOG_SLUGS).update(
        is_published=False,
        is_featured=False,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0017_support_title_only_catalogue_projects"),
    ]

    operations = [
        migrations.RunPython(load_catalogue_content, migrations.RunPython.noop),
    ]
