import yaml
from line_notify import LineNotify

def main():
    with (open("../config.yaml", "rt", encoding="utf-8") as config_file,
          open("../secret.yaml", "rt", encoding="utf-8") as secret_file):
        config_data = yaml.safe_load(config_file)
        secret_data = yaml.safe_load(secret_file)
        candidate_name = config_data["candidate-name"]
        access_token = secret_data[config_data["line-access-token-key"]]

        notify = LineNotify(access_token)
        notify.send(f"Hello! This is a message from {candidate_name}")

if __name__ == '__main__':
    main()
