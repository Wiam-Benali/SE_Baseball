from database.DB_connect import DBConnect
from model.team import Team


class DAO:
    @staticmethod
    def read_anni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT distinct year 
                    FROM team
                     WHERE YEAR >= 1980"""

        cursor.execute(query)

        for row in cursor:
            result.append(row['year'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_team(anno):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT distinct team_code, name 
                        FROM team
                        WHERE YEAR = %s"""

        cursor.execute(query,(anno,))

        for row in cursor:
            result[row['team_code']]= Team(row['team_code'],row['name'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_salary_team(anno):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT s.team_code, SUM(s.salary) AS tot_salary
                    FROM salary s
                    WHERE s.year = %s
                    GROUP BY s.team_id"""

        cursor.execute(query,(anno,))

        for row in cursor:
            result[row['team_code']]= row['tot_salary']

        cursor.close()
        conn.close()
        return result