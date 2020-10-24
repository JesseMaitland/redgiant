{%for column in columns%}
    {{column[2].ljust(4)}} {{' ' * (i - column[2].__len__()) }} {{column[4]}} {{column[5]}} {{column[6]}} {{column[7]}}{%if not loop.last%},{%endif%}

{%endfor%}
