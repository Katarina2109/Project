s_query = """SELECT  title       
             FROM film
             WHERE title LIKE %s
             LIMIT 10 
             ;"""

get_films_by_keyword_query = """SELECT f.title, c.name AS genre, f.release_year
                               FROM film f
                               LEFT JOIN film_category fc ON f.film_id = fc.film_id
                               LEFT JOIN category c ON fc.category_id = c.category_id
                               WHERE f.title LIKE %s
                               Limit 10 OFFSET %s;"""

get_film_genre_year_query = """SELECT f.title, c.name AS genre, f.release_year
                               FROM film f
                               LEFT JOIN film_category fc ON f.film_id = fc.film_id
                               LEFT JOIN category c ON fc.category_id = c.category_id
                               WHERE c.name = %s AND f.release_year = %s
                               ORDER BY f.release_year, c.name 
                               Limit 10 OFFSET %s
                               ;
                               """

get_film_genre_query = """SELECT f.title, c.name AS genre, f.release_year
                          FROM film f
                          LEFT JOIN film_category fc ON f.film_id = fc.film_id
                          LEFT JOIN category c ON fc.category_id = c.category_id
                          WHERE c.name = %s 
                          ORDER BY f.release_year
                          Limit 10 OFFSET %s
                          ;
                          """

get_film_year_query = """SELECT f.title, c.name AS genre, f.release_year
                          FROM film f
                          LEFT JOIN film_category fc ON f.film_id = fc.film_id
                          LEFT JOIN category c ON fc.category_id = c.category_id
                          WHERE f.release_year = %s
                          ORDER BY f.release_year
                          Limit 10 OFFSET %s
                          ;
                          """

get_table_keywords_query = """CREATE TABLE IF NOT EXISTS search_keywords (
                              id INT AUTO_INCREMENT PRIMARY KEY,
                              keyword VARCHAR(255) NOT NULL,
                              search_count INT DEFAULT 1,
                              UNIQUE (keyword)
                              );"""

get_count_keywords_query = """INSERT INTO search_keywords (keyword, search_count)
                              VALUES (%s, 1)
                              ON DUPLICATE KEY UPDATE search_count = search_count + 1;"""

get_popular_query = """SELECT keyword, search_count
                       FROM search_keywords
                       ORDER BY search_count DESC
                       LIMIT %s OFFSET %s;
                       """

get_category_query = """SELECT name
                        FROM category;"""
