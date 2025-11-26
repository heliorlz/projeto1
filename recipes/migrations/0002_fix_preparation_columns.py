from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            """
            ALTER TABLE recipes_recipe
            RENAME COLUMN preparation_step TO preparation_steps;
            """,
            reverse_sql="""
            ALTER TABLE recipes_recipe
            RENAME COLUMN preparation_steps TO preparation_step;
            """,
        ),
        migrations.RunSQL(
            """
            ALTER TABLE recipes_recipe
            RENAME COLUMN preparation_step_is_html TO preparation_steps_is_html;
            """,
            reverse_sql="""
            ALTER TABLE recipes_recipe
            RENAME COLUMN preparation_steps_is_html TO preparation_step_is_html;
            """,
        ),
    ]
