from newscatcherapi import NewsCatcherApiClient
from datetime import datetime, timedelta

KEYWORDS = 'Employee Ownership, ESOP, Worker Cooperative, Worker Coop, Employee Ownership Trust, EOT, Direct Employee Ownership, Employee Profit Sharing, employee engagement, wealth gap, retirement gap, business succession, business exit, sale to employees, Private equity & employee ownership';
API_KEY = 'A6p-Xe0UKBQqftsF0I90b-j0wT-iaZwB'
newscatcherapi = NewsCatcherApiClient(x_api_key=API_KEY)

def search_news(query, lang='en', countries=['US'], from_date=None, to_date=None, is_paid_content=False, exclude_duplicates=True):
    """
    Search for news articles using the Newscatcher API.
    
    Args:
        query (str): Search query (keywords).
        lang (str): Language of the articles.
        countries (str): Comma-separated country codes.
        from_date (str): Start date for the news search in YYYY-MM-DD format. Defaults to three months ago.
        to_date (str): End date for the news search in YYYY-MM-DD format. Defaults to today.
        is_paid_content (bool): Whether to include paid content or not.
        exclude_duplicates (bool): Whether to exclude duplicate articles.
    
    Returns:
        list: List of news articles.
    """
    # Set default dates if not provided
    if not from_date:
        from_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    if not to_date:
        to_date = datetime.now().strftime('%Y-%m-%d')

    try:
        # Perform the search
        response = newscatcherapi.get_search(
            q=query,
            lang=lang,
            from_=from_date,
            to_=to_date        )
        # Extract articles from the response
        articles = response.get('articles', [])
        
        # Optionally filter by country and duplicates if necessary
        if countries:
            country_list = countries.split(',')
            articles = [article for article in articles if article.get('country') in country_list]
        if exclude_duplicates:
            seen_titles = set()
            filtered_articles = []
            for article in articles:
                if article['title'] not in seen_titles:
                    filtered_articles.append(article)
                    seen_titles.add(article['title'])
            articles = filtered_articles

        return articles
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    articles = search_news(KEYWORDS, from_date=None, to_date=None)
    for article in articles:
        print(article['title'], "-", article['link'])