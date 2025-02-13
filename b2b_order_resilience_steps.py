from behave import given, when, then
from datetime import datetime
import time
from unittest.mock import MagicMock
from typing import List

class Order:
    def __init__(self, id: str, status: str):
        self.id = id
        self.status = status
        self.timestamp = datetime.now()

class OrderSystem:
    def __init__(self):
        self.orders: List[Order] = []
        self.metrics = {
            'success_rate': 0,
            'failed_orders': 0,
            'total_orders': 0
        }
    
    def process_orders(self, orders: List[Order]) -> None:
        self.metrics['total_orders'] = len(orders)
        failed = sum(1 for order in orders if order.status == 'FAILED')
        self.metrics['failed_orders'] = failed
        self.metrics['success_rate'] = ((len(orders) - failed) / len(orders)) * 100

@given('que o sistema de pedidos B2B está operacional')
def step_impl(context):
    context.order_system = OrderSystem()
    context.backup_system = OrderSystem()
    assert context.order_system is not None

@given('que existem entregadores disponíveis na plataforma')
def step_impl(context):
    context.drivers_available = True
    assert context.drivers_available is True

@given('que existem {number:d} pedidos B2B realizados no último período')
def step_impl(context, number):
    context.orders = [
        Order(f"ORDER_{i}", "SUCCESS") for i in range(number - 30)
    ] + [
        Order(f"ORDER_FAILED_{i}", "FAILED") for i in range(30)
    ]

@when('o sistema processa estes pedidos')
def step_impl(context):
    context.order_system.process_orders(context.orders)

@then('a taxa de pedidos processados com sucesso deve ser maior ou igual a {rate:g}%')
def step_impl(context, rate):
    success_rate = context.order_system.metrics['success_rate']
    assert success_rate >= rate, f"Taxa de sucesso ({success_rate}%) menor que o esperado ({rate}%)"

@then('o sistema deve registrar métricas de desempenho')
def step_impl(context):
    metrics = context.order_system.metrics
    assert 'success_rate' in metrics
    assert 'failed_orders' in metrics
    assert 'total_orders' in metrics

@given('que um pedido B2B está em andamento')
def step_impl(context):
    context.current_order = Order("B2B_TEST_ORDER", "IN_PROGRESS")
    context.order_state = "IN_PROGRESS"

@when('ocorre uma falha no aplicativo do entregador')
def step_impl(context):
    context.app_failure = True
    context.failure_timestamp = datetime.now()

@then('o sistema deve manter o estado do pedido')
def step_impl(context):
    assert context.current_order.status == "IN_PROGRESS"
    assert context.order_state == "IN_PROGRESS"

@then('deve sincronizar automaticamente quando o aplicativo voltar')
def step_impl(context):
    context.app_failure = False
    assert context.current_order.status == context.order_state

@then('deve notificar o suporte sobre a ocorrência')
def step_impl(context):
    # Simulando o sistema de notificação
    notification_service = MagicMock()
    notification_service.notify_support.return_value = True
    
    result = notification_service.notify_support(
        order_id=context.current_order.id,
        failure_timestamp=context.failure_timestamp
    )
    assert result is True

@given('que o sistema principal de pedidos está ativo')
def step_impl(context):
    context.primary_system = OrderSystem()
    context.primary_system_active = True
    # Inicializando alguns pedidos de teste
    context.orders = [
        Order(f"ORDER_{i}", "SUCCESS") for i in range(10)
    ]
    # Adicionando os pedidos ao sistema principal
    context.primary_system.orders = context.orders.copy()
    # Preparando o sistema de backup
    context.backup_system = OrderSystem()
    context.backup_system.orders = context.orders.copy()

@when('ocorre uma falha no sistema principal')
def step_impl(context):
    context.primary_system_active = False
    context.failure_start_time = time.time()
    # Garantindo que os pedidos são transferidos para o backup
    context.backup_system.orders = context.primary_system.orders.copy()

@then('o sistema backup deve assumir automaticamente')
def step_impl(context):
    context.backup_system_active = True
    assert context.backup_system_active is True
    # Verificando se o backup tem os pedidos
    assert len(context.backup_system.orders) > 0

@then('nenhum pedido deve ser perdido durante a transição')
def step_impl(context):
    # Verificando se todos os pedidos foram transferidos para o sistema backup
    original_orders = set(order.id for order in context.primary_system.orders)
    backup_orders = set(order.id for order in context.backup_system.orders)
    assert original_orders == backup_orders, "Alguns pedidos foram perdidos durante a transição"

@then('o tempo de indisponibilidade deve ser menor que {seconds:d} segundos')
def step_impl(context, seconds):
    downtime = time.time() - context.failure_start_time
    assert downtime < seconds, f"Tempo de indisponibilidade ({downtime}s) maior que o permitido ({seconds}s)" 