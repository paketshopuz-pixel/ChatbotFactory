# "ChatBot Factory" Loyihasi Bo'yicha Hisobot (1-Bosqich)

## 1. Xulosa
Foydalanuvchi autentifikatsiyasi tizimi muvaffaqiyatli implementatsiya qilindi. Foydalanuvchilar endi ro'yxatdan o'tishi, tizimga kirishi, sessiyalarini boshqarishi va himoyalangan sahifalarga kirishi mumkin.

## 2. Bajarilgan Ishlar
- [x] Ro'yxatdan o'tish va kirish uchun `Flask-WTF` formalari yaratildi.
- [x] `/register`, `/login`, `/logout`, `/dashboard` marshrutlari to'liq logikasi bilan yaratildi.
- [x] `Flask-Login` yordamida sessiyalarni boshqarish va sahifalarni himoyalash joriy etildi.
- [x] Barcha kerakli shablonlar (`register.html`, `login.html`, `dashboard.html`) yaratildi va `base.html` yangilandi.

## 3. Loyihani Tekshirish Yo'riqnomasi
Quyidagi amallarni bajarib, yangi funksionallikni tekshiring:
1. "Register" sahifasiga o'ting va yangi hisob yarating.
2. "Login" sahifasiga o'ting va shu hisob bilan tizimga kiring.
3. Tizimga kirgach, "Dashboard" sahifasiga yo'naltirilganingizni tekshiring.
4. Navigatsiya panelida "Dashboard" va "Logout" linklari paydo bo'lganini tekshiring.
5. "Logout" tugmasini bosing va tizimdan chiqing.
6. Tizimdan chiqqan holda `/dashboard` manziliga kirishga harakat qiling. Siz "Login" sahifasiga qayta yo'naltirilishingiz kerak.