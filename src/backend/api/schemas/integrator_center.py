import strawberry

from ..modules.auth.mutations import AuthMutation
from ..modules.dictionary_manager.mutations import DictionaryManagerMutation
from ..modules.dictionary_manager.queries import DictionaryManagerQuery
from ..modules.flow_manager.mutations import FlowManagerMutation
from ..modules.flow_manager.queries import FlowManagerQuery
from ..modules.function_manager.queries import FunctionManagerQuery
from ..modules.integrator_center.mutations import IntegratorCenterMutation
from ..modules.integrator_center.queries import IntegratorCenterQuery
from ..modules.store.queries import StoreQuery


@strawberry.type
class Query(
    IntegratorCenterQuery,
    DictionaryManagerQuery,
    FunctionManagerQuery,
    StoreQuery,
    FlowManagerQuery,
    # TODO: WidgetManagerQuery
    # TODO: UIManagerQuery
    # TODO: StorageManager
):
    pass


@strawberry.type
class Mutation(
    AuthMutation,
    IntegratorCenterMutation,
    FlowManagerMutation,
    DictionaryManagerMutation,
):
    pass


schema = strawberry.Schema(
    query=Query,
    # mutation=Mutation,
)
