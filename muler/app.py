#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for, session as flask_session
from flask_babel import Babel, gettext, ngettext, lazy_gettext, get_locale
from googletrans import Translator
from muler.database import regex
import markdown
import muler.query as query

db_session = query.db_session()
pattern_values, patterns = query.get_patterns(db_session)

# Initialize Google Translator
translator = Translator()

def translate_text(text, target_lang='th'):
    """Translate text using Google Translate"""
    if not text or target_lang == 'en':
        return text
    
    try:
        # Clean up HTML tags for better translation
        clean_text = regex.drop_tags(text) if hasattr(regex, 'drop_tags') else text
        
        # Skip if text is too short or looks like technical terms
        if len(clean_text.strip()) < 10:
            return text
            
        translated = translator.translate(clean_text, dest=target_lang, src='en')
        return translated.text
    except Exception as e:
        # If translation fails, return original text
        print(f"Translation error: {e}")
        return text

def get_userinput():
    userinput = request.form['search'].lower().strip()
    return userinput

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'muler-translation-secret-key'
    app.config['LANGUAGES'] = {
        'en': 'English',
        'th': 'ไทย'
    }
    
    # Initialize Babel
    babel = Babel()
    babel.init_app(app)
    
    # Make gettext available in templates as _
    @app.context_processor
    def inject_conf_vars():
        return {
            '_': gettext,
            'get_locale': get_locale
        }
    
    def get_locale():
        # 1. Check if language is forced in URL
        if request.args.get('lang'):
            flask_session['language'] = request.args.get('lang')
        # 2. Check if language is in session
        if 'language' in flask_session:
            return flask_session['language']
        # 3. Fall back to best match from Accept-Language header
        return request.accept_languages.best_match(['en', 'th']) or 'en'
    
    # Set the locale selector
    babel.locale_selector_func = get_locale
    
    @app.route('/set_language/<language>')
    def set_language(language=None):
        flask_session['language'] = language
        # Get the 'next' parameter from the query string, or fall back to referrer or index
        next_page = request.args.get('next') or request.referrer or url_for('index')
        return redirect(next_page)
    

    @app.route('/about')
    def about():
      return render_template('about.html')

    @app.route('/legal')
    def legal():
      return render_template('legal.html')

    # /search route for queries to avoid querying database with bot-entered strings
    @app.route('/search/<search_query>', methods=['GET', 'POST'])  
    def link(search_query):
        '''Queries the database via search() using the url slug 
        '''
        if request.method == 'POST':    # Searching while on a result page
            return redirect(url_for('link', search_query=get_userinput()))
        
        # Get search results
        results = query.Query(db_session, pattern_values, patterns).get_results(search_query.lower())
        
        # Get current language
        current_lang = get_locale()
        print(f"DEBUG: Current language in link route: {current_lang}")
        print(f"DEBUG: Session language: {flask_session.get('language', 'not set')}")
        
        # Translate content if user is in Thai mode
        if current_lang == 'th':
            print("DEBUG: Attempting to translate content to Thai...")
            # Translate drug class
            if results.get('d_class'):
                print(f"DEBUG: Translating d_class: {results['d_class'][:50]}...")
                results['d_class_translated'] = translate_text(results['d_class'], 'th')
            
            # Translate indication
            if results.get('ind'):
                print(f"DEBUG: Translating indication: {results['ind'][:50]}...")
                results['ind_translated'] = translate_text(results['ind'], 'th')
            
            # Translate pharmacodynamics  
            if results.get('pd'):
                print(f"DEBUG: Translating pharmacodynamics: {results['pd'][:50]}...")
                results['pd_translated'] = translate_text(results['pd'], 'th')
                
            # Translate mechanism of action
            if results.get('mech'):
                print(f"DEBUG: Translating mechanism: {results['mech'][:50]}...")
                results['mech_translated'] = translate_text(results['mech'], 'th')
        else:
            print(f"DEBUG: Not translating, current language is: {current_lang}")
        
        # Render template with results
        return render_template('result.html',
                               results=results,
                               drugbank_id=results['drugbank_id'],
                               name=results['name'],
                               d_class=results.get('d_class_translated', results['d_class']),
                               ind=regex.drop_tags(results.get('ind_translated', results['ind'])),
                               pd=regex.drop_tags(results.get('pd_translated', results['pd'])),
                               mech=regex.drop_tags(results.get('mech_translated', results['mech'])),
                               synonyms=query.stringify(results['synonyms']),
                               products=query.stringify(results['products']),
                               suggestions=results['suggestions'],
                               current_lang=current_lang)
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            return redirect(url_for('link', search_query=get_userinput()))        
        elif request.method == 'GET':    
            return render_template('index.html')
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Check if running in Docker container
    import os
    host = '0.0.0.0' if os.getenv('FLASK_ENV') == 'production' else '127.0.0.1'
    app.run(debug=True, host=host)
