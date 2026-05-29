from django.db import migrations


KOREYS_DATA = {
    'Koreys tili 1': [
        ('저는 내일 친구를 ___ 거예요.', '만나', '만나고', '만날', '만나서', 'C'),
        ('비가 와서 학교에 ___.', '갑니다', '안 갑니다', '못 갑니다', '갈 겁니다', 'C'),
        ('저는 어제 숙제를 다 ___ 했어요.', '—', '해서', '하고', '해고', 'A'),
        ('저는 한국어___ 잘 못해요.', '를', '에', '는', '도', 'A'),
        ('배가 아파서 밥을 ___.', '안 먹어요', '못 먹어요', '먹지 않아요', '먹을 거예요', 'B'),
        ('저는 공부하___ 도서관에 갔어요.', '러', '고', '서', '는', 'A'),
        ('저는 책을 읽___ 음악을 들었어요.', '고', '서', '러', '는', 'A'),
        ('어제 본 영화___ 생각보다 재미있었어요.', '는', '을', '이', '도', 'A'),
        ('저는 친구___ 같이 여행을 갈 거예요.', '와', '를', '에', '은', 'A'),
        ('저는 주말에 집___ 쉬고 싶어요.', '에', '에서', '와', '도', 'B'),
        ('저는 내일 일찍 일어나___ 운동할 거예요.', '고', '서', '러', '는', 'B'),
        ('어제는 너무 피곤해서 공부를 ___.', '안 했어요', '못 했어요', '하지 않았어요', '할 거예요', 'B'),
        ('저는 한국어___ 영어도 같이 공부하고 있어요.', '는', '를', '와', '에', 'C'),
        ('친구를 만나___ 같이 밥을 먹었어요.', '고', '서', '러', '는', 'B'),
        ('저는 시간이 없어서 숙제를 다 ___.', '못 했어요', '안 했어요', '할 거예요', '하고', 'A'),
        ('저는 운동하___ 공원에 갑니다.', '러', '고', '서', '는', 'A'),
        ('어제 읽은 책___ 너무 어려웠어요.', '는', '을', '이', '도', 'A'),
        ('저는 매일 한국어를 ___ 공부합니다.', '열심히', '못', '안', '같이', 'A'),
        ('친구___ 선물을 줬어요.', '에게', '를', '와', '은', 'A'),
        ('저는 피곤해서 일찍 ___.', '잤어요', '자요', '잘 거예요', '자고', 'A'),
    ],
    'Koreys tili 2': [
        ('저는 시간이 없___ 오늘 못 만나요.', '아서', '여서', '기 때문에', '는데', 'C'),
        ('비가 오___ 우산을 가져가세요.', '어서', '니까', '는데', '고', 'B'),
        ('저는 한국에 가___ 한국어를 배우고 싶어요.', '고', '서', '러', '면', 'B'),
        ('이 책은 생각보다 ___ 재미있어요.', '더', '가장', '너무', '잘', 'A'),
        ('어제 너무 피곤해서 일찍 ___.', '자요', '잤어요', '잘 거예요', '자고', 'B'),
        ('저는 친구___ 선물을 받았어요.', '에', '에게', '를', '와', 'B'),
        ('날씨가 좋___ 산에 갈 거예요.', '아서', '으면', '으니까', '는데', 'B'),
        ('저는 매일 운동을 하___ 건강해졌어요.', '아서', '고', '면', '러', 'A'),
        ('이 음식은 너무 매워___ 못 먹겠어요.', '서', '고', '면', '니까', 'A'),
        ('저는 한국어를 배우___ 한국에 가고 싶어요.', '아서', '려고', '고', '면', 'B'),
        ('시간이 있___ 같이 영화 봐요.', '아서', '으면', '고', '는데', 'B'),
        ('저는 책을 읽___ 잠들었어요.', '고', '서', '다가', '러', 'C'),
        ('이 문제는 생각보다 ___ 어렵네요.', '더', '너무', '잘', '아주', 'A'),
        ('저는 어제 친구를 만나___ 밥을 먹었어요.', '고', '서', '다가', '러', 'B'),
        ('한국어를 열심히 공부하___ 시험에 합격했어요.', '아서', '고', '면', '러', 'A'),
        ('저는 어릴 때부터 음악을 ___ 좋아했어요.', '많이', '잘', '자주', '너무', 'A'),
        ('비가 오___ 밖에 나가지 않았어요.', '아서', '으면', '고', '는데', 'A'),
        ('저는 운동을 하___ 스트레스를 풀어요.', '고', '서', '면', '러', 'B'),
        ('친구가 오___ 같이 저녁을 먹을 거예요.', '아서', '으면', '고', '는데', 'B'),
        ('저는 한국어를 잘하___ 매일 연습해요.', '아서', '려고', '고', '면', 'B'),
    ],
}


def seed_koreys_tili_tests(apps, schema_editor):
    Subject = apps.get_model('olympiad', 'Subject')
    Level = apps.get_model('olympiad', 'Level')
    Question = apps.get_model('olympiad', 'Question')
    Student = apps.get_model('olympiad', 'Student')

    subject, _ = Subject.objects.get_or_create(name='Koreys tili')

    rename_map = {
        'Koreys 1': 'Koreys tili 1',
        'Koreys': 'Koreys tili 1',
        'Koreys 2': 'Koreys tili 2',
        'Koreys tili Level 2': 'Koreys tili 2',
        'Koreys tili 02': 'Koreys tili 2',
    }

    targets = {}
    for level_name in KOREYS_DATA:
        level, _ = Level.objects.get_or_create(
            subject=subject,
            name=level_name,
            defaults={'duration_minutes': 30},
        )
        targets[level_name] = level

    for old_name, target_name in rename_map.items():
        old_level = Level.objects.filter(subject=subject, name=old_name).first()
        target_level = targets[target_name]
        if old_level and old_level.id != target_level.id:
            Student.objects.filter(subject=subject, level=old_level).update(level=target_level, selected_version=None)
            Question.objects.filter(subject=subject, level=old_level).delete()
            if not Student.objects.filter(level=old_level).exists():
                old_level.delete()

    for level_name, questions in KOREYS_DATA.items():
        level = targets[level_name]
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
            for text, a, b, c, d, correct in questions
        ])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0006_question_version_student_selected_version'),
    ]

    operations = [
        migrations.RunPython(seed_koreys_tili_tests, noop_reverse),
    ]
