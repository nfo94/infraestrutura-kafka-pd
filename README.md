## Kafka infrastructure project

This is an infrastructure project to primarily showcase Apache Kafka. It's originated
from a proposed system design for a real time fraud detection system, for educational
purposes. Be warned that the solution was not used in a real interview or project.

### High level design

![high level design](highleveldesign.png)

### Data model

![data model](datamodel.png)

### Kafka design

![kafka design](kafkadesign.png)

### Technology decisions

Here we use:

- `aiokafka` to create asynchronous producers and consumers;
- `kafka-python` client to administrate Kafka (`aiokafka` does not provide it);
- `pydantic` to define models with types and validation;
- `fastavro` for data serialization for Kafka messages;
- AKHQ as a GUI tool for Kafka;
- `mimesis` to generate Kafka messages with a schema;
- Ruff as linting/formatting (faster than black/flake8/isort and simplified tooling).
