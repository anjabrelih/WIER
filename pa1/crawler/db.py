import threading
import psycopg2
import time


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
            
            sql = 'SELECT crawl_delay, id FROM crawldb.site WHERE domain = %s;'
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
            
            sql = "SELECT COUNT ( * ) FROM crawldb.page WHERE page_type_code = 'FRONTIER';"
            cur.execute(sql, )
            frontier_size = cur.fetchone()[0]
            print("Frontier size: ", frontier_size)
            cur.close()
            return frontier_size
        
        except Exception as error:
            print("Error geting frontier size: ", error)
            return -1

        finally:
            if conn is not None:
                conn.close()

#print(get_frontier_size())


# Get URL from frontier (one at the time)
def get_url_from_frontier():
    with lock:
        
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()

            # Get urls from frontier
            sql = "SELECT (url, site_id) FROM crawldb.page WHERE page_type_code = 'FRONTIER' ORDER BY id ASC LIMIT 100"

              #      INNER JOIN crawldb.site ON (page.site_id = site.id) WHERE 
                #    (last_accessed_time <=  (%s - crawl_delay))
                #    ORDER BY page.id ASC LIMIT 1;'''
            
            cur.execute(sql, )
            urls = cur.fetchall()
            print(urls)

            for url in urls:

                frontier_url = -1
                print(url[1])

                # Check crawl-delay
                sql = 'SELECT (crawl_delay, last_accessed_time) FROM crawldb.site WHERE id = %s'
                cur.execute(sql, (url[1]))
                delay_time = cur.fetchall()

                lat = delay_time[1]
                print(lat)
                delay = delay_time[0]
                print(delay)

                if delay_time[1] <= (int(time.time()) - delay_time[0]):

                    # Update page_type_code
                    sql = 'UPDATE crawldb.page SET page_type_code = NULL WHERE url = %s;'
                    cur.execute(sql, (url[0],))
                    frontier_url = url[0]



            # Get allowed domains
            #sql = "SELECT id FROM crawldb.site WHERE last_accessed_time <= (%s - crawl_delay)"
            #cur.execute(sql, (int(time.time()),))
            #sitesite_id = cur.fetchall()


    


            cur.close()


            return frontier_url
        
        except Exception as error:
            print("Error geting URLs from frontier: ", error)
            return -1

        finally:
            if conn is not None:
                conn.close()

# Insert domain/check domain index
def write_domain_to_site(domain):
    with lock:
        index = -1
        flag = -1 # to ni ok!
        disallow = []
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True
            cur =conn.cursor()

            # Check if domain exists, if so get site_id
            try:
                sql = 'SELECT id FROM crawldb.site WHERE domain = %s;'
                cur.execute(sql, (domain,))
                index = cur.fetchone()[0]
                if index != -1:
                    flag = 1

                sql = 'SELECT disallow FROM crawldb.site WHERE domain = %s;'
                cur.execute(sql, (domain,))
                disallow = cur.fetchall()
                

            except Exception as e:
                conn.rollback()

            if index == -1:
                try:
                    # Add new site
                    sql = 'INSERT INTO crawldb.site (domain) VALUES (%s);'
                    cur.execute(sql, (domain,))
                    # Get site_id
                    sql = 'SELECT id FROM crawldb.site WHERE domain = %s;'
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
def write_url_to_frontier(number, links, site_ids):
    with lock:
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            index = -1
            tag = 'FRONTIER'

            cur =conn.cursor()

            if number == 1:
                # Check if url exists in db
                try:
                    sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                    cur.execute(sql, (links,))
                    index = cur.fetchone()[0]

                except Exception as e:
                    conn.rollback()

                if index == -1:
                    try:
                        # Add new url to frontier
                        sql = 'INSERT INTO crawldb.page (url, site_id, page_type_code) VALUES (%s, %s, %s);'
                        cur.execute(sql, (links, site_ids, tag,))

                        # Get page id
                        sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                        cur.execute(sql, (links,))
                        index = cur.fetchone()[0]

                        # Add connection to link table
                        sql = 'INSERT INTO crawldb.link (from_page, to_page) VALUES (%s,%s)'
                        cur.execute(sql, (index, index))

                    except Exception as e:
                        print(e)
                        print('failed to log link')
                        conn.rollback()

            else:

                for link in links:
                    i = links.index(link)
                    # Check if url exists in db
                    try:
                        sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                        cur.execute(sql, (link,))
                        index = cur.fetchone()[0]

                    except Exception as e:
                        conn.rollback()

                    if index == -1:
                        try:
                            # Add new url to frontier
                            sql = 'INSERT INTO crawldb.page (url, site_id, page_type_code) VALUES (%s, %s, %s);'
                            cur.execute(sql, (link, site_ids[i], tag,))

                            # Get page id
                            sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                            cur.execute(sql, (link,))
                            index = cur.fetchone()[0]

                            # Add connection to link table
                            sql = 'INSERT INTO crawldb.link (from_page, to_page) VALUES (%s,%s)'
                            cur.execute(sql, (index, index))

                        except Exception as e:
                            print(e)
                            print('failed to log link')
                            conn.rollback()
                    i = i + 1

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
                        hash = %s WHERE url = %s;'''
                        cur.execute(sql, (page_type_code, html_content, http_status_code, accessed_time, hash, url,))
                        
                        # Get page id
                        sql = 'SELECT id FROM crawldb.page WHERE page_hash = %s;'
                        cur.execute(sql, (hash,))
                        id = cur.fetchone()[0]

                        # Update last accessed time for domain
                        sql = 'UPDATE crawldb.site SET last_accessed_time = %s WHERE site_id = %s;'
                        cur.execute(sql, (last_accessed_time, site_id,))

                        print('Logged into page: '+ url)
                        print('ID: ', id)

                    except Exception as e:
                        conn.rollback()
                
                if index != -1:
                    try:
                        # Update row (as DUPLICATE)
                        sql = 'UPDATE crawldb.page SET page_type_code = %s, accessed_time = %s WHERE url = %s;'
                        cur.execute(sql, (tag_duplicate, accessed_time, url,))
                        
                        # Get page id
                        sql = 'SELECT id FROM crawldb.page WHERE page_hash = %s;'
                        cur.execute(sql, (hash,))
                        id = cur.fetchone()[0]

                        # Update last accessed time for domain
                        sql = 'UPDATE crawldb.page SET last_accessed_time = %s WHERE site_id = %s;'
                        cur.execute(sql, (last_accessed_time, site_id,))

                        print('Logged into page as DUPLICATE: '+ url)
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
                sql = 'UPDATE crawldb.page (page_type_code, http_status_code, accessed_time) VALUES (%s, %s, %s) WHERE url = %s;'
                cur.execute(sql, (page_type_code, http_status_code, accessed_time, url,))
                

                # Get id and site_id
                sql = 'SELECT (id, site_id) FROM crawldb.page WHERE url = %s;'
                cur.execute(sql, (url,))
                page_id, site_id = cur.fetchall()
                print('RETURNING page_id SITE id: ', page_id, site_id)


                # Write page_data
                sql = 'INSERT INTO crawldb.page_data (page_id, data_type_code) VALUES (%s,%s)'
                cur.execute(sql, (page_id, page_data_type,))

                # Update last accessed time for domain
                sql = 'UPDATE crawldb.site SET last_accessed_time = %s WHERE site_id = %s;'
                cur.execute(sql, (last_accessed_time, site_id,))

           
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed: ", error)

            finally:
                if conn is not None:
                    conn.close()


# Write image
def write_img(number,new_urls, site_ids, page_type_code, content_type, accessed_time):
    with lock:
#add number"""""""""""
        index = -1
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()

            if number == 1:
                try:
                    sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                    cur.execute(sql, (new_urls,))
                    index = cur.fetchone()[0]

                   # # Update site
                    #sql = 'UPDATE last_accessed_time FROM crawldb.site WHERE id = %s'
                    #cur.execute(sql, (line[1],))

                except Exception as e:
                    conn.rollback()

                if index == -1:
                    try:
                        # New image to page
                        sql = 'INSERT INTO crawldb.page (url, site_id, page_type_code, accessed_time) VALUES (%s, %s, %s, %s);'
                        cur.execute(sql, (new_urls, site_ids, page_type_code, accessed_time,))
                        
                        # Get id
                        sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                        cur.execute(sql, (new_urls,))
                        page_id = cur.fetchone()[0]

                        # Add new image to image
                        sql = 'INSERT INTO crawldb.image (page_id, content_type, accessed_time) VALUES (%s, %s, %s)'
                        cur.execute(sql, (page_id, content_type, accessed_time))

                    except Exception as e:
                        conn.rollback()


            else:

                for link in new_urls:
                    i = new_urls.index(link)
                        # Check if image url exists
                    try:
                        sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                        cur.execute(sql, (link,))
                        index = cur.fetchone()[0]

                   # # Update site
                    #sql = 'UPDATE last_accessed_time FROM crawldb.site WHERE id = %s'
                    #cur.execute(sql, (line[1],))

                    except Exception as e:
                        conn.rollback()

                    if index == -1:
                        try:
                            # New image to page
                            sql = 'INSERT INTO crawldb.page (url, site_id, page_type_code, accessed_time) VALUES (%s, %s, %s, %s);'
                            cur.execute(sql, (link, site_ids[i], page_type_code, accessed_time,))
                        
                            # Get id
                            sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                            cur.execute(sql, (link,))
                            page_id = cur.fetchone()[0]

                            # Add new image to image
                            sql = 'INSERT INTO crawldb.image (page_id, content_type, accessed_time) VALUES (%s, %s, %s)'
                            cur.execute(sql, (page_id, content_type, accessed_time))

                       # # Update site
                       # sql = 'UPDATE last_accessed_time FROM crawldb.site WHERE id = %s'
                        #cur.execute(sql, (line[1],))

                        except Exception as e:
                            conn.rollback()

                    i = i + 1

            cur.close()

        finally:
            if conn is not None:
                conn.close()