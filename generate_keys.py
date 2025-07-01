# generate_keys.py
import streamlit_authenticator as stauth

# Você pode adicionar quantos usuários quiser aqui
passwords = ['abc', 'def'] # Senhas que você quer hashear
hashed_passwords = stauth.Hasher(passwords).generate()

print(hashed_passwords)
