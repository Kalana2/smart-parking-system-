import json
import time
import pika
from jsonschema import Draft202012Validator


class Publisher:
	def __init__(self, config):
		self.config = config
		self.validator = self._load_schema(config.event_schema_path)
		self.connection = None
		self.channel = None

	def _load_schema(self, schema_path):
		with open(schema_path, "r", encoding="utf-8") as handle:
			schema = json.load(handle)
		return Draft202012Validator(schema)

	def connect(self):
		credentials = pika.PlainCredentials(
			self.config.rabbitmq_user, self.config.rabbitmq_password
		)
		parameters = pika.ConnectionParameters(
			host=self.config.rabbitmq_host,
			port=self.config.rabbitmq_port,
			credentials=credentials,
			heartbeat=30,
			blocked_connection_timeout=30,
		)
		self.connection = pika.BlockingConnection(parameters)
		self.channel = self.connection.channel()
		self.channel.exchange_declare(
			exchange=self.config.rabbitmq_exchange,
			exchange_type="topic",
			durable=True,
		)

	def close(self):
		if self.channel:
			self.channel.close()
		if self.connection:
			self.connection.close()

	def _validate(self, payload):
		errors = sorted(self.validator.iter_errors(payload), key=lambda e: e.path)
		if errors:
			message = "; ".join(err.message for err in errors)
			raise ValueError(f"Event schema validation failed: {message}")

	def publish(self, payload):
		self._validate(payload)
		body = json.dumps(payload).encode("utf-8")
		properties = pika.BasicProperties(
			content_type="application/json",
			delivery_mode=2,
		)
		attempt = 0
		while True:
			try:
				if not self.connection or self.connection.is_closed:
					self.connect()
				self.channel.basic_publish(
					exchange=self.config.rabbitmq_exchange,
					routing_key=self.config.rabbitmq_routing_key,
					body=body,
					properties=properties,
				)
				return
			except Exception as exc:
				attempt += 1
				if attempt > self.config.rabbitmq_retry_max:
					raise RuntimeError("RabbitMQ publish failed after retries") from exc
				delay = self.config.rabbitmq_retry_base_sec * (2 ** (attempt - 1))
				time.sleep(delay)
