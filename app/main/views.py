from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PitchForm,UpdateProfile,CommentForm
from ..models import  User,Pitch,Comment
from flask_login import login_required,current_user
from .. import db,photos
# from .models import pitch


# Pitch = pitch.Pitch

@main.route('/')
def index():
    """ View root page function that returns index page """
    # # Getting categiries of pitch
    # pickup_lines = get_movies('pickup lines')
    # interview_pitch = get_movies('interview pitch')
    # product_pitch = get_movies('now_playing')
    # promotion_pitch = get_movies('promotion pitch')

    title = 'Home- Welcome'
    all_pitches = Pitch.get_pitches()
    
    return render_template('index.html', title = title,all_pitches=all_pitches)

def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/pickup_line')
def pickup_line():
  
    pickup_line_pitch = Pitch.query.filter_by(category='pickup_line').all()

    return render_template('index.html', pickup_line=pickup_line_pitch)

@main.route('/business')
def business():
  
    business_pitch = Pitch.query.filter_by(category='business').all()

    return render_template('index.html', business=business_pitch)


@main.route('/jobs')
def jobs():
    jobs_pitch = Pitch.query.filter_by(category='jobs').all()
    return render_template('index.html', jobs=jobs_pitch)
    
@main.route('/promotion')
def promotion():
    promotion_pitch = Pitch.query.filter_by(category='promotion').all()
    return render_template('index.html', promotion=promotion_pitch)
    
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user,pitch_form=pitch_form)

@main.route('/new', methods=['GET', 'POST'])
@login_required
def new_pitch():
    pitch_form = PitchForm()
    
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        content  = pitch_form.content.data
        category = pitch_form.category.data
        # upvote = pitch_form.category.data
        user_id = pitch_form.user_id.data
        new_pitch = Pitch(title=title,content=content,category=category,user_id=current_user.id)
        new_pitch.save_pitch() 
    
        return redirect(url_for('main.index'))

    return render_template('new_pitch.html', pitch_form=pitch_form)

@main.route('/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    description_form = CommentForm()

    pitch = Pitch.query.get(id)

    if description_form.validate_on_submit():
        description = description_form.description.data
        new_comment = Comment(description=description,user_id=current_user.id,pitch_id = pitch.id )
        new_comment.save_comments() 
        return redirect(url_for('main.index'))

    return render_template('comment.html',description_form=description_form)
    
@main.route('/vote', methods=['POST'])
def vote():
    data = simplejson.loads(request.data)
    update_item(c, [data['member']])
    output = select_all_items(c, [data['member']])
    pusher.trigger(u'poll', u'vote', output)
    return request.data