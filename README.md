## Kafka infrastructure project

This is an infrastructure project to primarily showcase Apache Kafka. It's originated
from a proposed system design and a proposed practical coding problem for a real time
fraud detection system, for educational purposes. Be warned that the design or code were
not used in a real interview or project.

### Kafka design

This is the Kafka design of the practical part of the exercise, and what's inside this
repository:

![kafka design](kafkadesign.png)

### High level design

System design solution for the teorical part of the exercise:

![high level design](highleveldesign.png)

### Data model

Data model solution for the theorical part:

![data model](datamodel.png)

### How to run this project

First, make sure you have `Docker` and `docker compose` installed on your machine. Then
run this command:

```bash
make u
```

This command will run all the containers necessary for the project. Take a look at the
logs of the applications. If you wish to see the topics in AKHQ (a graphical user interface)
access http://localhost:8080/. Hit `cmd/ctrl+c` in your terminal if you wish to stop the
containers. To run them in the background:

```make
make ud
```
