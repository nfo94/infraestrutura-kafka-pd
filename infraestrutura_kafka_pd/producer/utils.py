from mimesis import Field, Fieldset, Schema
from mimesis.enums import Gender, TimestampFormat
from mimesis.locales import Locale
from models import KafkaMessage


class KafkaMessageFactory:
    """Generates messages to be sent to Kafka."""

    def __init__(self):
        self.field = Field(Locale.EN, seed=0xFF)
        self.fieldset = Fieldset(Locale.EN, seed=0xFF)

    def schema_definition(self) -> KafkaMessage:
        return {
            "pk": self.field("increment"),
            "uid": self.field("uuid"),
            "name": self.field("text.word"),
            "version": self.field("version"),
            "timestamp": self.field("timestamp", fmt=TimestampFormat.POSIX),
            "owner": {
                "email": self.field("person.email", domains=["mimesis.name"]),
                "creator": self.field("full_name", gender=Gender.FEMALE),
            },
        }

    def create_kafka_message(self) -> KafkaMessage:
        message_data = Schema(schema=self.schema_definition, iterations=1).create()[0]
        return KafkaMessage(**message_data)
