# Set up Azure Monitor
from opentelemetry import  trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from dotenv import load_dotenv
import os

load_dotenv()

# SET UP CONNECTION STRING
APPLICATIONINSIGHTS_CONNECTION_STRING=os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
# Create a Resource object with the cloud.role attribute

if APPLICATIONINSIGHTS_CONNECTION_STRING:
    # SET UP TRACE EXPORTER
    trace_exporter = AzureMonitorTraceExporter(
        connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING
    )
    resource = Resource(attributes={"cloud.role": "FastAPIApplication"})
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer(__name__)
def init_tracing(app):
    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)
    app.add_middleware(OpenTelemetryMiddleware)