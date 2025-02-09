import io
import random
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a secure key in production

# Make Python's built-in enumerate function available in Jinja2 templates.
app.jinja_env.globals.update(enumerate=enumerate)

# -------------------------
# Data Definitions
# -------------------------
# Leadership Assessment Questions (Created by Olanrewaju Daramola)
questions = [
    "When I enter a room, I make others feel uplifted:",
    "I give confidence and encouragement to others:",
    "I am genuinely interested in other people:",
    "I assume responsibility for myself and my team",
    "I am secure in my identity and my self-esteem", 
    "I do what I should, even when I don't feel like it",
    "I will help those in need even when it costs me",
    "I am moved emotionally by my love for others",
    "I am fulfilled when I serve and meet others needs",
    "I like to start new projects, even when it is scary",
    "I don't mind being the first to take a risk",
    "When ideas arise, I want to take action, not talk",
    "My ideas often turn into plans",
    "I can figure out how to finish a job I start",
    "I am good at solving problems",
    "I know exactly what I believe",
    "I make sacrifices because of my beliefs",
    "Passion enables me to act on what I believe",
    "I finish what I start",
    "Obstacles don't discourage me but challenge me",
    "I can stay focused on one goal" 
]

# Mapping of categories to question ranges.
category_ranges = {
    'Charisma': (0, 3),
    'Character': (3, 6),
    'Compassion': (6, 9),
    'Courage': (9, 12),
    'Competency': (12, 15),
    'Conviction': (15, 18),
    'Commitment': (18, 21),
}

# -------------------------
# Routes and Views
# -------------------------

# Home page – Assessment form.
@app.route('/')
def index():
    display_order = questions.copy()
    random.shuffle(display_order)
    mapping = [questions.index(q) for q in display_order]
    session['mapping'] = mapping
    session['display_order'] = display_order
    return render_template('index.html', display_order=display_order)

# Process assessment submission.
@app.route('/submit', methods=['POST'])
def submit():
    mapping = session.get('mapping')
    if not mapping:
        flash("Session expired, please try again.", "error")
        return redirect(url_for('index'))

    responses = [0] * len(questions)
    n = len(mapping)
    for i in range(n):
        rating_value = request.form.get(f"rating_{i}")
        if rating_value is None or rating_value == "":
            flash("Please rate all questions.", "warning")
            return redirect(url_for('index'))
        try:
            rating = int(rating_value)
        except ValueError:
            rating = 0
        responses[mapping[i]] = rating

    overall_score = sum(responses) / len(responses) if responses else 0
    session['responses'] = responses
    session['overall_score'] = overall_score

    cat_avgs = {}
    for category, (start, end) in category_ranges.items():
        cat_responses = responses[start:end]
        cat_avgs[category] = sum(cat_responses) / len(cat_responses) if cat_responses else 0
    session['cat_avgs'] = cat_avgs

    return redirect(url_for('results'))

# Results page.
@app.route('/results')
def results():
    overall_score = session.get('overall_score', 0)
    cat_avgs = session.get('cat_avgs', {})
    return render_template('results.html', overall_score=overall_score, cat_avgs=cat_avgs)

# Generate the results graph.
@app.route('/graph.png')
def graph_png():
    cat_avgs = session.get('cat_avgs', {})
    categories = list(cat_avgs.keys())
    averages = list(cat_avgs.values())
    
    # Different colors for each category.
    colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#A133FF', '#33FFF6', '#FFC133']
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(categories, averages, color=colors[:len(categories)])
    ax.set_xlabel('Categories', fontsize=10)
    ax.set_ylabel('Average Ratings', fontsize=10)
    ax.set_title('Leadership Assessment Results by Category', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    output = io.BytesIO()
    fig.savefig(output, format='png')
    plt.close(fig)
    output.seek(0)
    return send_file(output, mimetype='image/png')

# Send results via email.
@app.route('/send_email', methods=['POST'])
def send_email():
    overall_score = session.get('overall_score')
    cat_avgs = session.get('cat_avgs')
    if overall_score is None:
        flash("No results available to send.", "error")
        return redirect(url_for('index'))

    user_email = request.form.get('email')
    if not user_email:
        flash("Please enter a valid email address.", "warning")
        return redirect(url_for('results'))

    subject = "Leadership Assessment Results"
    body = f"Your overall leadership score: {overall_score:.2f}\n\nCategory Averages:\n"
    for category, avg in cat_avgs.items():
        body += f"{category}: {avg:.2f}\n"
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "easyquickpiano.com"  # Replace with your email
    msg["To"] = user_email

    try:
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login("easyquickpiano.com", "your_app_password")
        smtp_server.sendmail(msg["From"], [msg["To"]], msg.as_string())
        smtp_server.quit()
        flash(f"Results sent to {user_email}", "success")
    except Exception as e:
        flash(f"Error sending email: {e}", "danger") # Provide user feedback
        print(f"Error details: {e}") # Print error details for debugging
    return redirect(url_for('results'))

# About page.
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
