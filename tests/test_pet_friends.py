from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос api ключа возвращает статус 200,
    и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа - в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key.
    Далее, используя этот ключ, запрашиваем список всех питомцев и проверяем что список - не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барсик', animal_type='кот',
                                     age=3, pet_photo='images/cat2222.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Муррзик", "кот", "3", "images/cat22.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котяра', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_add_pet_simple_valid_data(name='Муська', animal_type='Кошка', age=6):
    """Проверяем, что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_set_pet_photo_valid_data(pet_photo='images/cat.jpg'):
    """Проверяем, что можно добавить изображение к последнему добавленному питомцу"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_simple_pet_invalid_animal_type(name: str = 'Рузик',
                                               animal_type: str = 'xx', age: int = 5):
    """Проверим по негативному сценарию, что в поле "Порода" при заведении нового питомца должно быть более двух симсволов"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['animal_type']) > 2, 'В поле "Порода" должно быть больше символов'

def test_add_simple_pet_invalid_name(name: str = 'Барсик23', animal_type: str = 'Кот', age: int = 1):
    """Проверим по негативному сценарию, что в поле "Имя" при заведении нового питомца нельзя указывать числа"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Проверяем что статус ответа = 200, вид питомца указано в буквенном значении
    assert status == 200
    assert result['name'].isalpha(), 'Поле "Имя" не должно содержать цифры, только буквы'

def test_update_simple_pet_invalid_animal_type(name: str = 'Барсик', animal_type: str = 'Кот22', age: int = 1):
    """Проверим по негативному сценарию, что при заведении нового питомца в поле "Порода" нельзя указывать числа"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Проверяем что статус ответа = 200, вид питомца указано в буквенном значении
    assert status == 200
    assert result['animal_type'].isalpha(), 'Поле "Порода" не должно содержать цифры, только буквы'

def test_update_simple_pet_invalid_age(name: str ='Нюша', animal_type: str = 'Кошка', age: int = 100):
    """Проверка по негативному сценарию на примере последнего добавленного питомца, поле "Возраст" не может принимать трехзначное число"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(result['age']) < 3, 'Для возраста трехзначное число не принимается'
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_invalid_add_simple_pet_animal_type(name: str = 'Кузя', animal_type: str = '', age: int = 1):
    """Проверим по негативному сценарию, что при добавлении нового питомца без указания породы, возникнет ошибка"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['animal_type'] != '', 'Поле "Порода" должно быть заполнено'

def test_invalid_add_simple_pet_name(name: str = '', animal_type: str = 'Пес', age: int = 1):
    """Проверим по негативному сценарию, что при добавлении нового питомца без указания имени, возникнет ошибка"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] != '', 'Поле "Имя" должно быть заполнено'

def test_get_api_key_for_invalid_user(email='121212@g.eru', password=valid_password):
    """Проверяем запрос с неверным e-mail, верным паролем и наличием ключа key в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа - в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_password(email=valid_email, password='qwerty'):
    """Проверяем запрос с верным e-mail, неверным паролем и наличием ключа key в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа - в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


