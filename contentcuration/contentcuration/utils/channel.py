import time

from django.core.cache import cache
from django.db.models import Count
from django.db.models import Sum
from django_cte import With

from contentcuration.models import Channel
from contentcuration.models import ContentNode
from contentcuration.models import FileCTE
from contentcuration.models import User


def cache_channel_metadata(channel=None, tree_id=None):
    if channel is None and tree_id is None:
        return  # this is an error, it should not happen, but just in case

    if channel is None:
        channel = Channel.objects.filter(main_tree__tree_id=319).values_list(
            "id", flat=True
        )[0]

    key = "channel_metadata_{}".format(channel)
    metadata = cache.get(key)
    if metadata is not None:
        if metadata["CALCULATING"]:
            return  # the task is already queue
    else:
        # the key will expire if the task is not achieved in one hour
        cache.set(key, {"CALCULATING": True}, timeout=3600)

        if tree_id is None:
            tree_id = Channel.objects.get(id=channel).main_tree.id

        nodes = With(
            ContentNode.objects.values("id", "tree_id")
            .filter(tree_id=tree_id)
            .order_by(),
            name="nodes",
        )
        size_sum = (
            nodes.join(FileCTE, contentnode_id=nodes.col.id)
            .values("checksum", "file_size")
            .with_cte(nodes)
            .distinct()
            .aggregate(Sum("file_size"))
        )
        size = size_sum["file_size__sum"] or 0

        editors = (
            User.objects.filter(editable_channels__id=channel)
            .values_list("id", flat=True)
            .distinct()
            .aggregate(Count("id"))
        )
        editors_count = editors["id__count"] or 0

        viewers = (
            User.objects.filter(view_only_channels__id=channel)
            .values_list("id", flat=True)
            .distinct()
            .aggregate(Count("id"))
        )
        viewers_count = viewers["id__count"] or 0

        # 1 day timeout, pending to review, maybe 0 (forever):
        metadata = {
            "CALCULATING": False,
            "SIZE": size,
            "EDITORS": editors_count,
            "VIEWERS": viewers_count,
            "LAST_CALCULATED": time.time(),
        }
        cache.set(key, metadata, timeout=86400)
