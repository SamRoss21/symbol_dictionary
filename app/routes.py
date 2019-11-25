from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app import app, db
from app.models import User, Concept, SearchWord, Image
from app.forms import LoginForm, RegistrationForm, AddConcept, AddSearchWord, AddImage, AddImport
from app import db 
import json


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = AddConcept()
    if form.validate_on_submit():
        user_concept = Concept.query.filter_by(concept=form.concept.data).first()
        if user_concept is None:
            concept = Concept(concept=form.concept.data, user_id=current_user.id, num_im=0, verified='0',deleted='0')
            db.session.add(concept)
            db.session.commit()
            flash('Concept Added')
            return redirect(url_for('index'))
        else:
            if str(user_concept.deleted)=='1':
                user_concept.deleted='0'
                user_concept.timestamp=datetime.utcnow()
                db.session.commit()
    concepts = Concept.query.filter_by(deleted='0').order_by(Concept.timestamp.desc())
    return render_template("index.html", title='Home Page', form=form,
                           concepts=concepts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/addSearchWord/<concept>', methods=['GET', 'POST'])
@login_required
def addSearchWord(concept):
    form = AddSearchWord()
    if form.validate_on_submit():
        user_word = SearchWord.query.filter_by(searchWord=form.searchWord.data).first()
        print(user_word)
        if user_word is None:
            searchWord = SearchWord(searchWord=form.searchWord.data)
            searchWord.brainstorm = '1'
            searchWord.concept = concept
            searchWord.num_im = 0
            searchWord.verified = '0'
            searchWord.deleted = '0'
            db.session.add(searchWord)
            db.session.commit()
            return redirect(url_for('addSearchWord', concept=concept))
        else:
            if str(user_word.deleted)=='1':
                user_word.deleted='0'
                user_word.timestamp=datetime.utcnow()
                db.session.commit()
    searchWords = SearchWord.query.filter_by(concept=concept, deleted='0').order_by(SearchWord.timestamp.desc())
    images = Image.query.filter_by(concept=concept, deleted='0').order_by(Image.timestamp.desc())
    return render_template("addSearchWord.html", concept=concept, form=form, searchWords=searchWords, images=images)


@app.route('/addImage/<concept>/<searchWord>', methods=['GET', 'POST'])
@login_required
def addImage(concept, searchWord):
    form = AddImage()
    if form.validate_on_submit():
        user_img = Image.query.filter_by(image=form.image.data).first()
        if user_img is None:
            image = Image(image=form.image.data)
            image.searchWord = searchWord
            image.concept = concept
            searchWord.verified = '0'
            searchWord.deleted = '0'
            db.session.add(image)
            rel_searchWord = SearchWord.query.filter_by(searchWord=searchWord).first()
            rel_searchWord.num_im = int(rel_searchWord.num_im) + 1
            rel_concept = Concept.query.filter_by(concept=concept).first()
            rel_concept.num_im = int(rel_concept.num_im) + 1
            db.session.commit()
            return redirect(url_for('addImage', searchWord=searchWord, concept=concept))
        else:
            if str(user_img.deleted)=='1':
                user_img.deleted='0'
                user_img.timestamp=datetime.utcnow()
                db.session.commit()
    images = Image.query.filter_by(concept=concept, searchWord=searchWord, deleted='0').order_by(Image.timestamp.desc())
    return render_template("images.html", concept=concept, form=form,
                           searchWord=searchWord, images=images)

@app.route("/deleteConcept", methods=['GET','POST'])
def deleteConcept():
    form = AddConcept()
    concept = request.form['data']
    del_concept = Concept.query.filter_by(concept=concept).first()
    del_concept.deleted='1'
    db.session.commit()
    concepts = Concept.query.filter_by(deleted='0').order_by(Concept.timestamp.desc())
    return render_template("index.html", title='Home Page', form=form,
                           concepts=concepts)

@app.route("/deleteSearchWord", methods=['GET','POST'])
def deleteSearchWord():
    form = AddSearchWord()
    searchWord = request.form['word']
    concept = request.form['concept']
    del_word = SearchWord.query.filter_by(searchWord=searchWord,concept=concept).first()
    del_word.deleted='1'
    db.session.commit()
    searchWords = SearchWord.query.filter_by(concept=concept, deleted='0').order_by(SearchWord.timestamp.desc())
    images = Image.query.filter_by(concept=concept,deleted='0').order_by(Image.timestamp.desc())
    return render_template("addSearchWord.html", concept=concept, form=form, searchWords=searchWords, images=images)

@app.route("/deleteImage", methods=['GET','POST'])
def deleteImage():
    form = AddImage()
    image = request.form['image']
    searchWord = request.form['word']
    concept = request.form['concept']
    del_img = Image.query.filter_by(image=image,searchWord=searchWord,concept=concept).first()
    del_img.deleted='1'
    rel_searchWord = SearchWord.query.filter_by(searchWord=searchWord).first()
    rel_searchWord.num_im = int(rel_searchWord.num_im) - 1
    rel_concept = Concept.query.filter_by(concept=concept).first()
    rel_concept.num_im = int(rel_concept.num_im) - 1
    db.session.commit()
    images = Image.query.filter_by(concept=concept, searchWord=searchWord, deleted='0').order_by(Image.timestamp.desc())
    return render_template("images.html", concept=concept, form=form,
                           searchWord=searchWord, images=images)

@app.route('/import_JSON', methods=['GET', 'POST'])
def import_JSON():
    #/Users/samross/Desktop/Main/Barnard/Research/symbol_dictionary/app/tests/load_json_test.json
    form = AddImport()
    if form.validate_on_submit():
        filename = form.path.data
        print(filename)
        with open(filename, 'r') as f:
            images = json.load(f)
            for each in images:
                x = images[each]
                url = x['imageURL']
                username = x['who']
                searchWord = x['term']
                concept = x['initialSearchTerm']
                time = x['time']
                user = User.query.filter_by(username=username).first()
                concept_match = Concept.query.filter_by(concept=concept).first()
                searchWord_match = SearchWord.query.filter_by(concept=concept, searchWord=searchWord).first()
                image_match = Image.query.filter_by(concept=concept, searchWord=searchWord, image=url).first()
                if user is not None:
                    print('got user')
                    if concept_match is None:
                        addConcept_JSON(concept, user)
                    if searchWord_match is None:
                        addSearchWord_JSON(concept, searchWord)
                    if image_match is None:
                        print("going to add image")
                        addImage_JSON(concept, searchWord, url)
                    db.session.commit()              
        return redirect(url_for('import_JSON'))
    return render_template("import.html", form=form)

def addConcept_JSON(concept, user):
    new_concept = Concept(concept=concept, user_id=user.id, num_im=0, verified='0',deleted='0')
    db.session.add(new_concept)

def addSearchWord_JSON(concept, searchWord):
    new_searchWord = SearchWord(searchWord=searchWord)
    new_searchWord.brainstorm = '1'
    new_searchWord.concept = concept
    new_searchWord.num_im = 0
    new_searchWord.verified = '0'
    new_searchWord.deleted = '0'
    db.session.add(new_searchWord)

def addImage_JSON(concept, searchWord, image):
    print("adding image")
    new_image = Image(image=image)
    new_image.searchWord = searchWord
    new_image.concept = concept
    new_image.verified = '0'
    new_image.deleted = '0'
    db.session.add(new_image)
    rel_searchWord = SearchWord.query.filter_by(searchWord=searchWord).first()
    rel_searchWord.num_im = int(rel_searchWord.num_im) + 1
    rel_concept = Concept.query.filter_by(concept=concept).first()
    rel_concept.num_im = int(rel_concept.num_im) + 1

#def export_JSON():
    #filepath = ""
    #turn the concept search words and images into a JSON file that then gets uploaded to wordblender ish
    # make dictionary of images each image object has above fields and a random id to be the unique key
    #random id = impurt uuid at top, str(uuid.uuid4()) and make it a string 
    #call it imgID
    #images = {}
    #create image obj w fields
    #rand_id = uuid
    #image_obj['imgID'] = rand_id
    #images[rand_id] = image_obj
    #with open(filepath, 'w') as outfile:
        #json.dump(images, outfile)




