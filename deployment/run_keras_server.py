from getcsv import bottell
#from keras.models import load_model
#import tensorflow as tf
from flask import Flask, render_template, request
from wtforms import Form, TextField, validators, SubmitField, DecimalField, IntegerField

# Create app
app = Flask(__name__)


class ReusableForm(Form):
    """User entry form for entering specifics for generation"""
    # Starting seed
    seed = TextField("Enter twitter id :", validators=[
                     validators.InputRequired()])
    
    # Submit button
    submit = SubmitField("Enter")


def load_keras_model():
    """Load in the pre-trained model"""
    global model
    model = load_model('../models/train-embeddings-rnn.h5')
    # Required for model to work
    global graph
    #graph = tf.get_default_graph()


# Home page
@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    # Create form
    form = ReusableForm(request.form)

    # On form entry and all conditions met
    if request.method == 'POST' and form.validate():
        # Extract information
        seed = request.form['seed']
        # Generate a random sequence
        if seed != '':
            prediction = bottell(seed)
            if prediction == 1:
                print ("it is")
                return render_template('index.html', form=form, input="It is a bot")
            else:
                print("not a bot")
                return render_template('index.html', form=form, input="It is not a bot")
    # Send template information to index.html'''
    return render_template('index.html', form=form, input="result")


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))
    #load_keras_model()
    # Run app
    app.run(host="0.0.0.0", port=80)
