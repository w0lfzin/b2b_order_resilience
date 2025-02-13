workspace "Rappi B2B Order System" "Sistema resiliente de pedidos B2B da Rappi" {

    !identifiers hierarchical

    model {
        # Pessoas
        customer = person "Cliente B2B" "Cliente corporativo que realiza pedidos"
        deliveryPerson = person "Entregador" "Profissional que realiza as entregas"
        supportTeam = person "Equipe de Suporte" "Time que monitora e dá suporte ao sistema"

        orderSystem = softwareSystem "Sistema de Pedidos B2B" "Sistema principal de processamento de pedidos B2B" {
            # Containers do sistema principal
            primaryAPI = container "API Principal" "API REST que processa os pedidos" "Spring Boot"
            deliveryApp = container "Aplicativo do Entregador" "App móvel usado pelos entregadores" "React Native"
            orderProcessor = container "Processador de Pedidos" "Serviço que gerencia o ciclo de vida dos pedidos" "Java"
            metricsCollector = container "Coletor de Métricas" "Monitora e registra métricas de desempenho" "Prometheus"
            primaryDB = container "Banco de Dados Principal" "Armazena pedidos e dados do sistema" "PostgreSQL" {
                tags "Database"
            }
            backupAPI = container "API Backup" "API redundante" "Spring Boot"
            backupDB = container "Banco Backup" "Banco de dados redundante" "PostgreSQL" {
                tags "Database"
            }
        }

        # Relacionamentos
        customer -> orderSystem "Realiza pedidos B2B"
        deliveryPerson -> orderSystem.deliveryApp "Utiliza"
        orderSystem.deliveryApp -> orderSystem.primaryAPI "Envia/Recebe dados" "HTTPS"
        orderSystem.primaryAPI -> orderSystem.orderProcessor "Processa pedidos"
        orderSystem.orderProcessor -> orderSystem.primaryDB "Persiste dados"
        orderSystem.orderProcessor -> orderSystem.metricsCollector "Envia métricas"
        orderSystem.metricsCollector -> supportTeam "Notifica problemas"
        
        # Relacionamentos do backup
        orderSystem.primaryAPI -> orderSystem.backupAPI "Replica dados em tempo real"
        orderSystem.backupAPI -> orderSystem.backupDB "Persiste dados redundantes"
        orderSystem.backupAPI -> orderSystem.primaryAPI "Assume operação em caso de falha"
    }

    views {
        systemContext orderSystem "SystemContext" {
            include *
            autolayout tb
        }

        container orderSystem "Containers" {
            include *
            autolayout tb
        }

        styles {
            element "Person" {
                background #08427b
                shape person
            }
            element "Software System" {
                background #1168bd
            }
            element "Container" {
                background #23a2d9
            }
            element "Database" {
                shape cylinder
            }
        }

        theme default
    }

    configuration {
        scope softwaresystem
    }
} 