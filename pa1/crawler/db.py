import threading
import psycopg2
import time
from general import *


# Set threading lock for database
lock = threading.Lock()


# Update last accessed time
def update_last_accessed_time(site_id, last_accessed_time, site_lock):
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        conn.autocommit = True
        cur =conn.cursor()
        try:
            # Update
            sql2 = "UPDATE crawldb.site SET last_accessed_time = %s WHERE id = %s;"
            cur.execute(sql2, (last_accessed_time,site_id,))
            print("Updated LAT for site")


            sql3 = "UPDATE crawldb.site SET lock = %s WHERE id = %s;"
            cur.execute(sql3, (site_lock, site_id,))
            
            cur.close()
        
        except Exception as error:
            conn.rollback()
            cur.close()
            print("Error geting crawl delay: ", error)

        finally:
            if conn is not None:
                conn.close()


# Get crawl delay, site_id and last accessed time for thread
def get_job_info(url):
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        crawl_delay = 5
        last_accessed_time = 0
        site_lock = 1
        conn.autocommit = True
        cur =conn.cursor()
        try:
                    
            # Get site id
            sql = 'SELECT site_id FROM crawldb.page WHERE url = %s;'
            cur.execute(sql, (url,))
            site_id = cur.fetchone()[0]

            # Get crawl_delay
            sql1 = "SELECT crawl_delay FROM crawldb.site WHERE id = %s"
            cur.execute(sql1, (site_id,))
            if cur.rowcount != 0:
                crawl_delay = cur.fetchone()[0]

            # Get last_accessed_time
            sql2 = "SELECT last_accessed_time FROM crawldb.site WHERE id = %s"
            cur.execute(sql2, (site_id,))
            if cur.rowcount != 0:
                last_accessed_time = cur.fetchone()[0]

            # Update last accessed time - to "lock" the domain
            #sql3 = 'UPDATE crawldb.site SET last_accessed_time = %s WHERE id = %s;'
            #cur.execute(sql3, (int(time.time()), site_id,))

            # Get site lock
            sql4 = 'SELECT lock FROM crawldb.site WHERE id = %s;'
            cur.execute(sql4, (site_id,))
            site_lock = cur.fetchone()[0]

            if site_lock == 0:
                # Lock the domain
                sql5 = 'UPDATE crawldb.site SET lock = %s WHERE id = %s;'
                cur.execute(sql5, (1,site_id,))
            


            cur.close()

            
        except Exception as error:
            print("Error geting crawl delay: ", error)
            conn.rollback()
            cur.close()
            crawl_delay = 5
            site_id = -1
            last_accessed_time = -1

            

        finally:
            if conn is not None:
                conn.close()

        return crawl_delay, site_id, last_accessed_time, site_lock
                


# Get frontier size
def get_frontier_size():
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        conn.autocommit = True
        cur =conn.cursor()
        try:
            frontier_size = 0
                        
            sql = "SELECT COUNT ( * ) FROM crawldb.page WHERE page_type_code = 'FRONTIER';"
            cur.execute(sql, )
            if cur.rowcount != 0:
                frontier_size = cur.fetchone()[0]
            #print("Frontier size: ", frontier_size)
            cur.close()
            #return frontier_size
        
        except Exception as error:
            print("Error geting frontier size: ", error)
            conn.rollback()
            cur.close()
            #return frontier_size

        finally:
            if conn is not None:
                conn.close()    

        return frontier_size



### NOT USED in current version! ###
# Get URL from frontier (one at the time)
def get_url_from_frontier():
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        crawl_delay = 5
        last_accessed_time = int(time.time())
        conn.autocommit = True
        cur =conn.cursor()
        try:
            # Get urls from frontier
            sql = "SELECT url FROM crawldb.page WHERE page_type_code = 'FRONTIER' ORDER BY id ASC LIMIT 1;"
            cur.execute(sql, )
            if cur.rowcount != 0:
                url = cur.fetchone()[0]

            # Get site id
            sql = 'SELECT site_id FROM crawldb.page WHERE url = %s;'
            cur.execute(sql, (url,))
            site_id = cur.fetchone()[0]

            # Get crawl_delay
            sql1 = "SELECT crawl_delay FROM crawldb.site WHERE id = %s"
            cur.execute(sql1, (site_id,))
            if cur.rowcount != 0:
                crawl_delay = cur.fetchone()[0]

            # Get last_accessed_time
            sql2 = "SELECT last_accessed_time FROM crawldb.site WHERE id = %s"
            cur.execute(sql2, (site_id,))
            if cur.rowcount != 0:
                last_accessed_time = cur.fetchone()[0]


            # Update page_type_code
            sql2 = "UPDATE crawldb.page SET page_type_code = NULL WHERE url = %s;"
            cur.execute(sql2, (url,))

            print("Got URL from FRONTIER")
                

            cur.close()

        
        except Exception as error:
            print("Error geting URL from frontier: ", error)
            url = -1
            conn.rollback()
            cur.close()
            

        finally:
            if conn is not None:
                conn.close()

        return url, crawl_delay, site_id, last_accessed_time

# Get one url
def get_url_from_frontier1():
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        url = ""
        conn.autocommit = True
        cur =conn.cursor()
        try:
            # Get urls from frontier
            #sql = "SELECT url FROM crawldb.page WHERE page_type_code = 'FRONTIER' ORDER BY id ASC LIMIT 1;"
            sql = "SELECT url FROM crawldb.page INNER JOIN crawldb.site ON site.id = page.site_id WHERE page.page_type_code = 'FRONTIER' AND site.lock <> 1 ORDER BY page.id ASC LIMIT 1;"
            cur.execute(sql, )
            if cur.rowcount != 0:
                url = cur.fetchone()[0]

            # Update page_type_code
            sql2 = "UPDATE crawldb.page SET page_type_code = NULL WHERE url = %s;"
            cur.execute(sql2, (url,))
        
            print("Got URL from FRONTIER")
                

            cur.close()

        
        except Exception as error:
            print("Error geting URL from frontier: ", error)
            url = -1
            conn.rollback()
            cur.close()
            

        finally:
            if conn is not None:
                conn.close()

        return url


# Insert domain/check domain index
def write_domain_to_site(domain):
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        index = -1
        flag = -1
        robots_content = ''
        conn.autocommit = True
        cur =conn.cursor()
        try:
           
            # Check if domain exists, if so get site_id
            try:
                sql = 'SELECT id FROM crawldb.site WHERE domain = %s;'
                cur.execute(sql, (domain,))
                if cur.rowcount != 0:
                    index = cur.fetchone()[0]
                    if index != -1:
                        flag = 1

                sql1 = 'SELECT robots_content FROM crawldb.site WHERE domain = %s;'
                cur.execute(sql1, (domain,))
                if cur.rowcount != 0:
                    robots_content = cur.fetchall()
                

            except Exception as e:
                print("Error getting site id and robots_content (site doesnt exist): ", e)
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
                    sql4 = 'UPDATE crawldb.site SET lock = %s WHERE id = %s;'
                    cur.execute(sql4, (0,index,))

                except Exception as e:
                    print("Error writing new site:", e)
                    conn.rollback()          


            cur.close()
        
        except Exception as error:
            print("Error getting domain to database/getting domain id: ", error)
            conn.rollback()  
            cur.close()
            

        finally:
            if conn is not None:
                conn.close()
        
        return index, flag, robots_content
            


# Update site with domain content
def update_site(siteid, domain, robots_content, sitemap_content, ip_address, crawl_delay, last_accessed_time):
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        conn.autocommit = True

        cur =conn.cursor()
        try:                

            if robots_content == '':

                sql = "UPDATE crawldb.site SET crawl_delay = %s,last_accessed_time = %s WHERE id=%s"
                cur.execute(sql, (crawl_delay, last_accessed_time, siteid,))

                sql1 = "SELECT id FROM crawldb.site WHERE domain = %s;"
                cur.execute(sql1, (domain,))
                id = cur.fetchone()[0]


            else:                
                sql = "UPDATE crawldb.site SET robots_content = %s,sitemap_content=%s,ip_address = %s,crawl_delay = %s,last_accessed_time = %s WHERE id=%s"
                cur.execute(sql, (robots_content, sitemap_content, ip_address, crawl_delay, last_accessed_time, siteid,))

                sql1 = "SELECT id FROM crawldb.site WHERE domain = %s;"
                cur.execute(sql1, (domain,))
                id = cur.fetchone()[0]

            print('Updated site: ', domain)
            print('Domain ID: ', id)
            
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed to UPDATE SITE", error)
            cur.close()
            conn.rollback()
        
        finally:
            if conn is not None:
                conn.close()

            


# Insert URLs to frontier (multiple urls)
def write_url_to_frontier(number, links, site_ids, start_url):
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        conn.autocommit = True

        index = -1
        tag = 'FRONTIER'

        cur =conn.cursor()
        try:

        
            if number == 1: # if only one url to write
                # Check if url exists in db
                try:
                    sql = 'SELECT id FROM crawldb.page WHERE url = %s;'
                    cur.execute(sql, (links[0],))
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
                        print("New frontier at ID:", index)

                        # Get original site ID
                        sql3 = "SELECT id FROM crawldb.page WHERE url = %s;"
                        cur.execute(sql3, (start_url,))
                        start_id = cur.fetchone()[0]

                        # Write link to link_tree
                        sql4 = "INSERT INTO crawldb.link_tree (from_page, to_page) VALUES (%s,%s)"
                        cur.execute(sql4, (start_id, index,))

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
                            print("New frontier at ID:", index)

                            # Write to link_tree table
                            # Get original site ID
                            sql3 = "SELECT id FROM crawldb.page WHERE url = %s;"
                            cur.execute(sql3, (start_url,))
                            start_id = cur.fetchone()[0]

                            # Write link to link_tree
                            sql4 = "INSERT INTO crawldb.link_tree (from_page, to_page) VALUES (%s,%s)"
                            cur.execute(sql4, (start_id, index,))


                        except Exception as e:
                            conn.rollback()
                            print('failed to log link')
                            print(e)
                    i = i + 1

            cur.close()

        
        except Exception as error:
            print("Error geting URLs to frontier: ", error)
            conn.rollback()
            cur.close()

        finally:
            if conn is not None:
                conn.close()



# Update page
def update_page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, last_accessed_time):
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        conn.autocommit = True

        cur =conn.cursor()
        tag_duplicate = 'DUPLICATE'
        hash =  hashlib.md5((html_content).encode()).hexdigest()
        try:
                    
            # Check if hash exists in db
            sql = 'SELECT id FROM crawldb.page WHERE page_hash = %s;'
            cur.execute(sql, (hash,))
            if cur.rowcount == 0:
                                        
                try:

                    sql1 = "UPDATE crawldb.page SET page_type_code = %s,html_content=%s,http_status_code = %s,accessed_time = %s,page_hash = %s WHERE url=%s RETURNING id;"
                    cur.execute(sql1, (page_type_code, html_content, http_status_code, accessed_time, hash, url,))
                    if cur.rowcount != 0:
                        id = cur.fetchone()[0]
                    print('Logged content to page (db.update_page):', id, "tag: ", page_type_code, " url: ", url)

                except Exception as e:
                    print("Failed to update page:", e)
                    conn.rollback()
                        
                
            else:
                index = cur.fetchone()[0]
                try:
                    # Update row (as DUPLICATE)
                    sql4 = 'UPDATE crawldb.page SET page_type_code = %s, accessed_time = %s WHERE url = %s RETURNING id;'
                    cur.execute(sql4, (tag_duplicate, accessed_time, url,))
                    if cur.rowcount != 0:
                        id_dup = cur.fetchone()[0]
                               

                    print('Logged duplicate:', id_dup, "for page: ", index) 

                    # Link duplicate
                    sql6 = 'INSERT INTO crawldb.link (from_page, to_page) VALUES (%s,%s)'
                    cur.execute(sql6, (index, id_dup))
                    id = id_dup
                    print('Logged duplicate in link table: ', url)

                except Exception as e:
                    print(e)
                    conn.rollback()

            try:
                # Update last accessed time
                sql3 = 'UPDATE crawldb.site SET last_accessed_time = %s, lock = %s WHERE id = %s;'
                cur.execute(sql3, (last_accessed_time, 0, site_id,))

            except Exception as e:
                print(e)
                print("Couldnt update last accessed time in site")
                conn.rollback()

            # Unlock
            sql3 = "UPDATE crawldb.site SET lock = %s WHERE id = %s;"
            cur.execute(sql3, (0, site_id,))
            print("Site lock RELESED")

                
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed updating html page: ", error)
            #conn.rollback()
            cur.close()
            conn.close()

        finally:
            if conn is not None:
                conn.close()

        return id


# Update page after HTML
def update_page1(site_id, page_type_code, url, http_status_code, accessed_time, last_accessed_time):
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        conn.autocommit = True

        cur =conn.cursor()

        try:
            sql1 = "UPDATE crawldb.page SET page_type_code = %s,http_status_code = %s,accessed_time = %s WHERE url=%s RETURNING id;"
            cur.execute(sql1, (page_type_code, http_status_code, accessed_time, url,))
            if cur.rowcount != 0:
                id = cur.fetchone()[0]
            print('Logged HTML page (db.update_page):', id, "tag: ", page_type_code, " url: ", url)

                        
            
            # Update last accessed time
            sql3 = 'UPDATE crawldb.site SET last_accessed_time = %s WHERE id = %s;'
            cur.execute(sql3, (last_accessed_time, site_id,))
            print("UPDATED LAT")

            # Unlock
            sql3 = "UPDATE crawldb.site SET lock = %s WHERE id = %s;"
            cur.execute(sql3, (0, site_id,))
            print("Site lock RELESED")

               
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed updating HTML page: ", error)
            #conn.rollback()
            cur.close()
            conn.close()

        finally:
            if conn is not None:
                conn.close()

        return id

# Write BINARY data
def write_data(page_type_code, url, http_status_code, accessed_time, page_data_type):
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        conn.autocommit = True
        cur =conn.cursor()
        try:                
                
            # Update page
            sql = 'UPDATE crawldb.page SET page_type_code = %s, http_status_code =%s, accessed_time=%s WHERE url = %s RETURNING id;'
            cur.execute(sql, (page_type_code, http_status_code, accessed_time, url,))
            page_id = cur.fetchone()[0]
                               

            # Write page_data
            sql3 = 'INSERT INTO crawldb.page_data (page_id, data_type_code) VALUES (%s,%s)'
            cur.execute(sql3, (page_id, page_data_type,))
            #print('Inserted into page_data table')
            print('RETURNING page_id from DOCUMENT insert: ', page_id)

            #print("Updated BINARY data: ", page_id)
           
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed do write data: ", error)
            conn.rollback()
            cur.close()

        finally:
            if conn is not None:
                conn.close()



# Write image
def write_img(new_urls, site_ids, page_type_code, content_type, accessed_time):
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        conn.autocommit = True

        cur =conn.cursor()
           
        try:


            sql1 = "UPDATE crawldb.page SET page_type_code = %s,accessed_time = %s WHERE url=%s RETURNING id;"
            cur.execute(sql1, (page_type_code, accessed_time, new_urls))
            if cur.rowcount != 0:
                page_id = cur.fetchone()[0]
            print("UPDATED image info to page (image - page_id, site_id)", page_id, site_ids)
    

            # Add new image to image
            sql3 = 'INSERT INTO crawldb.image (page_id, content_type, accessed_time) VALUES (%s, %s, %s)'
            cur.execute(sql3, (page_id, content_type, accessed_time))
            print("Inserted IMAGE to image table")

            cur.close()
                        

        except Exception as e:
            print("Error writing image: ",e)
            conn.rollback()
            cur.close()

        finally:
            if conn is not None:
                conn.close()


# Write unknown BINARY
def write_binary(page_type_code, url, http_status_code, accessed_time):
    with lock:
        conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
        conn.autocommit = True
        cur =conn.cursor()
        try:
                
            # Update page
            sql = 'UPDATE crawldb.page SET page_type_code = %s, http_status_code =%s, accessed_time=%s WHERE url = %s RETURNING id;'
            cur.execute(sql, (page_type_code, http_status_code, accessed_time, url,))
            page_id = cur.fetchone()[0]
            print("WROTE UNKNOW BINARY ", page_id)
                                          
            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Failed do write data: ", error)
            conn.rollback()
            cur.close()

        finally:
            if conn is not None:
                conn.close()
