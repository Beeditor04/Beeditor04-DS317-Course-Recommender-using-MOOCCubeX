import subprocess


def predict(user_id):
    result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    predict('U_12')
