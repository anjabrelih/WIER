import threading
import psycopg2
import time


# Set threading lock for database
lock = threading.Lock()

# Get crawl delay and site id
def get_crawl_delay_siteid(domain):
    with lock:
        crawl_delay = 5
        site_id = 0
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()
            
            sql = 'SELECT crawl_delay FROM crawldb.site WHERE domain = %s;'
            cur.execute(sql, (domain,))
            if cur.rowcount != 0:
                crawl_delay = cur.fetchone()[0]

            # Get site id
            sql1 = "SELECT id FROM crawldb.site WHERE domain = %s"
            cur.execute(sql1, (domain,))
            if cur.rowcount != 0:
                site_id = cur.fetchone()[0]

            cur.close()
            return crawl_delay, site_id
        
        except Exception as error:
            print("Error geting crawl delay: ", error)
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



# Get URL from frontier (one at the time)
def get_url_from_frontier():
    with lock:
        
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()

            # Get urls from frontier
            sql = "SELECT url FROM crawldb.page WHERE page_type_code = 'FRONTIER' ORDER BY id ASC LIMIT 1"
            cur.execute(sql, )
            if cur.rowcount != 0:
                url = cur.fetchone()[0]

            # Get site id
            sql1 = "SELECT site_id FROM crawldb.page WHERE url = %s"
            cur.execute(sql1, (url,))
            site_id = cur.fetchone()[0]


            # Update page_type_code
            sql2 = 'UPDATE crawldb.page SET page_type_code = NULL WHERE url = %s;'
            cur.execute(sql2, (url,))

            # Get crawl delay
            sql3 = "SELECT crawl_delay FROM crawldb.site WHERE id = %s"
            cur.execute(sql3, (site_id,))
            crawl_delay = cur.fetchone()[0]

            # Get last access time
            sql4 = "SELECT last_accessed_time FROM crawldb.site WHERE id = %s"
            cur.execute(sql4, (site_id,))
            last_accessed_time = cur.fetchone()[0]
                

            cur.close()


            return url, site_id, crawl_delay, last_accessed_time
        
        except Exception as error:
            print("Error geting URL from frontier: ", error)
            return -1, -1, -1, -1

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
                sql = 'SELECT id FROM crawldb.site WHERE domain = %s;'
                cur.execute(sql, (domain,))
                if cur.rowcount != 0:
                    index = cur.fetchone()[0]
                    if index != -1:
                        flag = 1

                sql1 = 'SELECT disallow FROM crawldb.site WHERE domain = %s;'
                cur.execute(sql1, (domain,))
                if cur.rowcount != 0:
                    disallow = cur.fetchall()
                

            except Exception as e:
                print("Error getting site id and disallow (site doesnt exist): ", e)
                conn.rollback()

            if index == -1:
                try:
                    # Add new site
                    sql2 = 'INSERT INTO crawldb.site (domain) VALUES (%s);'
                    cur.execute(sql2, (domain,))
                    # Get site_id
                    sql3 = 'SELECT id FROM crawldb.site WHERE domain = %s;'
                    cur.execute(sql3, (domain,))
                    index = cur.fetchone()[0]

                except Exception as e:
                    print("Error writing new site:", e)
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
def update_site(siteid, domain, robots_content, sitemap_content, ip_address, crawl_delay, last_accessed_time, disallow):
    with lock:
            try:
                conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
                conn.autocommit = True

                cur =conn.cursor()
                
                sql = "UPDATE crawldb.site SET robots_content = %s,sitemap_content=%s,ip_address = %s,crawl_delay = %s,last_accessed_time = %s,disallow=%s WHERE id=%s"
                cur.execute(sql, (robots_content, sitemap_content, ip_address, crawl_delay, last_accessed_time, disallow, siteid,))


                sql1 = "SELECT id FROM crawldb.site WHERE domain = %s;"
                cur.execute(sql1, (domain,))
                id = cur.fetchone()[0]

                print('Updated site: '+ domain)
                print('ID: ', id)
            
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed to update site: ", error)

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
                    if cur.rowcount != 0:
                        index = cur.fetchone()[0]

                except Exception as e:
                    print("Error writing URL to frontir: ", e)
                    conn.rollback()

                if index == -1:
                    try:
                        # Add new url to frontier
                        sql1 = 'INSERT INTO crawldb.page (url, site_id, page_type_code) VALUES (%s, %s, %s);'
                        cur.execute(sql1, (links, site_ids, tag,))

                        # Get page id
                        sql2 = 'SELECT id FROM crawldb.page WHERE url = %s;'
                        cur.execute(sql2, (links,))
                        index = cur.fetchone()[0]

                    except Exception as e:
                        print("Error writing to frontir", e)
                        conn.rollback()


            else:

                for link in links:
                    i = links.index(link)
                    index = -1
                    # Check if url exists in db
                    try:
                        sql1 = 'SELECT id FROM crawldb.page WHERE url = %s;'
                        cur.execute(sql1, (link,))
                        if cur.rowcount != 0:
                            index = cur.fetchone()[0]

                        print(index)

                    except Exception as e:
                        conn.rollback()

                    if index == -1:
                        try:
                            # Add new url to frontier
                            sql2 = 'INSERT INTO crawldb.page (url, site_id, page_type_code) VALUES (%s, %s, %s);'
                            cur.execute(sql2, (link, site_ids[i], tag,))

                            # Get page id
                            sql3 = 'SELECT id FROM crawldb.page WHERE url = %s;'
                            cur.execute(sql3, (link,))
                            index = cur.fetchone()[0]


                        except Exception as e:
                            conn.rollback()
                            print('failed to log link')
                            print(e)
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
                    if cur.rowcount != 0:
                        #list(cur.fetchone())[0]
                        index = cur.fetchone()[0]

                except Exception as e:
                    print(e)
                    conn.rollback()

                if index == -1:
                    try:
                        # Update row (as HTML) , html_content = %s, accessed_time = %s, hash = %s
                        sql1 = "UPDATE crawldb.page SET page_type_code = %s,html_content=%s,http_status_code = %s,accessed_time = %s,page_hash = %s WHERE url=%s RETURNING id;"
                        cur.execute(sql1, (page_type_code, html_content, http_status_code, accessed_time, hash, url,))
                        id = cur.fetchone()[0]
                        print('Logged content to page:' +id)

                        # Update last accessed time for domain
                        sql3 = 'UPDATE crawldb.site SET last_accessed_time = %s WHERE id = %s;'
                        cur.execute(sql3, (last_accessed_time, site_id,))

                        print('Logged into page: '+ url)
                        print('ID: ', id) #Popravi, ker ni -1

                    except Exception as e:
                        print("Failed to update page:" +e)
                        
                
                if index != -1:
                    try:
                        # Update row (as DUPLICATE)
                        sql4 = 'UPDATE crawldb.page SET page_type_code = %s, accessed_time = %s WHERE url = %s RETURNING id;'
                        cur.execute(sql4, (tag_duplicate, accessed_time, url,))
                        id = cur.fetchone()[0]                 

                        # Link duplicate
                        sql6 = 'INSERT INTO crawldb.link (from_page, to_page) VALUES (%s,%s)'
                        cur.execute(sql6, (index, id))

                        # Update last accessed time for domain
                        sql7 = 'UPDATE crawldb.page SET last_accessed_time = %s WHERE site_id = %s;'
                        cur.execute(sql7, (last_accessed_time, site_id,))

                        print('Logged into page as DUPLICATE: '+ url)
                        print('ID: ', id)

                    except Exception as e:
                        print(e)
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
                sql = 'UPDATE crawldb.page (page_type_code, http_status_code, accessed_time) VALUES (%s, %s, %s) WHERE url = %s RETURNING id;'
                cur.execute(sql, (page_type_code, http_status_code, accessed_time, url,))
                page_id = cur.fetchone()[0]
                

                # Get id and site_id
                #sql1 = 'SELECT id FROM crawldb.page WHERE url = %s;'
                #cur.execute(sql1, (url,))
                #page_id = cur.fetchone()[0]
                

                # Get id and site_id
                sql2 = 'SELECT site_id FROM crawldb.page WHERE url = %s;'
                cur.execute(sql2, (url,))
                site_id = cur.fetchone()[0]
                print('RETURNING page_id & SITE id from DOCUMENT insert: ', page_id, site_id)

                # Write page_data
                sql3 = 'INSERT INTO crawldb.page_data (page_id, data_type_code) VALUES (%s,%s)'
                cur.execute(sql3, (page_id, page_data_type,))

                # Update last accessed time for domain
                sql4 = 'UPDATE crawldb.site SET last_accessed_time = %s WHERE site_id = %s;'
                cur.execute(sql4, (last_accessed_time, site_id,))

           
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed do write data: ", error)

            finally:
                if conn is not None:
                    conn.close()


# Write image
def write_img(number,new_urls, site_ids, page_type_code, content_type, accessed_time):
    with lock:

        index = -1
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()

            if number == 1:
                try:
                    sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                    cur.execute(sql, (new_urls,))
                    if cur.rowcount != 0:
                        index = cur.fetchone()[0]

                   # # Update site
                    #sql = 'UPDATE last_accessed_time FROM crawldb.site WHERE id = %s'
                    #cur.execute(sql, (line[1],))

                except Exception as e:
                    print(e)
                    conn.rollback()

                if index == -1:
                    try:
                        # New image to page
                        sql1 = 'INSERT INTO crawldb.page (url, site_id, page_type_code, accessed_time) VALUES (%s, %s, %s, %s) RETURNING id;'
                        cur.execute(sql1, (new_urls, site_ids, page_type_code, accessed_time,))
                        page_id = cur.fetchone()[0]
                        
                        # Get id
                        #sql2 = 'SELECT id FROM crawldb.page WHERE url = %s;'
                        #cur.execute(sql2, (new_urls,))
                        #page_id = cur.fetchone()[0]

                        # Add new image to image
                        sql3 = 'INSERT INTO crawldb.image (page_id, content_type, accessed_time) VALUES (%s, %s, %s)'
                        cur.execute(sql3, (page_id, content_type, accessed_time))

                    except Exception as e:
                        print(e)
                        conn.rollback()


            else:

                for link in new_urls:
                    i = new_urls.index(link)
                        # Check if image url exists
                    try:
                        sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                        cur.execute(sql, (link,))
                        if cur.rowcount != 0:
                            index = cur.fetchone()[0]

                   # # Update site
                    #sql = 'UPDATE last_accessed_time FROM crawldb.site WHERE id = %s'
                    #cur.execute(sql, (line[1],))

                    except Exception as e:
                        print(e)
                        conn.rollback()

                    if index == -1:
                        try:
                            # New image to page
                            sql1 = 'INSERT INTO crawldb.page (url, site_id, page_type_code, accessed_time) VALUES (%s, %s, %s, %s) RETURNING id;'
                            cur.execute(sql1, (link, site_ids[i], page_type_code, accessed_time,))
                            page_id = cur.fetchone()[0]
                        
                            # Get id
                            #sql2 = 'SELECT id FROM crawldb.page WHERE url = %s;'
                            #cur.execute(sql2, (link,))
                            #page_id = cur.fetchone()[0]

                            # Add new image to image
                            sql3 = 'INSERT INTO crawldb.image (page_id, content_type, accessed_time) VALUES (%s, %s, %s)'
                            cur.execute(sql3, (page_id, content_type, accessed_time))

                       # # Update site
                       # sql = 'UPDATE last_accessed_time FROM crawldb.site WHERE id = %s'
                        #cur.execute(sql, (line[1],))

                        except Exception as e:
                            print(e)
                            conn.rollback()

                    i = i + 1

            cur.close()

        finally:
            if conn is not None:
                conn.close()