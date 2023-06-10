import re
import vk_api


# получение ссылки пользователя
def get_profile_link(user_id):
    return f"https://vk.com/id{user_id}"


# исключения для видов ссылок
def get_user_id(user_input, api):
    # Функция для получения ID пользователя на основе введенных данных (user_input)
    # и объекта API VK (api)

    # Проверяем, является ли ввод коротким именем пользователя
    if re.match(r'^[a-zA-Z0-9_.]+$', user_input):
        try:
            # Получаем информацию о пользователе по короткому имени
            response = api.users.get(user_ids=user_input)
            user_id = response[0]['id']
            return str(user_id)
        except vk_api.exceptions.VkApiError:
            pass

    # Проверяем, является ли ввод ссылкой на профиль
    if re.match(r'^(https?://)?(www\.)?vk\.com/[a-zA-Z0-9_.]+$', user_input):
        try:
            # Извлекаем короткое имя из ссылки на профиль
            screen_name = re.search(r'(?<=vk\.com/)[a-zA-Z0-9_.]+', user_input).group(0)
            # Получаем информацию о пользователе по короткому имени
            response = api.utils.resolveScreenName(screen_name=screen_name)
            user_id = response['object_id']
            return str(user_id)
        except (vk_api.exceptions.VkApiError, AttributeError):
            pass

    # Проверяем, является ли ввод числовым ID пользователя
    if user_input.isdigit():
        try:
            # Получаем информацию о пользователе по ID
            response = api.users.get(user_ids=user_input)
            user_id = response[0]['id']
            return str(user_id)
        except vk_api.exceptions.VkApiError:
            pass

    # Если не удалось получить ID, возвращаем None
    return None


# получение всех друзей пользователя
def get_user_friends(api, user_id):
    # Получаем список друзей пользователя с помощью метода friends.get API VK
    friends = api.friends.get(user_id=user_id, fields='first_name, last_name')

    # Извлекаем профили друзей из полученного списка
    friend_profiles = friends.get('items', [])

    # Создаем список для хранения информации о друзьях
    friend_list = []

    # Обрабатываем каждого друга
    for friend in friend_profiles:
        # Формируем ссылку на профиль друга
        friend_link = f"https://vk.com/id{friend['id']}"

        # Создаем строку с информацией о друге и добавляем ее в список
        friend_list.append(f"Имя: {friend.get('first_name', 'не указано')}, Фамилия: {friend.get('last_name', 'не указано')}, Ссылка: {friend_link}")

    # Возвращаем список с информацией о друзьях
    return friend_list


# словарь для гендера
def get_gender(sex):
    # Функция для определения пола пользователя на основе кода пола (sex)
    if sex == 1:
        return 'Женский'
    elif sex == 2:
        return 'Мужской'
    else:
        return 'Не указан'


# словарь жизненной позиции
def get_life_position_info(life_position):
    # Проверяем, если life_position не задан, возвращаем 'не указана'
    if not life_position:
        return 'не указана'

    # Словарь с политическими предпочтениями и их значениями
    political_preferences = {
        1: 'коммунистические',
        2: 'социалистические',
        3: 'умеренные',
        4: 'либеральные',
        5: 'консервативные',
        6: 'монархические',
        7: 'ультраконсервативные',
        8: 'индифферентные',
        9: 'либертарианские'
    }

    # Словарь с главными качествами в людях и их значениями
    main_in_people = {
        1: 'ум и креативность',
        2: 'доброта и честность',
        3: 'красота и здоровье',
        4: 'власть и богатство',
        5: 'смелость и упорство',
        6: 'юмор и жизнелюбие'
    }

    # Словарь с отношением к курению и его значениями
    smoking_attitude = {
        1: 'резко негативное',
        2: 'негативное',
        3: 'компромиссное',
        4: 'нейтральное',
        5: 'положительное'
    }

    # Словарь с отношением к алкоголю и его значениями
    alcohol_attitude = {
        1: 'резко негативное',
        2: 'негативное',
        3: 'компромиссное',
        4: 'нейтральное',
        5: 'положительное'
    }

    # Создаем словарь с информацией о позиции в жизни
    life_position_info = {
        'Политические предпочтения': political_preferences.get(life_position.get('political', 0), 'не указано'),
        'Мировоззрение': life_position.get('worldview', 'не указано'),
        'Главное в жизни': life_position.get('important_in_life', 'не указано'),
        'Главное в людях': main_in_people.get(life_position.get('people_main', 0), 'не указано'),
        'Отношение к курению': smoking_attitude.get(life_position.get('smoking', 0), 'не указано'),
        'Отношение к алкоголю': alcohol_attitude.get(life_position.get('alcohol', 0), 'не указано'),
        'Вдохновляют': life_position.get('inspired_by', 'не указано') or 'не указано'  # Если поле 'inspired_by' пустое, выводим 'не указано'
    }

    return life_position_info


# информация о карьере
def get_career_info(career_list):
    # Проверяем, если career_list не задан, возвращаем 'не указано'
    if not career_list:
        return 'не указано'

    positions = []
    for position in career_list:
        # Получаем group_id из словаря position
        group_id = position.get('group_id')
        if group_id:
            # Формируем ссылку на группу VK с использованием group_id
            group_link = f"https://vk.com/club{group_id}"
            # Получаем название группы VK с использованием group_id
            group_name = api.groups.getById(group_id=abs(group_id))[0].get('name', 'не указано')
        else:
            group_link = ""
            group_name = "не указано"

        # Получаем название должности из словаря position или 'должность не указана', если отсутствует
        position_name = position.get('position')
        if position_name:
            positions.append(f"{group_name}, {position_name}, {group_link}")
        else:
            positions.append(f"{group_name}, должность не указана, {group_link}")

    # Объединяем все должности через точку с запятой и пробел
    return ';\n'.join(positions)


# словарь семейного положения
def get_relation_status(relation_code):
    relations = {
        1: 'Не женат/Не замужем',
        2: 'Есть друг/Подруга',
        3: 'Помолвлен/Помолвлена',
        4: 'Женат/Замужем',
        5: 'Всё сложно',
        6: 'В активном поиске',
        7: 'Влюблён/Влюблена',
        8: 'В гражданском браке'
    }
    return relations.get(relation_code, 'Не указано')


# словари для проверки приватности
def get_is_closed(is_closed_code):
    closed_code = {
        True: 'Закрыт',
        False: 'Открыт',
    }
    return closed_code.get(is_closed_code)


# словарь для индексации на поисковых сайтах
def get_is_no_index(is_no_index_code):
    no_index_code = {
        0: 'да',
        1: 'нет'
    }
    return no_index_code.get(is_no_index_code)

# получение информации о близких NON WORK
# def process_relatives(relatives):
    print(f"{relatives}")
    relatives_dict = {
        "'Дедушки, бабушки'": "не указаны",
        "'Родители'": "не указаны",
        "'Братья, сестры'": "не указаны",
        "'Дети'": "не указаны",
        "'Внуки'": "не указаны"
    }

    for relative in relatives:
        relative_name = relative.get('name')
        relative_type = relative['type']
        relative_id = relative.get('id')

        if relative_name:
            profile_link = f"https://vk.com/id{relative_id}" if relative_id else "не указан"
            relative_info = f"{relative_name}, {profile_link}"

            if relative_type == 'grandparent':
                if relatives_dict["'Дедушки, бабушки'"] == "не указаны":
                    relatives_dict["'Дедушки, бабушки'"] = [relative_info]
                else:
                    relatives_dict["'Дедушки, бабушки'"].append(relative_info)
            elif relative_type == 'parent':
                if relatives_dict["'Родители'"] == "не указаны":
                    relatives_dict["'Родители'"] = [relative_info]
                else:
                    relatives_dict["'Родители'"].append(relative_info)
            elif relative_type == 'sibling':
                if relatives_dict["'Братья, сестры'"] == "не указаны":
                    relatives_dict["'Братья, сестры'"] = [relative_info]
                else:
                    relatives_dict["'Братья, сестры'"].append(relative_info)
            elif relative_type == 'child':
                if relatives_dict["'Дети'"] == "не указаны":
                    relatives_dict["'Дети'"] = [relative_info]
                else:
                    relatives_dict["'Дети'"].append(relative_info)
            elif relative_type == 'grandchild':
                if relatives_dict["'Внуки'"] == "не указаны":
                    relatives_dict["'Внуки'"] = [relative_info]
                else:
                    relatives_dict["'Внуки'"].append(relative_info)

    return relatives_dict


# Функция для получения информации о близких
def get_relatives_info(user_info, relative_type):
    relatives = user_info.get('relatives', [])
    if relatives:
        return ', '.join([f"{relative['first_name']} {relative['last_name']}, {get_profile_link(relative['id'])}" for relative in relatives if relative['type'] == relative_type])
    return 'не указаны'


# получение школы
def get_school(schools):
    if not schools:
        return "не указано"
    
    school_info = []
    for school in schools:
        school_name = school.get('name', 'не указано')
        year_graduated = school.get('year_graduated', 'не указано')
        school_type = school.get('type_str', 'не указано')
        school_info.append(f"{school_name}, год выпуска: {year_graduated}, тип: {school_type}")
    
    return "\n".join(school_info)


# получение университета
def get_university(universities):
    if not universities:
        return "не указано"
    
    university_info = []
    for university in universities:
        name = university.get('name', 'не указано')
        faculty_name = university.get('faculty_name', 'не указано')
        graduation = university.get('graduation', 'не указано')
        education_status = university.get('education_status', 'не указано')
        university_info.append(f"Название: {name}, факультет: {faculty_name}, выпуск: {graduation}, статус: {education_status}")
    
    return "\n".join(university_info)


# получение военной службы
# def get_military(military):
    if military:
        unit = military.get('unit', 'не указано')
        unit_id = military.get('unit_id', 'не указано')
        country_id = military.get('country_id', 'не указано')
        from_year = military.get('from', 'не указано')
        until_year = military.get('until', 'не указано')
        return f"Часть: {unit}, ID части: {unit_id}, Страна: {country_id}, Служба с {from_year} по {until_year}"
    else:
        return 'не указано'


# Получаем информацию о пользователе с помощью метода users.get API VK
def get_user_info(api, user_id):
    try:
        user_info = api.users.get(
            user_ids=user_id,
            fields='activities, bdate, books, career, child, city, connections, universities, \
                contacts, domain, education, education, first_name, games, grandchild, \
                grandparent, home_phone, id, interests, is_closed, is_no_index, last_name, \
                military, military, mobile_phone, movies, music, parent, personal, quotes, \
                relatives, relation, schools, sex, sibling, site, skype, status, title, tv' 
        )[0]
        
        
        # relatives = user_info.get('relatives', [])
        # processed_relatives = process_relatives(relatives)


        # Профиль
        profile = {
            'Профиль': get_is_closed(user_info.get('is_closed')),
            'Имя': user_info.get('first_name'),
            'Фамилия': user_info.get('last_name'),
            'Пол': get_gender(user_info.get('sex')),
            'ID': user_info.get('id'),
            'Статус': user_info.get('status') or 'не указан',
            'Короткое имя': user_info.get('domain') or 'не указано',
            'Дата рождения': user_info.get('bdate') or 'не указана',
            'Индексируется ли профиль поисковыми сайтами': get_is_no_index(user_info.get('is_no_index')),
            'Семейное положение': get_relation_status(user_info.get('relation')),
            'Город': user_info.get('city', {}).get('title') or 'не указан',
            'Владение языками': ', '.join(user_info.get('personal', {}).get('langs', [])) or 'не указаны',
            # **processed_relatives
            # 'Дедушки, бабушки': ', '.join(user_info.get('type: grandparents', {}).get('name', [])),
            # 'Родители': ', '.join(user_info.get('parents', {}).get('name', [])),
            # 'Братья, сестры': ', '.join(user_info.get('siblings', {}).get('name', [])),
            # 'Дети': ', '.join(user_info.get('grandparent', {}).get('name', [])),
            # 'Внуки': ', '.join(user_info.get('grandchild', {}).get('name', []))
            # 'Дедушки, бабушки': get_relatives_info(user_info, 'grandparents'),
            # 'Родители': get_relatives_info(user_info, 'parents'),
            # 'Братья, сестры': get_relatives_info(user_info, 'siblings'),
            # 'Дети': get_relatives_info(user_info, 'grandparent'),
            # 'Внуки': get_relatives_info(user_info, 'grandchild')
        }


        # Контакты
        contacts = {
        'Мобильный телефон': user_info.get('mobile_phone') or 'не указан',
        'Дополнительный телефон': user_info.get('home_phone') or 'не указан',
        'Skype': user_info.get('skype') or 'не указан',
        'Личный сайт': user_info.get('site') or 'не указан',
        }


        # Интересы
        interests = {
            'Деятельность': user_info.get('activities') or 'не указана',
            'Любимая музыка': user_info.get('music') or 'не указана',
            'Любимые фильмы': user_info.get('movies') or 'не указаны',
            'Любимые телешоу': user_info.get('tv') or 'не указаны',
            'Любимые книги': user_info.get('books') or 'не указаны',
            'Любимые игры': user_info.get('games') or 'не указаны',
            'Любимые цитаты': user_info.get('quotes') or 'не указаны',
        }


        # получение школы
        school_info = get_school(user_info.get('schools', []))


        # получение университета
        university_info = get_university(user_info.get('universities', []))


        # получение карьеры
        career_info = get_career_info(user_info.get('career', []))


        # получение военной службы
#         military_info = get_military(user_info.get('military', {}))


        # получение жизненной позиции
        life_position = get_life_position_info(user_info.get('personal', {}))


        # получение списка друзей
        friends = get_user_friends(api, user_id)


        # Возвращаем словарь с информацией о пользователе
        return {
            'Профиль': profile,
            'Контакты': contacts,
            'Интересы': interests,
            'Школа': school_info,
            'Университет': university_info,
            'Карьера': career_info,
#             'Военная служба': military_info,
            'Жизненная позиция': life_position,
            'Друзья': friends
        }
        
        
    # исключение на приватный профиль (code:30)
    except vk_api.exceptions.ApiError as err:
        if err.code == 30:
            print("Невозможно получить данные, закрытый профиль")
            exit()


# Создаем сессию API
vk_session = vk_api.VkApi('Login', 'Password')
vk_session.auth(token_only=True)


# Получаем объект API
api = vk_session.get_api()


# Ввод пользователя (ID, короткое имя пользователя или ссылка)
user_input = input("Введите ID, короткое имя пользователя или ссылку на профиль: ")


# Определяем user_id
user_id = get_user_id(user_input, api)


# выводим всю статистику
if user_id:
    # Получаем информацию о пользователе
    user_info = get_user_info(api, user_id)

    # Выводим информацию о пользователе
    print('---Информация о пользователе---')
    for category, data in user_info.items():
        print(f'{category}:')
        if isinstance(data, dict):
            for key, value in data.items():
                print(f'{key}: {value}')
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f'{key}: {value}')
                else:
                    print(item)
        else:
            print(data)
        print()
else:
    print('Пользователь не найден.')
