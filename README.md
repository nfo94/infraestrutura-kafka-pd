## Kafka infrastructure project

This is an infrastructure project to primarily showcase Apache Kafka.

### High level design


### Design decisions


### Technology decisions

Here we use:

- `aiokafka` to create asynchronous producers and consumers;
- `kafka-python` client to administrate Kafka (`aiokafka` does not provide it);
- `pydantic` to define models with types and validation;
- `fastavro` for data serialization for Kafka messages;
- AKHQ as a GUI tool for Kafka;
- `mimesis` to generate Kafka messages with a schema;
- Ruff as linting/formatting (faster than black/flake8/isort and simplified tooling).
