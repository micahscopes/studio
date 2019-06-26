# import django
# from .search_indexes import ContentNodeIndex
# from celery.app import shared_task
# from celery.utils.log import get_task_logger
# from django.core.management import call_command
# from celery_haystack.utils import get_handler, get_identifier
# from celery_haystack import exceptions
# from django.conf import settings
# from itertools import chain

# logger = get_task_logger(__name__)

# @shared_task(bind=True,
#              using=settings.CELERY_HAYSTACK_DEFAULT_ALIAS,
#              max_retries=settings.CELERY_HAYSTACK_MAX_RETRIES,
#              default_retry_delay=settings.CELERY_HAYSTACK_RETRY_DELAY)
# def partial_update_subtree_channel_info(self, parent_identifier, fields, **kwargs):
#     try:
#         handler = get_handler()(parent_identifier)
#         model_class = handler.get_model_class()
#         path, pk = handler.
#         nodes = chain(parent, parent.children)
#         ContentNodeIndex.partial_update(nodes, **fields)
#     except exceptions.IndexOperationException as exc:
#         logger.exception(exc)
#         self.retry(exc=exc)
#     except exceptions.InstanceNotFoundException as exc:
#         logger.error(exc)


# @shared_task(bind=True,
#              using=settings.CELERY_HAYSTACK_DEFAULT_ALIAS,
#              max_retries=settings.CELERY_HAYSTACK_MAX_RETRIES,
#              default_retry_delay=settings.CELERY_HAYSTACK_RETRY_DELAY)
# def partial_update(self, instance, fields):
#     identifier = get_identifier(instance)
#     handler = get_handler()(parent_identifier)
#     model_class = handler.get_model_class()
#     for current_index, _ in handler.get_indexes(model_class):
#         try:
#             current_index.partial_update(instance, **fields)
#         except exceptions.IndexOperationException as exc:
#             logger.exception(exc)
#             self.retry(exc=exc)
#         except exceptions.InstanceNotFoundException as exc:
#             logger.error(exc)
#         except exceptions.UnrecognizedActionException as exc:
#             logger.error("%s. Moving on..." % action)
