ENV: dict[str, str] = {}
ENV_FILE: str = '.env'

with open(ENV_FILE, 'r') as file:
    for line in file.readlines():
        key, value = line.strip().split('=')
        ENV[key] = value
