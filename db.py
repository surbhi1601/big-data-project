import pymysql.cursors
import genpass

class Database(object):
    def __init__(self):
        self.host = "localhost"
        self.usrnme = "root"
        self.pswrd = ""
        self.dbnme = "twitter_analysis"
        self.connection = pymysql.connect(host=self.host,
                             user=self.usrnme,
                             password=self.pswrd,
                             db=self.dbnme,
                             cursorclass=pymysql.cursors.DictCursor)

    def con_auth(self, user_name, user_pass):
        with self.connection.cursor() as cursor:
            com = "SELECT * FROM users WHERE username='"+user_name+"'"
            cursor.execute(com)
            check = cursor.fetchone()
        self.connection.commit()
        try:
            userpass = check["password"]
            if genpass.check_password_hash(userpass, user_pass):
                return check

        except:
            return None

    def check_id(self, unique_id):
        with self.connection.cursor() as cursor:
            com = "SELECT * FROM sentiment_search WHERE unique_id='"+unique_id+"'"
            try:
                cursor.execute(com)
                check = cursor.fetchone()
            except:
                return None
            self.connection.commit()
        return check

    def insertid(self, unique_id, username):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO sentiment_search VALUES('"+unique_id+"', '"+username+"')"
            cursor.execute(sql)

    def register_user(self, name, contact, email, username, password):
        with self.connection.cursor() as cursor:
            gen_hash = genpass.User(username, password)
            password = gen_hash.pw_hash
            sql = "INSERT INTO users VALUES('"+username+"', '"+name+"', '"+contact+"', '"+email+"', '"+password+"')"
            cursor.execute(sql)
            self.connection.commit()
