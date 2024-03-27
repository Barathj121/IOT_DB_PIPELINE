from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['http://localhost:8000','http://192.168.137.1:8000']

# Allow CORS for all origins during development (replace "*" with your actual frontend URL in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class Sensor(BaseModel):
    value: float

@app.post("/")
async def root():
    return {"message": "Hello World"}

@app.post("/sensor")
async def create_sensor_data(sensor: Sensor):
    conn = None
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="BARATHJP",
            host="localhost",
            port="5432"
        )

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Get current datetime
        now = datetime.now()

        # Insert sensor data and current datetime into the table
        cur.execute(
            """
            INSERT INTO "IOT_TEST" (datetime, sensor_value)
            VALUES (%s, %s)
            """,
            (now, sensor.value)
        )

        # Commit the changes
        conn.commit()

        return {"status": "success"}

    except (Exception, psycopg2.Error) as error:
        return {"status": "error", "detail": str(error)}

    finally:
        # Close communication with the database
        if conn:
            cur.close()
            conn.close()