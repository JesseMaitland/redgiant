PARTITION BY({%for interval in config.partition.by%}{{interval.name.lower()}}{{ ", " if not loop.last }}{%endfor%})
