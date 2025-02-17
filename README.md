## Kafka infrastructure project

This is an infrastructure project to primarily showcase Apache Kafka. It's originated
from a proposed system design and basic coding solution for a real time fraud detection
system, for educational purposes. Be warned that the solution was not used in a real
interview or project.

### High level design

System design from the teorical part of the exercise:

![high level design](highleveldesign.png)

### Data model

Data model from the theorical part:

![data model](datamodel.png)

### Kafka design

This is the Kafka design of the practical part of the exercise, and what's inside this
repository:

![kafka design](kafkadesign.png)

### Technology decisions

Here we use:

- `aiokafka` to create asynchronous producers and consumers;
- `kafka-python` client to administrate Kafka (`aiokafka` does not provide it);
- `pydantic` to define models with types and validation;
- `fastavro` for data serialization for Kafka messages;
- AKHQ as a GUI tool for Kafka;
- Ruff as linting/formatting (faster than black/flake8/isort and simplified tooling).
