[pytest]
norecursedirs = .* media
python_files = src/**/*_test.py
python_functions = test_*
env_files = .env.test
log_cli = true
log_level = WARNING
log_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S

[pytest-watch]
nobeep = True
ext = .py,.tz
