from litestar.di import Provide
import app.repositories.account
import app.repositories.client
import app.repositories.dialplan
import app.repositories.task
import app.services.account
import app.services.client
import app.services.dialplan
import app.services.task
import app.utils


dependencies = {
    "db_session": Provide(app.utils.provide_db_session),
    "redis_client": Provide(app.utils.provide_redis_client),

    # account
    "account_repository": Provide(app.repositories.account.provide_account_repository),
    "account_service": Provide(app.services.account.provide_account_service),

    # client
    "client_repository": Provide(app.repositories.client.provide_client_repository),
    "client_service": Provide(app.services.client.provide_client_service),

    # dialplan
    "dialplan_repository": Provide(app.repositories.dialplan.provide_dialplan_repository),
    "dialplan_service": Provide(app.services.dialplan.provide_dialplan_service),

    # task
    "task_repository": Provide(app.repositories.task.provide_task_repository),
    "task_service": Provide(app.services.task.provide_task_service),
}
