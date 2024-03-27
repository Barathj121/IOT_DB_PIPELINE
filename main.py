from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

DATABASE_URL = "dbname=aws_invoice user=aws_invoice_user password=oFsKPV03cSTIvRFwmkEiiJhnc99dNhxp host=dpg-cnu1hgda73kc73f5966g-a.singapore-postgres.render.com port=5432"


#origins = ['http://localhost:8000','http://192.168.137.1:8000']

# Allow CORS for all origins during development (replace "*" with your actual frontend URL in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class Sensor(BaseModel):
    value: float

class Alert(BaseModel):
    lat: float
    lng: float
    homeLat: float
    homeLng: float
    userId: int

@app.post("/")
async def root():
    return {"message": "Hello World"}

@app.post("/sensor")
async def create_sensor_data(sensor: Sensor):
    conn = None
    try:
        # Connect to your postgres DB
        conn=psycopg2.connect(DATABASE_URL)

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

@app.post("/alert")
async def create_alert(alert: Alert):
    conn = None
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(DATABASE_URL)

        # Open a cursor to perform database operations
        cur = conn.cursor()
        now = datetime.now()

        # Insert alert data into the table
        cur.execute(
            """
            INSERT INTO iot_project (lat, lng, homeLat, homeLng, userId)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (alert.lat, alert.lng, alert.homeLat, alert.homeLng, alert.userId, now)
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

@app.get("/latest")
async def get_latest_alert():
    conn = None
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(DATABASE_URL)

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Retrieve the most recently updated row
        cur.execute(
            """
            SELECT * FROM iot_project
            ORDER BY datetime DESC
            LIMIT 1
            """
        )

        # Fetch the result
        result = cur.fetchone()

        # Return the result
        return {"status": "success", "data": result}

    except (Exception, psycopg2.Error) as error:
        return {"status": "error", "detail": str(error)}

    finally:
        # Close communication with the database
        if conn:
            cur.close()
            conn.close()