import psycopg2
from pathlib import Path
from rsterm.configs import RsTermConfig


def get_redscope_connection() -> psycopg2.connect:
    redscope_config_path = Path(__file__).absolute().parent.parent / "redscope.yml"
    rsterm = RsTermConfig.parse_config(redscope_config_path)

    if rsterm.override_file:
        rsterm = RsTermConfig.override_config(rsterm)

    if rsterm.load_env:
        RsTermConfig.load_rsterm_env(rsterm)

    return rsterm.get_db_connection('redscope')
