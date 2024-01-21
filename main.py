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

    suggested = {

    }

    gen_names1 = {
        'Minji': [0, 0, 'Минджи'],
        'Minho': [0, 0, 'Минхо'],
        'Sua': [0, 0, 'Суа'],
        'Jungwoo': [0, 0, 'Чону'],
        'Subin': [0, 0, 'Субин'],
        'Kitae': [0, 0, 'Китэ']
    }

    gen_names2 = {
        'Chunha': [0, 0, 'Чунха'],
        'Eunju': [0, 0, 'Ынджу'],
        'Jiah': [0, 0, 'Джиа'],
        'Boyeon': [0, 0, 'Боён'],
        'Kyongho': [0, 0, 'Кёнхо'],
        'Sunok': [0, 0, 'Сунок']
    }

    f_count1 = []
    m_count1 = []
    names1= []

    gen_names3 = {
        'Seunhee': [0, 0, 'Сынхи'],
        'Seungsu': [0, 0, 'Сынсу'],
        'Nari': [0, 0, 'Нари'],
        'Hyejin': [0, 0, 'Хеджин'],
        'Namgyu': [0, 0, 'Намгю'],
        'Shihyuk': [0, 0, 'Шихёк']
    }

    gen_names4 = {
        'Chaewon': [0, 0, 'Чевон'],
        'Haneul': [0, 0, 'Ханыль'],
        'Kangmin': [0, 0, 'Канмин'],
        'Jeonghyo': [0, 0, 'Чонхё'],
        'Jinwoo': [0, 0, 'Джину'],
        'Narae': [0, 0, 'Нарэ']
    }

    f_count2 = []
    m_count2 = []
    names2 = []

    names_f = {
        "Кинам": [0, []],
        "Минсо": [0, []],
        "Кёна": [0, []],
        "Юбин": [0, []],
        "Ёнджин": [0, []]
    }

    names_m = {
        "Сонхва": [0, []],
        "Юбин": [0, []],
        "Воныль": [0, []],
        "Чан": [0, []],
        "Кинам": [0, []]
    }

    for d in alldata:
        for key in surn_stat.keys():
            if key in d.pr.a7:
                surn_stat[key][0] += 1

        l = d.pr.a8.split('; ')
        for name in l:
            name = name.strip(' ')
            if name not in suggested.keys() and name.lower() != 'нет' and name != '':
                suggested[name] = 1
            elif name in suggested.keys():
                suggested[name] += 1
                

        n1 = d.pr.a9.split('; ')

        for key in gen_names1.keys():
            if key in n1:
                gen_names1[key][0] += 1
            else:
                gen_names1[key][1] += 1
        
        n2 = d.pr.a10.split('; ')

        for key in gen_names2.keys():
            if key in n2:
                gen_names2[key][1] += 1
            else:
                gen_names2[key][0] += 1

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


        female_names = [d.pr.a13, d.pr.a16, d.pr.a18, d.pr.a21, d.pr.a22]
        male_names = [d.pr.a14, d.pr.a15, d.pr.a17, d.pr.a19, d.pr.a20]
        
        for i, key in enumerate(names_f.keys()):
            if key in female_names:
                names_f[key][0] += 1
                if key not in names_f[key][1]:
                    names_f[key][1].append(key)
            elif female_names[i].strip(' ') not in names_f[key][1]:
                names_f[key][1].append(female_names[i].strip(' '))
        
        for i, key in enumerate(names_m.keys()):
            if key in male_names:
                names_m[key][0] += 1
                if key not in names_m[key][1]:
                    names_m[key][1].append(key)
            elif male_names[i].strip(' ') not in names_m[key][1]:
                names_m[key][1].append(male_names[i].strip(' '))

    sorted_surn = sorted(surn_stat.items(), key=lambda item: item[1][0], reverse=True)

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

    values = names1
    female1 = f_count1
    male1 = m_count1
    width = 0.3
    x = np.arange(len(values))
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot()

    rect1 = ax.bar(x - width/2, female1, width, label='female', color='plum')
    rect2 = ax.bar(x + width/2, male1, width, label='male', color='indigo')
    # ax.set_title('Пример групповой диаграммы')
    ax.set_xticks(x)
    ax.set_xticklabels(values)
    plt.xticks(rotation=45)
    ax.bar_label(rect1, fmt='{:,.0f}')
    ax.bar_label(rect2, fmt='{:,.0f}')
    ax.legend()
    plt.savefig('static/gen_names1.png')


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
    ax.bar_label(rect1, fmt='{:,.0f}')
    ax.bar_label(rect2, fmt='{:,.0f}')
    ax.legend()
    plt.savefig('static/gen_names2.png')
 


    return render_template('statistics.html', n_resp=n_resp, know_kor=know_kor, know_kor_per=know_kor_per, sorted_surn=sorted_surn,
                           names_f=names_f, names_m=names_m, suggested=suggested, f_count1=f_count1, m_count1=m_count1, names1=names1)


if __name__ == '__main__':
    # след-е 2 строчки нужно запускать только 1 раз для создания базы данных
    # with app.app_context():
    #     db.create_all()
    app.run()
