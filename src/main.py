from neo4j import GraphDatabase
import json
from pathlib import Path
import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

file_path = Path("secrets/Neo4j-6dcf787b-Created-2023-07-08.json")

with open(file_path, 'r') as myfile:
    neo4j_creds = json.load(myfile)

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = neo4j_creds["NEO4J_URI"]
AUTH = (neo4j_creds["NEO4J_USERNAME"], neo4j_creds["NEO4J_PASSWORD"])

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    # Get the name of all 42 year-olds
    records, summary, keys = driver.execute_query(
        "MATCH (n:Category) RETURN n LIMIT 25;"
    )

    # Loop through results and do something with them
    for cat in records:
        logging.info(cat)

    # Summary information
    logging.info("The query `{query}` returned {records_count} records in {time} ms.".format(
        query=summary.query, records_count=len(records),
        time=summary.result_available_after,
    ))