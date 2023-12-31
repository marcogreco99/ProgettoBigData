from flask import Flask, render_template, request
import main

# istruzioni terminale per avviare il progetto
# set FLASK_APP=app
# set FLASK_ENV=development
# flask --app app.py --debug run

app = Flask(__name__)

currentReviews = main.reviews
filteredByPositive = False
filteredByNegative = False
orderedByShorter = False
orderedByLonger = False
filteredWithSpoilers = False
filteredWithoutSpoilers = False
searchString = ""

@app.route('/pagination')
def pagination():
    global currentReviews
    # Impostiamo il numero di elementi per pagina
    per_page = 6
    # Otteniamo la pagina corrente dalla richiesta HTTP
    page = int(request.args.get('page', 1))
    # Calcoliamo il numero totale di pagine necessarie
    total_pages = (currentReviews.count() + per_page - 1) // per_page
    paginated_reviews = paginated_data(currentReviews.collect(), page, per_page)
    return render_template('index.html', reviews=paginated_reviews, flags=getFlags(), page=page, total_pages=total_pages)

def paginated_data(data, page, per_page):
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]
    return paginated_data

@app.route('/')
def index():
    global currentReviews, filteredByPositive, filteredByNegative, orderedByShorter,\
        orderedByLonger, filteredWithoutSpoilers, filteredWithSpoilers, searchString
    filteredByPositive = False
    filteredByNegative = False
    orderedByShorter = False
    orderedByLonger = False
    filteredWithoutSpoilers = False
    filteredWithSpoilers = False
    searchString = ""
    currentReviews = main.reviews
    total_pages = (currentReviews.count() + 6 - 1) // 6
    paginated_reviews = paginated_data(currentReviews.collect(), 1, 6)
    return render_template('index.html', reviews=paginated_reviews, flags=getFlags(), page=1, total_pages=total_pages)

@app.route('/positive')
def getPositive():
    global currentReviews, filteredByPositive, filteredByNegative, orderedByShorter,\
        orderedByLonger, filteredWithoutSpoilers, filteredWithSpoilers, searchString
    if (not filteredByPositive):
        currentReviews = main.filterByPositive(main.reviews)
    else:
        currentReviews = main.reviews
    filteredByPositive = not filteredByPositive
    filteredByNegative = False
    # controlliamo se era stato effettuato l'ordinamento precedentemente
    if (orderedByShorter):
        currentReviews = main.orderByShortReviews(currentReviews)
    elif (orderedByLonger):
        currentReviews = main.orderByLongReviews(currentReviews)
    # controlliamo se era stato effettuato il filtro degli spoilers precedentemente
    if (filteredWithoutSpoilers):
        currentReviews = main.filterByNoSpoilers(currentReviews)
    elif (filteredWithSpoilers):
        currentReviews = main.filterBySpoilers(currentReviews)
    # controlliamo se era stato effettuata la ricerca per una determinata parola/frase
    if (searchString != ""):
        currentReviews = main.filterByWord(currentReviews, searchString)
    total_pages = (currentReviews.count() + 6 - 1) // 6
    paginated_reviews = paginated_data(currentReviews.collect(), 1, 6)
    return render_template('index.html', reviews=paginated_reviews, flags=getFlags(), page=1, total_pages=total_pages)

@app.route('/negative')
def getNegative():
    global currentReviews, filteredByNegative, filteredByPositive, orderedByShorter,\
        orderedByLonger, filteredWithoutSpoilers, filteredWithSpoilers, searchString
    if (not filteredByNegative):
        currentReviews = main.filterByNegative(main.reviews)
    else:
        currentReviews = main.reviews
    filteredByNegative = not filteredByNegative
    filteredByPositive = False
    # controlliamo se era stato effettuato l'ordinamento precedentemente
    if (orderedByShorter):
        currentReviews = main.orderByShortReviews(currentReviews)
    elif (orderedByLonger):
        currentReviews = main.orderByLongReviews(currentReviews)
    # controlliamo se era stato effettuato il filtro degli spoilers precedentemente
    if (filteredWithoutSpoilers):
        currentReviews = main.filterByNoSpoilers(currentReviews)
    elif (filteredWithSpoilers):
        currentReviews = main.filterBySpoilers(currentReviews)
    # controlliamo se era stato effettuata la ricerca per una determinata parola/frase
    if (searchString != ""):
        currentReviews = main.filterByWord(currentReviews, searchString)
    total_pages = (currentReviews.count() + 6 - 1) // 6
    paginated_reviews = paginated_data(currentReviews.collect(), 1, 6)
    return render_template('index.html', reviews=paginated_reviews, flags=getFlags(), page=1, total_pages=total_pages)

@app.route('/shorter')
def orderByShorterReviews():
    global currentReviews, orderedByShorter, orderedByLonger, filteredByPositive,\
        filteredByNegative, filteredWithoutSpoilers, filteredWithSpoilers, searchString
    if (not orderedByShorter):
        currentReviews = main.orderByShortReviews(currentReviews)
    else:
        currentReviews = main.reviews
        # applichiamo gli eventuali filtri che c'erano prima
        if (filteredByPositive): currentReviews = main.filterByPositive(currentReviews)
        elif (filteredByNegative): currentReviews = main.filterByNegative(currentReviews)
        if (filteredWithoutSpoilers): currentReviews = main.filterByNoSpoilers(currentReviews)
        elif (filteredWithSpoilers): currentReviews = main.filterBySpoilers(currentReviews)
        if (searchString != ""): currentReviews = main.filterByWord(currentReviews, searchString)
    orderedByShorter = not orderedByShorter
    orderedByLonger = False
    total_pages = (currentReviews.count() + 6 - 1) // 6
    paginated_reviews = paginated_data(currentReviews.collect(), 1, 6)
    return render_template('index.html', reviews=paginated_reviews, flags=getFlags(), page=1, total_pages=total_pages)

@app.route('/longer')
def orderByLongerReviews():
    global currentReviews, orderedByLonger, orderedByShorter, filteredByPositive,\
        filteredByNegative, filteredWithoutSpoilers, filteredWithSpoilers, searchString
    if (not orderedByLonger):
        currentReviews = main.orderByLongReviews(currentReviews)
    else:
        currentReviews = main.reviews
        # applichiamo gli eventuali filtri che c'erano prima
        if (filteredByPositive): currentReviews = main.filterByPositive(currentReviews)
        elif (filteredByNegative): currentReviews = main.filterByNegative(currentReviews)
        if (filteredWithoutSpoilers): currentReviews = main.filterByNoSpoilers(currentReviews)
        elif (filteredWithSpoilers): currentReviews = main.filterBySpoilers(currentReviews)
        if (searchString != ""): currentReviews = main.filterByWord(currentReviews, searchString)
    orderedByLonger = not orderedByLonger
    orderedByShorter = False
    total_pages = (currentReviews.count() + 6 - 1) // 6
    paginated_reviews = paginated_data(currentReviews.collect(), 1, 6)
    return render_template('index.html', reviews=paginated_reviews, flags=getFlags(), page=1, total_pages=total_pages)

@app.route('/withoutSpoilers')
def getReviewsWithoutSpoilers():
    global currentReviews, filteredByPositive, filteredByNegative, orderedByShorter,\
        orderedByLonger, filteredWithoutSpoilers, filteredWithSpoilers, searchString
    if (not filteredWithoutSpoilers):
        currentReviews = main.filterByNoSpoilers(main.reviews)
    else:
        currentReviews = main.reviews
    filteredWithoutSpoilers = not filteredWithoutSpoilers
    filteredWithSpoilers = False
    # controlliamo se era stato effettuato l'ordinamento precedentemente
    if (orderedByShorter):
        currentReviews = main.orderByShortReviews(currentReviews)
    elif (orderedByLonger):
        currentReviews = main.orderByLongReviews(currentReviews)
    # controlliamo se era stato effettuato il filtro delle positive/negative precedentemente
    if (filteredByPositive):
        currentReviews = main.filterByPositive(currentReviews)
    elif (filteredByNegative):
        currentReviews = main.filterByNegative(currentReviews)
    # controlliamo se era stato effettuata la ricerca per una determinata parola/frase
    if (searchString != ""):
        currentReviews = main.filterByWord(currentReviews, searchString)
    total_pages = (currentReviews.count() + 6 - 1) // 6
    paginated_reviews = paginated_data(currentReviews.collect(), 1, 6)
    return render_template('index.html', reviews=paginated_reviews, flags=getFlags(), page=1, total_pages=total_pages)

@app.route('/withSpoilers')
def getReviewsWithSpoilers():
    global currentReviews, filteredByPositive, filteredByNegative, orderedByShorter,\
        orderedByLonger, filteredWithoutSpoilers, filteredWithSpoilers, searchString
    if (not filteredWithSpoilers):
        currentReviews = main.filterBySpoilers(main.reviews)
    else:
        currentReviews = main.reviews
    filteredWithSpoilers = not filteredWithSpoilers
    filteredWithoutSpoilers = False
    # controlliamo se era stato effettuato l'ordinamento precedentemente
    if (orderedByShorter):
        currentReviews = main.orderByShortReviews(currentReviews)
    elif (orderedByLonger):
        currentReviews = main.orderByLongReviews(currentReviews)
    # controlliamo se era stato effettuato il filtro delle positive/negative precedentemente
    if (filteredByPositive):
        currentReviews = main.filterByPositive(currentReviews)
    elif (filteredByNegative):
        currentReviews = main.filterByNegative(currentReviews)
    # controlliamo se era stato effettuata la ricerca per una determinata parola/frase
    if (searchString != ""):
        currentReviews = main.filterByWord(currentReviews, searchString)
    total_pages = (currentReviews.count() + 6 - 1) // 6
    paginated_reviews = paginated_data(currentReviews.collect(), 1, 6)
    return render_template('index.html', reviews=paginated_reviews, flags=getFlags(), page=1, total_pages=total_pages)

@app.route('/search')
def search():
    global currentReviews, filteredByPositive, filteredByNegative, orderedByShorter,\
        orderedByLonger, filteredWithoutSpoilers, filteredWithSpoilers, searchString
    searchString = request.args.get('searchString')
    currentReviews = main.filterByWord(currentReviews, searchString)
    total_pages = (currentReviews.count() + 6 - 1) // 6
    paginated_reviews = paginated_data(currentReviews.collect(), 1, 6)
    return render_template('index.html', reviews=paginated_reviews, flags=getFlags(), page=1, total_pages=total_pages)

@app.route('/cancelResearch')
def cancelResearch():
    global currentReviews, filteredByPositive, filteredByNegative, orderedByShorter,\
        orderedByLonger, filteredWithoutSpoilers, filteredWithSpoilers, searchString
    searchString = ""
    currentReviews = main.reviews
    # controlliamo tutti i filtri e gli ordinamenti
    if (filteredByPositive): currentReviews = main.filterByPositive(currentReviews)
    elif (filteredByNegative): currentReviews = main.filterByNegative(currentReviews)
    if (filteredWithoutSpoilers): currentReviews = main.filterByNoSpoilers(currentReviews)
    elif (filteredWithSpoilers): currentReviews = main.filterBySpoilers(currentReviews)
    if (orderedByShorter): currentReviews = main.orderByShortReviews(currentReviews)
    elif (orderedByLonger): currentReviews = main.orderByLongReviews(currentReviews)
    total_pages = (currentReviews.count() + 6 - 1) // 6
    paginated_reviews = paginated_data(currentReviews.collect(), 1, 6)
    return render_template('index.html', reviews=paginated_reviews, flags=getFlags(), page=1, total_pages=total_pages)

@app.route('/counting')
def getCounting():
    counting = [currentReviews.count(), main.filterByPositive(currentReviews).count(), main.filterByNegative(currentReviews).count()]
    return counting

@app.route('/predict')
def predictSentiment():
    userReview = request.args.get('userReview')
    sentiment = main.predict_sentiment(userReview)
    return str(sentiment)

@app.route('/stats')
def stats():
    return render_template('stats.html')

def getFlags():
    return [filteredByPositive, filteredByNegative, filteredWithSpoilers, filteredWithoutSpoilers, orderedByShorter, orderedByLonger, searchString]