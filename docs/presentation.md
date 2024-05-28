% VitalVue
% João Alves, Luís Góis, Marco Silva
% \today

---

# Slide 1: Objectives

- The key points of this project was to develop a Hospital Management System (HMS) 
that will streamline hospital operations by managing patient care,
scheduling, billing, and resource allocation.

---

# Slide 2: Technologies Used

::: incremental

1. Python - Backend development and general programming
2. Flask - Web framework for building RESTful APIs
3. PostgreSQL - Database management system
4. Postman - API testing tool
5. Docker - Containerization tool

:::

---

# Slide 3: Project Arquitecture

![Entity Relation Diagram](/assets/er-diagram.png)

- This diagram shows the relationship between the different entities in the database. 
Every relationship is represented by a line that connects the entitites and various modifiers that show the cardinality of the relationship.


---

# Slide 4: Implementation Example
```python
@app.route('/user/', methods=['PUT'])
def user_authentication():
    # 1. get request payload
    payload = request.get_json()

    # 2. query statement and key values
    statement = """
                SELECT 
                    u.id, 
                    u.type
                FROM 
                    vital_vue_user AS u
                WHERE 
                    u.username = %s 
                    AND u.password = %s;
                """
    key_values = ['username', 'password']

    # 3. validate payload
    response = validate_payload(payload, key_values)
    if response:
        return jsonify(response)

    # 5. get input values from payload
    payload['password'] = hash_password(payload['password'])
    input_values = [payload[key] for key in key_values]

    # 6. connect to database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(statement, input_values)
        rows = cursor.fetchall()

        if rows:
            row = rows[0]
            access_token = create_access_token(identity = row[0],
                                               additional_claims = {
                                                   'type': row[1]
                                                   })
            response = {'status': StatusCode.SUCCESS.value,
                        'results': access_token}
        else:
            response = {'status': StatusCode.API_ERROR.value, 
                        'results': 'Invalid authentication credentials'}

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f'{endpoint} - error: {error}')
        response = {'status': StatusCode.INTERNAL_ERROR.value,
                    'error': str(error)}

    finally:
        if conn is not None:
            conn.close()

    return jsonify(response)
```

---

# Slide 5: Uses of Postman

- Postman is a tool that allows us to test our APIs and see the responses that we get from them.
by associating the endpoints with the methods we can test the different functionalities of the API.

- For example, the same functions thar are signaled in the previous slide can be tested in Postman.

```json
"item": [
		{
			"name": "Register Patient",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\r\n    \"id\": 123\r\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://localhost:8080/register/patient",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8080",
					"path": [
						"register",
						"patient"
					]
				}
			},
			"response": []
		},
]
```

---

# Slide 6: Results and benefits

- By using the technologies mentioned before we were able to develop a
  functional Hospital Management System (HMS) that will streamline hospital
  operations by managing patient care, scheduling, billing, and resource
  allocation. Also, the use of Postman allowed us to test the different
  functionalities of the API.

---

# Slide 7: Conclusion

- In conclusion we were able to develop a functional Hospital Management System
  (HMS) by using the technologies mentioned before. and following the directions
  of the project.

---

Thank you for your attention!
