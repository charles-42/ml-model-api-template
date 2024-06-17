# Set up Azure Monitor
from django.shortcuts import render
from opentelemetry import metrics, trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from query_app.forms import SatisfactionForm

APPLICATIONINSIGHTS_CONNECTION_STRING='InstrumentationKey=e41f1e99-c697-4c61-b12f-8e87e991709e;IngestionEndpoint=https://francecentral-1.in.applicationinsights.azure.com/;LiveEndpoint=https://francecentral.livediagnostics.monitor.azure.com/;ApplicationId=ff932b27-f670-4287-a35a-9ca756f4fa1a'
# APPLICATIONINSIGHTS_CONNECTION_STRING=os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
#    configure_azure_monitor(
#     connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING,enable_live_metrics=True
# )
# Set up trace exporter
trace_exporter = AzureMonitorTraceExporter(
    connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING
)
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
trace.set_tracer_provider(tracer_provider)

# Set up metrics exporter
metric_exporter = AzureMonitorMetricExporter(
    connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING
)
reader = PeriodicExportingMetricReader(exporter=metric_exporter, export_interval_millis=60000)
metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))
meter = metrics.get_meter_provider().get_meter("satisfaction_metrics")

# Create metric instruments
product_received_counter = meter.create_counter("product_received_values")
delivery_time_counter = meter.create_counter("delivery_time_values")
prediction_counter = meter.create_counter("prediction_values")
prediction_sum = meter.create_counter("prediction_sum")
prediction_count = meter.create_counter("prediction_count")

# Instrument Django
from opentelemetry.instrumentation.django import DjangoInstrumentor
DjangoInstrumentor().instrument()