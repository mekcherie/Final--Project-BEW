from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from rally_app.models import Rallyspot, Rallyevent, User
from rally_app.forms import RallyspotForm, RallyeventForm, SignUpForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from rally_app import bcrypt
from rally_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_spots = Rallyspot.query.all()
    print(all_spots)
    return render_template('home.html', all_spots=all_spots)


@main.route('/new_spot', methods=['GET', 'POST'])
@login_required
def new_spot():
    form = RallyspotForm()

    if form.validate_on_submit():
        new_spot = Rallyspot(
            title = form.title.data,
            address = form.address.data,
            created_by = current_user
        )

        db.session.add(new_spot)
        db.session.commit()

        flash('New spot Created')
        return redirect(url_for('main.spot_detail', spot_id = new_spot.id))
    
    return render_template('new_spot.html', form = form)


@main.route('/new_', methods=['GET', 'POST'])
@login_required
def new_event():
    form = RallyeventForm()

    if form.validate_on_submit():
        new_event = Rallyevent(
            name = form.name.data,
            price = form.price.data,
            category = form.category.data,
            photo_url = form.photo_url.data,
            spot = form.spot.data,
            created_by = current_user
        )

        db.session.add(new_event)
        db.session.commit()

        flash('New event Added')
        return redirect(url_for('main.event_detail', event_id = new_event.id))
    
    return render_template('new_event.html', form=form)


@main.route('/spot/<spot_id>', methods=['GET', 'POST'])
@login_required
def spot_detail(spot_id):
    spot = Rallyspot.query.get(spot_id)
    form = RallyspotForm (obj=spot)

    if form.validate_on_submit():
        spot.title = form.title.data
        spot.address = form.address.data

        db.session.commit()

        flash('Updated spot')
        return redirect(url_for('main.spot_detail', spot_id=spot.id, spot=spot))

    return render_template('spot_detail.html', spot=spot, form=form)


@main.route('/event/<event_id>', methods=['GET', 'POST'])
@login_required
def event_detail(event_id):
    event = Rallyevent.query.get(event_id)

    form = RallyeventForm(obj=event)

    if form.validate_on_submit():
        event.name = form.name.data
        event.price = form.price.data
        event.category = form.category.data
        event.photo_url = form.photo_url.data
        event.spot = form.spot.data

        db.session.commit()

        flash('Updated event')
        return redirect(url_for('main.event_detail', event_id=event.id, event=event))

    return render_template('event_detail.html', event=event, form=form)


@main.route('/add_to_shopping_list/<event_id>', methods = ['POST'])
def add_to_shopping_list(event_id):
    user_current = current_user
    event = Rallyevent.query.get(event_id)
    user_current.shopping_list_events.append(event)
    db.session.commit()

    flash('event was added to Cart')
    return redirect(url_for('main.event_detail', event_id = event.id))


@main.route('/shopping_list')
@login_required
def shopping_list():
    events = current_user.shopping_list_events
    return render_template('shopping_list.html', shopping_events = events)


##########################################
#         Authentication  Routes         #
##########################################

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
