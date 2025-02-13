# language: pt

Funcionalidade: Resiliência de Pedidos B2B
  Como um gestor da Rappi
  Eu quero garantir que os pedidos B2B sejam processados com alta confiabilidade
  Para manter a qualidade do serviço e satisfação dos clientes corporativos

  Contexto:
    Dado que o sistema de pedidos B2B está operacional
    E que existem entregadores disponíveis na plataforma

  Cenário: Monitoramento da taxa de sucesso dos pedidos B2B
    Dado que existem 1000 pedidos B2B realizados no último período
    Quando o sistema processa estes pedidos
    Então a taxa de pedidos processados com sucesso deve ser maior ou igual a 97%
    E o sistema deve registrar métricas de desempenho

  Cenário: Recuperação de pedidos em caso de falha do aplicativo
    Dado que um pedido B2B está em andamento
    Quando ocorre uma falha no aplicativo do entregador
    Então o sistema deve manter o estado do pedido
    E deve sincronizar automaticamente quando o aplicativo voltar
    E deve notificar o suporte sobre a ocorrência

  Cenário: Validação de redundância do sistema
    Dado que o sistema principal de pedidos está ativo
    Quando ocorre uma falha no sistema principal
    Então o sistema backup deve assumir automaticamente
    E nenhum pedido deve ser perdido durante a transição
    E o tempo de indisponibilidade deve ser menor que 5 segundos 