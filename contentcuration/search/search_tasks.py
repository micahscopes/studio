from celery.app import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command
import django
from celery_haystack.utils import get_handler
from celery_haystack import exceptions
from django.conf import settings


@shared_task(bind=True,
             using=settings.CELERY_HAYSTACK_DEFAULT_ALIAS,
             max_retries=settings.CELERY_HAYSTACK_MAX_RETRIES,
             default_retry_delay=settings.CELERY_HAYSTACK_RETRY_DELAY)
def update_subtree(self, parent_identifier, fields):
    parent_handler = get_handler()(parent_identifier)
    model_class = parent_handler.get_model_class()
    for current_index, _ in parent_handler.get_indexes(model_class):
        try:
            current_index.partial_update(**fields)
            current_index.partial_update_children(**fields)
        except exceptions.IndexOperationException as exc:
            logger.exception(exc)
            self.retry(exc=exc)
        except exceptions.InstanceNotFoundException as exc:
            logger.error(exc)
        except exceptions.UnrecognizedActionException as exc:
            logger.error("%s. Moving on..." % action)
