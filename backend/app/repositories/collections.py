from app.repositories.base import BaseRepository


class ProductsRepository(BaseRepository):
    collection_name = "products"


class RegionsRepository(BaseRepository):
    collection_name = "regions"


class PlantsRepository(BaseRepository):
    collection_name = "plants"


class WarehousesRepository(BaseRepository):
    collection_name = "warehouses"


class InventoryRepository(BaseRepository):
    collection_name = "inventory"


class SuppliersRepository(BaseRepository):
    collection_name = "suppliers"


class ShipmentsRepository(BaseRepository):
    collection_name = "shipments"


class LogisticsPartnersRepository(BaseRepository):
    collection_name = "logistics_partners"


class DemandSignalsRepository(BaseRepository):
    collection_name = "demand_signals"


class WeatherEventsRepository(BaseRepository):
    collection_name = "weather_events"


class PromotionsRepository(BaseRepository):
    collection_name = "promotions"


class RetailSalesRepository(BaseRepository):
    collection_name = "retail_sales"


class PlaybooksRepository(BaseRepository):
    collection_name = "playbooks"


class HistoricalIncidentsRepository(BaseRepository):
    collection_name = "historical_incidents"


class DecisionHistoryRepository(BaseRepository):
    collection_name = "decision_history"


class GraphNodesRepository(BaseRepository):
    collection_name = "graph_nodes"


class GraphEdgesRepository(BaseRepository):
    collection_name = "graph_edges"


class AgentMemoryRepository(BaseRepository):
    collection_name = "agent_memory"


COLLECTION_REPOSITORIES = (
    ProductsRepository,
    RegionsRepository,
    PlantsRepository,
    WarehousesRepository,
    InventoryRepository,
    SuppliersRepository,
    ShipmentsRepository,
    LogisticsPartnersRepository,
    DemandSignalsRepository,
    WeatherEventsRepository,
    PromotionsRepository,
    RetailSalesRepository,
    PlaybooksRepository,
    HistoricalIncidentsRepository,
    DecisionHistoryRepository,
    GraphNodesRepository,
    GraphEdgesRepository,
    AgentMemoryRepository,
)
