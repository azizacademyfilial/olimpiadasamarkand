from django.db import migrations


FRONTEND_2_DATA = [('console.log(error) da error o‘zgaruvchiga qiymat berilmagan bo‘lsa nima chiqadi?',
  'null',
  'undefined',
  'error',
  'false',
  'B'),
 ('const bilan e’lon qilingan qiymatni keyin o‘zgartirish mumkinmi?',
  'Ha',
  'Yo‘q',
  'Faqat number bo‘lsa',
  'Faqat string bo‘lsa',
  'B'),
 ('typeof "Hello" natijasi nima bo‘ladi?', 'number', 'string', 'boolean', 'object', 'B'),
 ('Boolean qiymatlar qaysilar?', 'yes / no', 'true / false', 'on / off', '1 / 2', 'B'),
 ('if operatori nima uchun ishlatiladi?',
  'Takrorlash uchun',
  'Shart tekshirish uchun',
  'Matn chiqarish uchun',
  'Fayl ochish uchun',
  'B'),
 ('== nimani tekshiradi?',
  'Qiymatni taqqoslaydi',
  'Qiymat beradi',
  'Funksiya yaratadi',
  'Console ochadi',
  'A'),
 ('true qanday ma’lumot turi?', 'string', 'number', 'boolean', 'object', 'C'),
 ('"JavaScript".toUpperCase() natijasi nima bo‘ladi?',
  'javascript',
  'JavaScript',
  'JAVASCRIPT',
  'undefined',
  'C'),
 ('let arr = [10, 20, 30]; console.log(arr[0]); natijasi nima bo‘ladi?',
  '10',
  '20',
  '30',
  'undefined',
  'A'),
 ('JavaScript’da data typelar nechta?', '5 ta', '6 ta', '8 ta', '10 ta', 'C'),
 ('JavaScript’da data typelar nechta katta turga bo‘linadi?', '1 ta', '2 ta', '3 ta', '4 ta', 'B'),
 ('Arrow function qanday yoziladi?',
  'function = () {}',
  'const test = () => {}',
  'arrow function test() {}',
  'const test => () {}',
  'B'),
 ('Array ichiga object qo‘shsa bo‘ladimi?',
  'Ha, bo‘ladi',
  'Yo‘q, bo‘lmaydi',
  'Faqat number qo‘shiladi',
  'Faqat string qo‘shiladi',
  'A'),
 ('Array bilan Objectning farqi nimada?',
  'Array tartibli ro‘yxat, Object esa key-value ko‘rinishida bo‘ladi',
  'Array faqat matn saqlaydi, Object faqat son saqlaydi',
  'Array JavaScript’da ishlamaydi, Object ishlaydi',
  'Array bilan Object bir xil narsa',
  'A'),
 ('Console’ga aynan "undefined" degan yozuv chiqishi uchun qaysi kod to‘g‘ri?',
  'console.log(undefined) — qiymat sifatida undefined chiqaradi',
  'console.log("undefined") — matn sifatida undefined chiqaradi',
  'console.log(undefind) — xato, noto‘g‘ri yozilgan',
  'console.log(null) — null chiqaradi',
  'B'),
 ('console.log(true == false) natijasi nima bo‘ladi?',
  'true — chunki ikkalasi boolean',
  'false — chunki true va false bir-biriga teng emas',
  'undefined — qiymat yo‘q',
  'error — kod noto‘g‘ri yozilgan',
  'B'),
 ('console.log(false == null) natijasi nima bo‘ladi?',
  'true — chunki false bo‘sh qiymatga teng',
  'false — chunki false va null == da teng emas',
  'undefined — qiymat topilmadi',
  'error — kod noto‘g‘ri yozilgan',
  'B'),
 ('console.log(typeof(null)) natijasi nima bo‘ladi?',
  'null — chunki qiymat null',
  'undefined — chunki qiymat yo‘q',
  'object — JavaScript’da typeof null natijasi object chiqadi',
  'boolean — true/false qiymat',
  'C'),
 ('setTimeout nima uchun ishlatiladi?',
  'Kodni ma’lum vaqt kutib keyin ishlatish uchun',
  'Kodni darrov to‘xtatish uchun',
  'Array ichiga element qo‘shish uchun',
  'Object yaratish uchun',
  'A'),
 ('NodeList qachon chiqadi?',
  'querySelectorAll() bilan bir nechta HTML element tanlanganda',
  'console.log() noto‘g‘ri yozilganda',
  'typeof null yozilganda',
  'setTimeout ishlaganda',
  'A')]


def seed_frontend2_javascript_tests(apps, schema_editor):
    Subject = apps.get_model('olympiad', 'Subject')
    Level = apps.get_model('olympiad', 'Level')
    Question = apps.get_model('olympiad', 'Question')

    subject, _ = Subject.objects.get_or_create(name='IT')
    level, _ = Level.objects.get_or_create(
        subject=subject,
        name='Frontend 2',
        defaults={'duration_minutes': 30},
    )

    Question.objects.filter(subject=subject, level=level).delete()
    Question.objects.bulk_create([
        Question(
            subject=subject,
            level=level,
            version=1,
            text=text,
            option_a=a,
            option_b=b,
            option_c=c,
            option_d=d,
            correct_answer=correct,
        )
        for text, a, b, c, d, correct in FRONTEND_2_DATA
    ])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0008_seed_rus_tili_harder_tests'),
    ]

    operations = [
        migrations.RunPython(seed_frontend2_javascript_tests, noop_reverse),
    ]
