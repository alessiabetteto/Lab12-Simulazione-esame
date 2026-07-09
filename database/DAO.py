from database.DB_connect import DBConnect
from model.actor import Actor
from model.arco import Arco


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct (avg_rating )
                    from ratings r
                    order by avg_rating asc"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(rat1, rat2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT n.* FROM names n, role_mapping rm, ratings r
                WHERE n.id = rm.name_id 
                AND rm.movie_id = r.movie_id 
                AND r.avg_rating BETWEEN %s AND %s
                AND n.date_of_birth IS NOT NULL"""

        cursor.execute(query, (rat1,rat2))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(rat1, rat2, idMapActor):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.id as a1, n1.id as a2, SUM( cast((REPLACE(m.worlwide_gross_income, '$ ', '')) AS DECIMAL ) ) AS peso 
                    from role_mapping rm ,role_mapping rm1,  ratings r, names n, names n1, movie m
                    where rm.movie_id = rm1.movie_id  
                    and rm.name_id < rm1.name_id 
                    and rm.movie_id = r.movie_id 
                    and rm.name_id = n.id 
                    and rm1.name_id = n1.id  
                    and rm.movie_id = m.id 
                    and rm1.movie_id = m.id
                    and r.avg_rating between  %s and %s
                    AND m.worlwide_gross_income IS NOT NULL
                    and n.date_of_birth is not null  and n1.date_of_birth is not null 
                    group by n.id, n.name, n.height, n.date_of_birth, n.known_for_movies,
                        n1.id, n1.name, n1.height, n1.date_of_birth, n1.known_for_movies 
                    order by peso desc"""

        cursor.execute(query, (rat1, rat2))

        for row in cursor:
            results.append(Arco(idMapActor[row["a1"]], idMapActor[row["a2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results
