from django.db import migrations


PATTERNS = {
    ('IT', 'Backend 1'): [
        'B', 'D', 'A', 'C', 'A', 'C', 'D', 'B', 'C', 'A',
        'B', 'D', 'D', 'B', 'C', 'A', 'A', 'D', 'B', 'C',
    ],
    ('IT', 'Backend 2'): [
        'D', 'A', 'C', 'B', 'C', 'B', 'A', 'D', 'B', 'D',
        'C', 'A', 'A', 'C', 'D', 'B', 'C', 'A', 'B', 'D',
    ],
    ('Matematika', '1-sinf'): [
        'C', 'B', 'D', 'A', 'D', 'A', 'C', 'B', 'A', 'C',
        'D', 'B', 'B', 'D', 'A', 'C', 'D', 'A', 'C', 'B',
    ],
    ('Matematika', '5-sinf'): [
        'A', 'C', 'B', 'D', 'B', 'D', 'A', 'C', 'D', 'B',
        'C', 'A', 'C', 'A', 'D', 'B', 'A', 'C', 'D', 'B',
    ],
}


def remix_options(apps, schema_editor):
    Subject = apps.get_model('olympiad', 'Subject')
    Level = apps.get_model('olympiad', 'Level')
    Question = apps.get_model('olympiad', 'Question')

    for (subject_name, level_name), pattern in PATTERNS.items():
        subject = Subject.objects.filter(name=subject_name).first()
        if not subject:
            continue
        level = Level.objects.filter(subject=subject, name=level_name).first()
        if not level:
            continue
        questions = list(Question.objects.filter(subject=subject, level=level).order_by('id'))
        for index, question in enumerate(questions):
            target = pattern[index % len(pattern)]
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
        ('olympiad', '0011_mix_backend_math_options'),
    ]

    operations = [
        migrations.RunPython(remix_options, migrations.RunPython.noop),
    ]
