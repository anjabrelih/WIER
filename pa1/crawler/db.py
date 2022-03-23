import threading
import psycopg2
import time

from validator_collection import url



# Set threading lock for database
lock = threading.Lock()

# Get crawl delay
def get_crawl_delay(domain):
    with lock:
        crawl_delay = 5
        site_id = ''
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()
            
            sql = 'SELECT site.crawl_delay, site.id FROM crawldb.site WHERE site.domain = %s;'
            cur.execute(sql, (domain,))
            crawl_delay, site_id = cur.fetchall()[0][1] # zakaj site ID? bit more tud v poizvedbi

            cur.close()
            return crawl_delay, site_id
        
        except Exception as error:
            print("Error geting frontier size: ", error)
            return crawl_delay, site_id

        finally:
            if conn is not None:
                conn.close()

# Get frontier size
def get_frontier_size():
    with lock:
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()
            
            sql = "SELECT COUNT (ALL crawldb.page WHERE page_type_code = 'FRONTIER');"
            cur.execute(sql, )
            frontier_size = cur.fetchall()[0]
            print("Frontier size: ", frontier_size)
            cur.close()
            return frontier_size
        
        except Exception as error:
            print("Error geting frontier size: ", error)
            return -1

        finally:
            if conn is not None:
                conn.close()


# Get URL from frontier (one at the time)
def get_url_from_frontier():
    with lock:
        flag = -1
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()

            # Get url from frontier
            sql = '''SELECT crawldb.page.url WHERE page_type_code = 'FRONTIER'
                    INNER JOIN crawldb.site ON (crawldb.page.site_id = crawldb.site.id) WHERE 
                    (site.last_accessed_time <=  (%s - site.crawl_delay))
                    ORDER BY page.id ASC LIMIT 1;'''
            
            cur.execute(sql, (int(time.time()),))
            frontier_url = cur.fetchone()[0]
            flag = 1

            # Update page_type_code
            sql = 'UPDATE crawldb.page SET page_type_code = NULL WHERE page.url = %s;'
            cur.execute(sql, (frontier_url,))
            


            # Update page_type_code - dont need
            #sql = 'UPDATE crawldb.site SET crawldb.last_accessed_time = %s WHERE site_id = %s;'
            #cur.execute(sql, (int(time.time()), site_id,))

            cur.close()


            return frontier_url, flag
        
        except Exception as error:
            print("Error geting URLs from frontier: ", error)
            return '', -10

        finally:
            if conn is not None:
                conn.close()

# Insert domain/check domain index
def write_domain_to_site(domain):
    with lock:
        index = -1
        flag = -1
        disallow = []
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True
            cur =conn.cursor()

            # Check if domain exists, if so get site_id
            try:
                sql = 'SELECT id FROM crawldb.site WHERE site.domain = %s;'
                cur.execute(sql, (domain,))
                index = cur.fetchone()[0]
                flag = 1

                sql = 'SELECT disallow FROM crawldb.site WHERE site.domain = %s;'
                cur.execute(sql, (domain,))
                disallow = cur.fetchall()

            except Exception as e:
                conn.rollback()

            if index == -1:
                try:
                    # Add new site
                    sql = 'INSERT INTO crawldb.site(site.domain) VALUES (%s);'
                    cur.execute(sql, (domain,))
                    # Get site_id
                    sql = 'SELECT id FROM crawldb.site WHERE site.domain = %s;'
                    cur.execute(sql, (domain,))
                    index = cur.fetchone()[0]

                except Exception as e:
                    conn.rollback()          


            cur.close()

            return index, flag, disallow
        
        except Exception as error:
            print("Error geting getting domain to database/getting domain id: ", error)
            return index

        finally:
            if conn is not None:
                conn.close()


# Update site with domain content
def update_site(siteid, domain, robots_content, sitemap_content, ip_address, crawl_delay, last_accessed_time):
    with lock:
            try:
                conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
                conn.autocommit = True

                cur =conn.cursor()
                
                sql = '''UPDATE crawldb.site SET robots_content = %s, sitemap_content = %s, ip_address = %s, crawl_delay = %s, last_accessed_time = %s 
                WHERE id = %s RETURNING id;'''
                cur.execute(sql, (robots_content, sitemap_content, ip_address, crawl_delay, last_accessed_time, siteid,))
                id = cur.fetchone()[0]

                print('Logged into site: '+ domain)
                print('ID: ', id)
            
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed: ", error)

            finally:
                if conn is not None:
                    conn.close()


# Insert URLs to frontier (multiple urls)
def write_url_to_frontier(urls_siteid):
    with lock:
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            index = -1
            tag = 'FRONTIER'

            cur =conn.cursor()

            for line in urls_siteid:
                # Check if url exists in db
                try:
                    sql = 'SELECT id FROM crawldb.page WHERE page.url = %s;'
                    cur.execute(sql, (line[0],))
                    index = cur.fetchone()[0]

                except Exception as e:
                    conn.rollback()

                if index == -1:
                    try:
                        # Add new url to frontier
                        sql = 'INSERT INTO crawldb.page (page.url, page.site_id, page.page_type_code) VALUES (%s, %s, %s) RETURNING id;'
                        cur.execute(sql, (line[0], line[1], tag,))
                        page_id = cur.fetchone()[0]

                        # Add connection to link table
                        sql = 'INSERT INTO crawldb.link (from_page, to_page) VALUES (%s,%s)'
                        cur.execute(sql, (page_id, line[0],))

                    except Exception as e:
                        conn.rollback()

            cur.close()

        
        except Exception as error:
            print("Error geting URLs to frontier: ", error)


        finally:
            if conn is not None:
                conn.close()



# Update page
def update_page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, hash, last_accessed_time):
        with lock:
            try:
                conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
                conn.autocommit = True

                cur =conn.cursor()

                id = -1
                index = -1
                tag_duplicate = 'DUPLICATE'

                # Check if hash exists in db
                try:
                    sql = 'SELECT id FROM crawldb.page WHERE page_hash = %s;'
                    cur.execute(sql, (hash,))
                    index = cur.fetchone()[0]

                except Exception as e:
                    conn.rollback()

                if index == -1:
                    try:
                        # Update row (as HTML)
                        sql = '''UPDATE crawldb.page SET page_type_code = %s, html_content = %s, http_status_code = %s, accessed_time = %s,
                        hash = %s WHERE url = %s RETURNING id;'''
                        cur.execute(sql, (page_type_code, html_content, http_status_code, accessed_time, hash, url,))
                        id = cur.fetchone()[0]

                        # Update last accessed time for domain
                        sql = 'UPDATE crawldb.page SET last_accessed_time = %s WHERE site_id = %s;'
                        cur.execute(sql, (last_accessed_time, site_id,))

                        print('Logged into page: '+ url)
                        print('ID: ', id)

                    except Exception as e:
                        conn.rollback()
                
                if index != -1:
                    try:
                        # Update row (as DUPLICATE)
                        sql = 'UPDATE crawldb.page SET page_type_code = %s, accessed_time = %s WHERE url = %s RETURNING id;'
                        cur.execute(sql, (tag_duplicate, accessed_time, url,))
                        id = cur.fetchone()[0]

                        # Update last accessed time for domain
                        sql = 'UPDATE crawldb.page SET last_accessed_time = %s WHERE site_id = %s;'
                        cur.execute(sql, (last_accessed_time, site_id,))

                        print('Logged into page: '+ url)
                        print('ID: ', id)

                    except Exception as e:
                        conn.rollback()
                
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed updating html page: ", error)

            finally:
                if conn is not None:
                    conn.close()

        return id

# Write BINARY data
def write_data(page_type_code, url, http_status_code, accessed_time, last_accessed_time, page_data_type):
    with lock:
            try:
                conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
                conn.autocommit = True

                cur =conn.cursor()
                
                # Update page
                sql = 'UPDATE crawldb.page (page_type_code, http_status_code, accessed_time) VALUES (%s, %s, %s) WHERE url = %s RETURNING id, site_id;'
                cur.execute(sql, (page_type_code, http_status_code, accessed_time, url,))
                page_id, site_id = cur.fetchall()
                print('RETURNING page_id SITE id: ', page_id, site_id)

                # Write page_data
                sql = 'INSERT INTO crawldb.page_data (page_id, data_type_code) VALUES (%s,%s)'
                cur.execute(sql, (page_id, page_data_type,))

                # Update last accessed time for domain
                sql = 'UPDATE crawldb.page SET last_accessed_time = %s WHERE site_id = %s;'
                cur.execute(sql, (last_accessed_time, site_id,))

           
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed: ", error)

            finally:
                if conn is not None:
                    conn.close()


# Write image
def write_img(url_site_id, page_type_code, content_type, accessed_time):
    with lock:

        index = -1
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()

            for line in url_site_id:
                    # Check if image url exists
                try:
                    sql = 'SELECT id FROM crawldb.page WHERE page.url = %s;'
                    cur.execute(sql, (line[0],))
                    index = cur.fetchone()[0]

                   # # Update site
                    #sql = 'UPDATE last_accessed_time FROM crawldb.site WHERE id = %s'
                    #cur.execute(sql, (line[1],))

                except Exception as e:
                    conn.rollback()

                if index == -1:
                    try:
                        # New image to page
                        sql = 'INSERT INTO crawldb.page (page.url, page.site_id, page.page_type_code, page.accessed_time) VALUES (%s, %s, %s, %s) RETURNING id;'
                        cur.execute(sql, (line[0], line[1], page_type_code, accessed_time,))
                        page_id = cur.fetchone()[0]

                        # Add new image to image
                        sql = 'INSERT INTO crawldb.image (image.page_id, image.content_type, image.accessed_time) VALUES (%s, %s, %s)'
                        cur.execute(sql, (page_id, content_type, accessed_time))

                       # # Update site
                       # sql = 'UPDATE last_accessed_time FROM crawldb.site WHERE id = %s'
                        #cur.execute(sql, (line[1],))

                    except Exception as e:
                        conn.rollback()

            cur.close()

        finally:
            if conn is not None:
                conn.close()