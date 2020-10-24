{%for column in columns%}
    {{column[2].ljust(4)}} {{' ' * (i - column[2].__len__()) }} {{column[4]}}{%if not loop.last%},{%endif%}

{%endfor%}
