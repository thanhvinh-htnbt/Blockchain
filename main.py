import base64

import deploy.deploy as deploy
import encryptor
import decryptor

if __name__ == '__main__':
    w3, contract, server = deploy.deploy()
    user = deploy.create_player(w3, contract, server)

    print(deploy.get_user_balance(w3, contract, server))
    print(deploy.get_user_balance(w3, contract, user))


    deploy.reward(w3, contract, server, user, 100)

    print(deploy.get_user_balance(w3, contract, server))
    print(deploy.get_user_balance(w3, contract, user))

    with open("NFTsData/image.jpg", "rb") as f:
        file_data = f.read()

    symmetric_key, encrypted_image = encryptor.encrypt_image(file_data)

    cipher_str = base64.b64encode(encrypted_image).decode("utf-8")

    receipt = deploy.buy_item(w3, contract, user, 100, cipher_str)

    print(deploy.get_user_balance(w3, contract, server))
    print(deploy.get_user_balance(w3, contract, user))

    image_int = deploy.get_user_image_count(w3, contract, user)

    string = deploy.get_image_cipher(w3, contract, user, image_int - 1)

    cipher_bytes = base64.b64decode(string)

    decrypted_data = decryptor.decrypt_image(symmetric_key, cipher_bytes)

    with open("output.jpg", "wb") as f:
        f.write(decrypted_data)



