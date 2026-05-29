from django.db import migrations


TARGETS = [
    ('IT', 'Backend 1'),
    ('IT', 'Backend 2'),
    ('Matematika', '1-sinf'),
]

PATTERN = [
    'C', 'A', 'D', 'B', 'A', 'D', 'C', 'B', 'D', 'A',
    'B', 'C', 'A', 'D', 'B', 'C', 'D', 'B', 'A', 'C',
]


def mix_options(apps, schema_editor):
    Subject = apps.get_model('olympiad', 'Subject')
    Level = apps.get_model('olympiad', 'Level')
    Question = apps.get_model('olympiad', 'Question')

    for subject_name, level_name in TARGETS:
        subject = Subject.objects.filter(name=subject_name).first()
        if not subject:
            continue
        level = Level.objects.filter(subject=subject, name=level_name).first()
        if not level:
            continue

        questions = list(Question.objects.filter(subject=subject, level=level).order_by('id'))
        for index, question in enumerate(questions):
            target = PATTERN[index % len(PATTERN)]
            options = {
                'A': question.option_a,
                'B': question.option_b,
                'C': question.option_c,
                'D': question.option_d,
            }
            correct_text = options.get(question.correct_answer, question.option_a)

            new_options = {target: correct_text}
            remaining_letters = [letter for letter in ['A', 'B', 'C', 'D'] if letter != target]
            remaining_values = [value for letter, value in options.items() if letter != question.correct_answer]
            for letter, value in zip(remaining_letters, remaining_values):
                new_options[letter] = value

            question.option_a = new_options['A']
            question.option_b = new_options['B']
            question.option_c = new_options['C']
            question.option_d = new_options['D']
            question.correct_answer = target
            question.save(update_fields=['option_a', 'option_b', 'option_c', 'option_d', 'correct_answer'])


class Migration(migrations.Migration):

    dependencies = [
        ('olympiad', '0010_reverse_arab_hamshiralik_tests'),
    ]

    operations = [
        migrations.RunPython(mix_options, migrations.RunPython.noop),
    ]
