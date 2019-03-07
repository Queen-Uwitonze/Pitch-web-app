from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class PitchForm(FlaskForm):
    category = StringField('category',validators=[Required()])
    title = StringField('pitch title',validators=[Required()])
    content= TextAreaField('add pitch', validators=[Required()])
    user_id = TextAreaField('author', validators=[Required()])
    # upvote = SubmitField('upvote',validators=[Required()])
    # downvote = SubmitField('downvote',validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):

    description= TextAreaField('comment', validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')