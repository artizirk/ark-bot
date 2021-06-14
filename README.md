# ARK Sõidueksami bot
Küsib ARK-i lehelt uusimad eksami ajad ja saadab sõnumi [Matrixi](https://matrix.org/) kanali

## Dev setup Linux

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Also copy create a correct dotenv file

    cp example.env .env

## Usage
After sourcing venv run like so:

    python main.py
