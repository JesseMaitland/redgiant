  {%for interval in config.partition.by%}
    {% if interval.name == 'DATES'%}
       {{config.partition.column}}::DATE AS {{interval.name.lower().rstrip('s')}}{{ ", " if not loop.last }}
    {%else%}
       DATEPART({{interval.name}}, {{config.partition.column}}) AS {{interval.name.lower()}}{{ ", " if not loop.last }}
    {% endif %}
  {% endfor %}
