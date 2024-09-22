remove_words_dotted_dict = {
    "г.": "",
    "Б.": "",
    "ул.": "",  # иногда улицу надо добавлять
    "пр-кт": "проспект",
    "пер.": "переулок",
    "Респ.": "Республика",
    "край.": "край",
    "край": "край",
    "обл": "область",
    "пл.": "площадь",
    "ал.": "аллея",
    "ж/р": "",
    "к.": "",
    "обл.": "область",
    "д.": "дом",
    "Д.": "дом",
    "мкр.": "микрорайон",
    "б-р.": "бульвар",
    "ш.": "шоссе",
    "п.": "",
    "кв.": "квартира",
    "рп.": "",
    "кп.": "",
    "с.": "",
    "стр.": "",
    "АО,": "",
    "пгт.": "",
    "им.": "имени",
    "Им": "",
    "тер.": "",
    "наб.": "набережная",
    "пр-д.": "",
    "р-н": "район",
    "/Якутия/": "",
    "Н.Г.": "",
    "В.Н.": "",
    "В.С.": "",
    "П.Ф.": "",  # добавить регулярку на фикс этого
    "кв-л": "квартал",
    "туп.": "тупик",
    "СНТ": "",
    "ЛИТ.": "",
    "соор.": "сооружение",
    "р.": "",
    "Респ": "Республика",
    "проезд.": "проезд"
}


remove_words_not_dotted_dict = {
    "мкр": "микрорайон",
    "им": "",
    "АО": "",
    "обл": "область",
    "г": "",
    "ул": "",
    "пр-кт": "проспект",
    "пер": "переулок",
    "Респ": "Республика",
    "край": "край",
    "пл": "площадь",
    "ал": "аллея",
    "к": "",
    "-": "",
    "д": "дом",
    "б-р": "бульвар",
    "ш": "шоссе",
    "п": "",
    "А": "",
    "кв": "",
    "рп": "",
    "кп": "",
    "с": "",
    "стр": "",
    "пгт": "",
    "тер": "",
    "наб": "набережная",
    "пр-д": "",
    "р-н": "район",
    "/Якутия/": "",
    "Н.Г.": "",
    "кв-л": "квартал",
    "туп": "тупик",
    "СНТ": "",
    "ЛИТ": "",
    "соор": "сооружение",
    "р": "",
    # Добавлять корпусы к номеру дома, типо 10к2
    # Также строение: 10с1
    # Иногда и корпус и строение идут вместе - 10к2с1
    # После строения или корпуса иногда идет буква (А, Б) - должно быть 10с1А, 10к2Б

    # Пофиксить микрорайоны (мкр)

    # Иногда впритык к номеру дома стоит буква (А, Б итд)
}
