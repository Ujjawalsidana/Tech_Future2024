from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    age_group = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Question {self.id}>'
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age_group = db.Column(db.String(10), nullable=False)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Student {self.id}: {self.name}, Age: {self.age_group}, Score: {self.score}>'
    
with app.app_context():
    db.create_all()    
def init_db():
    with app.app_context():
        db.create_all()

        if not Question.query.first():
            # Questions for 2-5 years
            questions_2_5 = [
                {'text': 'How many fingers do you have?', 'answer': '10', 'age_group': '2-5'},
                {'text': 'What is the first letter of the alphabet?', 'answer': 'A', 'age_group': '2-5'},
                {'text': 'What does a cat say?', 'answer': 'Meow', 'age_group': '2-5'},
                {'text': 'How many fingers do you have on one hand?','answer':'5', 'age_group':'2-5'},
                {'text': 'With help of which sense organ you can see?','answer':'Eyes', 'age_group':'2-5'},
                {'text': 'Which letter comes after B?','answer':'C', 'age_group':'2-5'},
                {'text': 'What color is the sky during the day?','answer':'Blue', 'age_group':'2-5'},
                {'text': 'How many legs does a cat have?','answer':'4', 'age_group':'2-5'},
                {'text': 'What is the opposite of "big"','answer':'Small', 'age_group':'2-5'},
                {'text': 'What is the shape of a circle?','answer':'ROund', 'age_group':'2-5'},
                {'text': 'What is the color of grass?','answer':'green', 'age_group':'2-5'},
                {'text': 'How many eyes do you have?','answer':'2', 'age_group':'2-5'},
                {'text': 'How many wheels does a bicycle have?','answer':'2', 'age_group':'2-5'},
                {'text': 'Which animal says "quack, quack"?','answer':'', 'age_group':'2-5'},
                {'text': 'What do you use to clean your teeth?','answer':'Toothbrush', 'age_group':'2-5'},
                {'text': 'What is the opposite of "hot"?','answer':'Cold', 'age_group':'2-5'},
                {'text': 'Tell the name of meal you have in morning?','answer':'Breakfast', 'age_group':'2-5'},
                {'text': 'what is name of big,round, white element in sky at night','answer':'Moon', 'age_group':'2-5'},
                {'text': 'Twinkle,twinle little _____','answer':'Stars', 'age_group':'2-5'},
                {'text': 'Tell the name of meal you have in night?','answer':'Dinner', 'age_group':'2-5'}

            ]

            # Questions for 5-8 years
            questions_5_8 = [
                {'text': 'What is the capital of India?', 'answer': 'New Delhi', 'age_group': '5-8'},
                {'text': 'Who is known as the "Father of the Nation" in India?', 'answer': 'Mahatma Gandhi', 'age_group': '5-8'},
                {'text': 'What is the largest planet in our solar system?', 'answer': 'Jupiter', 'age_group': '5-8'},
                # Add more questions for 5-8 years
                {'text': 'What color is the sun?','answer':'Yellow','age_group':'5-8'},
                {'text': 'What do you use to brush your teeth?','answer':'toothbrush','age_group':'5-8'},
                {'text': 'what comes after 999','answer':'1000','age_group':'5-8'},
                {'text': 'primary gas that makes up earth atmosphere?','answer':'Nitrogen','age_group':'5-8'},
                {'text': 'Which is the longest river in the world?','answer':'Nile','age_group':'5-8'},
                {'text': 'What is the name of our galaxy?','answer':'Milky-way','age_group':'5-8'},
                {'text': 'How many continents are there on Earth?','answer':'7','age_group':'5-8'},
                {'text': 'Which is the tallest mountain in the world?','answer':'Mount Everest','age_group':'5-8'},
                {'text': 'Which animal is known as the "King of the Jungle"?','answer':'Lion','age_group':'5-8'},
                {'text': 'Where is the India Gate located?','answer':'New delhi','age_group':'5-8'},
                {'text': 'Who is the Prime Minister of India','answer':'Narendra Modi','age_group':'5-8'}

            ]

            # Questions for 8+ years
            questions_8 = [
                {'text': 'In which year did World War II end?', 'answer': '1945', 'age_group': '8-10'},
                {'text': 'Who painted the Mona Lisa?', 'answer': 'Leonardo da Vinci', 'age_group': '8-10'},
                {'text': 'What is the currency of US?', 'answer': 'Dollar', 'age_group': '8-10'},
                # Add more questions for 8+ years
                {'text':'What is the capital city of France?','answer': 'Paris','age_group':'8-10'},
                {'text':'What is the currency of Japan?','answer': 'Yen','age_group':'8-10'},
                {'text':'Who was the first President of the India','answer': 'Rajendra Prasad','age_group':'8-10'},
                {'text':'Which two elements make up water?','answer': 'hydrogen and oxygen','age_group':'8-10'},
                {'text':'what protects us from harmful CFCs?','answer': 'Ozone','age_group':'8-10'},
                {'text':'What is the capital city of China?','answer': 'Beijing','age_group':'8-10'},
                {'text':'If a train travels at 60 km/h for 3 hours, how far does it travel?','answer': '180','age_group':'8-10'},
                {'text':'If a triangle has angles measuring 45°, 45°, and 90°, what type of triangle is it?','answer': 'isosceles','age_group':'8-10'},
                {'text':'How many continents are there in the world?','answer': '7','age_group':'8-10'},
                {'text':'What is the result of 15*8?','answer': '120','age_group':'8-10'},
                {'text':'If a rectangle has a length of 12 units and a width of 8 units, what is its area?','answer': '96','age_group':'8-10'},
                {'text':'Which planet is known as the "Red Planet"? Answer this','answer': 'Mars','age_group':'8-10'}
                
            ]

            # Add questions to the database
            for questions_set in [questions_2_5, questions_5_8, questions_8]:
                for question_data in questions_set:
                    question = Question(**question_data)
                    db.session.add(question)

            db.session.commit()

    
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/quiz', methods=['GET', 'POST'])
def quiz_index():
    if request.method == 'POST':
        return redirect(url_for('enter_name'))
    return render_template('index.html')


@app.route('/enter_name', methods=['GET', 'POST'])
def enter_name():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            age_group = request.form.get('age')
            if age_group:
                student = Student(name=name, age_group=age_group)
                db.session.add(student)
                db.session.commit()
                return redirect(url_for('quiz_by_age', name=name, age_group=age_group))

    return render_template('enter_name.html')


@app.route('/quiz/<name>/<age_group>', methods=['GET', 'POST'])
def quiz_by_age(name, age_group):
    if request.method == 'POST':
        questions = get_daily_questions(age_group)

        # Initialize score for the current quiz attempt
        quiz_score = 0

        for question in questions:
            user_answer = request.form.get(f'answer_{question.id}')
            correct_answer = get_correct_answer(question.id)

            # Check if the answer is correct and update the quiz score
            if user_answer.lower() == correct_answer.lower():
                quiz_score += 1

        # Update the student's total score after completing the quiz
        student = Student.query.filter_by(name=name, age_group=age_group).first()
        student.score += quiz_score
        print(f"Score updated for {student.name}: {student.score}")
        db.session.commit()

    questions = get_daily_questions(age_group)
    return render_template('quiz.html', questions=questions, name=name, age_group=age_group)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_answers = {}
    for key, value in request.form.items():
        if key.startswith('answer_'):
            question_id = key.split('_')[-1]
            user_answers[question_id] = value.lower()

    student_name = request.form.get('name')
    age_group = request.form.get('age_group')
    student = Student.query.filter_by(name=student_name, age_group=age_group).first()

    # Calculate the score based on correct answers
    score = 0
    for question_id, user_answer in user_answers.items():
        correct_answer = get_correct_answer(question_id)
        if user_answer == correct_answer.lower():
            score += 1

    # Update the student's score
    student.score += score
    db.session.commit()

    return jsonify({'result': f'Correct answers: {score} out of {len(user_answers)}'})


@app.route('/leaderboard')
def leaderboard():
    # Retrieve and display leaderboard data
    students = Student.query.order_by(Student.score.desc()).all()
    return render_template('leaderboard.html',students=students)

def get_daily_questions(age_group):
    questions = Question.query.filter_by(age_group=age_group).all()
    random.shuffle(questions)
    return random.sample(questions,min(5, len(questions)))

def get_correct_answer(question_id):
    return Question.query.get(question_id).answer

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
