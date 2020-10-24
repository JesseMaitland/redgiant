{% if 'CREATE OR REPLACE VIEW' in content or 'CREATE VIEW' in content %}
{{content.replace('CREATE VIEW', 'CREATE OR REPLACE VIEW')}}
{% else %}
CREATE OR REPLACE VIEW {{schema}}.{{name}}
AS
{{content}}
{% endif %}


