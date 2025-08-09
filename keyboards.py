from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram import Update, InlineKeyboardMarkup, ChatMember, InlineKeyboardButton

from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes, \
    CallbackQueryHandler

from telegram.constants import ParseMode


syr = ''

usd = 0

auto_app = True 

main_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('شراء رقم 📞' , callback_data = 'الخدمات')
        ],
        [
            InlineKeyboardButton('قسم الرشـق  🖥️' , callback_data = 'تواصل اجتماعي')
        ],
        [
            InlineKeyboardButton('العروض المفعلة ⏳' , callback_data = 'العرض المفعل')
        ],
        [
            InlineKeyboardButton('حسابي 🗂' , callback_data = 'حسابي'),
            InlineKeyboardButton('الإدارة ⚙️' , callback_data = 'الدعم')
        ]
    ]
)




owner_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('إضافة رصيد' , callback_data = 'إضافة رصيد'),
            InlineKeyboardButton('حذف رصيد' , callback_data = 'حذف رصيد')
        ],
        [
            InlineKeyboardButton('تغيير api token' , callback_data = 'تغيير api token'),
            InlineKeyboardButton('تغيير سعر الدولار' , callback_data = 'تغيير سعر الدولار')
        ],
        [
            InlineKeyboardButton('تعديل الأسعار' , callback_data = 'تعديل الأسعار'),
            InlineKeyboardButton('تعديل الدول المتاحة' , callback_data = 'تعديل الدول المتاحة')
        ],
        [
            InlineKeyboardButton('حظر مستخدم' , callback_data = 'حظر مستخدم'),
            InlineKeyboardButton('فك حظر مستخدم' , callback_data = 'فك حظر مستخدم')
        ],
        [
            InlineKeyboardButton('إذاعة' , callback_data = 'إذاعة'),
            InlineKeyboardButton('إرسال رسالة خاصة' , callback_data = 'إرسال رسالة خاصة')
        ],
        [
            InlineKeyboardButton('تشغيل البوت' , callback_data = 'تشغيل البوت'),
            InlineKeyboardButton('إيقاف البوت' , callback_data = 'إيقاف البوت')
        ],
        [
            InlineKeyboardButton('بيانات مستخدم' , callback_data = 'بيانات مستخدم'),
            InlineKeyboardButton('سجلات البوت' , callback_data = 'سجلات البوت')
        ],
        [
            InlineKeyboardButton('عناوين الإيداع' , callback_data = 'عناوين الإيداع'),
            InlineKeyboardButton('خدمات الرشق' , callback_data = 'خدمات الرشق')
        ]
    ]
)



social_owner_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('الأسعار' , callback_data = 'socialprices'),
            InlineKeyboardButton('المعرفات' , callback_data = 'socialids')
        ]
    ]
)




service_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('غوغل-google 💛' , callback_data = 'app:Google'),
            InlineKeyboardButton('واتساب-whatsapp 💚' , callback_data = 'app:Whatsapp')
        ],
        [
            InlineKeyboardButton('سيرفر عام-other 🩶' , callback_data = 'app:General')
        ],
        [
            InlineKeyboardButton('أرقام تيليجرام (جاهزة) 💙' , callback_data = 'Telegram')
        ],
        [
            InlineKeyboardButton('رجوع' , callback_data = 'أساسي')
        ]
    ]
)


my_account = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('شحن الرصيد' , callback_data = 'شحن الرصيد')
        ],
        [
            InlineKeyboardButton('سجل الشراء' , callback_data = 'سجل الشراء'),
            InlineKeyboardButton('سجل الإيداع' , callback_data = 'سجل الإيداع')
        ]
    ]
)



topup_methods = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('سيرياتيل كاش' , callback_data = 'سيرياتيل كاش')
        ],
        [
            InlineKeyboardButton('بايير' , callback_data = 'بايير'),
            InlineKeyboardButton('USDT' , callback_data = 'USDT')
        ],
        [
            InlineKeyboardButton('Binance' , callback_data = 'binance'),
            InlineKeyboardButton('شام كاش' , callback_data = 'شام كاش')
        ],
        [
            InlineKeyboardButton('رجوع' , callback_data = 'حسابي تعديل')
        ]
    ]
)





api_tokens_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('lion BOT' , callback_data = 'changeapi:lion BOT')
        ],
        [
            InlineKeyboardButton('VIOTP' , callback_data = 'changeapi:VIOTP')
        ],
        [
            InlineKeyboardButton('Drop SMS BOT' , callback_data = 'changeapi:Drop SMS BOT')
        ],
        [
            InlineKeyboardButton('SMS live' , callback_data = 'changeapi:SMS live')
        ],
        [
            InlineKeyboardButton('durianrcs' , callback_data = 'changeapi:durianrcs')
        ],
        [
            InlineKeyboardButton('رجوع' , callback_data = 'admin back to main')
        ]
    ]
)



credit_prices_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('سيرياتيل' , callback_data = 'changecredit:syriatel')
        ],
        [
            InlineKeyboardButton('بايير' , callback_data = 'changecredit:payeer')
        ],
        [
            InlineKeyboardButton('شام كاش سوري' , callback_data = 'changecredit:shamsyr'),
            InlineKeyboardButton('شام كاش دولار' , callback_data = 'changecredit:shamdol')
        ],
        [
            InlineKeyboardButton('رجوع' , callback_data = 'admin back to main')
        ]
    ]
)


topup_links_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('سيرياتيل' , callback_data = 'changelink:syr')
        ],
        [
            InlineKeyboardButton('BEP-20' , callback_data = 'changelink:bep20')
        ],
        [
            InlineKeyboardButton('COINEX' , callback_data = 'changelink:coinex')
        ],
        [
            InlineKeyboardButton('بايير' , callback_data = 'changelink:payeer')
        ],
        [
            InlineKeyboardButton('شام كاش سوري' , callback_data = 'changelink:sham_cash_syr'),
            InlineKeyboardButton('شام كاش دولار' , callback_data = 'changelink:sham_cash_dol')
        ],
        [
            InlineKeyboardButton('Binance' , callback_data = 'changelink:binance')
        ],
        [
            InlineKeyboardButton('رجوع' , callback_data = 'admin back to main')
        ]
    ]
)


providers_prices_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('lion BOT' , callback_data = 'prices:lion BOT')
        ],
        [
            InlineKeyboardButton('VIOTP' , callback_data = 'prices:VIOTP')
        ],
        [
            InlineKeyboardButton('Drop SMS BOT' , callback_data = 'prices:Drop SMS BOT')
        ],
        [
            InlineKeyboardButton('SMS live' , callback_data = 'prices:SMS live')
        ],
        [
            InlineKeyboardButton('durianrcs' , callback_data = 'prices:durianrcs')
        ],
        [
            InlineKeyboardButton('رجوع' , callback_data = 'admin back to main')
        ]
    ]
)



available_providers = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('lion BOT' , callback_data = 'foravailable:lion BOT')
        ],
        [
            InlineKeyboardButton('VIOTP' , callback_data = 'foravailable:VIOTP')
        ],
        [
            InlineKeyboardButton('Drop SMS BOT' , callback_data = 'foravailable:Drop SMS BOT')
        ],
        [
            InlineKeyboardButton('SMS live' , callback_data = 'foravailable:SMS live')
        ],
        [
            InlineKeyboardButton('Duriancrs' , callback_data = 'foravailable:durianrcs')
        ],
        [
            InlineKeyboardButton('رجوع' , callback_data = 'admin back to main')
        ]
    ]
)



back_admin_button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('رجوع' , callback_data = 'admin back to main')
        ]
    ]
)




contact_the_bot_button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('طلب رقم من البوت ' , url = 'http://t.me/Denji_sms_bot?start=ID3')
        ]
    ]
)









social_media_main_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Tik tok - تيك توك 🖤' , callback_data = 'social:Tik Tok')
        ],
        [
            InlineKeyboardButton('FaceBook - فيسبوك 💙' , callback_data = 'social:FaceBook')
        ],
        [
            InlineKeyboardButton('Instagram - انستاغرام 💜' , callback_data = 'social:Instagram')
        ],
        [
            InlineKeyboardButton('رجوع' , callback_data = 'أساسي')
        ]
    ]
)


social_offers = {
    "Tik Tok" : 
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('متابعين بدون ضمان 👤❌' , callback_data = 'sofer:Tik Tok:متابعين بدون ضمان')
                ],
                [
                    InlineKeyboardButton('متابعين ضمان سنة 👤✅' , callback_data = 'sofer:Tik Tok:متابعين ضمان سنة')
                ],
                [
                    InlineKeyboardButton('لايكات 👍' , callback_data = 'sofer:Tik Tok:لايكات')
                ],
                [
                    InlineKeyboardButton('مشاهدات ▶️' , callback_data = 'sofer:Tik Tok:مشاهدات')
                ],
                [
                    InlineKeyboardButton('رجوع' , callback_data = 'تواصل اجتماعي')
                ]
            ]
        ) ,
    "FaceBook" :
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('متابعين بدون ضمان 👤❌' , callback_data = 'sofer:FaceBook:متابعين بدون ضمان')
                ],
                [
                    InlineKeyboardButton('متابعين ضمان سنة 👤✅' , callback_data = 'sofer:FaceBook:متابعين ضمان سنة')
                ],
                [
                    InlineKeyboardButton('لايكات 👍' , callback_data = 'sofer:FaceBook:لايكات')
                ],
                [
                    InlineKeyboardButton('مشاهدات ▶️' , callback_data = 'sofer:FaceBook:مشاهدات')
                ],
                [
                    InlineKeyboardButton('رجوع' , callback_data = 'تواصل اجتماعي')
                ]
            ]
        ) ,
    "Instagram" :
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('متابعين بدون ضمان 👤❌' , callback_data = 'sofer:Instagram:متابعين بدون ضمان')
                ],
                [
                    InlineKeyboardButton('متابعين ضمان سنة 👤✅' , callback_data = 'sofer:Instagram:متابعين ضمان سنة')
                ],
                [
                    InlineKeyboardButton('لايكات 👍' , callback_data = 'sofer:Instagram:لايكات')
                ],
                [
                    InlineKeyboardButton('مشاهدات ▶️' , callback_data = 'sofer:Instagram:مشاهدات')
                ],
                [
                    InlineKeyboardButton('رجوع' , callback_data = 'تواصل اجتماعي')
                ]
            ]
        ) 
}













social_owner_app_choosing_prices = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Tik Tok' , callback_data = 'ownprice:Tik Tok')
        ],
        [
            InlineKeyboardButton('FaceBook' , callback_data = 'ownprice:FaceBook')
        ],
        [
            InlineKeyboardButton('Instagram' , callback_data = 'ownprice:Instagram')
        ],
        [
            InlineKeyboardButton('رجوع' , callback_data = 'admin back to main')
        ]
    ]
)


social_owner_app_choosing_ids = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Tik Tok' , callback_data = 'ownid:Tik Tok')
        ],
        [
            InlineKeyboardButton('FaceBook' , callback_data = 'ownid:FaceBook')
        ],
        [
            InlineKeyboardButton('Instagram' , callback_data = 'ownid:Instagram')
        ],
        [
            InlineKeyboardButton('رجوع' , callback_data = 'admin back to main')
        ]
    ]
)


social_offers_owner_prices = {
    "Tik Tok" : 
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('متابعين بدون ضمان' , callback_data = 'sofownpric:Tik Tok:متابعين بدون ضمان')
                ],
                [
                    InlineKeyboardButton('متابعين ضمان سنة' , callback_data = 'sofownpric:Tik Tok:متابعين ضمان سنة')
                ],
                [
                    InlineKeyboardButton('لايكات' , callback_data = 'sofownpric:Tik Tok:لايكات')
                ],
                [
                    InlineKeyboardButton('مشاهدات' , callback_data = 'sofownpric:Tik Tok:مشاهدات')
                ],
                [
                    InlineKeyboardButton('رجوع' , callback_data = 'socialprices')
                ]
            ]
        ) ,
    "FaceBook" :
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('متابعين بدون ضمان' , callback_data = 'sofownpric:FaceBook:متابعين بدون ضمان')
                ],
                [
                    InlineKeyboardButton('متابعين ضمان سنة' , callback_data = 'sofownpric:FaceBook:متابعين ضمان سنة')
                ],
                [
                    InlineKeyboardButton('لايكات' , callback_data = 'sofownpric:FaceBook:لايكات')
                ],
                [
                    InlineKeyboardButton('مشاهدات' , callback_data = 'sofownpric:FaceBook:مشاهدات')
                ],
                [
                    InlineKeyboardButton('رجوع' , callback_data = 'socialprices')
                ]
            ]
        ) ,
    "Instagram" :
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('متابعين بدون ضمان' , callback_data = 'sofownpric:Instagram:متابعين بدون ضمان')
                ],
                [
                    InlineKeyboardButton('متابعين ضمان سنة' , callback_data = 'sofownpric:Instagram:متابعين ضمان سنة')
                ],
                [
                    InlineKeyboardButton('لايكات' , callback_data = 'sofownpric:Instagram:لايكات')
                ],
                [
                    InlineKeyboardButton('مشاهدات' , callback_data = 'sofownpric:Instagram:مشاهدات')
                ],
                [
                    InlineKeyboardButton('رجوع' , callback_data = 'socialprices')
                ]
            ]
        ) 
}




social_offers_owner_ids = {
    "Tik Tok" : 
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('متابعين بدون ضمان' , callback_data = 'sofownids:Tik Tok:متابعين بدون ضمان')
                ],
                [
                    InlineKeyboardButton('متابعين ضمان سنة' , callback_data = 'sofownids:Tik Tok:متابعين ضمان سنة')
                ],
                [
                    InlineKeyboardButton('لايكات' , callback_data = 'sofownids:Tik Tok:لايكات')
                ],
                [
                    InlineKeyboardButton('مشاهدات' , callback_data = 'sofownids:Tik Tok:مشاهدات')
                ],
                [
                    InlineKeyboardButton('رجوع' , callback_data = 'socialids')
                ]
            ]
        ) ,
    "FaceBook" :
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('متابعين بدون ضمان' , callback_data = 'sofownids:FaceBook:متابعين بدون ضمان')
                ],
                [
                    InlineKeyboardButton('متابعين ضمان سنة' , callback_data = 'sofownids:FaceBook:متابعين ضمان سنة')
                ],
                [
                    InlineKeyboardButton('لايكات' , callback_data = 'sofownids:FaceBook:لايكات')
                ],
                [
                    InlineKeyboardButton('مشاهدات' , callback_data = 'sofownids:FaceBook:مشاهدات')
                ],
                [
                    InlineKeyboardButton('رجوع' , callback_data = 'socialids')
                ]
            ]
        ) ,
    "Instagram" :
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('متابعين بدون ضمان' , callback_data = 'sofownids:Instagram:متابعين بدون ضمان')
                ],
                [
                    InlineKeyboardButton('متابعين ضمان سنة' , callback_data = 'sofownids:Instagram:متابعين ضمان سنة')
                ],
                [
                    InlineKeyboardButton('لايكات' , callback_data = 'sofownids:Instagram:لايكات')
                ],
                [
                    InlineKeyboardButton('مشاهدات' , callback_data = 'sofownids:Instagram:مشاهدات')
                ],
                [
                    InlineKeyboardButton('رجوع' , callback_data = 'socialids')
                ]
            ]
        ) 
}