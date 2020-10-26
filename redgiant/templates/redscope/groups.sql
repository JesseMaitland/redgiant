{% for group in groups %}
ALTER GROUP {{group[1]}} ADD USER {{user}};
{% endfor %}
