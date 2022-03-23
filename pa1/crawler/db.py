import threading
import psycopg2
import time


# Set threading lock for database
lock = threading.Lock()

# Get frontier size
def get_url_from_frontier():
    with lock:
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()
            # TESTRAJ
            sql = "SELECT COUNT (ALL crawldb.page WHERE page_type_code = 'FRONTIER')"
            cur.execute(sql, )
            frontier_size = cur.fetchall()
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

            # Get url from frontier
            sql = '''SELECT * crawldb.page (url, site_id) WHERE page_type_code = 'FRONTIER' 
                    JOIN crawldb.site ON (site_id = id) WHERE 
                    (site.last_accessed_time <=  (%s - site.crawl_delay))
                    ORDER BY page.id ASC LIMIT 1'''
            
            cur.execute(sql, (int(time.time()),))
            frontier_url, site_id = cur.fetchall()
            

            # Update page_type_code
            sql = '''UPDATE crawldb.page SET page_type_code = NULL WHERE page.url == %s'''
            cur.execute(sql, (frontier_url,))
            


            # Update page_type_code
            sql = '''UPDATE crawldb.site SET crawldb.last_accessed_time = %s WHERE site_id == %s'''
            cur.execute(sql, (int(time.time()),site_id))

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

    return

# Insert URLs to frontier (multiple urls)
def write_url_to_frontier(urls, siteid):
    with lock:
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            tag = 'FRONTIER'

            cur =conn.cursor()
            sql = ""
            cur.execute(sql, (urls, siteid, tag))
            frontier_url = cur.fetchall()
            cur.close()
            return frontier_url
        
        except Exception as error:
            print("Error geting URLs to frontier: ", error)
            return -1

        finally:
            if conn is not None:
                conn.close()




def update_page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, hash):
    # NI OK, POSODOBIT MORE FRONTIR (uporabi metodo update)
        with lock:
            try:
                conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword") # connect to db
                conn.autocommit = True

                cur =conn.cursor()
                
                sql = "INSERT INTO crawldb.page (site_id, page_type_code, url, html_content, http_status_code, accessed_time, page_hash) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;"
                cur.execute(sql, (site_id, page_type_code, url, html_content, http_status_code, accessed_time, hash)) #write to db
                id = cur.fetchone()[0]

                print('Logged into page: '+ url)
                print('ID: ', id)
            
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed: ", error)

            finally:
                if conn is not None:
                    conn.close()


def insert_site(id, domain, robots_content, sitemap_content, ip_address, last_accessed_time, crawl_delay):
        with lock:
            try:
                conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword") # connect to db
                conn.autocommit = True

                cur =conn.cursor()
                
                sql = "INSERT INTO crawldb.site (domain, robots_content, sitemap_content, ip_address, last_accessed_time, crawl_delay) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;"
                cur.execute(sql, (domain, robots_content, sitemap_content, ip_address, last_accessed_time, crawl_delay)) #write to db
                id = cur.fetchone()[0]

                print('Logged into site: '+ domain)
                print('ID: ', id)
            
                cur.close()

            except (Exception, psycopg2.DatabaseError) as error:
                print("Failed: ", error)

            finally:
                if conn is not None:
                    conn.close()