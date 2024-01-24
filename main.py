from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import numpy as np


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///statistics.db'
db = SQLAlchemy(app)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'{self.question}'
    

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    native_language = db.Column(db.String(50), nullable=False)
    korean = db.Column(db.String(10))

    pr = db.relationship('Answers', backref='users', uselist=False)

    def __repr__(self):
        return f'{self.name}'
    

class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))


    a5 = db.Column(db.String(10), nullable=False)
    a6 = db.Column(db.String(100), nullable=False)
    a7 = db.Column(db.String(300), nullable=False)
    a8 = db.Column(db.String(300), nullable=True)
    a9 = db.Column(db.String(300), nullable=False)
    a10 = db.Column(db.String(300), nullable=False)
    a11 = db.Column(db.String(300), nullable=False)
    a12 = db.Column(db.String(300), nullable=False)
    a13 = db.Column(db.String(50), nullable=False)
    a14 = db.Column(db.String(50), nullable=False)
    a15 = db.Column(db.String(50), nullable=False)
    a16 = db.Column(db.String(50), nullable=False)
    a17 = db.Column(db.String(50), nullable=False)
    a18 = db.Column(db.String(50), nullable=False)
    a19 = db.Column(db.String(50), nullable=False)
    a20 = db.Column(db.String(50), nullable=False)
    a21 = db.Column(db.String(50), nullable=False)
    a22 = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'{self.answer}'



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        name = request.form['name']
       
        age = request.form['age']
        
        l1 = request.form['L1']
        
        kor_yes_no = request.form['kor_yes_no']
        
        names_yes_no = request.form['names_yes_no']
        
        order = request.form['order']
        
        familiar_surn = '; '.join(request.form.getlist('familiar_surn'))
        
        known_name = '; '.join(request.form.getlist('known_name'))
        
        name_f1 = '; '.join(request.form.getlist('name_f1'))
        
        name_m1 = '; '.join(request.form.getlist('name_m1'))
        
        name_f2 = '; '.join(request.form.getlist('name_f2'))
      
        name_m2 = '; '.join(request.form.getlist('name_m2'))
        
        inflected1 = request.form['inflected1']
        inflected2 = request.form['inflected2']
        inflected3 = request.form['inflected3']
        inflected4 = request.form['inflected4']
        inflected5 = request.form['inflected5']
        inflected6 = request.form['inflected6']
        inflected7 = request.form['inflected7']
        inflected8 = request.form['inflected8']
        inflected9 = request.form['inflected9']
        inflected10 = request.form['inflected10']
        

        try:
            u = Users(name=name, age=age, native_language=l1, korean=kor_yes_no)
            db.session.add(u)
            db.session.flush()

            a = Answers(id_user=u.id, a5=names_yes_no, a6=order,
                        a7=familiar_surn, a8=known_name, a9=name_f1,
                        a10=name_m1, a11=name_f2, a12=name_m2, a13=inflected1,
                        a14=inflected2, a15=inflected3, a16=inflected4, a17=inflected5,
                        a18=inflected6, a19=inflected7, a20=inflected8,
                        a21=inflected9, a22=inflected10)
            db.session.add(a)
            db.session.commit()
        except:
            db.session.rollback()
            print('Ошибка добавления в базу данных')


        return render_template('sent.html')
    else:
        questions = Questions.query.all()
        return render_template('questions.html', questions=questions)
    

@app.route('/sent')
def sent():
    return render_template('sent.html')


@app.route('/statistics')
def statistics():
    alldata = Users.query.all()
    n_resp = len(alldata)
    know_kor = len(Users.query.filter(Users.korean == 'yes').all())
    know_kor_per = round(know_kor / n_resp * 100, 2)
    
    
    # словарь фамилий, из которых респонденту нужно выбрать знакомые
    # ключ -- значение из html файла, которое вносится в db, число в списке -- количество отметок на фамилию
    # потом кириллица -- для отображения в статистике
    surn_stat = {
        'Kim': [0, 'Ким'],
        'Lee': [0, 'Ли'],
        'Park': [0, 'Пак'],
        'Jeon': [0, 'Чон'],
        'Hwang': [0, 'Хван'],
        'Kwon': [0, 'Квон'],
        'Yoon': [0, 'Юн'],
        'Choi': [0, 'Чхве'],
        'Moon': [0, 'Мун'],
        'Seo': [0, 'Со'],
        'Kang': [0, 'Кан'],
        'Yang': [0, 'Ян'],
        'Bang': [0, 'Бан'],
        'Boo': [0, 'Бу'],
        'No': [0, 'Не знаю']
    }

    # пока пустой словарь для имен, которые предложат респонденты
    suggested = {

    }

    # далее идут словари из имен в вопросах 9-12
    # ключ -- значение из html, первое число в списке -- количество отметок имени как женского
    # второй число -- отметки как мужского, имя кириллицей для вывода в статистике
    # словарь для имен из вопроса 9
    gen_names1 = {
        'Minji': [0, 0, 'Минджи'],
        'Minho': [0, 0, 'Минхо'],
        'Sua': [0, 0, 'Суа'],
        'Jungwoo': [0, 0, 'Чону'],
        'Subin': [0, 0, 'Субин'],
        'Kitae': [0, 0, 'Китэ']
    }

    # словарь для имен из вопроса 10
    gen_names2 = {
        'Chunha': [0, 0, 'Чунха'],
        'Eunju': [0, 0, 'Ынджу'],
        'Jiah': [0, 0, 'Джиа'],
        'Boyeon': [0, 0, 'Боён'],
        'Kyongho': [0, 0, 'Кёнхо'],
        'Sunok': [0, 0, 'Сунок']
    }

    # чтобы сделать два графика на все имена из вопросов 9-12,
    # объединим имена из вопросов 9 и 10 для первого графика и 11 и 12 для второго

    # для первого графика создадим списки 
    f_count1 = [] # список отметок имен как женских
    m_count1 = [] # как мужских
    names1= [] # список имен кириллицей для вывода на графики

    # словарь для имен из вопроса 11
    gen_names3 = {
        'Seunhee': [0, 0, 'Сынхи'],
        'Seungsu': [0, 0, 'Сынсу'],
        'Nari': [0, 0, 'Нари'],
        'Hyejin': [0, 0, 'Хеджин'],
        'Namgyu': [0, 0, 'Намгю'],
        'Shihyuk': [0, 0, 'Шихёк']
    }

    # словарь для имен из вопроса 12
    gen_names4 = {
        'Chaewon': [0, 0, 'Чевон'],
        'Haneul': [0, 0, 'Ханыль'],
        'Kangmin': [0, 0, 'Канмин'],
        'Jeonghyo': [0, 0, 'Чонхё'],
        'Jinwoo': [0, 0, 'Джину'],
        'Narae': [0, 0, 'Нарэ']
    }

    # такие же списки для второго графика
    f_count2 = []
    m_count2 = []
    names2 = []

    # словарь женских имен, которые было предложено просклонять
    # число в списке -- количество совпадений введеной пользователем формы с начальной формой
    # пустой список -- список введеных форм имени, которые отличаются от начальной
    names_f = {
        "Кинам": [0, []],
        "Минсо": [0, []],
        "Кёна": [0, []],
        "Юбин": [0, []],
        "Ёнджин": [0, []]
    }

    # такой же список для мужских имен
    names_m = {
        "Сонхва": [0, []],
        "Юбин": [0, []],
        "Воныль": [0, []],
        "Чан": [0, []],
        "Кинам": [0, []]
    }

    # в цикле будем проходить по данным, который ввел каждый пользователь (d -- все ответы одного пользователя)
    for d in alldata:
        # для тех фамилий из словаря, которые нашлись в ответах пользователя, увеличивается счетчик отметок
        for key in surn_stat.keys():
            if key in d.pr.a7:
                surn_stat[key][0] += 1

        l = d.pr.a8.split('; ')
        for name in l:
            name = name.strip(' ')
            # если предложенное пользователем имя еще не встречалось, 
            # оно вносится в словарь как ключ (значение -- количество упоминаний этого имени разными пользователями)
            if name not in suggested.keys() and name.lower() != 'нет' and name != '':
                suggested[name] = 1
            # если имя уже есть в словаре, просто увеличивается счетчик
            elif name in suggested.keys():
                suggested[name] += 1
                

        n1 = d.pr.a9.split('; ')

        # этот вопрос касался женских имен ("выберите имена, которые на ваш взгляд можно дать девочке")
        for key in gen_names1.keys():
            # если пользователь выбрал имя, оно оказалось в ответе -- увеличивается "женский счетчик" данного имени
            if key in n1:
                gen_names1[key][0] += 1
            # если пользователь не выбрал имя, увеличивается "мужской счетчик"
            else:
                gen_names1[key][1] += 1
        
        n2 = d.pr.a10.split('; ')

        # этот вопрос про мужскиеа имен ("какие имена можно дать мальчику")
        for key in gen_names2.keys():
            # соответственно, обратная схема. если имя оказалось среди выбранных -- "мужской счетчик"
            if key in n2:
                gen_names2[key][1] += 1
            # если нет, что "женский"
            else:
                gen_names2[key][0] += 1

        # с другими двумя группами имен то же
        n3 = d.pr.a11.split('; ')

        for key in gen_names3.keys():
            if key in n3:
                gen_names3[key][0] += 1
            else:
                gen_names3[key][1] += 1

        n4 = d.pr.a12.split('; ')

        for key in gen_names4.keys():
            if key in n4:
                gen_names4[key][1] += 1
            else:
                gen_names4[key][0] += 1

        # списки женских и мужских имен из вопросов 13-22
        female_names = [d.pr.a13, d.pr.a16, d.pr.a18, d.pr.a21, d.pr.a22]
        male_names = [d.pr.a14, d.pr.a15, d.pr.a17, d.pr.a19, d.pr.a20]
        
        for i, key in enumerate(names_f.keys()):
            # если предложенная пользователем форма есть среди начальных форм словаря, то счетчик увеличивается
            #и список пополняется введенной формой имени
            if key in female_names:
                names_f[key][0] += 1
                if key not in names_f[key][1]:
                    names_f[key][1].append(key)
            # если форма не совпадает с начальной, то просто вносится в список
            elif female_names[i].strip(' ') not in names_f[key][1]:
                names_f[key][1].append(female_names[i].strip(' '))

        # то же с мужскими именами
        for i, key in enumerate(names_m.keys()):
            if key in male_names:
                names_m[key][0] += 1
                if key not in names_m[key][1]:
                    names_m[key][1].append(key)
            elif male_names[i].strip(' ') not in names_m[key][1]:
                names_m[key][1].append(male_names[i].strip(' '))

    # все фамилии из вопроса 7 сортируем по убыванию количества их отметок (самые известные сверху)
    sorted_surn = sorted(surn_stat.items(), key=lambda item: item[1][0], reverse=True)

    # проходясь по каждому имени в словарях для вопросов 9-12, добавляем данные в соответствующие списки
    for key in gen_names1.keys():
        f_count1.append(gen_names1[key][0])
        m_count1.append(gen_names1[key][1])
        names1.append(gen_names1[key][2])

    for key in gen_names2.keys():
        f_count1.append(gen_names2[key][0])
        m_count1.append(gen_names2[key][1])
        names1.append(gen_names2[key][2])

    for key in gen_names3.keys():
        f_count2.append(gen_names3[key][0])
        m_count2.append(gen_names3[key][1])
        names2.append(gen_names3[key][2])

    for key in gen_names4.keys():
        f_count2.append(gen_names4[key][0])
        m_count2.append(gen_names4[key][1])
        names2.append(gen_names4[key][2])

    # делаем первый график
    # подписи столбцов -- список имен
    values = names1
    # значения столбцов -- количества "женских" и "мужских" отметок на каждое имя
    female1 = f_count1
    male1 = m_count1
    width = 0.3
    x = np.arange(len(values))
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot()

    # задаем "женский" и "мужской" столбики, делаем их разных цветов
    rect1 = ax.bar(x - width/2, female1, width, label='female', color='plum')
    rect2 = ax.bar(x + width/2, male1, width, label='male', color='indigo')
    # ax.set_title('Пример групповой диаграммы')
    ax.set_xticks(x)
    ax.set_xticklabels(values)
    plt.xticks(rotation=45)
    ax.bar_label(rect1)
    ax.bar_label(rect2)
    ax.legend()
    # и сохраняем график картинкой, чтобы вставить в html
    plt.savefig('static/gen_names1.png')

    # все то же самое для второго графика
    values = names2
    female2 = f_count2
    male2 = m_count2
    width = 0.3
    x = np.arange(len(values))
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot()

    rect1 = ax.bar(x - width/2, female2, width, label='female', color='plum')
    rect2 = ax.bar(x + width/2, male2, width, label='male', color='indigo')
    # ax.set_title('Пример групповой диаграммы')
    ax.set_xticks(x)
    ax.set_xticklabels(values)
    plt.xticks(rotation=45)
    ax.bar_label(rect1)
    ax.bar_label(rect2)
    ax.legend()
    plt.savefig('static/gen_names2.png')
 

    # передаем все полученные данные в html-файл со статистикой
    return render_template('statistics.html', n_resp=n_resp, know_kor=know_kor, know_kor_per=know_kor_per, sorted_surn=sorted_surn,
                           names_f=names_f, names_m=names_m, suggested=suggested, f_count1=f_count1, m_count1=m_count1, names1=names1)


if __name__ == '__main__':
    # след-е 2 строчки нужно запускать только 1 раз для создания базы данных
    # with app.app_context():
    #     db.create_all()
    app.run()
