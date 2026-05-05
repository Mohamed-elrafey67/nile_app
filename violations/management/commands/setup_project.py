"""
أمر إعداد المشروع الكامل:
  python manage.py setup_project

يقوم بـ:
  1. تطبيق جميع الـ migrations
  2. إنشاء المستخدمين التجريبيين الأربعة (أو تحديث كلمات مرورهم)
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from violations.models import UserProfile


USERS = [
    {'username': 'manager',    'password': 'Manager@123',    'first_name': 'مدير النظام',   'role': 'manager'},
    {'username': 'supervisor', 'password': 'Supervisor@123', 'first_name': 'المشرف العام',  'role': 'supervisor'},
    {'username': 'data_entry', 'password': 'DataEntry@123',  'first_name': 'مدخل البيانات', 'role': 'data_entry'},
    {'username': 'viewer',     'password': 'Viewer@123',     'first_name': 'مستخدم مشاهد',  'role': 'viewer'},
]


class Command(BaseCommand):
    help = 'إعداد المشروع: تطبيق المهاجرات + إنشاء المستخدمين'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n══ الخطوة 1: تطبيق المهاجرات ══'))
        call_command('migrate', verbosity=1)

        self.stdout.write(self.style.MIGRATE_HEADING('\n══ الخطوة 2: إنشاء المستخدمين ══'))
        self.stdout.write('─' * 60)

        for u in USERS:
            user, created = User.objects.get_or_create(username=u['username'])
            user.set_password(u['password'])
            user.first_name = u['first_name']
            user.is_active  = True
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = u['role']
            profile.save()

            status = self.style.SUCCESS('تم إنشاؤه ✓') if created else self.style.WARNING('تم تحديثه ↺')
            self.stdout.write(f"  {status}  {u['first_name']:<20} | {u['username']:<12} | {u['password']}")

        self.stdout.write('─' * 60)
        self.stdout.write(self.style.SUCCESS('\n✅ المشروع جاهز! شغّل الخادم بـ:'))
        self.stdout.write(self.style.HTTP_INFO('   python manage.py runserver\n'))

        self.stdout.write(self.style.MIGRATE_HEADING('══ بيانات تسجيل الدخول ══'))
        self.stdout.write(f"  {'الاسم':<22} {'المستخدم':<14} {'كلمة المرور'}")
        self.stdout.write('─' * 55)
        for u in USERS:
            self.stdout.write(f"  {u['first_name']:<22} {u['username']:<14} {u['password']}")
        self.stdout.write('')
