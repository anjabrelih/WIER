import threading
import psycopg2
from sys import getsizeof


# Set threading lock for database
lock = threading.Lock()


# Get URLs from frontier
def get_url_from_frontier(number):
    with lock:
        try:
            conn = psycopg2.connect(host="localhost", user="crawler", password="SecretPassword")
            conn.autocommit = True

            cur =conn.cursor()
            sql = "" ########################################
            cur.execute(sql, (number))
            frontier_url = cur.fetchall()
            cur.close()
            return frontier_url
        
        except Exception as error:
            print("Error geting URLs from frontier: ", error)
            return -1

        finally:
            if conn is not None:
                conn.close()


# Insert URLs to frontier (multiple urls)
def write_url_to_frontier(urls, siteid):
    return''




def insert2page(site_id, page_type_code, url, html_content, http_status_code, accessed_time, hash):
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